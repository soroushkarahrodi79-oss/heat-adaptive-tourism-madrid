"""
Phase 1.2 buffer sensitivity check (NOT the gate decision - see
src/shade_proxy_prereg.py). Runs P1/P2/P3 at the two pre-registered
sensitivity buffer sizes (25 m, 100 m) and reports Madrid-vs-TCD agreement at
each, purely as a documented robustness check on the 50 m primary choice.
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shade_proxy_prereg import SENSITIVITY_BUFFERS_M
from shade_proxy_comparison import build_for_buffer, run_feasibility
from build_classifications import load_assets, load_hazard_readings, UTM30N

ROOT = Path(__file__).resolve().parents[1]
INTERIM = ROOT / "data" / "interim"
RAW = ROOT / "data" / "raw"


def pct_agreement(df, col_a, col_b):
    valid = df.dropna(subset=[col_a, col_b])
    if len(valid) == 0:
        return None, 0
    agree = (valid[col_a] == valid[col_b]).sum()
    return 100 * agree / len(valid), len(valid)


def run():
    madrid_trees = gpd.read_file(INTERIM / "madrid_arbolado_points.geojson").to_crs(UTM30N)
    tif_path = RAW / "copernicus_tcd" / "tcd_2018_study_area.tif"
    hazard_by_time = load_hazard_readings()

    results = []
    for radius in SENSITIVITY_BUFFERS_M:
        assets = load_assets()
        assets, cuts = build_for_buffer(radius, assets, madrid_trees, tif_path, f"b{radius}")
        feas_madrid = run_feasibility(assets, f"exposure_state_madrid_b{radius}", hazard_by_time)
        feas_tcd = run_feasibility(assets, f"exposure_state_tcd_b{radius}", hazard_by_time)
        merged = feas_madrid.merge(feas_tcd, on=["asset_id", "timestamp"], suffixes=("_madrid", "_tcd"))
        outdoor = assets[assets["indoor_outdoor"] == "outdoor"]["asset_id"]
        merged = merged[merged["asset_id"].isin(outdoor)]
        pct, n = pct_agreement(merged, "feasibility_madrid", "feasibility_tcd")
        print(f"Buffer {radius}m: Madrid vs TCD feasibility agreement = {pct:.1f}% (n={n})")
        results.append({"buffer_m": radius, "madrid_vs_tcd_agreement_pct": round(pct, 1), "n": n})

    return pd.DataFrame(results)


if __name__ == "__main__":
    run()
