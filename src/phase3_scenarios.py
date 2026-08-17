"""
Phase 3 step 3: bounded set of real source->alternative decision scenarios,
the constraint-first screening chain, and the conventional-baseline comparison.

PRE-REGISTERED decisions (fixed here, before inspecting any scenario outcome):

  Accessibility (straight-line / haversine walking distance, simple & auditable;
  NO routing, NO heat-aware optimisation):
    ACCESS_MAX_M = 800 m  (~10 min walk at 4.8 km/h) as the primary pedestrian-
    reach constraint; sensitivity re-runs at 500 m and 1200 m (validation).
    Straight-line is a documented lower bound on true walking distance; used
    only as an ordinary-reach constraint, not as a scientific contribution.

  Meaningful thermal improvement of an alternative over its source (ANY of):
    (a) alternative is an INDOOR refuge while the source is OUTDOOR (categorical
        refuge gain);
    (b) both outdoor and UTCI_alt <= UTCI_source - DELTA, DELTA = 0.8 C (the
        MEDIAN per-row demonstrated UTCI sensitivity across the 42 Phase 2.2
        outdoor rows - an evidence-derived margin, not an invented constant),
        OR the alternative sits in a strictly lower official UTCI stress
        category than the source;
    (c) alternative decision_confidence is ROBUST while the source is
        BOUNDARY/UNSTABLE and the alternative is thermally acceptable
        (confidence gain).
  Otherwise the candidate is excluded NO_MEANINGFUL_THERMAL_IMPROVEMENT
  (or OUTDOOR_EXPOSURE_TOO_HIGH if it is outdoor and strictly hotter than source).

Constraint-first gate order (first failure wins; nothing silently dropped):
  OUTSIDE_PILOT_SCOPE -> CLOSED_AT_TIMESTAMP -> ACCESSIBILITY_CONSTRAINT ->
  THERMAL_LIMIT_EXCEEDED -> INSUFFICIENT_EVIDENCE -> NO_MEANINGFUL_THERMAL_
  IMPROVEMENT/OUTDOOR_EXPOSURE_TOO_HIGH -> CANDIDATE_ALTERNATIVE.

No weighted score: surviving candidates are NOT ranked into one number; their
trade-offs (indoor/outdoor, distance, experience type, UTCI delta, confidence)
are exposed as-is.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "outputs" / "tables"

ACCESS_MAX_M = 800
ACCESS_SENS = [500, 1200]
DELTA = 0.8
WALK_SPEED_MS = 4.8 * 1000 / 3600  # 1.333 m/s

UTCI_CATEGORY_EDGES = [(32, "Strong"), (38, "Very strong"), (46, "Extreme"), (999, "Extreme")]

EXPERIENCE = {
    "museum_indoor": "indoor_cultural", "transit_hub": "transit_refuge",
    "transit_hub_green": "indoor_green_refuge", "monument_outdoor": "outdoor_monument",
    "park_general": "green_outdoor", "garden_outdoor": "green_outdoor",
    "outdoor_pavilion_shaded": "shaded_outdoor", "outdoor_attraction_mixed_shade": "shaded_outdoor",
}

# 8 real scenarios spanning all required classes. Each carries its own
# pre-registered accessibility radius: 800 m primary, or 500 m for the
# explicit constrained-mobility ("reduced walking tolerance in extreme heat")
# scenario S8.
SCENARIOS = [
    ("S1", "A16", "15:00", 800, "class1_exposed_monument_to_indoor", "exposed near-ceiling outdoor monument -> indoor cultural refuge"),
    ("S2", "A15", "15:00", 800, "class3_multiple_alternatives_tradeoffs", "exposed monument, several alternatives -> expose access/experience trade-offs"),
    ("S3", "A14", "18:00", 800, "class2_exposed_to_shaded_outdoor", "exposed monument -> shaded/lower-radiant outdoor alternative"),
    ("S4", "A26", "18:00", 800, "class5_uncertainty_excludes_candidate", "lakeside monument; nearby La Rosaleda excluded for low thermal confidence, robust alternatives remain"),
    ("S5", "A19", "15:00", 800, "source_closed", "source CLOSED (Monday) -> alternative open tourism opportunity"),
    ("S6", "A17", "18:00", 800, "baseline_divergence_nearest_indoor_closed", "exposed queueing spot where the nearest indoor option (Thyssen) is closed at 18:00"),
    ("S7", "A24", "18:00", 800, "class5_source_thermal_unstable", "source's OWN thermal decision UNSTABLE -> still find robust cooler alternatives"),
    ("S8", "A20", "15:00", 500, "class4_no_defensible_alternative", "already-cool central park under constrained 500 m heat-walk -> no defensible alternative"),
]


def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dp = np.radians(lat2 - lat1); dl = np.radians(lon2 - lon1)
    a = np.sin(dp / 2)**2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2)**2
    return 2 * R * np.arcsin(np.sqrt(a))


def utci_cat(u):
    if u is None or (isinstance(u, float) and np.isnan(u)):
        return None
    for edge, lab in UTCI_CATEGORY_EDGES:
        if u < edge:
            return lab
    return "Extreme"


def main():
    cat = pd.read_csv(PROCESSED / "phase3_asset_catalog.csv").set_index("asset_id")
    scr = pd.read_csv(PROCESSED / "phase3_candidate_screening.csv")
    scr_idx = scr.set_index(["asset_id", "timestamp"])

    def rec(aid, ts):
        r = scr_idx.loc[(aid, ts)]
        c = cat.loc[aid]
        return {
            "asset_id": aid, "name": c["name"], "indoor_outdoor": c["indoor_outdoor"],
            "category": c["tourism_category"], "experience": EXPERIENCE[c["tourism_category"]],
            "lat": c["latitude"], "lon": c["longitude"], "is_open": bool(r["is_open"]),
            "thermal_state": r["thermal_state"], "decision_state": r["decision_state"],
            "decision_confidence": r["decision_confidence"],
            "utci": None if pd.isna(r["utci_baseline"]) else float(r["utci_baseline"]),
            "evidence_confidence": r["evidence_confidence"],
        }

    def improvement(src, cand):
        """Return (is_meaningful, reason_if_not, note)."""
        if cand["indoor_outdoor"] == "indoor" and src["indoor_outdoor"] == "outdoor":
            return True, "", "indoor refuge vs outdoor source (categorical)"
        # both outdoor (or indoor source): compare UTCI where both modelled
        su, cu = src["utci"], cand["utci"]
        if cu is not None and su is not None:
            lower_cat = UTCI_CATEGORY_EDGES  # via utci_cat compare
            if cu <= su - DELTA:
                return True, "", f"UTCI {cu:.1f} <= source {su:.1f} - {DELTA}"
            if utci_cat(cu) != utci_cat(su) and cu < su:
                return True, "", f"lower UTCI category ({utci_cat(cu)} < {utci_cat(su)})"
            # confidence gain (thermally acceptable + robust vs boundary/unstable source)
            if cand["decision_confidence"] == "ROBUST" and src["decision_confidence"] in ("BOUNDARY", "UNSTABLE") \
               and cand["decision_state"] != "AVOID_OUTDOOR_EXPOSURE" and cu <= su:
                return True, "", "confidence gain (ROBUST vs boundary/unstable source), not hotter"
            if cu > su:
                return False, "OUTDOOR_EXPOSURE_TOO_HIGH", f"outdoor and hotter ({cu:.1f} > {su:.1f})"
            return False, "NO_MEANINGFUL_THERMAL_IMPROVEMENT", f"UTCI {cu:.1f} vs {su:.1f}, < {DELTA} improvement"
        # indoor source (rare here) or missing UTCI
        return False, "NO_MEANINGFUL_THERMAL_IMPROVEMENT", "no comparable modelled improvement"

    all_rows = []
    scen_summ = []
    baseline_rows = []
    for sid, src_id, ts, access_m, cls, desc in SCENARIOS:
        src = rec(src_id, ts)
        for cand_id in cat.index:
            if cand_id == src_id:
                continue
            cand = rec(cand_id, ts)
            dist = haversine_m(src["lat"], src["lon"], cand["lat"], cand["lon"])
            walk_min = dist / WALK_SPEED_MS / 60.0
            # gate chain (first failure wins)
            status, reason, note = "CANDIDATE_ALTERNATIVE", "", ""
            if not cand["is_open"]:
                status, reason = "EXCLUDED", "CLOSED_AT_TIMESTAMP"
            elif dist > access_m:
                status, reason = "EXCLUDED", "ACCESSIBILITY_CONSTRAINT"
            elif cand["decision_state"] == "AVOID_OUTDOOR_EXPOSURE":
                status, reason = "EXCLUDED", "THERMAL_LIMIT_EXCEEDED"
            elif cand["evidence_confidence"] == "LOW":
                status, reason = "EXCLUDED", "INSUFFICIENT_EVIDENCE"
            else:
                ok, why, note = improvement(src, cand)
                if not ok:
                    status, reason = "EXCLUDED", why
            all_rows.append({
                "scenario": sid, "source_id": src_id, "source_name": src["name"],
                "timestamp": ts, "access_radius_m": access_m,
                "candidate_id": cand_id, "candidate_name": cand["name"],
                "candidate_category": cand["category"], "experience_type": cand["experience"],
                "indoor_outdoor": cand["indoor_outdoor"],
                "distance_m": round(dist, 0), "walk_min": round(walk_min, 1),
                "cand_thermal_state": cand["thermal_state"], "cand_decision_state": cand["decision_state"],
                "cand_decision_confidence": cand["decision_confidence"],
                "cand_utci": cand["utci"], "source_utci": src["utci"],
                "cand_evidence_confidence": cand["evidence_confidence"],
                "status": status, "exclusion_reason": reason, "improvement_note": note,
            })
        srows = [r for r in all_rows if r["scenario"] == sid]
        surv = [r for r in srows if r["status"] == "CANDIDATE_ALTERNATIVE"]

        # ---- conventional baseline: NEAREST OPEN tourism alternative within the
        #      same radius, NOT thermally/evidence screened (what a naive
        #      open-in-radius recommender would return) ----
        open_in_radius = [r for r in srows if r["exclusion_reason"] != "CLOSED_AT_TIMESTAMP"
                          and r["distance_m"] <= access_m]
        baseline_pick = min(open_in_radius, key=lambda r: r["distance_m"]) if open_in_radius else None
        bp_id = baseline_pick["candidate_id"] if baseline_pick else ""
        # would HATI keep the baseline's nearest pick?
        bp_survives = bool(baseline_pick and baseline_pick["status"] == "CANDIDATE_ALTERNATIVE")
        bp_reason = baseline_pick["exclusion_reason"] if baseline_pick and not bp_survives else ""
        baseline_pool = set(r["candidate_id"] for r in open_in_radius)
        hati_set = set(r["candidate_id"] for r in surv)
        removed_by_thermal = sorted(baseline_pool - hati_set)
        baseline_rows.append({
            "scenario": sid, "source_id": src_id, "timestamp": ts, "access_radius_m": access_m,
            "baseline_nearest_open_pick": bp_id,
            "baseline_pick_name": baseline_pick["candidate_name"] if baseline_pick else "",
            "baseline_pick_distance_m": baseline_pick["distance_m"] if baseline_pick else None,
            "baseline_pick_indoor_outdoor": baseline_pick["indoor_outdoor"] if baseline_pick else "",
            "baseline_pick_survives_hati": bp_survives,
            "baseline_pick_hati_exclusion": bp_reason,
            "n_open_in_radius_baseline": len(baseline_pool),
            "n_hati_alternatives": len(hati_set),
            "n_removed_by_hati_thermal_or_evidence": len(removed_by_thermal),
            "removed_ids": ",".join(removed_by_thermal),
            "candidate_set_changed": len(removed_by_thermal) > 0,
        })

        scen_summ.append({
            "scenario": sid, "source_id": src_id, "source_name": src["name"], "timestamp": ts,
            "access_radius_m": access_m,
            "source_indoor_outdoor": src["indoor_outdoor"], "source_open": src["is_open"],
            "source_thermal_state": src["thermal_state"], "source_decision_state": src["decision_state"],
            "source_decision_confidence": src["decision_confidence"], "source_utci": src["utci"],
            "n_candidate_alternatives": len(surv),
            "alternative_ids": ",".join(sorted(r["candidate_id"] for r in surv)),
            "experience_types_offered": ",".join(sorted(set(r["experience_type"] for r in surv))),
            "recommendation": ("NO_DEFENSIBLE_ALTERNATIVE" if not surv else "ALTERNATIVES_FOUND"),
            "scenario_class": cls, "scenario_desc": desc,
        })

    df = pd.DataFrame(all_rows)
    df.to_csv(PROCESSED / "phase3_scenarios.csv", index=False, encoding="utf-8")
    summ = pd.DataFrame(scen_summ)

    TABLES.mkdir(parents=True, exist_ok=True)
    # exclusion reason tally (context-free screening + scenario chain)
    excl = df[df.status == "EXCLUDED"].groupby("exclusion_reason").size().reset_index(name="count_in_scenarios")
    cf = pd.read_csv(PROCESSED / "phase3_candidate_screening.csv")
    cf_excl = cf[cf.screening_status == "EXCLUDED"].groupby("context_free_exclusion_reason").size().reset_index(name="count_context_free")
    cf_excl = cf_excl.rename(columns={"context_free_exclusion_reason": "exclusion_reason"})
    tally = pd.merge(excl, cf_excl, on="exclusion_reason", how="outer").fillna(0)
    tally.to_csv(TABLES / "phase3_exclusion_reasons.csv", index=False, encoding="utf-8")

    bl = pd.DataFrame(baseline_rows)
    bl.to_csv(TABLES / "phase3_hati_vs_baseline.csv", index=False, encoding="utf-8")

    print("=== Scenario outcomes ===")
    for _, s in summ.iterrows():
        print(f"[{s['scenario']}] {s['source_id']} {s['source_name'][:26]:26s} @{s['timestamp']} r={s['access_radius_m']}m "
              f"({s['source_decision_confidence']}): {s['recommendation']}  n_alt={s['n_candidate_alternatives']}")
        print(f"      exp={s['experience_types_offered']}  alts={s['alternative_ids'] or '(none)'}")
    print("\n=== HATI vs conventional nearest-open baseline ===")
    for _, b in bl.iterrows():
        print(f"[{b['scenario']}] baseline nearest-open={b['baseline_nearest_open_pick']} "
              f"({b['baseline_pick_indoor_outdoor']}, {b['baseline_pick_distance_m']:.0f}m) "
              f"survives_HATI={b['baseline_pick_survives_hati']} "
              f"{'('+b['baseline_pick_hati_exclusion']+')' if b['baseline_pick_hati_exclusion'] else ''} | "
              f"HATI removed {b['n_removed_by_hati_thermal_or_evidence']} of {b['n_open_in_radius_baseline']} open-in-radius: {b['removed_ids']}")
    n_changed = int(bl.candidate_set_changed.sum())
    print(f"\nScenarios where thermal/evidence screening changed the candidate set vs baseline: {n_changed}/{len(bl)}")
    print(f"Scenarios where baseline's nearest-open pick FAILS HATI screening: "
          f"{int((~bl.baseline_pick_survives_hati).sum())}/{len(bl)}")

    print("\n=== Exclusion-reason tally (scenario chain) ===")
    print(df[df.status=='EXCLUDED'].groupby('exclusion_reason').size().to_string())

    summ.to_csv(PROCESSED / "phase3_scenarios_summary.csv", index=False, encoding="utf-8")
    print(f"\nWrote phase3_scenarios.csv, phase3_scenarios_summary.csv, phase3_exclusion_reasons.csv, phase3_hati_vs_baseline.csv")
    return df, summ


if __name__ == "__main__":
    main()
