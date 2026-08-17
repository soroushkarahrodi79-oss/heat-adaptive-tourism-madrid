"""
Phase 2: run SOLWEIG (package `solweig`, v0.1.0b92, UMEP-dev, pip-installed
in a dedicated Python 3.12 venv - see docs/PHASE2_SOLWEIG_METHOD.md for the
exact environment/version/workflow record) for the three real 2023-08-21
timestamps, producing per-timestep Tmrt and UTCI GeoTIFFs.

Each of the three timestamps is run as an INDEPENDENT single-step
calculation (not a continuous timeseries) because they are 3 hours apart,
matching how every prior phase of this project has treated these three
timestamps as independent snapshots, not a continuous series.
"""
import sys
from pathlib import Path

import pandas as pd
import solweig
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
INTERIM = ROOT / "data" / "interim" / "solweig"
RAW = ROOT / "data" / "raw"
OUT_MAPS = ROOT / "outputs" / "maps"
CACHE = ROOT / "data" / "interim" / "solweig_cache"

UTC_OFFSET = 2  # CEST, 2023-08-21
TIMESTAMP_LABELS = {"12:00": "1200", "15:00": "1500", "18:00": "1800"}


def run():
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT_MAPS.mkdir(parents=True, exist_ok=True)

    print("Preparing surface (SVF + shadow matrices) - one-time cost, reused for all 3 timestamps...")
    surface = solweig.SurfaceData.prepare(
        dsm=str(INTERIM / "dsm_2m5.tif"),
        cdsm=str(INTERIM / "cdsm_2m5.tif"),
        dem=str(INTERIM / "dem_2m5.tif"),
        working_dir=str(CACHE),
        dsm_relative=False,
        cdsm_relative=True,
    )
    location = solweig.Location.from_surface(surface, utc_offset=UTC_OFFSET, altitude=650.0)
    print(f"Location derived from surface CRS: {location}")

    met = pd.read_csv(RAW / "phase2_met_forcing.csv")

    results = {}
    for _, row in met.iterrows():
        local_time = row["local_time"]
        label = TIMESTAMP_LABELS[local_time]
        hh, mm = map(int, local_time.split(":"))
        weather = solweig.Weather(
            datetime=datetime(2023, 8, 21, hh, mm),
            ta=float(row["ta_c"]),
            rh=float(row["rh_pct"]),
            global_rad=float(row["ghi_wm2"]),
            ws=float(row["ws_ms"]),
            pressure=float(row["pressure_hpa"]),
        )
        out_dir = CACHE / f"run_{label}"
        print(f"\n=== Running SOLWEIG for {local_time} local (CEST), "
              f"ta={weather.ta}C rh={weather.rh}% ghi={weather.global_rad}W/m2 ws={weather.ws}m/s ===")
        summary = solweig.calculate(
            surface=surface,
            weather=weather,
            location=location,
            output_dir=str(out_dir),
            outputs=["tmrt", "utci", "shadow"],
        )
        print(summary.report())
        results[local_time] = summary

        # Copy the TRUE per-timestep raw GeoTIFFs (out_dir/<var>/<var>_YYYYMMDD_HHMM.tif)
        # to outputs/maps with the required names - NOT the summary/*_day_mean.tif
        # aggregates (numerically identical here since each run is a single
        # timestep, but the raw per-timestep file is the correct "preserve raw
        # model output" artefact per the task specification).
        import shutil
        date_str = "20230821"
        for varname in ("tmrt", "utci"):
            src = out_dir / varname / f"{varname}_{date_str}_{label}.tif"
            dst = OUT_MAPS / f"{varname}_{label}.tif"
            if src.exists():
                shutil.copy(src, dst)
                print(f"  Copied {src} -> {dst}")
            else:
                print(f"  WARNING: expected raw output not found: {src}")

    return results


if __name__ == "__main__":
    run()
