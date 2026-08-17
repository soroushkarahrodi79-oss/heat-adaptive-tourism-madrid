"""
Phase 2.1 Audit 1: run SOLWEIG for the REAL_SATELLITE, SENS_A, and SENS_B
solar-forcing scenarios (BASELINE is Phase 2's own locked, unmodified
result - not re-run here). Reuses the EXACT SAME locked surface geometry
(DSM/DEM/CDSM, and the cached SVF/shadow matrices from Phase 2) - only
`global_rad` varies between scenarios and versus Phase 2's baseline; Ta/RH/
wind/pressure are identical to Phase 2 in every scenario, and no SOLWEIG
parameter is touched, per the task's explicit restrictions.
"""
from pathlib import Path

import pandas as pd
import solweig
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
INTERIM = ROOT / "data" / "interim" / "solweig"
RAW = ROOT / "data" / "raw"
CACHE = ROOT / "data" / "interim" / "solweig_cache"  # Phase 2's own cache - reused, not rebuilt
OUT = ROOT / "data" / "interim" / "solweig_cache_phase2_1"

UTC_OFFSET = 2
TIMESTAMP_LABELS = {"12:00": "1200", "15:00": "1500", "18:00": "1800"}
SCENARIOS = ["REAL_SATELLITE", "SENS_A_minus10pct", "SENS_B_minus20pct"]


def run():
    OUT.mkdir(parents=True, exist_ok=True)

    print("Loading the SAME locked surface geometry SOLWEIG prepared for Phase 2 "
          "(reusing the cached SVF/shadow matrices - geometry is unchanged)...")
    surface = solweig.SurfaceData.prepare(
        dsm=str(INTERIM / "dsm_2m5.tif"),
        cdsm=str(INTERIM / "cdsm_2m5.tif"),
        dem=str(INTERIM / "dem_2m5.tif"),
        working_dir=str(CACHE),
        dsm_relative=False,
        cdsm_relative=True,
    )
    location = solweig.Location.from_surface(surface, utc_offset=UTC_OFFSET, altitude=650.0)

    scenarios_df = pd.read_csv(RAW / "phase2_1_solar_scenarios.csv")

    for scenario in SCENARIOS:
        sdf = scenarios_df[scenarios_df["scenario"] == scenario]
        for _, row in sdf.iterrows():
            local_time = row["local_time"]
            label = TIMESTAMP_LABELS[local_time]
            hh, mm = map(int, local_time.split(":"))
            weather = solweig.Weather(
                datetime=datetime(2023, 8, 21, hh, mm),
                ta=float(row["ta_c"]),
                rh=float(row["rh_pct"]),
                global_rad=float(row["ghi_wm2"]),  # ONLY this differs from Phase 2 baseline / between scenarios
                ws=float(row["ws_ms"]),
                pressure=float(row["pressure_hpa"]),
            )
            out_dir = OUT / scenario / f"run_{label}"
            print(f"\n=== {scenario} @ {local_time} local: ta={weather.ta}C ghi={weather.global_rad}W/m2 ===")
            summary = solweig.calculate(
                surface=surface, weather=weather, location=location,
                output_dir=str(out_dir), outputs=["tmrt", "utci"],
            )
            print(f"  Tmrt mean={summary.tmrt_mean.mean():.1f}C range={summary.tmrt_mean.min():.1f}-{summary.tmrt_mean.max():.1f}C")
            print(f"  UTCI mean={summary.utci_mean.mean():.1f}C range={summary.utci_mean.min():.1f}-{summary.utci_mean.max():.1f}C")


if __name__ == "__main__":
    run()
