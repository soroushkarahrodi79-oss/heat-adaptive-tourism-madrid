"""
Phase 3 step 2: per asset x timestamp candidate decision record. Joins the
locked Phase 2.2 thermal evidence (outdoor) and the locked Phase 1 indoor rule
(indoor) onto the catalog, and applies the CONTEXT-FREE constraint gates
(open? / thermal limit? / evidence sufficient?). Scenario-relative gates
(accessibility, thermal improvement vs a specific source) are applied later in
phase3_scenarios.py — this file is the reusable per-candidate substrate.

Architectural rule (carried from Phase 2.2): thermal_state, decision_state,
decision_confidence, evidence_confidence and exclusion_reason are SEPARATE
fields — never collapsed into one score.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
TIMES = ["12:00", "15:00", "18:00"]


def evidence_rank(x):
    return {"HIGH": 3, "MODERATE": 2, "LOW": 1}[x]


def main():
    cat = pd.read_csv(PROCESSED / "phase3_asset_catalog.csv")
    conf = pd.read_csv(PROCESSED / "phase2_2_decision_confidence.csv")
    conf_idx = conf.set_index(["asset_id", "timestamp"])
    open_col = {"12:00": "open_1200", "15:00": "open_1500", "18:00": "open_1800"}

    rows = []
    for _, a in cat.iterrows():
        aid = a["asset_id"]
        oh_ev = a["evidence_completeness"]  # COMPLETE/PARTIAL/MISSING
        oh_conf = {"COMPLETE": "HIGH", "PARTIAL": "MODERATE", "MISSING": "LOW"}[oh_ev]
        for ts in TIMES:
            is_open = bool(a[open_col[ts]])
            if a["indoor_outdoor"] == "indoor":
                thermal_state = "INDOOR_NOT_MODELLED"
                decision_state = "INDOOR_REFUGE"
                decision_conf = "INDOOR_BYPASS"
                utci = None
                env_lo = env_hi = None
                # indoor refuge assumed thermally buffered, but A/C status
                # unverified and approach/queue exposure unmodelled (Phase 1 caveat)
                thermal_ev = "MODERATE"
            else:
                r = conf_idx.loc[(aid, ts)]
                thermal_state = r["thermal_stress_state"]
                decision_state = r["decision_state"]
                decision_conf = r["decision_confidence"]
                utci = float(r["utci_baseline"])
                env_lo, env_hi = float(r["envelope_low"]), float(r["envelope_high"])
                thermal_ev = {"ROBUST": "HIGH", "BOUNDARY": "MODERATE", "UNSTABLE": "LOW"}[decision_conf]

            # evidence_confidence = weakest link of (opening-hours, thermal) evidence
            evidence_conf = min([oh_conf, thermal_ev], key=evidence_rank)

            # ----- context-free constraint gates (first failure wins) -----
            status, reason = "AVAILABLE_CANDIDATE", ""
            if not is_open:
                status, reason = "EXCLUDED", "CLOSED_AT_TIMESTAMP"
            elif decision_state == "AVOID_OUTDOOR_EXPOSURE":  # UTCI >= 46, outdoor
                status, reason = "EXCLUDED", "THERMAL_LIMIT_EXCEEDED"
            elif evidence_conf == "LOW":
                status, reason = "EXCLUDED", "INSUFFICIENT_EVIDENCE"

            rows.append({
                "asset_id": aid, "name": a["name"], "timestamp": ts,
                "tourism_category": a["tourism_category"], "indoor_outdoor": a["indoor_outdoor"],
                "is_open": is_open,
                "thermal_state": thermal_state, "decision_state": decision_state,
                "decision_confidence": decision_conf,
                "utci_baseline": utci, "utci_envelope_low": env_lo, "utci_envelope_high": env_hi,
                "opening_hours_evidence": oh_ev, "thermal_evidence": thermal_ev,
                "evidence_confidence": evidence_conf,
                "screening_status": status, "context_free_exclusion_reason": reason,
                "tourism_relevance_evidence": a["tourism_relevance_evidence"],
            })

    out = pd.DataFrame(rows)
    out_path = PROCESSED / "phase3_candidate_screening.csv"
    out.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Wrote {out_path} ({len(out)} rows = 27 assets x 3 timestamps)\n")

    for ts in TIMES:
        s = out[out.timestamp == ts]
        avail = s[s.screening_status == "AVAILABLE_CANDIDATE"]
        print(f"[{ts}] available candidates: {len(avail)}/27  "
              f"(indoor {len(avail[avail.indoor_outdoor=='indoor'])}, outdoor {len(avail[avail.indoor_outdoor=='outdoor'])})")
        for reason, g in s[s.screening_status == "EXCLUDED"].groupby("context_free_exclusion_reason"):
            print(f"        EXCLUDED {reason}: {sorted(g.asset_id)}")
    return out


if __name__ == "__main__":
    main()
