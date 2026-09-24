"""
Independent re-execution check for the HATI-Madrid screening chain (Layer A).

Re-runs the EXISTING, unmodified pipeline scripts in a disposable copy of the
repository and compares every regenerated table with the locked reference copy
in this repository. Nothing inside the repository is written.

Chain re-executed (analysis environment only; SOLWEIG is NOT re-run):
  committed SOLWEIG UTCI/Tmrt rasters (outputs/maps/*.tif)
    -> src/extract_asset_thermal_exposure.py   per-asset UTCI, proxy vs physical
    -> src/phase2_2_decision_confidence.py     ROBUST / BOUNDARY / UNSTABLE
    -> src/phase3_extract_opening_hours.py     OSM opening-hours harvest
    -> src/phase3_build_catalog.py             27-asset catalogue
    -> src/phase3_candidate_screening.py       context-free gates
    -> src/phase3_scenarios.py                 8 scenarios + nearest-open baseline
    -> src/phase3_validation.py                accessibility sensitivity
  + the headline-number assertions embedded in three publication figure scripts.

Model-derived inputs taken AS GIVEN (not regenerated here): the SOLWEIG rasters,
data/processed/phase2_1_solar_scenario_assets.csv and
data/processed/phase2_2_corrected_geometry_utci.csv (both need SOLWEIG runs).

Comparison rule: identical column names/order and row count; numeric columns
equal within an absolute tolerance of 1e-9; text columns exactly equal. Byte
identity is reported for information only (the locked tables were written on
Windows with CRLF line endings, so byte identity is not expected on Linux/macOS).

Usage (Windows, macOS or Linux; needs the packages in requirements.txt):
    python professional/reproduce_screening.py [--workdir DIR] [--keep]
Exit code 0 = every step ran and every table matched; 1 otherwise.
"""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]

STEPS = [
    "src/extract_asset_thermal_exposure.py",
    "src/phase2_2_decision_confidence.py",
    "src/phase3_extract_opening_hours.py",
    "src/phase3_build_catalog.py",
    "src/phase3_candidate_screening.py",
    "src/phase3_scenarios.py",
    "src/phase3_validation.py",
]

# Figure scripts that assert locked headline numbers before saving.
FIGURE_ASSERTIONS = [
    "outputs/publication/figures/render_fig02.py",  # FIG02: 42/14/9/5
    "outputs/publication/figures/render_fig04.py",  # FIG03: 7/8, 3/8, 23, S8
    "outputs/publication/figures/render_fig05.py",  # FIG04: 1/0/0, 35/6/1
]

TABLES = [
    "data/processed/phase2_asset_thermal_exposure.csv",
    "data/processed/phase2_2_decision_confidence.csv",
    "data/processed/phase3_osm_opening_hours_raw.csv",
    "data/processed/phase3_asset_catalog.csv",
    "data/processed/phase3_candidate_screening.csv",
    "data/processed/phase3_scenarios.csv",
    "data/processed/phase3_scenarios_summary.csv",
    "outputs/tables/phase3_exclusion_reasons.csv",
    "outputs/tables/phase3_hati_vs_baseline.csv",
    "outputs/tables/phase3_accessibility_sensitivity.csv",
]

COPY_IGNORE = shutil.ignore_patterns(".git", ".venv*", "venv*", "__pycache__", ".pytest_cache")


def run(script, cwd, log_dir):
    log = log_dir / (Path(script).stem + ".log")
    with open(log, "w", encoding="utf-8") as fh:
        proc = subprocess.run([sys.executable, script], cwd=cwd, stdout=fh, stderr=subprocess.STDOUT)
    return proc.returncode, log


def compare_table(rel, work):
    ref = pd.read_csv(REPO / rel)
    rep = pd.read_csv(work / rel)
    problems = []
    if list(ref.columns) != list(rep.columns):
        problems.append("column names/order differ")
    if ref.shape != rep.shape:
        problems.append(f"shape {rep.shape} vs reference {ref.shape}")
    if not problems:
        for col in ref.columns:
            a, b = ref[col], rep[col]
            if pd.api.types.is_numeric_dtype(a) and pd.api.types.is_numeric_dtype(b):
                if not np.allclose(a.to_numpy(float), b.to_numpy(float), rtol=0, atol=1e-9, equal_nan=True):
                    problems.append(f"numeric mismatch in '{col}'")
            else:
                if not a.fillna("<NA>").astype(str).equals(b.fillna("<NA>").astype(str)):
                    problems.append(f"value mismatch in '{col}'")
    ref_bytes, rep_bytes = (REPO / rel).read_bytes(), (work / rel).read_bytes()
    byte_identical = ref_bytes == rep_bytes
    eol_identical = ref_bytes.replace(b"\r\n", b"\n") == rep_bytes.replace(b"\r\n", b"\n")
    return problems, byte_identical, eol_identical, len(rep)


