# PHASE5_0_FIGURE_PLAN.md — HATI-Madrid Phase 5.0

Version 1.0 · 2026-08-18. Publication figure plan: **6 main figures** (+1
optional appendix). Argument-driven, not a dump of every existing map. For each:
scientific purpose, source files, panels, key message, and whether existing
artwork suffices or must be re-rendered. **No figures rendered in this phase.**

Existing map inventory reviewed: `outputs/maps/` (01–05 analysis maps,
`tmrt_*`/`utci_*` rasters+PNGs, `phase3_scenario_map.png`,
`shade_proxy_instability.png`, `phase2_1_unstable_assets.png`) and
`outputs/design/phase4_0_wireframes.html`. Most are analysis-grade; publication
use generally needs re-rendering to a consistent style, shared colour ramps,
scale bars, and figure-quality labels.

---

## Figure 1 — Study area + methodological pipeline
- **Purpose:** orient the reader and show the two-track method (proxy vs physical
  feeding one screening engine).
- **Source:** `outputs/maps/01_study_area.png`, `02_pilot_assets.png`;
  pipeline schematic from `PHASE3_DECISION_ARCHITECTURE.md` §1.
- **Panels:** (a) study-area map with 27 assets (indoor/outdoor); (b) pipeline
  flow: data → [proxy baseline | SOLWEIG/UTCI] → constraint-first screen →
  outputs + uncertainty.
- **Key message:** one bounded pilot; two thermal methods compared inside one
  transparent architecture.
- **Artwork:** panel (a) re-render (publication labels/scale bar); panel (b)
  **new vector schematic**.

## Figure 2 — Proxy vs physical classification difference (CENTERPIECE)
- **Purpose:** show H1/H2 — where and when the two methods disagree.
- **Source:** `data/processed/phase2_asset_thermal_exposure.csv`,
  `outputs/tables/proxy_vs_physical_comparison.csv`.
- **Panels:** (a) asset×timestamp matrix, cells coloured by agreement / physical-
  more-restrictive / physical-less-restrictive; (b) reclassification rate by
  timestamp bar (64.3 / 0.0 / 35.7%).
- **Key message:** method choice changes 33.3% of classifications, concentrated at
  noon and running in both directions.
- **Artwork:** **new** (no existing figure encodes the paired comparison).

## Figure 3 — UTCI spatial / timestamp differentiation
- **Purpose:** support C3 — modelled radiant load is high and spatially
  structured; noon already ≥32 °C despite "low" air temperature.
- **Source:** `outputs/maps/utci_1200.tif/.png`, `utci_1500`, `utci_1800`
  (optionally `03_exposure_differentiation.png`).
- **Panels:** three-timestamp small-multiple of UTCI with asset points and a
  shared colour ramp; 32/46 °C category breaks marked.
- **Key message:** the physical field carries information air temperature cannot.
- **Artwork:** **re-render** as a unified small-multiple with one shared ramp,
  scale bar, category contours (existing PNGs are separate, non-uniform).

## Figure 4 — Uncertainty / robustness
- **Purpose:** support H5/C8–C9 — decisions stable under tested solar forcing; the
  one UNSTABLE case shown honestly.
- **Source:** `outputs/tables/solar_forcing_sensitivity.csv`,
  `phase2_2_decision_confidence.csv`, `outputs/maps/05_audit4_unstable_assets.png`.
- **Panels:** (a) decisions changed vs GHI perturbation (real/-10/-20%); (b)
  per-asset robustness class map or the A24 @ 18:00 boundary case.
- **Key message:** headline results are not an artefact of the forcing estimate;
  residual uncertainty is localized and carried, not hidden.
- **Artwork:** panel (a) **new** chart; panel (b) re-render from `05_*`.

## Figure 5 — Decision architecture (constraint-first + separate fields)
- **Purpose:** support C10/C13 — the gate chain and the five separate decision
  fields, vs a collapsed composite score.
- **Source:** `PHASE3_DECISION_ARCHITECTURE.md` §1–3; optionally a cleaned frame
  from `phase4_0_wireframes.html`.
- **Panels:** (a) ordered gate chain with exclusion vocabulary; (b) the five
  non-collapsed fields (thermal/decision/decision-confidence/evidence/exclusion).
- **Key message:** transparency by construction — no opaque weighting.
- **Artwork:** **new vector schematic**.

## Figure 6 — Baseline vs HATI scenarios (incl. S8)
- **Purpose:** support C5/C6/C7 — the option set changes, and S8 returns none.
- **Source:** `outputs/tables/phase3_hati_vs_baseline.csv`,
  `phase3_scenarios_summary.csv`, `outputs/maps/phase3_scenario_map.png`.
- **Panels:** (a) per-scenario S1–S8: nearest-open pick vs HATI alternative set,
  removed-count, baseline-fails flag; (b) S8 spotlight — 26 evaluated, 0 survive.
- **Key message:** heat-aware screening changes what a proximity tool returns and
  fails safe when nothing qualifies.
- **Artwork:** **new** composite (existing scenario map is a locator only; may be
  an inset).

## Figure 7 — (OPTIONAL, appendix) Visual prototype
- **Purpose:** show the read-only decision-support UI (five channels) as evidence
  the architecture is presentable — **not** a result.
- **Source:** screenshot of the Dash app / `phase4_0_wireframes.html`.
- **Panels:** one annotated screenshot.
- **Key message:** the locked outputs render as an auditable interface.
- **Artwork:** **new** screenshot; appendix only, clearly non-headline.

---

**Summary:** 6 main + 1 optional appendix. New artwork: Fig 2, most of Fig 4/5/6,
Fig 1b, Fig 7. Re-render: Fig 1a, Fig 3, Fig 4b. Direct reuse: none at
publication quality — every existing PNG needs at least restyling. Do **not**
render until the manuscript charter is approved and Results §5 is fixed.
