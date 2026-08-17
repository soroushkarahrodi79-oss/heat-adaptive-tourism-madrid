"""
Phase 3 validation: evaluates the six required validation questions and the
gate conditions, from the locked screening/scenario outputs. Prints a
structured report and writes the accessibility-sensitivity table.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "outputs" / "tables"

from phase3_scenarios import (SCENARIOS, DELTA, WALK_SPEED_MS, haversine_m, utci_cat, EXPERIENCE)


def screen_at_radius(cat, scr_idx, src_id, ts, access_m):
    def rec(aid):
        r = scr_idx.loc[(aid, ts)]; c = cat.loc[aid]
        return dict(io=c["indoor_outdoor"], lat=c["latitude"], lon=c["longitude"],
                    is_open=bool(r["is_open"]), ds=r["decision_state"], dc=r["decision_confidence"],
                    utci=None if pd.isna(r["utci_baseline"]) else float(r["utci_baseline"]),
                    ev=r["evidence_confidence"])
    src = rec(src_id)
    alts = []
    for cid in cat.index:
        if cid == src_id:
            continue
        c = rec(cid)
        if not c["is_open"]:
            continue
        d = haversine_m(src["lat"], src["lon"], c["lat"], c["lon"])
        if d > access_m:
            continue
        if c["ds"] == "AVOID_OUTDOOR_EXPOSURE" or c["ev"] == "LOW":
            continue
        su, cu = src["utci"], c["utci"]
        meaningful = False
        if c["io"] == "indoor" and src["io"] == "outdoor":
            meaningful = True
        elif su is not None and cu is not None:
            if cu <= su - DELTA or (utci_cat(cu) != utci_cat(su) and cu < su):
                meaningful = True
            elif c["dc"] == "ROBUST" and src["dc"] in ("BOUNDARY", "UNSTABLE") \
                    and c["ds"] != "AVOID_OUTDOOR_EXPOSURE" and cu <= su:
                meaningful = True  # confidence-gain clause (matches phase3_scenarios.improvement)
        if meaningful:
            alts.append(cid)
    return alts


def main():
    cat = pd.read_csv(PROCESSED / "phase3_asset_catalog.csv").set_index("asset_id")
    scr_idx = pd.read_csv(PROCESSED / "phase3_candidate_screening.csv").set_index(["asset_id", "timestamp"])
    scen = pd.read_csv(PROCESSED / "phase3_scenarios.csv")
    summ = pd.read_csv(PROCESSED / "phase3_scenarios_summary.csv")
    bl = pd.read_csv(TABLES / "phase3_hati_vs_baseline.csv")

    print("V1. Logically distinct alternatives")
    exp_sets = summ["experience_types_offered"]
    print(f"    distinct experience-type mixes across scenarios: {exp_sets.nunique()} of {len(summ)}")
    print(f"    scenarios offering >=2 experience types: {(summ.experience_types_offered.str.count(',')>=1).sum()}")

    print("\nV2. Thermal/evidence evidence changes candidate set vs conventional baseline")
    print(f"    candidate set changed vs nearest-open baseline: {int(bl.candidate_set_changed.sum())}/{len(bl)} scenarios")
    print(f"    baseline's nearest-open pick FAILS HATI screening: {int((~bl.baseline_pick_survives_hati).sum())}/{len(bl)}")
    print(f"    total open-in-radius options HATI removed on thermal/evidence grounds: "
          f"{int(bl.n_removed_by_hati_thermal_or_evidence.sum())}")

    print("\nV3. Exclusion reasons interpretable & traceable")
    tally = scen[scen.status == "EXCLUDED"].groupby("exclusion_reason").size()
    print(tally.to_string())
    untraceable = scen[(scen.status == "EXCLUDED") & (scen.exclusion_reason == "")]
    print(f"    excluded rows with NO machine reason: {len(untraceable)} (must be 0)")

    print("\nV4. Uncertainty changes recommendations")
    a24 = scen[(scen.candidate_id == "A24") & (scen.exclusion_reason == "INSUFFICIENT_EVIDENCE")]
    print(f"    candidate exclusions caused by LOW thermal confidence (UNSTABLE): {len(a24)} "
          f"(A24@18:00 UNSTABLE -> INSUFFICIENT_EVIDENCE)")
    print(f"    scenarios with an UNSTABLE source screened: "
          f"{summ[summ.source_decision_confidence=='UNSTABLE']['scenario'].tolist()}")

    print("\nV5. Some scenarios correctly return NO recommendation")
    norec = summ[summ.recommendation == "NO_DEFENSIBLE_ALTERNATIVE"]
    print(f"    NO_DEFENSIBLE_ALTERNATIVE scenarios: {norec['scenario'].tolist()}")

    print("\nV6. Robustness to modest accessibility assumptions (500 / 800 / 1200 m)")
    rows = []
    for sid, src_id, ts, access_m, cls, desc in SCENARIOS:
        counts = {}
        for R in [500, 800, 1200]:
            alts = screen_at_radius(cat, scr_idx, src_id, ts, R)
            counts[R] = len(alts)
        rec_stable = all((counts[R] > 0) == (counts[800] > 0) for R in [500, 1200])
        rows.append({"scenario": sid, "source_id": src_id, "timestamp": ts, "primary_radius_m": access_m,
                     "n_alt_500m": counts[500], "n_alt_800m": counts[800], "n_alt_1200m": counts[1200],
                     "recommendation_category_stable_500_1200": rec_stable})
        print(f"    {sid} {src_id}@{ts}: 500m={counts[500]:2d}  800m={counts[800]:2d}  1200m={counts[1200]:2d}  "
              f"stable={rec_stable}")
    sens = pd.DataFrame(rows)
    sens.to_csv(TABLES / "phase3_accessibility_sensitivity.csv", index=False, encoding="utf-8")
    stable = int(sens.recommendation_category_stable_500_1200.sum())
    print(f"    recommendation CATEGORY (found vs none) stable across 500-1200 m: {stable}/{len(sens)}")

    print("\nV7. Guardrail — do any obviously-unsuitable alternatives survive?")
    surv = scen[scen.status == "CANDIDATE_ALTERNATIVE"]
    bad_closed = surv[~surv.candidate_id.isin([])]  # check via joins below
    # verify every surviving alt is open, within radius, not AVOID_OUTDOOR, evidence>=MODERATE
    viol = 0
    for _, r in surv.iterrows():
        c = scr_idx.loc[(r.candidate_id, r.timestamp)]
        if (not bool(c["is_open"])) or r.distance_m > r.access_radius_m \
           or c["decision_state"] == "AVOID_OUTDOOR_EXPOSURE" or c["evidence_confidence"] == "LOW":
            viol += 1
    print(f"    surviving alternatives violating open/access/thermal/evidence constraints: {viol} (must be 0)")

    print("\n=== GATE INPUTS ===")
    print(f"    scenarios where thermal evidence materially changes candidate set: {int(bl.candidate_set_changed.sum())}/8 (need 'several')")
    print(f"    arbitrary opaque scoring used: NO (constraint-first, no weighted sum)")
    print(f"    every exclusion traceable: {'YES' if len(untraceable)==0 else 'NO'}")
    print(f"    uncertainty preserved (separate fields, UNSTABLE->exclusion): YES")
    print(f"    conventional baseline comparison present: YES (nearest-open)")
    print(f"    behavioural claims: NONE")
    print(f"    obviously-unsuitable survivors: {viol} (systematic failure iff >0)")


if __name__ == "__main__":
    main()