def headline_numbers(work):
    """Recompute the headline results from the REPRODUCED tables."""
    t = pd.read_csv(work / "data/processed/phase2_asset_thermal_exposure.csv")
    o = t[t.indoor_outdoor == "outdoor"]
    direction = o.reclassification_direction.fillna("")
    bl = pd.read_csv(work / "outputs/tables/phase3_hati_vs_baseline.csv")
    summ = pd.read_csv(work / "data/processed/phase3_scenarios_summary.csv")
    conf = pd.read_csv(work / "data/processed/phase2_2_decision_confidence.csv")
    failing = bl[~bl.baseline_pick_survives_hati]
    return {
        "outdoor observations": len(o),
        "reclassified (proxy vs physical)": int(o.reclassified.sum()),
        "  of which physical MORE restrictive": int(direction.str.contains("MORE").sum()),
        "  of which physical LESS restrictive": int(direction.str.contains("LESS").sum()),
        "reclassification rate by timestamp (%)":
            o.groupby("timestamp").reclassified.mean().mul(100).round(1).to_dict(),
        "scenarios whose candidate set changed vs nearest-open baseline":
            f"{int(bl.candidate_set_changed.sum())}/{len(bl)}",
        "scenarios whose nearest-open pick is excluded by the screening":
            f"{len(failing)}/{len(bl)} "
            f"{dict(zip(failing.scenario, failing.baseline_pick_hati_exclusion))}",
        "open-in-radius candidates removed by thermal/evidence gates (sum)":
            int(bl.n_removed_by_hati_thermal_or_evidence.sum()),
        "no-survivor scenarios":
            list(summ.loc[summ.recommendation == "NO_DEFENSIBLE_ALTERNATIVE", "scenario"]),
        "decision confidence (outdoor rows)": conf.decision_confidence.value_counts().to_dict(),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--workdir", type=Path, help="empty directory for the disposable copy")
    ap.add_argument("--keep", action="store_true", help="keep the disposable copy afterwards")
    args = ap.parse_args()

    base = args.workdir.resolve() if args.workdir else Path(tempfile.mkdtemp(prefix="hati_repro_"))
    if base == REPO or REPO in base.parents:
        sys.exit("refusing to run inside the repository: choose a --workdir outside it")
    work = base / "repo_copy"
    logs = base / "logs"
    if work.exists():
        sys.exit(f"{work} already exists; use an empty --workdir")
    logs.mkdir(parents=True, exist_ok=True)

    print(f"python      : {sys.version.split()[0]} ({sys.executable})")
    print(f"pandas/numpy: {pd.__version__} / {np.__version__}")
    print(f"repository  : {REPO}")
    print(f"copy        : {work}\n")
    shutil.copytree(REPO, work, ignore=COPY_IGNORE)

    ok = True
    print("== Pipeline steps (existing scripts, unmodified)")
    for s in STEPS + FIGURE_ASSERTIONS:
        code, log = run(s, work, logs)
        ok &= code == 0
        print(f"  [{'OK ' if code == 0 else 'FAIL'}] {s}  (exit {code}, log: {log.name})")
        if code != 0:
            print("        " + log.read_text(encoding="utf-8").strip().splitlines()[-1])
            break

    if ok:
        print("\n== Reproduced tables vs locked reference")
        for rel in TABLES:
            problems, byte_id, eol_id, n = compare_table(rel, work)
            ok &= not problems
            status = "MATCH" if not problems else "DIFFER"
            text = "byte-identical" if byte_id else ("text-identical except line endings" if eol_id else "text differs")
            print(f"  [{status}] {rel}  rows={n}  ({text})")
            for p in problems:
                print(f"        - {p}")

        print("\n== Headline numbers recomputed from the reproduced tables")
        for k, v in headline_numbers(work).items():
            print(f"  {k}: {v}")

    print(f"\nRESULT: {'PASS - all steps ran and all tables matched' if ok else 'FAIL - see above'}")
    if args.keep or not ok:
        print(f"(copy and logs kept in {base})")
    else:
        shutil.rmtree(base, ignore_errors=True)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
