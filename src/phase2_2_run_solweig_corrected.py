"""
Phase 2.2 Task A, step 3: run SOLWEIG on the localized corrected-canopy CDSM
variant(s) built by phase2_2_build_corrected_cdsm.py. Uses the EXACT Phase 2
baseline weather (data/raw/phase2_met_forcing.csv) - only the CDSM geometry
differs from Phase 2, and only in the A23/A27 30 m neighbourhoods. Ta/RH/wind/
pressure/GHI are Phase 2's own clear-sky baseline values, so any change vs
Phase 2 is attributable solely to the corrected canopy geometry.

Separate cache + output tree (data/interim/solweig_cache_phase2_2/) - Phase 2
and Phase 2.1 caches/outputs are never touched. A fresh SVF/shadow precompute
is required per variant because the canopy changed (the Phase 2 cache is only
valid for the Phase 2 geometry).

Usage: python phase2_2_run_solweig_corrected.py [central|narrow|wide ...]
       (default: central)
"""
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import solweig

ROOT = Path(__file__).resolve().parents[1]
GEOM_ROOT = ROOT / "data" / "interim" / "solweig_phase2_2"
RAW = ROOT / "data" / "raw"
CACHE_ROOT = ROOT / "data" / "interim" / "solweig_cache_phase2_2"

UTC_OFFSET = 2
TIMESTAMP_LABELS = {"12:00": "1200", "15:00": "1500", "18:00": "1800"}


def run_variant(variant):
    gdir = GEOM_ROOT / variant
    cache = CACHE_ROOT / variant
    cache.mkdir(parents=True, exist_ok=True)
    print(f"\n########## VARIANT: {variant} ##########")
    print("Preparing surface (fresh SVF + shadow matrices for corrected canopy)...")
    surface = solweig.SurfaceData.prepare(
        dsm=str(gdir / "dsm_2m5.tif"),
        cdsm=str(gdir / "cdsm_2m5.tif"),
        dem=str(gdir / "dem_2m5.tif"),
        working_dir=str(cache),
        dsm_relative=False,
        cdsm_relative=True,
    )
    location = solweig.Location.from_surface(surface, utc_offset=UTC_OFFSET, altitude=650.0)
    met = pd.read_csv(RAW / "phase2_met_forcing.csv")

    for _, row in met.iterrows():
        local_time = row["local_time"]
        label = TIMESTAMP_LABELS[local_time]
        hh, mm = map(int, local_time.split(":"))
        weather = solweig.Weather(
            datetime=datetime(2023, 8, 21, hh, mm),
            ta=float(row["ta_c"]), rh=float(row["rh_pct"]),
            global_rad=float(row["ghi_wm2"]), ws=float(row["ws_ms"]),
            pressure=float(row["pressure_hpa"]),
        )
        out_dir = cache / f"run_{label}"
        print(f"=== {variant} @ {local_time}: ta={weather.ta}C ghi={weather.global_rad}W/m2 ===")
        summary = solweig.calculate(
            surface=surface, weather=weather, location=location,
            output_dir=str(out_dir), outputs=["tmrt", "utci"],
        )
        print(f"  Tmrt mean={summary.tmrt_mean.mean():.1f}C  UTCI mean={summary.utci_mean.mean():.1f}C")


if __name__ == "__main__":
    variants = sys.argv[1:] or ["central"]
    for v in variants:
        run_variant(v)
