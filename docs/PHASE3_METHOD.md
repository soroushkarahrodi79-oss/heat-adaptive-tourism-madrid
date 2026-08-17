# PHASE3_METHOD.md — HATI-Madrid Phase 3

Version 1.0 · 2026-08-17. **Heat-Adaptive Tourism Opportunity Screening.**
Moves the project from urban-thermal modelling into transparent, constraint-first
tourism decision-support. Phase 0–2.2 scientific and numerical outputs are
treated as **immutable historical evidence**; nothing in Phase 3 reopens or
alters them (verified: no SOLWEIG rerun, no change to any Phase 2.2 thermal
value).

---

## 1. Research question (and what it is NOT)

Given a tourism opportunity that becomes thermally unsuitable or constrained at
a specific time, can a transparent constraint-first system identify feasible
alternative opportunities that are (a) thermally acceptable or materially less
exposed, (b) open at that time, (c) realistically accessible, (d) tourism-
relevant, and (e) supported by sufficient evidence?

This is **opportunity screening, not behavioural prediction**. The system makes
no claim that any tourist will choose, follow, or prefer a recommendation. It
screens the *option set*; it does not model people.

## 2. Scope and restrictions honoured

- Existing pilot geography and the 27 curated assets; the three locked
  timestamps (12:00 / 15:00 / 18:00, 2023-08-21). No city-wide expansion, no
  synthetic assets.
- **No** dashboard, route optimisation, heat-aware routing, ML, LLM ranking,
  agents, user personas, behavioural prediction, or composite/weighted
  attractiveness score. Accessibility is a simple straight-line constraint, not
  the scientific contribution.

## 3. Inputs (all real, all provenance-tracked)

| Input | Source | Use |
|---|---|---|
| 27 pilot assets (id, name, category, indoor/outdoor, coords) | `data/processed/pilot_assets.csv` (Phase 1, OSM/ODbL) | catalog spine |
| Thermal evidence (outdoor): UTCI, thermal_stress_state, decision_state, decision_confidence, uncertainty envelope | `data/processed/phase2_2_decision_confidence.csv` (Phase 2.2, LOCKED) | thermal gate |
| Indoor rule | Phase 1 indoor-bypass (refuge; A/C unverified) | thermal gate (indoor) |
| Opening hours | OSM `opening_hours` tags in this project's own extracts (11/27) + documented authoritative institutional/operational schedules (16/27), each with source | open/closed gate |
| Tourism-relevance evidence | OSM `tourism`/`historic`/`amenity`/`leisure` + Wikidata IDs (24/27) | relevance gate |

Opening hours were harvested from the project's already-fetched OSM data
(`src/phase3_extract_opening_hours.py`); gaps filled with documented, citable
institutional hours recorded in `src/phase3_build_catalog.py` `DOCUMENTED_HOURS`
(each carries a source string and an evidence-completeness flag). None is
invented to produce a result.

## 4. The study date matters (and is used honestly)

2023-08-21 is a **Monday in August**. Real OSM hours make several indoor
refuges genuinely unavailable that day: Museo Naval (A05, "Mo off"),
Antropología (A06) and Artes Decorativas (A07) (no Monday opening), Real Fábrica
de Tapices (A08, "Aug off"), and Thyssen (A03) closes at 16:00 on Mondays; the
Real Observatorio (A19) runs guided visits Fri–Sun only. The screening therefore
operates on a realistically *constrained* refuge pool, not an idealised one.

## 5. Pre-registered decisions (fixed before any scenario was evaluated)

1. **Accessibility** — straight-line (haversine) walking distance, converted to
   time at 4.8 km/h. Primary pedestrian-reach constraint **800 m** (~10 min);
   sensitivity re-runs at **500 m** and **1200 m**. Straight-line is a documented
   lower bound on true walking distance, used only as an ordinary-reach
   constraint (no routing, no heat-aware optimisation).
2. **Meaningful thermal improvement** margin **Δ = 0.8 °C** — the *median*
   per-row demonstrated UTCI sensitivity across the 42 Phase 2.2 outdoor rows
   (evidence-derived, not an invented constant). An alternative is a meaningful
   improvement over its source if it is an indoor refuge vs an outdoor source
   (categorical), OR (both outdoor) its UTCI is ≥ Δ lower or in a strictly lower
   official UTCI category, OR it is ROBUST-confident where the source is
   BOUNDARY/UNSTABLE and not hotter (confidence gain).

## 6. Pipeline (scripts)

```
phase3_extract_opening_hours.py  -> harvest OSM opening_hours (own extracts)
phase3_build_catalog.py          -> phase3_asset_catalog.csv (+ audited hours evaluator)
phase3_candidate_screening.py    -> phase3_candidate_screening.csv (per asset x timestamp)
phase3_scenarios.py              -> phase3_scenarios.csv, phase3_scenarios_summary.csv,
                                    phase3_exclusion_reasons.csv, phase3_hati_vs_baseline.csv
phase3_make_map.py               -> outputs/maps/phase3_scenario_map.png
phase3_validation.py             -> phase3_accessibility_sensitivity.csv + validation report
```

Decision architecture and field semantics: `docs/PHASE3_DECISION_ARCHITECTURE.md`.
Scenarios: `docs/PHASE3_SCENARIOS.md`. Validation & limits:
`docs/PHASE3_VALIDATION_REPORT.md`. Gate: `docs/PHASE3_GATE.md`.

## 7. What this phase deliberately does not do

No aggregate attractiveness score is created; surviving candidates are exposed
with their trade-offs (indoor/outdoor, distance, experience type, UTCI delta,
confidence), not ranked into one number. The engine never asserts a tourist's
choice. Accessibility is intentionally the simplest defensible metric.
