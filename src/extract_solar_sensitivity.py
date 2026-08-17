"""
Phase 2.1 Audit 1: extract per-asset Tmrt/UTCI (pre-registered 10 m buffer
mean - same statistic and same asset points as Phase 2, src/phase2_prereg.py)
for the three solar-forcing scenarios, and compare each against the LOCKED
Phase 2 BASELINE result (data/processed/phase2_asset_thermal_exposure.csv,
not modified).
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from rasterstats import zonal_stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phase2_prereg import PRIMARY_BUFFER_M
from extract_asset_thermal_exposure import utci_category, utci_to_feasibility

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
CACHE = ROOT / "data" / "interim" / "solweig_cache_phase2_1"
WGS84 = "EPSG:4326"
UTM30N = "EPSG:25830"

SCENARIOS = ["REAL_SATELLITE", "SENS_A_minus10pct", "SENS_B_minus20pct"]
TIMESTAMP_LABELS = {"12:00": "1200", "15:00": "1500", "18:00": "1800"}


def load_assets():
    df = pd.read_csv(PROCESSED / "pilot_assets.csv")
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs=WGS84)
    return gdf[gdf["indoor_outdoor"] == "outdoor"].to_crs(UTM30N)


def main():
    assets = load_assets()
    buffers = assets.geometry.buffer(PRIMARY_BUFFER_M)
    baseline = pd.read_csv(PROCESSED / "phase2_asset_thermal_exposure.csv")
    baseline_outdoor = baseline[baseline["indoor_outdoor"] == "outdoor"]

    rows = []
    for scenario in SCENARIOS:
        for local_time, label in TIMESTAMP_LABELS.items():
            tmrt_path = CACHE / scenario / f"run_{label}" / "tmrt" / f"tmrt_20230821_{label}.tif"
            utci_path = CACHE / scenario / f"run_{label}" / "utci" / f"utci_20230821_{label}.tif"
            tmrt_stats = zonal_stats(buffers, str(tmrt_path), stats=["mean"])
            utci_stats = zonal_stats(buffers, str(utci_path), stats=["mean"])

            for i, (_, a) in enumerate(assets.iterrows()):
                aid = a["asset_id"]
                base_row = baseline_outdoor[(baseline_outdoor.asset_id == aid) & (baseline_outdoor.timestamp == local_time)]
                base_feas = base_row.iloc[0]["feasibility_phase1_proxy"]  # Phase 1 proxy, for the 3-way comparison
                base_phys_feas = base_row.iloc[0]["feasibility_phase2_physical"]
                base_utci = base_row.iloc[0]["utci_mean_10m"]

                utci_mean = round(float(utci_stats[i]["mean"]), 1)
                tmrt_mean = round(float(tmrt_stats[i]["mean"]), 1)
                scenario_feas = utci_to_feasibility(utci_mean)

                rows.append({
                    "scenario": scenario, "asset_id": aid, "name": a["name"], "timestamp": local_time,
                    "tmrt_mean_10m": tmrt_mean, "utci_mean_10m": utci_mean,
                    "utci_category": utci_category(utci_mean),
                    "feasibility_this_scenario": scenario_feas,
                    "feasibility_phase2_baseline": base_phys_feas,
                    "feasibility_phase1_proxy": base_feas,
                    "utci_delta_vs_baseline": round(utci_mean - base_utci, 1),
                    "decision_changed_vs_phase2_baseline": scenario_feas != base_phys_feas,
                })

    out = pd.DataFrame(rows)
    out_path = ROOT / "data" / "processed" / "phase2_1_solar_scenario_assets.csv"
    out.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Wrote {out_path} with {len(out)} rows")

    print("\n=== Decision changes vs Phase 2 baseline, by scenario ===")
    for scenario, g in out.groupby("scenario"):
        n_changed = g["decision_changed_vs_phase2_baseline"].sum()
        print(f"  {scenario}: {n_changed} / {len(g)} ({100*n_changed/len(g):.1f}%) decisions changed")

    print("\n=== UTCI delta stats by scenario ===")
    print(out.groupby("scenario")["utci_delta_vs_baseline"].agg(["mean", "min", "max"]).round(2))

    print("\n=== 12:00 finding check: does UTCI stay >= 32 (Strong+) at 12:00 in every scenario? ===")
    noon = out[out["timestamp"] == "12:00"]
    for scenario, g in noon.groupby("scenario"):
        n_above32 = (g["utci_mean_10m"] >= 32).sum()
        print(f"  {scenario}: {n_above32}/{len(g)} assets >= 32C UTCI at 12:00 "
              f"(min={g['utci_mean_10m'].min():.1f}, max={g['utci_mean_10m'].max():.1f})")

    return out


if __name__ == "__main__":
    main()
