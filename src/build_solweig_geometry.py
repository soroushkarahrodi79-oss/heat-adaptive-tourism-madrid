"""
Phase 2: build the DSM / DEM / CDSM GeoTIFFs SOLWEIG needs, from real PNOA-LiDAR-
derived official IGN products fetched via the public, no-login IGN/CNIG WCS
services (data/raw/pnoa_lidar/, see docs/PHASE2_INPUT_FEASIBILITY.md).

Working resolution: 2.5 m (see docs/PHASE2_INPUT_FEASIBILITY.md "Resolution
justification") - matches the native resolution of the two geometrically
decisive inputs (building and vegetation normalized height models), so DEM
(native 5 m) is the only layer upsampled, and only for a smooth, low-frequency
terrain surface where upsampling introduces negligible artefacts.

Outputs (data/interim/solweig/):
  dem_2m5.tif   - bare-earth terrain, absolute elevation (m)
  dsm_2m5.tif   - ground+building surface, absolute elevation (m) = DEM + building_ndsm
  cdsm_2m5.tif  - vegetation canopy height ABOVE GROUND (m), i.e. cdsm_relative=True convention
"""
from pathlib import Path

import numpy as np
import rasterio
from rasterio.crs import CRS
from rasterio.enums import Resampling
from rasterio.warp import reproject

RAW = Path(__file__).resolve().parents[1] / "data" / "raw" / "pnoa_lidar"
OUT = Path(__file__).resolve().parents[1] / "data" / "interim" / "solweig"
TARGET_RES = 2.5

# The IGN/CNIG WCS services (servicios.idee.es, wcs-mds.idee.es) serve
# GeoTIFFs tagged with a malformed generic LOCAL_CS WKT
# ("ETRS89 / UTM zone 30N" as a LOCAL_CS, not a proper PROJCS) even though
# the actual coordinate values returned are genuine EPSG:25830 UTM30N
# metres (confirmed: the WCS request explicitly specified
# .../EPSG/0/25830(...) axes and the numeric extents match the requested
# bbox exactly). SOLWEIG's CRS validator rejects LOCAL_CS as "geographic".
# This is a METADATA correction (relabelling a CRS tag rasterio/pyproj
# cannot parse as projected), not a reprojection - no coordinate values are
# altered.
CRS_FIX = CRS.from_epsg(25830)


def load(path):
    with rasterio.open(path) as src:
        profile = src.profile.copy()
        profile["crs"] = CRS_FIX
        return src.read(1).astype("float64"), profile


def resample_to(src_path, ref_profile):
    """Resample src_path onto the exact grid described by ref_profile (bilinear)."""
    with rasterio.open(src_path) as src:
        dst = np.empty((ref_profile["height"], ref_profile["width"]), dtype="float64")
        reproject(
            source=rasterio.band(src, 1),
            destination=dst,
            src_transform=src.transform,
            src_crs=CRS_FIX,  # see CRS_FIX note above - same malformed-tag fix
            dst_transform=ref_profile["transform"],
            dst_crs=ref_profile["crs"],
            resampling=Resampling.bilinear,
        )
    return dst


def build():
    OUT.mkdir(parents=True, exist_ok=True)

    # Reference grid = building nDSM (native 2.5 m, defines the working grid)
    building, ref_profile = load(RAW / "building_ndsm_025.tif")
    vegetation, _ = load(RAW / "veg_ndsm_025.tif")
    dem_resampled = resample_to(RAW / "dem_wcs_5m.tif", ref_profile)

    # Building/vegetation nDSM values are height-above-ground; treat negative
    # noise (LiDAR speckle) as 0, consistent with SOLWEIG's own
    # min_object_height flattening intent, applied here explicitly and
    # documented rather than left implicit.
    building = np.clip(building, 0, None)
    vegetation = np.clip(vegetation, 0, None)

    dsm = dem_resampled + building  # absolute elevation, ground+building surface
    dem = dem_resampled             # absolute elevation, bare earth
    cdsm = vegetation               # height above ground (cdsm_relative=True)

    profile = ref_profile.copy()
    profile.update(dtype="float32", count=1, nodata=None)

    for name, arr in [("dem_2m5.tif", dem), ("dsm_2m5.tif", dsm), ("cdsm_2m5.tif", cdsm)]:
        with rasterio.open(OUT / name, "w", **profile) as dst:
            dst.write(arr.astype("float32"), 1)
        print(f"Wrote {OUT / name}: shape={arr.shape} min={np.nanmin(arr):.1f} "
              f"max={np.nanmax(arr):.1f} mean={np.nanmean(arr):.2f}")

    return dem, dsm, cdsm, profile


if __name__ == "__main__":
    build()
