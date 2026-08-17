"""
Phase 1.1 Audit 2: EXTREME meteorological-hazard branch validation.

The Phase 1 baseline's three fixed timestamps (12:00/15:00/18:00 local,
2023-08-21) never reached AEMET's EXTREME (>=42C) warning band - the branch was
implemented but empirically untested (docs/PHASE1_VALIDATION_REPORT.md S5).

This script does NOT fabricate a temperature to force the branch. It runs the
existing, unmodified architecture (src/build_classifications.py's
compute_site_metrics / feasibility_decision / evidence_confidence) against a
REAL, officially-documented Madrid extreme-heat day: 2021-08-14, part of an
AEMET-confirmed "intensa ola de calor" (11-15 Aug 2021), during which Barajas
recorded an official daily max of 42.7C (data/raw/aemet_official_pdfs/
AEMET_avance_climat_MAD_202108.pdf) - AEMET's own account of an all-time record
for that station at the time. This project's own real hourly extract for that
day (data/raw/extreme_aug2021_barajas_raw.csv) independently confirms 42.4C at
18:00 local, using the identical three canonical clock times
(12:00/15:00/18:00) the Phase 1 baseline already uses, for direct comparability.

SCOPE STATEMENT (read before interpreting output): this is an ARCHITECTURE
STRESS TEST, not a second real episode adopted by the project. The exposure and
adaptation-resource layers (tree counts, water/transit distances) are the
current (2026) OSM snapshot, not conditions on 2021-08-14 - exactly the same
temporal-mismatch caveat already documented for the Phase 1 baseline's own
2023-08-21 episode (docs/PHASE1_DATA_PROVENANCE.md S3.1), just three years
larger. The output answers "does the EXTREME branch behave sensibly when a real
extreme reading is fed into it", not "what was thermal suitability actually like
on 2021-08-14".
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thresholds as th
from build_classifications import (
    load_assets, compute_site_metrics, feasibility_decision, evidence_confidence,
)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

EPISODE_DATE = "2021-08-14"
TIMESTAMPS = [("12:00", "10"), ("15:00", "13"), ("18:00", "16")]  # identical to Phase 1 baseline
STATION_NOTE = (
    "STRESS TEST using a real, AEMET-confirmed extreme-heat day (2021-08-14, "
    "official Barajas daily max 42.7C per AEMET's August 2021 Comunidad de "
    "Madrid climatological advance report) - NOT the project's adopted episode "
    "(that remains 2023-08-21). Exposure/adaptation layers are the current "
    "(2026) OSM snapshot, not 2021 conditions - see module docstring."
)


def load_2021_hazard_readings():
    df = pd.read_csv(RAW / "extreme_aug2021_barajas_raw.csv", dtype={"hour_utc": str})
    df = df[df["date"] == EPISODE_DATE]
    out = {}
    for local_time, utc_hour in TIMESTAMPS:
        row = df[df["hour_utc"] == utc_hour.zfill(2)]
        out[local_time] = float(row.iloc[0]["temp_c"]) if not row.empty else None
    return out


def run():
    hazard_by_time = load_2021_hazard_readings()
    print(f"Real Barajas hourly readings, {EPISODE_DATE} (local Europe/Madrid, official AEMET daily max 42.7C):")
    for t, v in hazard_by_time.items():
        print(f"  {t} -> {v} C -> {th.meteorological_hazard_state(v)}")

    assets = load_assets()
    assets, tercile_cuts = compute_site_metrics(assets)

    rows = []
    for _, a in assets.iterrows():
        for local_time, utc_hour in TIMESTAMPS:
            temp_c = hazard_by_time[local_time]
            hz = th.meteorological_hazard_state(temp_c)
            row = {
                "asset_id": a["asset_id"], "name": a["name"],
                "indoor_outdoor": a["indoor_outdoor"],
                "timestamp": f"{EPISODE_DATE}T{local_time}:00+02:00",
                "temp_c_barajas": temp_c,
                "meteorological_hazard_state": hz,
                "tree_count_50m": a["tree_count_50m"],
                "exposure_state": a["exposure_state"],
                "exposure_override_note": a["exposure_override_note"],
                "water_dist_m": a["water_dist_m"],
                "transit_dist_m": a["transit_dist_m"],
                "adaptation_state": a["adaptation_state"],
            }
            feas, reason, missing = feasibility_decision(row)
            row["feasibility_state"] = feas
            row["exclusion_reason"] = reason if feas in ("NOT RECOMMENDED", "INSUFFICIENT EVIDENCE") else ""
            row["evidence_confidence"] = evidence_confidence(row)
            row["stress_test_note"] = STATION_NOTE
            rows.append(row)

    out = pd.DataFrame(rows)
    cols = ["asset_id", "name", "indoor_outdoor", "timestamp", "temp_c_barajas",
            "meteorological_hazard_state", "tree_count_50m", "exposure_state",
            "water_dist_m", "transit_dist_m", "adaptation_state",
            "feasibility_state", "exclusion_reason", "evidence_confidence",
            "stress_test_note"]
    out = out[cols]
    out_path = PROCESSED / "extreme_branch_stress_test_2021-08-14.csv"
    out.to_csv(out_path, index=False, encoding="utf-8")
    print(f"\nWrote {out_path} with {len(out)} rows")

    print("\nFeasibility state counts (all 3 timestamps):")
    print(out["feasibility_state"].value_counts())

    ext = out[out["meteorological_hazard_state"] == "EXTREME"]
    print(f"\n--- EXTREME-hazard timestamp only (18:00 local, {ext['temp_c_barajas'].iloc[0]}C) ---")
    print(ext["feasibility_state"].value_counts())
    print("\nIndoor assets at EXTREME (should all be FEASIBLE WITH CONDITIONS per rule):")
    print(ext[ext["indoor_outdoor"] == "indoor"][["asset_id", "name", "feasibility_state"]].to_string(index=False))
    print("\nOutdoor assets at EXTREME (should ALL be NOT RECOMMENDED per rule 1, unconditionally):")
    print(ext[ext["indoor_outdoor"] == "outdoor"][["asset_id", "name", "exposure_state", "adaptation_state", "feasibility_state"]].to_string(index=False))

    return out


if __name__ == "__main__":
    run()
