"""
Phase 2.2 Task A, step 4: extract the pre-registered 10 m-buffer mean UTCI at
the corrected assets (A23, A27) from each corrected-canopy variant, alongside
A24 as an UNCHANGED CONTROL (its neighbourhood canopy was not modified, so its
value must match Phase 2 to within rounding - a built-in sanity check that the
localized edit did not perturb the rest of the grid).

Uses the SAME extraction convention as Phase 2 (phase2_prereg.PRIMARY_BUFFER_M
= 10 m, zonal mean) so corrected and original UTCI are directly comparable.
"""
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from rasterstats import zonal_stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phase2_prereg import PRIMARY_BUFFER_M

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
CACHE_ROOT = ROOT / "data" / "interim" / "solweig_cache_phase2_2"
WGS84 = "EPSG:4326"
UTM30N = "EPSG:25830"

ASSETS = ["A23", "A24", "A27"]            # A24 = unchanged control
VARIANTS = ["narrow", "central", "wide"]
TIMESTAMPS = [("12:00", "1200"), ("15:00", "1500"), ("18:00", "1800")]


def utci_to_feasibility(u):
    if u >= 46:
        return "NOT RECOMMENDED"
    if u >= 32:
        return "FEASIBLE WITH CONDITIONS"
    return "FEASIBLE"


def main():
    df = pd.read_csv(PROCESSED / "pilot_assets.csv")
    df = df[df["asset_id"].isin(ASSETS)]
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude),
                           crs=WGS84).to_crs(UTM30N)
    buffers = gdf.geometry.buffer(PRIMARY_BUFFER_M)

    base = pd.read_csv(PROCESSED / "phase2_asset_thermal_exposure.csv")

    rows = []
    for variant in VARIANTS:
        for local_time, label in TIMESTAMPS:
            utci_tif = CACHE_ROOT / variant / f"run_{label}" / "utci" / f"utci_20230821_{label}.tif"
            if not utci_tif.exists():
                # some solweig builds name single-step output without date; find it
                cand = list((CACHE_ROOT / variant / f"run_{label}" / "utci").glob("utci_*.tif"))
                utci_tif = cand[0] if cand else utci_tif
            stats = zonal_stats(buffers, str(utci_tif), stats=["mean"], nodata=np.nan)
            for i, (_, a) in enumerate(gdf.iterrows()):
                aid = a["asset_id"]
                u_corr = round(float(stats[i]["mean"]), 1)
                brow = base[(base.asset_id == aid) & (base.timestamp == local_time)].iloc[0]
                u_base = float(brow["utci_mean_10m"])
                rows.append({
                    "variant": variant, "crown_radius_m": {"narrow": 2.0, "central": 3.0, "wide": 4.0}[variant],
                    "asset_id": aid, "name": a["name"], "timestamp": local_time,
                    "utci_phase2_baseline": u_base,
                    "utci_corrected": u_corr,
                    "utci_delta": round(u_corr - u_base, 1),
                    "feas_phase2_baseline": brow["feasibility_phase2_physical"],
                    "feas_corrected": utci_to_feasibility(u_corr),
                    "decision_changed": utci_to_feasibility(u_corr) != brow["feasibility_phase2_physical"],
                    "corrected_here": aid in ("A23", "A27"),
                })
    out = pd.DataFrame(rows)
    out_path = PROCESSED / "phase2_2_corrected_geometry_utci.csv"
    out.to_csv(out_path, index=False, encoding="utf-8")
    pd.set_option("display.width", 220, "display.max_columns", 60)
    print(out.to_string(index=False))
    print(f"\nWrote {out_path}")

    # Control check: A24 (uncorrected) deltas must be ~0
    ctrl = out[out.asset_id == "A24"]
    print(f"\nCONTROL A24 max |delta| across variants/timestamps: {ctrl['utci_delta'].abs().max()} C "
          f"(should be ~0.0 - confirms localized edit did not perturb rest of grid)")
    return out


if __name__ == "__main__":
    main()
