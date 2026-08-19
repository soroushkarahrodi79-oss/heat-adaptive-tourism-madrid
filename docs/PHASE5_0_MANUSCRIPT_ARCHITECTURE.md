# PHASE5_0_MANUSCRIPT_ARCHITECTURE.md — HATI-Madrid Phase 5.0

Version 1.0 · 2026-08-18. Section-by-section manuscript skeleton for the A+B
hybrid. **No prose drafted.** Each section states purpose, the exact claims it
may carry (by `claim_id` from `PHASE5_0_EVIDENCE_MATRIX.csv`), the repository
evidence, and what is explicitly excluded. Task 8 (table plan) is folded in at
§10.

---

## 1. Introduction
- **Purpose:** frame extreme heat + tourism concentration in Madrid; state the
  *screening* gap (which options are candidates at all), distinct from routing;
  introduce method-choice sensitivity as the question.
- **Claims:** context only (settled knowledge, cited); forward-references C1, C5,
  C14. No result stated as novel here.
- **Evidence:** `docs/RESEARCH_GAP.md` A/B/C, `docs/PROJECT_CHARTER.md` §1.
- **Excluded:** any behavioural framing; any "we improve tourism" motivation;
  routing as the contribution.

## 2. Literature / conceptual positioning
- **Purpose:** locate the paper against (a) heat-aware routing (saturated,
  upstream-complemented not competed), (b) weighted composite tourism-suitability
  indices (weight-sensitivity problem), (c) LST-as-comfort errors, (d) resident-
  oriented Madrid/Barcelona heat work.
- **Claims:** C13 (constraint-first vs composite), C14 (bounded scope). Positioning
  arguments, not results.
- **Evidence:** `docs/RESEARCH_GAP.md`, `docs/LITERATURE_MATRIX.csv`.
- **Excluded:** claim of methodological breakthrough; claim to lead the routing
  frontier.

## 3. Study area and data
- **Purpose:** define the pilot precisely and the open-data provenance; state the
  extreme-heat episode designation.
- **Claims:** unit-of-analysis facts; C3 setup (air-temp trajectory vs modelled
  load teaser).
- **Evidence:** `docs/PHASE1_METHOD.md` §2–4, `data/processed/study_area.geojson`,
  `pilot_assets.csv`, `docs/PHASE1_DATA_PROVENANCE.md`, `docs/DATA_SOURCE_INVENTORY.csv`.
- **Excluded:** any city-wide generalization; unlisted assets.

## 4. Methods
### 4.1 Proxy baseline
- **Purpose:** define the frozen Phase 1 P0 proxy *exactly* per
  `docs/PHASE5_0_PROXY_DEFINITION.md` — air-temperature hazard band × OSM
  tree-count exposure tercile → constraint-first feasibility. State the Phase 1.2
  proxy-convergence failure that motivated physical modelling.
- **Claims:** C12 (proxies do not converge). Definitional.
- **Evidence:** `docs/PHASE1_METHOD.md` §5, `docs/PHASE1_2_SHADE_EVIDENCE_GATE.md`,
  `outputs/tables/shade_proxy_agreement.csv`, `src/thresholds.py`.
- **Excluded:** any word implying LST/shade-model/canopy-model for the baseline.
### 4.2 Physical thermal modelling
- **Purpose:** SOLWEIG geometry+forcing → Tmrt → UTCI at 2.5 m; 10 m-buffer-mean
  extraction; UTCI-category feasibility mapping. State plausibility checks and the
  explicit no-field-validation limitation up front.
- **Claims:** C3 (noon UTCI ≥32). Method + honest caveat.
- **Evidence:** `docs/PHASE2_SOLWEIG_METHOD.md`, `docs/PHASE2_UTCI_METHOD.md`,
  `docs/PHASE2_VALIDATION_REPORT.md`, `src/extract_asset_thermal_exposure.py`.
- **Excluded:** any claim the modelled values are validated ground truth.
### 4.3 Uncertainty treatment
- **Purpose:** solar-forcing realizations + geometry brackets → per-row robustness
  class (ROBUST/BOUNDARY/UNSTABLE) → evidence_confidence gate.
- **Claims:** C8, C9. Method.
- **Evidence:** `docs/PHASE2_2_DECISION_UNCERTAINTY.md`, `docs/PHASE2_2_METHOD.md`,
  `phase2_2_decision_confidence.csv`, `outputs/tables/solar_forcing_sensitivity.csv`.
