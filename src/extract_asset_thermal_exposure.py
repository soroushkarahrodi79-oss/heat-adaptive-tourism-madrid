"""
Phase 2: extract asset-level Tmrt/UTCI statistics from the SOLWEIG rasters,
translate UTCI to a feasibility_state via the pre-registered rule (official
UTCI thermal-stress category boundaries, Broede et al. 2012 - see
docs/PHASE2_UTCI_METHOD.md), and build the required comparison outputs.

Spatial statistic: PRE-REGISTERED in src/phase2_prereg.py BEFORE this script
was run - 10 m buffer mean is primary; centroid and 90th-percentile are
sensitivity companions, not the gate statistic.
"""
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterstats import zonal_stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phase2_prereg import REPRESENTATIVE_ASSET_IDS, PRIMARY_BUFFER_M, SENSITIVITY_PERCENTILE

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
MAPS = ROOT / "outputs" / "maps"
TABLES = ROOT / "outputs" / "tables"
WGS84 = "EPSG:4326"
UTM30N = "EPSG:25830"

TIMESTAMPS = [("12:00", "1200"), ("15:00", "1500"), ("18:00", "1800")]

# Official UTCI thermal-stress category boundaries (Broede et al. 2012, "UTCI-
# Fiala model", the standard published category system - not project-invented).
UTCI_CATEGORY_BOUNDS = [
    (9, "No thermal stress"), (26, "Moderate heat stress"),
    (32, "Strong heat stress"), (38, "Very strong heat stress"),
    (46, "Extreme heat stress"), (float("inf"), "Extreme heat stress"),
]


def utci_category(utci_c):
    if utci_c < 9:
        return "Below moderate range (not applicable to this heat episode)"
    for bound, label in UTCI_CATEGORY_BOUNDS:
        if utci_c < bound:
            return label
    return "Extreme heat stress"


def utci_to_feasibility(utci_c):
    """Pre-registered translation (docs/PHASE2_UTCI_METHOD.md) - a project
    decision informed by, but not identical to, the official UTCI stress
    categories (which describe physiological stress, not tourism
    feasibility). Documented explicitly, not claimed as an official
    threshold."""
    if utci_c >= 46:
        return "NOT RECOMMENDED"
    elif utci_c >= 32:
        return "FEASIBLE WITH CONDITIONS"
    else:
        return "FEASIBLE"


def load_assets():
    df = pd.read_csv(PROCESSED / "pilot_assets.csv")
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs=WGS84)
    return gdf.to_crs(UTM30N)


def extract_stats(assets_utm, tif_path, buffer_m):
    buffers = assets_utm.geometry.buffer(buffer_m)
    stats = zonal_stats(buffers, str(tif_path), stats=["mean", "median", "min", "max", "percentile_90"], nodata=np.nan)
    with rasterio.open(tif_path) as src:
        centroids = [
            list(src.sample([(geom.x, geom.y)]))[0][0]
            for geom in assets_utm.geometry
        ]
    return stats, centroids


