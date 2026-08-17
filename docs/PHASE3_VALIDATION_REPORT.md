# PHASE3_VALIDATION_REPORT.md — HATI-Madrid Phase 3

Version 1.0 · 2026-08-17. Evaluates the six required validation questions plus a
guardrail check, from the locked screening/scenario outputs
(`src/phase3_validation.py`). Also states explicitly what this phase cannot
claim.

---

## Results against the six validation questions

**V1 — Does the framework produce logically distinct alternatives?** Yes. Across
8 scenarios there are 6 distinct experience-type mixes; 7 of 8 scenarios offer
≥2 experience types (e.g. indoor cultural + transit refuge + shaded green),
exposed as trade-offs rather than merged.

**V2 — Does thermal evidence change the candidate set vs a conventional
baseline?** Yes, materially. Versus the naive nearest-open-in-radius recommender:
the candidate set changed in **7 of 8** scenarios; the baseline's nearest-open
pick **fails** HATI screening in **3 of 8** (each time because it is another hot
outdoor site, `OUTDOOR_EXPOSURE_TOO_HIGH`); **23** open-in-radius options were
removed in total on thermal/evidence grounds
(`outputs/tables/phase3_hati_vs_baseline.csv`).

**V3 — Are exclusion reasons interpretable?** Yes; all excluded rows carry a
machine reason (0 untraceable). Scenario-chain tally: ACCESSIBILITY_CONSTRAINT
93, CLOSED_AT_TIMESTAMP 43, OUTDOOR_EXPOSURE_TOO_HIGH 20,
NO_MEANINGFUL_THERMAL_IMPROVEMENT 2, INSUFFICIENT_EVIDENCE 1
(`outputs/tables/phase3_exclusion_reasons.csv`).

**V4 — Does uncertainty change recommendations?** Yes. The single Phase 2.2
UNSTABLE row (A24 @ 18:00) propagates to `evidence_confidence = LOW` and so to an
`INSUFFICIENT_EVIDENCE` exclusion when A24 is a candidate (S4), and is carried as
an explicitly-flagged fragile source when A24 is itself the source (S7). Removing
the uncertainty layer would silently re-admit that candidate.

**V5 — Do some scenarios correctly return no recommendation?** Yes — S8
(NO_DEFENSIBLE_ALTERNATIVE). The engine declines to recommend when nothing
accessible is materially better.

**V6 — Robust to modest accessibility assumptions?** The recommendation
*category* (alternatives-found vs none) is stable across 500 / 800 / 1200 m in
**7 of 8** scenarios (`outputs/tables/phase3_accessibility_sensitivity.csv`). The
one that changes is S8 by construction: from the already-cool central park,
0 alternatives at 500 m, 2 at 800 m, 7 at 1200 m — a real, reportable dependency
on how far a visitor will walk in extreme heat, not a defect. The *number* of
alternatives naturally grows with radius in all scenarios, but no scenario
flips from "found" to "none" except this intended constrained-mobility case.

**Guardrail — do obviously-unsuitable alternatives survive?** No. Every one of
the surviving `CANDIDATE_ALTERNATIVE` rows is verified open, within radius, not
`AVOID_OUTDOOR_EXPOSURE`, and evidence ≥ MODERATE (0 violations). No systematic
failure where a closed, over-threshold, or low-evidence option slips through.

## What this phase CANNOT claim

- **No behavioural claim.** It screens the option set; it does not predict, model,
  or assert that any tourist chooses, follows, or prefers an alternative. No
  flow, demand, or adoption is estimated.
- **No routing / no travel-time-in-heat.** Accessibility is straight-line
  distance (a lower bound on real walking distance) used purely as a reach
  constraint. Actual paths, gradients, crossings, and heat exposure *en route*
  are not modelled — heat-aware routing is explicitly out of scope.
- **No field-validated thermal ground truth.** Thermal inputs are the Phase 2.2
  modelled UTCI, which remains un-validated against measured Tmrt/UTCI (permanent
  project caveat). "Thermally acceptable / materially less exposed" is a
  statement about modelled exposure, not measured comfort.
- **Opening hours are point-in-time documented values**, not a live feed; the
  Monday/August closures used are real and cited, but a production system would
  need current hours. `evidence_completeness` flags where hours are PARTIAL.
- **Indoor "refuge" assumes thermal buffering** without verifying A/C status or
  queue/approach exposure (inherited Phase 1 caveat); indoor thermal evidence is
  therefore capped at MODERATE.
- **Not a ranking.** The engine deliberately produces no single attractiveness
  score; it exposes trade-offs. Choosing among surviving alternatives is left to
  the user.
- **Pilot-bounded.** 27 assets, one date, three timestamps, ~3.5 km². No claim
  generalises city-wide or to other days without re-running.

## Reproducibility

All outputs regenerate from `src/phase3_*.py` over locked Phase 0–2.2 data plus
the project's own OSM extracts; the opening-hours evaluator is unit-checked
against the tricky Monday/August cases inside `phase3_build_catalog.py`.
