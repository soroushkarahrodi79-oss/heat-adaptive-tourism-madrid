# PHASE3_SCENARIOS.md — HATI-Madrid Phase 3

Version 1.0 · 2026-08-17. Eight real source→alternative decision scenarios on
2023-08-21, spanning every required scenario class. Full per-candidate detail:
`data/processed/phase3_scenarios.csv`; summary:
`data/processed/phase3_scenarios_summary.csv`; baseline comparison:
`outputs/tables/phase3_hati_vs_baseline.csv`; map:
`outputs/maps/phase3_scenario_map.png`.

Each scenario begins with a real asset whose current state is unsuitable or
constrained (exposed, near-ceiling, closed, or thermally uncertain). No scenario
is forced to yield a recommendation.

---

## Scenario table

| # | Source @ time (r) | Source state | Outcome | # alt | Experience types offered |
|---|---|---|---|---:|---|
| S1 | A16 Fuente de Neptuno @15:00 (800 m) | outdoor, UTCI 45.0, BOUNDARY | ALTERNATIVES_FOUND | 9 | indoor cultural, transit, outdoor monument, green |
| S2 | A15 Fuente de Cibeles @15:00 (800 m) | outdoor, UTCI 44.4, BOUNDARY | ALTERNATIVES_FOUND | 6 | indoor cultural, transit, outdoor monument |
| S3 | A14 Puerta de Alcalá @18:00 (800 m) | outdoor, UTCI 42.7, ROBUST | ALTERNATIVES_FOUND | 4 | indoor cultural, transit, green |
| S4 | A26 Monumento a Alfonso XII @18:00 (800 m) | outdoor, UTCI 43.9, ROBUST | ALTERNATIVES_FOUND | 8 | green, shaded, transit, outdoor monument |
| S5 | A19 Real Observatorio @15:00 (800 m) | **closed (Mon)** | ALTERNATIVES_FOUND | 7 | indoor cultural, transit, indoor-green, green |
| S6 | A17 Estatua de Goya @18:00 (800 m) | outdoor, UTCI 43.9, ROBUST | ALTERNATIVES_FOUND | 9 | indoor cultural, transit, outdoor monument, green |
| S7 | A24 La Rosaleda @18:00 (800 m) | outdoor, UTCI 45.4, **UNSTABLE** | ALTERNATIVES_FOUND | 6 | green, shaded |
| S8 | A20 Parque del Retiro @15:00 (**500 m**) | outdoor, UTCI 38.6, ROBUST | **NO_DEFENSIBLE_ALTERNATIVE** | 0 | — |

## Scenario classes covered

- **Class 1 — exposed outdoor monument → indoor cultural alternative:** S1. The
  near-ceiling Neptuno fountain (UTCI 45.0, boundary) is screened to nine
  alternatives; the adjacent Prado (A01) and Thyssen (A03) are indoor refuges
  offering a categorical thermal gain.
- **Class 2 — exposed outdoor → shaded/lower-radiant outdoor:** S3. Puerta de
  Alcalá screens to Parque del Retiro (A20, UTCI ~40, a green lower-radiant
  outdoor alternative) plus indoor/transit refuges.
- **Class 3 — multiple alternatives, different trade-offs:** S2. Cibeles yields
  indoor cultural (A01, A03), transit refuge (A11, A12) and another monument
  (A14, A17) — exposed as distinct experience types, not merged into a rank.
- **Class 4 — no defensible alternative:** **S8**. From the already-relatively-cool
  central park (A20, UTCI 38.6) under a heat-realistic 500 m walking limit,
  nothing accessible is materially cooler and no indoor refuge is within reach —
  the engine correctly returns NO_DEFENSIBLE_ALTERNATIVE rather than a
  false-confidence suggestion.
- **Class 5 — candidate available but evidence too low:** **S4** and **S7**. In
  S4 (Alfonso XII), nearby La Rosaleda (A24) is excluded `INSUFFICIENT_EVIDENCE`
  because its Phase 2.2 thermal decision is UNSTABLE, while eight robust
  alternatives remain. In S7 the *source itself* (A24) is UNSTABLE, and the
  engine still finds six robust cooler alternatives.

## HATI vs conventional nearest-open baseline (per scenario)

| # | Baseline nearest-open pick | Survives HATI? | HATI removed (thermal/evidence) |
|---|---|---|---|
| S1 | A03 Thyssen (indoor, 134 m) | yes | 2 (A15, A25) |
| S2 | A18 Palacio de Cibeles (outdoor, 114 m) | **no — OUTDOOR_EXPOSURE_TOO_HIGH** | 3 (A16, A18, A25) |
| S3 | A11 Retiro metro (indoor, 202 m) | yes | 6 (A15, A16, A17, A18, A25, A26) |
| S4 | A20 Retiro (outdoor, 274 m) | yes | 1 (A24) |
| S5 | A10 Estación del Arte (indoor, 359 m) | yes | 3 (A22, A24, A25) |
| S6 | A16 Fuente de Neptuno (outdoor, 140 m) | **no — OUTDOOR_EXPOSURE_TOO_HIGH** | 2 (A15, A16) |
| S7 | A22 Palacio de Cristal (outdoor, 345 m) | yes | 0 |
| S8 | A22 Palacio de Cristal (outdoor, 152 m) | **no — OUTDOOR_EXPOSURE_TOO_HIGH** | 6 (all in radius) |

In **3 of 8** scenarios the naive nearest-open recommender would hand a
heat-stressed visitor another **hot outdoor** site; HATI removes it. In **7 of
8** scenarios thermal/evidence screening changed the option set (23 open-in-radius
options removed in total on thermal/evidence grounds).

## Strongest scenario

**S8 (A20 @15:00, 500 m).** The conventional baseline confidently returns the
nearest open attraction — Palacio de Cristal (A22, 152 m, still an extreme-heat
outdoor site). HATI instead removes all six open-in-radius options (none is a
meaningful improvement over the already-cool source) and returns
NO_DEFENSIBLE_ALTERNATIVE. This is the scientific heart of the phase: heat-aware
screening not only *substitutes* options but knows when *not* to recommend,
which a proximity-only tool cannot.

## Honest reading

Every "ALTERNATIVES_FOUND" is a statement about the *option set*, not about what
a tourist will do. The engine screens opportunities; it does not predict choice,
route people, or rank by an opaque score.
