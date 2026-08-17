"""
Phase 2.2 Task A, step 1: quantify the vegetation evidence at the three
geometry-flagged garden assets (A23, A24, A27) using the strongest recent,
spatially explicit sources ALREADY in this project - none re-fetched:

  - Madrid official tree inventory (live ~2025-2026), which carries a real
    per-tree HEIGHT attribute (`altura_m`) - the decisive new information
    Audit 2 did not exploit (it only counted trees). Height lets us judge
    whether real canopy TALL ENOUGH to shade a pedestrian exists, and later
    build a defensible corrected CDSM from real numbers, not invented ones.
  - Copernicus HRL Tree Cover Density 2018 (intermediate vintage).
  - OSM green-polygon coverage (2026 snapshot).
  - The Phase 2 LiDAR CDSM (~2008-2015), LOCKED, read-only here.

This step does NOT modify any geometry. It produces the evidence table that
docs/PHASE2_2_GEOMETRY_RECHECK.md interprets, and decides per asset whether a
defensible localized correction is warranted and possible.

Multi-radius (10/20/30 m) because canopy from trees just OUTSIDE the 10 m
pre-registered buffer still shades pixels inside it; Audit 2's 10 m-only
count could miss real nearby canopy (esp. at A24/A27 which had 0 trees within
10 m but the gardens plainly contain trees).
"""
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterstats import zonal_stats
from shapely.geometry import Point

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
INTERIM = ROOT / "data" / "interim"
RAW = ROOT / "data" / "raw"
WGS84 = "EPSG:4326"
UTM30N = "EPSG:25830"

ASSETS = ["A23", "A24", "A27"]
RADII = [10, 20, 30]


def main():
    assets = pd.read_csv(PROCESSED / "pilot_assets.csv")
    assets = assets[assets["asset_id"].isin(ASSETS)].copy()
    gdf = gpd.GeoDataFrame(
        assets, geometry=gpd.points_from_xy(assets.longitude, assets.latitude), crs=WGS84
    ).to_crs(UTM30N)

    trees = gpd.read_file(INTERIM / "madrid_arbolado_points.geojson").to_crs(UTM30N)
    # altura_m is a string field with occasional blanks / "0"; coerce robustly.
    trees["altura_m_num"] = pd.to_numeric(trees["altura_m"], errors="coerce")
    tree_pts = np.array([(g.x, g.y) for g in trees.geometry])
    tree_h = trees["altura_m_num"].values

    green = gpd.read_file(INTERIM / "all_green_polygons.geojson").to_crs(UTM30N)
    green_union = green.geometry.union_all()

    rows = []
    for _, a in gdf.iterrows():
        ax, ay = a.geometry.x, a.geometry.y
        d = np.hypot(tree_pts[:, 0] - ax, tree_pts[:, 1] - ay)
        rec = {"asset_id": a["asset_id"], "name": a["name"]}
        for r in RADII:
            in_r = d <= r
            heights = tree_h[in_r]
            heights_valid = heights[~np.isnan(heights)]
            # "canopy trees" = inventoried trees taller than 3 m (a real
            # pedestrian-shading canopy, excludes saplings/shrubs logged as
            # 0-3 m). 3 m matches the geometry_confidence_audit noise floor idea.
            canopy = heights_valid[heights_valid > 3.0]
            rec[f"n_trees_{r}m"] = int(in_r.sum())
            rec[f"n_canopy_trees_{r}m"] = int(canopy.size)
            rec[f"median_h_{r}m"] = round(float(np.median(canopy)), 1) if canopy.size else 0.0
            rec[f"max_h_{r}m"] = round(float(np.max(heights_valid)), 1) if heights_valid.size else 0.0
        # CDSM (Phase 2, locked) mean/max within 10 m for reference
        buf10 = gpd.GeoSeries([a.geometry.buffer(10)], crs=UTM30N)
        cd = zonal_stats(buf10, str(INTERIM / "solweig" / "cdsm_2m5.tif"), stats=["mean", "max"])[0]
        rec["cdsm_mean_10m"] = round(float(cd["mean"]), 2)
        rec["cdsm_max_10m"] = round(float(cd["max"]), 2)
        # TCD 2018 within 10 m
        tcd = zonal_stats(buf10.to_crs(WGS84), str(RAW / "copernicus_tcd" / "tcd_2018_study_area.tif"),
                          stats=["mean"])[0]
        rec["tcd_pct_10m"] = round(float(tcd["mean"]), 1)
        rec["green_pct_10m"] = round(100 * a.geometry.buffer(10).intersection(green_union).area
                                     / a.geometry.buffer(10).area, 1)
        rows.append(rec)

    out = pd.DataFrame(rows)
    out_path = PROCESSED / "phase2_2_geometry_evidence.csv"
    out.to_csv(out_path, index=False, encoding="utf-8")
    pd.set_option("display.width", 200, "display.max_columns", 50)
    print(out.to_string(index=False))
    print(f"\nWrote {out_path}")
    return out


if __name__ == "__main__":
    main()