- **Excluded:** claim of full/probabilistic uncertainty quantification.
### 4.4 Constraint-first tourism screening
- **Purpose:** the ordered gate chain, separate decision fields, exclusion
  vocabulary, trade-off (not ranking) output.
- **Claims:** C10, C13.
- **Evidence:** `docs/PHASE3_DECISION_ARCHITECTURE.md`, `docs/PHASE3_METHOD.md`,
  `src/phase3_candidate_screening.py`.
- **Excluded:** any composite score; any ranking language.
### 4.5 Baseline comparison
- **Purpose:** define the naive nearest-open-in-radius comparator and the 8
  pre-registered scenarios and radii.
- **Claims:** C5, C6 setup.
- **Evidence:** `docs/PHASE3_SCENARIOS.md`, `docs/PHASE3_DECISION_ARCHITECTURE.md` §5,
  `phase3_scenarios.csv`.
- **Excluded:** claim the baseline represents any specific commercial product.

## 5. Results
- **5.1 Method sensitivity (RQ1):** C1, C2, C3, C4 — the centerpiece.
- **5.2 Decision-support value (RQ2):** C5, C6, C7, C10, C11.
- **5.3 Robustness & traceability (RQ3):** C8, C9.
- **Evidence:** the eight locked tables in `outputs/tables/` +
  `phase2_asset_thermal_exposure.csv` + `phase3_scenarios_summary.csv`.
- **Excluded:** QA/due-diligence numbers as headline results (Tier 3 → Methods
  only); any behavioural or outcome result.

## 6. Discussion
- **Purpose:** interpret method-choice sensitivity (why noon, why both
  directions); position constraint-first vs composite; reproducibility/transfer.
- **Claims:** C1–C2 interpreted, C13, C15 — as *demonstration*, not proof of
  superiority.
- **Evidence:** synthesis of §5 + `RESEARCH_GAP.md`.
- **Excluded:** superiority claim; generalization; behaviour.

## 7. Limitations
- **Purpose:** consolidate the seven permanent limitations + the method-comparison
  caveat (no ground truth) as first-class, not buried.
- **Claims:** frames the ceilings behind C1–C15.
- **Evidence:** `docs/PHASE4_1_TO_NEXT_PHASE_HANDOFF.md` §7,
  `docs/PHASE2_VALIDATION_REPORT.md` §4, `docs/PHASE3_VALIDATION_REPORT.md`.
- **Excluded:** nothing may be hidden here that a headline elsewhere depends on.

## 8. Conclusion
- **Purpose:** restate the one primary contribution and the bounded claim ceiling;
  name field validation as the highest-value next investment.
- **Claims:** C1 (primary) + explicit non-claims.
- **Excluded:** any forward claim beyond the evidence.

## 9. Back matter
- Data availability (open pipeline, per-file hashes: `PHASE4_1_IMPLEMENTATION_BASELINE.md`);
  reproducibility statement; the read-only visual prototype as an optional appendix
  (C-tier, not a result).

## 10. Table plan (Task 8)

| # | Table | Source | Placement |
|---|---|---|---|
| T1 | Data sources / provenance (layer, dataset, vintage, licence, what it does NOT measure) | `DATA_SOURCE_INVENTORY.csv`, `PHASE5_0_PROXY_DEFINITION.md` | **Main** (compact) or supplementary if long |
| T2 | Decision architecture: gates, thresholds, exclusion vocabulary | `PHASE3_DECISION_ARCHITECTURE.md`, `src/thresholds.py` | **Main** |
| T3 | Proxy-vs-physical reclassification (overall, by timestamp, by direction) | `proxy_vs_physical_comparison.csv` | **Main** (the centerpiece table) |
| T4 | Scenario comparison HATI vs nearest-open baseline (S1–S8) | `phase3_hati_vs_baseline.csv`, `phase3_scenarios_summary.csv` | **Main** |
| T5 | Limitations / evidence boundaries (limitation → status → why permanent) | handoff §7, validation reports | **Main** (short) |
| T6 | Proxy-family agreement (Phase 1.2) | `shade_proxy_agreement.csv` | **Supplementary** |
| T7 | Solar-forcing & accessibility sensitivity detail | `solar_forcing_sensitivity.csv`, `phase3_accessibility_sensitivity.csv` | **Supplementary** |

Principle: implementation minutiae (per-asset dumps, code paths) go to
supplementary; the main text keeps five focused tables maximum.
