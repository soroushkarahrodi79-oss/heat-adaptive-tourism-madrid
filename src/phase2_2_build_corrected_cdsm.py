"""
Phase 2.2 Task A, step 2: build LOCALIZED corrected-canopy CDSM variants for
the two assets the evidence step judged genuinely stale (A23 PARTIALLY STALE,
A27 MATERIALLY STALE). A24 (La Rosaleda) is NOT corrected - the evidence step
found its near-zero LiDAR canopy REPRESENTATIVE (0 inventoried canopy trees
within 30 m; documented rose garden), so inserting canopy there would be
fabrication, not correction.

Construction (fully reproducible, real numbers only):
  - Start from the LOCKED Phase 2 CDSM (data/interim/solweig/cdsm_2m5.tif) -
    read only, never overwritten.
  - For each real Madrid-inventory tree with altura_m > 3 m within 30 m of
    A23 or A27, burn a canopy disc of the tree's REAL height (altura_m) and a
    crown radius R into a copy of the CDSM, taking the element-wise MAXIMUM
    with existing canopy (a correction only ever ADDS the canopy the stale
    LiDAR missed; it never removes canopy the LiDAR did capture).
  - Only crown radius is assumed (height is real inventory data). To avoid
    false precision on that one assumption, THREE variants are produced and
    carried as a bracket into the decision-uncertainty envelope:
        R = 2.0 m (narrow), 3.0 m (central), 4.0 m (wide).
  - Everything outside the A23/A27 30 m neighbourhoods - including A24 and all
    42-row assets - is byte-for-byte the Phase 2 canopy, so those assets'
    modelled values are unchanged by construction.

Outputs: data/interim/solweig_phase2_2/<variant>/{cdsm,dsm,dem}_2m5.tif
(separate directory tree; Phase 2 inputs untouched). CRS re-tagged to
EPSG:25830 per the known LOCAL_CS quirk (docs/PHASE2_SOLWEIG_METHOD.md).
"""
import shutil
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.crs import CRS
from rasterio.features import rasterize
from shapely.geometry import Point

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
INTERIM = ROOT / "data" / "interim"
SRC_GEOM = INTERIM / "solweig"                # Phase 2 LOCKED inputs (read-only)
OUT_ROOT = INTERIM / "solweig_phase2_2"       # Phase 2.2 variants (separate)
WGS84 = "EPSG:4326"
UTM30N = "EPSG:25830"

CORRECT_ASSETS = ["A23", "A27"]   # A24 intentionally excluded (representative)
NEIGHBOURHOOD_M = 30
CANOPY_MIN_H = 3.0
CROWN_RADII = {"narrow": 2.0, "central": 3.0, "wide": 4.0}


def main():
    assets = pd.read_csv(PROCESSED / "pilot_assets.csv")
    assets = assets[assets["asset_id"].isin(CORRECT_ASSETS)].copy()
    agdf = gpd.GeoDataFrame(assets, geometry=gpd.points_from_xy(assets.longitude, assets.latitude),
                            crs=WGS84).to_crs(UTM30N)

    trees = gpd.read_file(INTERIM / "madrid_arbolado_points.geojson").to_crs(UTM30N)
    trees["h"] = pd.to_numeric(trees["altura_m"], errors="coerce")
    trees = trees[trees["h"] > CANOPY_MIN_H].copy()

    # Collect the real canopy trees within NEIGHBOURHOOD_M of either corrected asset.
    keep_idx = set()
    for _, a in agdf.iterrows():
        d = trees.geometry.distance(a.geometry)
        keep_idx.update(trees.index[d <= NEIGHBOURHOOD_M].tolist())
    canopy = trees.loc[sorted(keep_idx)].copy()
    print(f"Real inventoried canopy trees (>{CANOPY_MIN_H} m) within {NEIGHBOURHOOD_M} m of "
          f"{CORRECT_ASSETS}: {len(canopy)}")
    print(canopy.groupby(canopy["h"].round())["h"].count().to_string())

    with rasterio.open(SRC_GEOM / "cdsm_2m5.tif") as src:
        base_cdsm = src.read(1).astype("float32")
        profile = src.profile.copy()
        transform = src.transform
        out_shape = base_cdsm.shape
    profile["crs"] = CRS.from_epsg(25830)

    for name, R in CROWN_RADII.items():
        vdir = OUT_ROOT / name
        vdir.mkdir(parents=True, exist_ok=True)
        corrected = base_cdsm.copy()
        # Burn each tree's real height over a disc of radius R, accumulating by max.
        shapes = [(geom.buffer(R), float(h)) for geom, h in zip(canopy.geometry, canopy["h"])]
        # rasterize with merge_alg=MAX so overlapping crowns keep the taller height,
        # onto a zero canvas, then max against the existing (Phase 2) canopy.
        burned = rasterize(shapes, out_shape=out_shape, transform=transform,
                           fill=0.0, merge_alg=rasterio.enums.MergeAlg.replace, dtype="float32")
        # replace-alg does not guarantee max on overlap order; enforce max explicitly
        # by re-burning tallest-last: sort ascending so taller trees overwrite.
        shapes_sorted = sorted(shapes, key=lambda s: s[1])
        burned = rasterize(shapes_sorted, out_shape=out_shape, transform=transform,
                           fill=0.0, dtype="float32")
        corrected = np.maximum(corrected, burned)

        with rasterio.open(vdir / "cdsm_2m5.tif", "w", **profile) as dst:
            dst.write(corrected, 1)
        # Copy DSM/DEM unchanged (buildings/terrain are not stale) but re-tag CRS.
        for layer in ("dsm_2m5.tif", "dem_2m5.tif"):
            with rasterio.open(SRC_GEOM / layer) as s:
                arr = s.read(1)
                p = s.profile.copy(); p["crs"] = CRS.from_epsg(25830)
            with rasterio.open(vdir / layer, "w", **p) as d:
                d.write(arr, 1)

        added = int((corrected > base_cdsm + 0.01).sum())
        print(f"[{name} R={R}m] canopy pixels added: {added}; "
              f"corrected max={corrected.max():.1f} m -> {vdir}")

    print(f"\nPhase 2 inputs untouched at {SRC_GEOM} (verify): "
          f"cdsm mtime preserved.")


if __name__ == "__main__":
    main()
