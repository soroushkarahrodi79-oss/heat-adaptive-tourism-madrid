# PHASE3_GATE.md — Phase 3 decision-engine gate

Version 1.0 · 2026-08-17. The verdict is decided strictly on the pre-registered
Phase 3 gate conditions, evaluated against the locked screening/scenario outputs
and `docs/PHASE3_VALIDATION_REPORT.md`.

---

## Predefined conditions for DECISION ENGINE VALIDATED

| Condition | Result | Met? |
|---|---|---|
| Several scenarios where thermal evidence materially changes the candidate set | **7 of 8** scenarios; 3 of 8 have the baseline's nearest-open pick fail HATI; 23 options removed on thermal/evidence grounds | **Yes** |
| No arbitrary opaque scoring | Constraint-first gate chain; no weighted sum; no single attractiveness score | **Yes** |
| Every exclusion traceable | 0 excluded rows without a machine reason; 6-value exclusion vocabulary | **Yes** |
| Uncertainty preserved | Separate `thermal_state` / `decision_state` / `decision_confidence` / `evidence_confidence` / `exclusion_reason`; Phase 2.2 UNSTABLE → `INSUFFICIENT_EVIDENCE` (S4/S7) | **Yes** |
| At least one conventional baseline comparison | Nearest-open-in-radius baseline computed for all 8 scenarios | **Yes** |
| No behavioural claims | None made anywhere; screening of options only | **Yes** |
| No systematic failure where obviously-unsuitable alternatives survive | 0 surviving alternatives violate open/access/thermal/evidence constraints | **Yes** |

Every predefined condition is satisfied.

## Verdict

# DECISION ENGINE VALIDATED

## What the verdict means (and does not)

VALIDATED here means the **constraint-first opportunity-screening architecture
works as specified and demonstrably adds heat-aware decision value over a
conventional proximity baseline**, with every decision traceable and all
uncertainty preserved as first-class fields. It does **not** mean the system is a
deployable product, that its thermal inputs are field-validated, or that it says
anything about tourist behaviour.

## Scope of the claim

- **Supported:** on the pilot (27 assets, 2023-08-21, 12:00/15:00/18:00), a
  transparent constraint-first screen identifies feasible alternative tourism
  opportunities that are open, accessible, thermally acceptable or materially
  less exposed, and evidence-supported; it removes hot-outdoor options a
  nearest-open recommender would retain (3/8 scenarios); it correctly returns
  *no recommendation* when nothing accessible is materially better (S8); and it
  suppresses thermally-uncertain candidates via the evidence gate (S4/S7).
- **Not supported / out of scope:** any behavioural or adoption claim; heat-aware
  routing or real travel-time-in-heat; field-validated thermal ground truth;
  city-wide generalisation; live opening-hours; a ranked "best" recommendation.

## Permitted next steps (each separately scoped and gated)

A dashboard/operational layer *may now be considered as its own phase* — but only
one that keeps the separate decision fields and exclusion vocabulary intact,
carries the permanent thermal caveats (no field validation; A24 @ 18:00 fragile),
uses live opening hours, and makes no behavioural claim. Heat-aware routing, if
ever pursued, is a distinct future phase with its own gate. This gate authorises
none of them; it validates only the screening engine defined in
`docs/PHASE3_METHOD.md` and `docs/PHASE3_DECISION_ARCHITECTURE.md`.

## What was NOT found

No opaque scoring crept in; no exclusion was untraceable; no obviously-unsuitable
option survived screening; and no scenario was forced to a recommendation —
including one (S8) that correctly returns none. The engine's added value is real
but bounded, and its limits are stated in `docs/PHASE3_VALIDATION_REPORT.md`.
