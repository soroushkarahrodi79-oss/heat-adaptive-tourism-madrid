# PHASE5_0_RESULTS_HIERARCHY.md — HATI-Madrid Phase 5.0

Version 1.0 · 2026-08-18. Ranks the locked evidence into headline vs supporting
vs QA/due-diligence findings, so the manuscript gives substantive findings the
space and QA findings a subordinate, brief treatment. No new analysis.

---

## Tier 1 — Headline findings (carry the paper; Results §5)

**H1. Thermal-method choice materially changes feasibility classifications.**
Proxy vs physical reclassification = **14/42 outdoor rows (33.3%)**; both
directions occur (9 physical-more-restrictive, 5 physical-less-restrictive).
Source: `outputs/tables/proxy_vs_physical_comparison.csv`,
`data/processed/phase2_asset_thermal_exposure.csv`. **This is the empirical
centerpiece (framing B inside spine A).**

**H2. The divergence is concentrated at noon and is physically interpretable.**
Reclassification by timestamp: **12:00 = 64.3%**, 15:00 = 0.0%, 18:00 = 35.7%.
At noon, ambient air temperature (34.2 °C, "LOW" civil-protection band) hides a
modelled UTCI already ≥ 32 °C across all outdoor assets — the proxy underestimates
midday radiant load. Source: same table + `outputs/tables/solar_forcing_sensitivity.csv`
(14/14 assets ≥ 32 °C at every hour). This is what makes H1 a *mechanism*, not a
coincidence.

**H3. Constraint-first heat-aware screening changes the feasible-alternative set
vs a conventional nearest-open baseline.** Candidate set changes in **7/8**
scenarios; the naive nearest-open pick **fails** HATI screening in **3/8** (each
an `OUTDOOR_EXPOSURE_TOO_HIGH` hot outdoor site); **23** open-in-radius options
removed on thermal/evidence grounds. Source:
`outputs/tables/phase3_hati_vs_baseline.csv`,
`data/processed/phase3_scenarios_summary.csv`.

**H4. The architecture fails safe — it returns *no defensible alternative* when
appropriate.** S8 (Retiro, 15:00, 500 m): 26 candidates evaluated, 0 survive →
explicit NO_DEFENSIBLE_ALTERNATIVE rather than a forced pick. Source:
`phase3_scenarios_summary.csv`, `outputs/tables/phase3_accessibility_sensitivity.csv`.

**H5. Core results are robust to tested solar-forcing uncertainty.** Using real
satellite GHI vs clear-sky baseline changes **1/42** decisions (2.4%); ±10% and
±20% GHI perturbations change **0**; the noon ≥32 °C finding holds under all.
Source: `outputs/tables/solar_forcing_sensitivity.csv`. (Robustness *bounds* the
headline claims; it is Tier 1 because it is what protects H1–H4 from "artefact of
the forcing estimate".)

## Tier 2 — Supporting findings (Results/Discussion; brief, subordinate)

- **S-a. Recommendation category is stable across access radius** (500/800/1200 m)
  in 7/8 scenarios; the one that changes (S8) is the intended constrained-mobility
  case. `phase3_accessibility_sensitivity.csv`.
- **S-b. Full exclusion traceability** — 0 untraceable excluded rows; 5–6-value
  machine vocabulary; scenario tally (ACCESSIBILITY_CONSTRAINT 93,
  CLOSED_AT_TIMESTAMP 43, OUTDOOR_EXPOSURE_TOO_HIGH 20,
  NO_MEANINGFUL_THERMAL_IMPROVEMENT 2, INSUFFICIENT_EVIDENCE 1).
  `outputs/tables/phase3_exclusion_reasons.csv`.
- **S-c. Uncertainty propagates into decisions** — the single UNSTABLE thermal row
  (A24 @ 18:00) becomes an evidence-based exclusion when A24 is a candidate (S4)
  and a flagged fragile source when A24 is itself the source (S7).
  `phase2_2_decision_confidence.csv`, `phase3_scenarios_summary.csv`.
- **S-d. Simple vegetation proxies do not converge among themselves** — the Phase
  1.2 result that motivated physical modelling: OSM-tree vs Copernicus canopy
  agreement 71.4% (κ 0.42), 57.1% of outdoor assets proxy-sensitive, below the
  pre-registered 85% bar. `outputs/tables/shade_proxy_agreement.csv`. (Supports
  *why* physical modelling was warranted; not itself a headline.)
- **S-e. Reproducible read-only visual prototype exists** — five concepts on five
  non-reused visual channels, 14/14 contract tests green. Evidence the
  architecture is presentable; not a scientific result.

## Tier 3 — QA / due-diligence findings (Limitations/Methods only; minimal space)

These establish integrity. They must **not** occupy headline space.

- **Q-a. Geometry-correction audit** — LiDAR canopy staleness real but localized
  to 3 assets; A23/A27 corrected (heat *reduced*, no feasibility flip), A24
  confirmed representative. `outputs/tables/phase2_2_geometry_changes.csv`.
- **Q-b. Confidence figures not a single trend line** — the Phase 2.1→2.2 ROBUST
  rise (45.2%→83.3%) is a like-for-unlike methodological refinement, not an
  improvement trajectory. `docs/PHASE2_2_DECISION_UNCERTAINTY.md`.
- **Q-c. Input plausibility checks** — elevation/vegetation/landmark spot-checks,
  buffer-mean vs centroid justification. `docs/PHASE2_VALIDATION_REPORT.md`.
- **Q-d. Baseline-hardening audits** — adaptation-resource indicator demoted after
  three non-discriminatory tests; extreme-band stress test. Phase 1.1 record.

**Rule:** Tier 1 gets the Results narrative and the figures; Tier 2 gets short
paragraphs or supplementary tables; Tier 3 is one Methods/Limitations paragraph
plus supplementary material. No QA finding may be elevated to a headline or given
its own main-text figure.