def main():
    assets = load_assets()
    morphology = pd.read_csv(PROCESSED / "shade_proxy_comparison.csv")[["asset_id", "morphology"]].drop_duplicates()
    baseline = pd.read_csv(PROCESSED / "pilot_classifications.csv")

    rows = []
    for local_time, label in TIMESTAMPS:
        tmrt_stats, tmrt_centroids = extract_stats(assets, MAPS / f"tmrt_{label}.tif", PRIMARY_BUFFER_M)
        utci_stats, utci_centroids = extract_stats(assets, MAPS / f"utci_{label}.tif", PRIMARY_BUFFER_M)

        for i, (_, a) in enumerate(assets.iterrows()):
            aid = a["asset_id"]
            io = a["indoor_outdoor"]
            base_row = baseline[(baseline["asset_id"] == aid) & (baseline["timestamp"].str.contains(local_time))]
            phase1_feas = base_row.iloc[0]["feasibility_state"] if len(base_row) else None
            phase1_exposure = base_row.iloc[0]["exposure_state"] if len(base_row) else None

            if io == "indoor":
                # SOLWEIG models the outdoor thermal environment only; indoor
                # assets keep their Phase 1 indoor-bypass feasibility
                # unchanged - the physical model has nothing new to say about
                # an indoor space's interior.
                row = {
                    "asset_id": aid, "name": a["name"], "indoor_outdoor": io,
                    "morphology": "indoor", "timestamp": local_time,
                    "tmrt_mean_10m": None, "tmrt_centroid": None, "tmrt_p90_10m": None,
                    "utci_mean_10m": None, "utci_centroid": None, "utci_p90_10m": None,
                    "utci_category": None,
                    "feasibility_phase1_proxy": phase1_feas,
                    "feasibility_phase2_physical": phase1_feas,
                    "reclassified": False, "reclassification_direction": "",
                    "evidence_note": "indoor asset - SOLWEIG models outdoor environment only; Phase 1 indoor rule retained unchanged",
                }
            else:
                tmrt_mean = round(float(tmrt_stats[i]["mean"]), 1)
                utci_mean = round(float(utci_stats[i]["mean"]), 1)
                phase2_feas = utci_to_feasibility(utci_mean)
                order = {"FEASIBLE": 0, "FEASIBLE WITH CONDITIONS": 1, "NOT RECOMMENDED": 2}
                reclass = phase1_feas != phase2_feas
                direction = ""
                if reclass and phase1_feas in order and phase2_feas in order:
                    diff = order[phase2_feas] - order[phase1_feas]
                    direction = ("physical model MORE restrictive (proxy underestimated hazard)" if diff > 0
                                 else "physical model LESS restrictive (proxy overestimated hazard)")
                row = {
                    "asset_id": aid, "name": a["name"], "indoor_outdoor": io,
                    "morphology": morphology.set_index("asset_id").loc[aid, "morphology"] if aid in morphology.asset_id.values else "",
                    "timestamp": local_time,
                    "tmrt_mean_10m": tmrt_mean,
                    "tmrt_centroid": round(float(tmrt_centroids[i]), 1),
                    "tmrt_p90_10m": round(float(tmrt_stats[i]["percentile_90"]), 1),
                    "utci_mean_10m": utci_mean,
                    "utci_centroid": round(float(utci_centroids[i]), 1),
                    "utci_p90_10m": round(float(utci_stats[i]["percentile_90"]), 1),
                    "utci_category": utci_category(utci_mean),
                    "feasibility_phase1_proxy": phase1_feas,
                    "feasibility_phase2_physical": phase2_feas,
                    "reclassified": reclass,
                    "reclassification_direction": direction,
                    "evidence_note": (
                        f"phase1 exposure_state={phase1_exposure}; "
                        f"SOLWEIG 2.5m, 10m-buffer mean; representative_asset={aid in REPRESENTATIVE_ASSET_IDS}"
                    ),
                }
            rows.append(row)

    out = pd.DataFrame(rows)
    out_path = PROCESSED / "phase2_asset_thermal_exposure.csv"
    out.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Wrote {out_path} with {len(out)} rows")

    outdoor = out[out["indoor_outdoor"] == "outdoor"]
    print(f"\nOutdoor rows: {len(outdoor)}")
    print(f"Reclassified: {outdoor['reclassified'].sum()} / {len(outdoor)} "
          f"({100*outdoor['reclassified'].sum()/len(outdoor):.1f}%)")
    print("\nBy direction:")
    print(outdoor[outdoor["reclassified"]]["reclassification_direction"].value_counts())
    print("\nBy morphology:")
    print(outdoor.groupby("morphology")["reclassified"].mean().mul(100).round(1))
    print("\nBy timestamp:")
    print(outdoor.groupby("timestamp")["reclassified"].mean().mul(100).round(1))
    print("\nUTCI category counts:")
    print(outdoor["utci_category"].value_counts())

    return out


if __name__ == "__main__":
    main()
