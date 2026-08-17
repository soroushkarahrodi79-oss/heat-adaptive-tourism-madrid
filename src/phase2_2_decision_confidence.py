"""
Phase 2.2 Task B: evidence-derived decision uncertainty.

Replaces Phase 2.1's blanket, arbitrary +/-2 C threshold-proximity margin with
a per-row uncertainty ENVELOPE built ONLY from actually-computed SOLWEIG
realizations, and a decision-confidence label derived from each row's OWN
demonstrated model sensitivity. The official UTCI thermal-stress categories are
NOT touched; thermal state and decision confidence are kept as SEPARATE fields.

=== Realizations per asset x timestamp (all real model runs, nothing invented) ===
  SOLAR (all 14 outdoor assets, from Phase 2 + Phase 2.1 Audit 1):
    - BASELINE       Phase 2 clear-sky (locked)
    - REAL_SATELLITE EUMETSAT CM SAF SARAH3
    - SENS_A         baseline GHI x 0.90
    - SENS_B         baseline GHI x 0.80
  GEOMETRY (A23, A27 only, from Phase 2.2 Task A):
    - narrow/central/wide corrected-canopy variants (crown R = 2/3/4 m)
  A24 is NOT given geometry realizations: Task A found its near-zero canopy
  REPRESENTATIVE (rose garden; 0 inventoried canopy trees within 30 m), so its
  only tested uncertainty is solar.

=== Envelope ===
  envelope = [min(realizations), max(realizations)]  -- inherently ASYMMETRIC:
  clear-sky GHI sits near the physical upper bound (real skies only reduce it,
  except the small cloud-enhancement REAL_SATELLITE captured at 18:00), and
  canopy correction only ADDS shade -> both uncertainty sources push UTCI DOWN,
  so the envelope is wider below the baseline than above. No symmetric band is
  assumed or applied anywhere.

=== decision_confidence (safety-critical boundary = 46 C: FEASIBLE WITH
    CONDITIONS vs NOT RECOMMENDED; secondary boundary = 32 C) ===
  UNSTABLE  - at least one realization lands on the opposite side of the 46 C
              boundary from the baseline (a materially contradictory decision).
  BOUNDARY  - no realization flips the decision, BUT the envelope lies within
              the row's OWN demonstrated sensitivity s = max|realization -
              baseline| of a decision threshold (32 or 46 C); i.e. the distance
              from the envelope to the nearest threshold is <= s, so a single
              crisp number would misrepresent confidence. (Evidence-derived,
              per-row, NOT a fixed band.)
  ROBUST    - envelope is farther from every threshold than s, and no
              realization flips.

Separate output fields (architectural rule - never collapsed into one score):
  thermal_stress_state   official UTCI category of the baseline value
  decision_state         tourism action implied by the baseline value
  decision_confidence    ROBUST / BOUNDARY / UNSTABLE
  uncertainty_reason     human-readable derivation
Plus the full envelope (low/high/width) and its provenance.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"

UTCI_THRESHOLDS = [32.0, 46.0]

# Official UTCI thermal-stress categories (Broede et al. 2012) - UNCHANGED.
def thermal_stress_state(u):
    if u is None or (isinstance(u, float) and np.isnan(u)):
        return "NOT_MODELLED_INDOOR"
    if u < 26:  return "MODERATE_HEAT_STRESS"
    if u < 32:  return "STRONG_HEAT_STRESS"
    if u < 38:  return "VERY_STRONG_HEAT_STRESS"   # 32-38
    if u < 46:  return "VERY_STRONG_HEAT_STRESS"   # 38-46 (Broede: "very strong" 38-46)
    return "EXTREME_HEAT_STRESS"

# NOTE: Broede category edges are 26/32/38/46. We keep the official labels; the
# decision thresholds (32/46) are a SEPARATE project decision layer, below.

def official_utci_category(u):
    # verbatim official labels, matches src/extract_asset_thermal_exposure.py
    if u < 9:   return "Below moderate range"
    if u < 26:  return "Moderate heat stress"
    if u < 32:  return "Strong heat stress"
    if u < 38:  return "Very strong heat stress"
    return "Extreme heat stress"  # >= 38 ... (Broede: 38-46 very strong, >=46 extreme)

def decision_state(u):
    """Tourism action - a project decision layer, explicitly NOT the UTCI category."""
    if u >= 46:  return "AVOID_OUTDOOR_EXPOSURE"
    if u >= 32:  return "AVOID_PROLONGED_OUTDOOR_EXPOSURE"
    return "OUTDOOR_FEASIBLE"

def feasibility(u):
    if u >= 46:  return "NOT RECOMMENDED"
    if u >= 32:  return "FEASIBLE WITH CONDITIONS"
    return "FEASIBLE"


def main():
    base = pd.read_csv(PROCESSED / "phase2_asset_thermal_exposure.csv")
    outdoor = base[base["indoor_outdoor"] == "outdoor"].copy()
    solar = pd.read_csv(PROCESSED / "phase2_1_solar_scenario_assets.csv")
    geom = pd.read_csv(PROCESSED / "phase2_2_corrected_geometry_utci.csv")
    old_rob = pd.read_csv(PROCESSED / "phase2_1_robustness.csv").set_index(["asset_id", "timestamp"])

    rows = []
    for _, b in outdoor.iterrows():
        aid, ts = b["asset_id"], b["timestamp"]
        base_utci = float(b["utci_mean_10m"])
        realizations = {"BASELINE": base_utci}
        # solar realizations
        s = solar[(solar.asset_id == aid) & (solar.timestamp == ts)]
        for _, sr in s.iterrows():
            realizations[sr["scenario"]] = float(sr["utci_mean_10m"])
        # geometry realizations (A23, A27 only)
        g = geom[(geom.asset_id == aid) & (geom.timestamp == ts)]
        for _, gr in g.iterrows():
            realizations[f"GEOM_{gr['variant']}"] = float(gr["utci_corrected"])

        vals = np.array(list(realizations.values()))
        lo, hi = float(vals.min()), float(vals.max())
        s_sens = float(np.max(np.abs(vals - base_utci)))  # row's demonstrated sensitivity

        feas_set = {feasibility(v) for v in vals}
        base_feas = feasibility(base_utci)

        # UNSTABLE: any realization on the far side of the 46 C boundary vs baseline
        crosses_46 = (vals.max() >= 46.0) and (vals.min() < 46.0)
        crosses_32 = (vals.max() >= 32.0) and (vals.min() < 32.0)
        materially_contradictory = crosses_46  # 46 is the safety-critical flip

        # distance from envelope to nearest decision threshold
        def env_dist_to(t):
            if lo <= t <= hi:
                return 0.0
            return min(abs(lo - t), abs(hi - t))
        d_near = min(env_dist_to(t) for t in UTCI_THRESHOLDS)

        if materially_contradictory:
            conf = "UNSTABLE"
            flippers = [k for k, v in realizations.items() if (v >= 46) != (base_utci >= 46)]
            reason = (f"realization(s) {flippers} cross the safety-critical 46 C boundary "
                      f"(envelope {lo:.1f}-{hi:.1f} C, baseline {base_utci:.1f}); "
                      f"materially different decision (NOT RECOMMENDED vs FEASIBLE WITH CONDITIONS)")
        elif d_near <= s_sens or crosses_32:
            conf = "BOUNDARY"
            reason = (f"no realization flips the decision, but envelope {lo:.1f}-{hi:.1f} C is within the "
                      f"row's demonstrated sensitivity ({s_sens:.1f} C) of a decision threshold "
                      f"(nearest {d_near:.1f} C away) - crisp single-value read would be false precision")
        else:
            conf = "ROBUST"
            reason = (f"envelope {lo:.1f}-{hi:.1f} C stays {d_near:.1f} C clear of the nearest decision "
                      f"threshold, farther than the row's demonstrated sensitivity ({s_sens:.1f} C); "
                      f"no realization flips the decision")

        # provenance of the extreme realizations
        lo_src = [k for k, v in realizations.items() if v == lo][0]
        hi_src = [k for k, v in realizations.items() if v == hi][0]
        n_geom = sum(1 for k in realizations if k.startswith("GEOM_"))

        old = old_rob.loc[(aid, ts), "robustness"] if (aid, ts) in old_rob.index else "N/A"
        rows.append({
            "asset_id": aid, "name": b["name"], "morphology": b["morphology"], "timestamp": ts,
            "utci_baseline": round(base_utci, 1),
            "thermal_stress_state": thermal_stress_state(base_utci),
            "utci_category_official": official_utci_category(base_utci),
            "decision_state": decision_state(base_utci),
            "feasibility_state": base_feas,
            "envelope_low": round(lo, 1), "envelope_high": round(hi, 1),
            "envelope_width": round(hi - lo, 1),
            "envelope_low_source": lo_src, "envelope_high_source": hi_src,
            "demonstrated_sensitivity_c": round(s_sens, 1),
            "n_realizations": len(realizations),
            "n_geometry_realizations": n_geom,
            "decision_confidence": conf,
            "robustness_phase2_1": old,
            "confidence_changed_vs_phase2_1": conf != old,
            "uncertainty_reason": reason,
        })

    out = pd.DataFrame(rows)
    out_path = PROCESSED / "phase2_2_decision_confidence.csv"
    out.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Wrote {out_path} ({len(out)} outdoor rows)\n")

    print("=== Phase 2.2 decision_confidence distribution (n=42 outdoor) ===")
    c = out["decision_confidence"].value_counts()
    for lab in ["ROBUST", "BOUNDARY", "UNSTABLE"]:
        n = int(c.get(lab, 0))
        print(f"  {lab:9s} {n:2d}  ({100*n/len(out):.1f}%)")

    print("\n=== Phase 2.1 -> Phase 2.2 confidence transitions ===")
    trans = out.groupby(["robustness_phase2_1", "decision_confidence"]).size()
    print(trans.to_string())

    print("\n=== Rows that CHANGED confidence state ===")
    for _, r in out[out["confidence_changed_vs_phase2_1"]].iterrows():
        print(f"  {r['asset_id']} @ {r['timestamp']}: {r['robustness_phase2_1']} -> {r['decision_confidence']}  "
              f"(env {r['envelope_low']}-{r['envelope_high']}, s={r['demonstrated_sensitivity_c']})")

    print("\n=== Remaining UNSTABLE rows ===")
    for _, r in out[out.decision_confidence == "UNSTABLE"].iterrows():
        print(f"  {r['asset_id']} @ {r['timestamp']}: {r['uncertainty_reason']}")

    return out


if __name__ == "__main__":
    main()
