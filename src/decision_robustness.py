"""
Phase 2.1 Audit 3: decision robustness classification.

Combines Audit 1 (solar-forcing scenario results,
data/processed/phase2_1_solar_scenario_assets.csv) and Audit 2 (vegetation-
geometry confidence flags, data/processed/phase2_1_geometry_confidence.csv)
into a ROBUST / BOUNDARY / UNSTABLE label for every one of the 42 outdoor
asset x timestamp rows from the LOCKED Phase 2 baseline
(data/processed/phase2_asset_thermal_exposure.csv - not modified).

Classification rule (documented, decided before inspecting the combined
table's overall pass/fail rate, so it is not tuned to hit a particular
ROBUST percentage):

  UNSTABLE  - the feasibility_state decision ACTUALLY CHANGES in at least
              one tested solar scenario (Audit 1), OR the asset is
              geometry-flagged POSSIBLY STALE (Audit 2) AND the baseline
              UTCI is within 2 C of the 46 C NOT-RECOMMENDED threshold
              (i.e. plausible geometry correction could plausibly flip it).
  BOUNDARY  - no tested scenario changes the decision, but EITHER the
              baseline UTCI is within 2 C of a decision threshold (32 or
              46 C) under solar testing, OR the asset is geometry-flagged
              POSSIBLY STALE / PARTIALLY REPRESENTATIVE (reduced confidence
              in the exact number, even though no threshold crossing was
              found).
  ROBUST    - no tested scenario changes the decision, baseline UTCI is not
              within 2 C of a threshold, and the asset (if audited in
              Audit 2) is geometry-flagged REPRESENTATIVE, or the asset was
              not part of the 8-asset geometry audit (Audit 2 was a
              targeted, not exhaustive, sample - assets outside the sample
              are not penalised for a check that was never run on them,
              but are also not asserted geometry-confirmed - this is
              stated explicitly in the output evidence_note).
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"

THRESHOLD_MARGIN_C = 2.0
UTCI_THRESHOLDS = [32.0, 46.0]


def nearest_threshold_distance(utci):
    return min(abs(utci - t) for t in UTCI_THRESHOLDS)


def main():
    baseline = pd.read_csv(PROCESSED / "phase2_asset_thermal_exposure.csv")
    baseline_outdoor = baseline[baseline["indoor_outdoor"] == "outdoor"].copy()

    solar = pd.read_csv(PROCESSED / "phase2_1_solar_scenario_assets.csv")
    geometry = pd.read_csv(PROCESSED / "phase2_1_geometry_confidence.csv").set_index("asset_id")

    rows = []
    for _, b in baseline_outdoor.iterrows():
        aid, ts = b["asset_id"], b["timestamp"]
        base_utci = b["utci_mean_10m"]
        base_feas = b["feasibility_phase2_physical"]

        scen = solar[(solar.asset_id == aid) & (solar.timestamp == ts)]
        any_decision_flip = bool(scen["decision_changed_vs_phase2_baseline"].any())
        min_utci_scen = scen["utci_mean_10m"].min() if len(scen) else base_utci
        max_utci_scen = scen["utci_mean_10m"].max() if len(scen) else base_utci
        min_dist_scen = min(nearest_threshold_distance(v) for v in
                             list(scen["utci_mean_10m"]) + [base_utci]) if len(scen) else nearest_threshold_distance(base_utci)

        geom_flag = geometry.loc[aid, "geometry_confidence"] if aid in geometry.index else "NOT AUDITED"

        reasons = []
        if any_decision_flip:
            label = "UNSTABLE"
            flipped_scenarios = scen[scen["decision_changed_vs_phase2_baseline"]]["scenario"].tolist()
            reasons.append(f"decision changes under solar scenario(s): {', '.join(flipped_scenarios)}")
        elif geom_flag == "POSSIBLY STALE" and (46.0 - base_utci) <= 2.0:
            label = "UNSTABLE"
            reasons.append(f"geometry-flagged POSSIBLY STALE and baseline UTCI ({base_utci}C) within "
                            f"{THRESHOLD_MARGIN_C}C of the 46C NOT-RECOMMENDED threshold - plausible canopy "
                            f"correction could flip this decision")
        else:
            label = "ROBUST"
            if min_dist_scen <= THRESHOLD_MARGIN_C:
                label = "BOUNDARY"
                reasons.append(f"UTCI ({min_utci_scen}-{max_utci_scen}C across scenarios) within "
                                f"{THRESHOLD_MARGIN_C}C of a decision threshold (32/46C), though no scenario "
                                f"actually crossed it")
            if geom_flag in ("POSSIBLY STALE", "PARTIALLY REPRESENTATIVE"):
                label = "BOUNDARY"
                reasons.append(f"asset geometry-flagged {geom_flag} (Audit 2) - reduced confidence in the "
                                f"exact modelled value even though no threshold crossing was found")
            if not reasons:
                reasons.append("no decision flip under any tested solar scenario; UTCI not near a threshold"
                                + ("; geometry-audited REPRESENTATIVE" if geom_flag == "REPRESENTATIVE"
                                   else "; not part of the 8-asset geometry audit sample"))

        rows.append({
            "asset_id": aid, "name": b["name"], "morphology": b.get("morphology", ""), "timestamp": ts,
            "baseline_utci_10m": base_utci, "baseline_feasibility": base_feas,
            "solar_scenario_utci_min": round(min_utci_scen, 1), "solar_scenario_utci_max": round(max_utci_scen, 1),
            "solar_decision_flip": any_decision_flip,
            "geometry_confidence_flag": geom_flag,
            "robustness": label,
            "reason": "; ".join(reasons),
        })

    out = pd.DataFrame(rows)
    out_path = PROCESSED / "phase2_1_robustness.csv"
    out.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Wrote {out_path} with {len(out)} rows")

    print("\n=== Robustness distribution ===")
    counts = out["robustness"].value_counts()
    print(counts)
    print((100 * counts / len(out)).round(1))

    print("\n=== BOUNDARY / UNSTABLE rows with reasons ===")
    flagged = out[out["robustness"] != "ROBUST"]
    for _, r in flagged.iterrows():
        print(f"  [{r['robustness']}] {r['asset_id']} {r['name']} @ {r['timestamp']}: {r['reason']}")

    # Decision-table version for outputs/tables/decision_robustness.csv
    table_path = ROOT / "outputs" / "tables" / "decision_robustness.csv"
    summary_rows = []
    for label, g in out.groupby("robustness"):
        summary_rows.append({"robustness": label, "count": len(g), "pct": round(100 * len(g) / len(out), 1)})
    for morph, g in out.groupby("morphology"):
        for label in ["ROBUST", "BOUNDARY", "UNSTABLE"]:
            n = (g["robustness"] == label).sum()
            summary_rows.append({"robustness": f"{label} [{morph}]", "count": n,
                                  "pct": round(100 * n / len(g), 1) if len(g) else 0})
    pd.DataFrame(summary_rows).to_csv(table_path, index=False, encoding="utf-8")
    print(f"\nWrote {table_path}")

    return out


if __name__ == "__main__":
    main()
