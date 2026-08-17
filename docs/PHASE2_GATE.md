# PHASE2_GATE.md — Phase 2 value-of-complexity gate decision

Version 1.0 · 2026-08-17. Thresholds below are reproduced **exactly as
predefined in the task specification, before any SOLWEIG output was
inspected**, and are not altered by this document.

---

## Research question

Does physical modelling of mean radiant temperature and UTCI materially
reduce the classification instability observed with simple vegetation/shade
proxies (`docs/PHASE1_2_SHADE_EVIDENCE_GATE.md`)?

## Predefined criteria, evaluated

**PHYSICAL MODEL ADDS DECISION VALUE** if *any* of the following hold:

| Condition | Result | Met? |
|---|---|---|
| ≥20% of asset×timestamp classifications materially change | **33.3%** (14/42 outdoor rows) reclassified between Phase 1 proxy-based `feasibility_state` and Phase 2 physical-model `feasibility_state` | **Yes** |
| A systematic morphology-specific proxy failure is discovered | Reclassification is **uniform at 33.3%** across all four morphologies (plaza_hardscape, park_garden, attraction_exterior, street_corridor) — real and pervasive, but not concentrated in one type | Partial / not in the "one morphology uniquely fails" sense |
| Physical modelling reveals decision-relevant thermal differences invisible to the simple baseline | **Yes, clearly** — see below | **Yes** |

Because the gate requires only **one** condition, and two are independently
satisfied, the outcome is unambiguous regardless of how the second
(morphology) condition is read.

## The decision-relevant difference the physical model reveals

The clearest, most mechanistically interpretable finding of this phase is
**timestamp-dependent, not morphology-dependent**:

| Timestamp | Phase 1 hazard state (air temp only) | Reclassification rate |
|---|---|---:|
| 12:00 | LOW (34.2 °C, below AEMET's yellow threshold) | **64.3%** (9/14) |
| 15:00 | ELEVATED (38.8 °C) | 0.0% (0/14) |
| 18:00 | SEVERE (40.5 °C) | 35.7% (5/14) |

At **12:00**, Phase 1's air-temperature-only hazard gate found most sites
FEASIBLE (regional air temperature had not yet crossed a warning threshold).
The physical model shows the opposite at the same hour: measured solar
elevation is already 48.6° and modelled UTCI at 9 of 14 outdoor assets is
already in the "Very strong" or "Extreme" heat-stress category (32.2–65.3 °C
Tmrt, 32.4–40.4 °C UTCI). **This is a real, mechanistically explicable
failure mode of an air-temperature-only proxy**: solar radiant load peaks
earlier in the day (tracking sun angle) than regional air temperature
(which lags, peaking mid-afternoon) — a distinction a single-variable
air-temperature gate architecturally cannot represent, and that only a
model resolving radiation and shadow geometry can reveal. In all 9 of these
cases the physical model is **more restrictive** than the proxy (the proxy
underestimated hazard) — the more consequential direction of error for a
heat-safety decision-support tool.

At **18:00**, the opposite pattern appears: 5 sites the proxy's exclusion
rule marked NOT RECOMMENDED (SEVERE hazard + bottom-tercile tree count) are
found FEASIBLE WITH CONDITIONS by the physical model (UTCI 41.7–45.4 °C, all
below the 46 °C extreme-stress cutoff). Here the physical model is **less
restrictive** — the crude tree-count exposure gate over-penalised sites
whose real radiant environment (accounting for building shadow, orientation,
and the specific sun angle at that hour) was less severe than a coarse
vegetation-presence count implied.

**Both directions of error are real and both matter**: the proxy is not
uniformly conservative (which would at least be safe) — it both
underestimates and overestimates hazard depending on time of day, in ways
that are individually explicable but were invisible to Phase 1/1.1/1.2's
simple-proxy architecture. Full detail:
`data/processed/phase2_asset_thermal_exposure.csv`,
`outputs/tables/proxy_vs_physical_comparison.csv`.

## What did NOT change

- The **hazard-gate concept itself is vindicated in structure**: the
  physical model does not contradict the idea that this is an extreme,
  high-stress episode — every single outdoor asset×timestamp combination
  (42/42) is at least in "Very strong heat stress" territory (UTCI ≥ 32 °C);
  none reach the official "No thermal stress" or "Moderate" bands. The
  disagreement is about *degree and timing*, not about whether this was a
  genuinely dangerous heat episode.
- Indoor assets are unaffected (SOLWEIG models the outdoor environment only;
  Phase 1's indoor-bypass rule is retained unchanged for all 39 indoor
  rows).

## Verdict

# PHYSICAL MODEL ADDS DECISION VALUE

The 33.3% reclassification rate clears the predefined 20% threshold on its
own, and the underlying mechanism (radiant load vs. air-temperature timing
mismatch at midday) is exactly the kind of "decision-relevant thermal
difference invisible to the simple baseline" the task anticipated finding
if physical modelling were warranted. This is not a marginal or
borderline result requiring the CONTEXT-DEPENDENT classification — both the
magnitude test and the mechanism test independently point the same way.

This verdict is offered together with, not in place of, the limitations in
`docs/PHASE2_VALIDATION_REPORT.md`: no direct field validation of Tmrt/UTCI
exists, the vegetation geometry is ~8–15 years stale, and wind is not
spatially resolved. "Adds decision value" is a statement about *marginal
information gain over the simpler baseline given real, current-best-
available inputs*, not a claim that this specific Phase 2 output is itself
final or field-validated. A future phase building on this result should
prioritise, in order: (1) closing the vegetation-vintage gap (the largest
uncertainty carried into this result), (2) a genuine field-validation
campaign if the project proceeds toward an operational tool, before (3) any
further model sophistication (URock wind, custom land-cover) — richer
inputs to the existing model before a richer model.
