# HATI-Madrid — Evidence matrix for professional use

**Prepared:** 2026-09-24 · **Repository base:** commit `c69688e` (`main`)
**Scope:** what the existing research can and cannot support when presented to a tourism
company, consultancy or employer. This file adds no scientific result; it classifies
existing ones. [`PROJECT_STATUS.md`](../PROJECT_STATUS.md) remains the canonical status
record and governs if anything here disagrees with it.

## Evidence categories

| Category | Meaning in this document |
|---|---|
| **IMPLEMENTED** | Functionality exists in committed code and was inspected. |
| **REPRODUCED** | Re-executed on 2026-09-24 in an isolated copy, with the output compared against the locked table ([`REPRODUCTION_REPORT.md`](REPRODUCTION_REPORT.md)). |
| **MODEL-DERIVED** | Output of the SOLWEIG → Tmrt → UTCI modelling chain. It is not an observation. |
| **HYPOTHETICAL** | A possible business use that has not been tested with any company. |
| **PENDING** | Evidence, validation or development that does not exist. |

A claim can carry two categories. For example, "REPRODUCED + MODEL-DERIVED" means that
re-running the pipeline gives the same modelled numbers. It does **not** mean those
numbers were checked against reality.

## Matrix

| # | Capability | Claim | Exact source | Verification performed | Category | Limitation | Permitted professional use |
|---|---|---|---|---|---|---|---|
| E1 | Thermal-method sensitivity | Replacing the operational proxy (AEMET hazard band + OSM tree count) with SOLWEIG-derived UTCI reclassified **14 of 42** outdoor observations (33.3%): 9 more restrictive, 5 less restrictive. | `src/extract_asset_thermal_exposure.py` → `data/processed/phase2_asset_thermal_exposure.csv` | Extraction re-run from the committed UTCI rasters. Table matched, and the counts were recomputed from the reproduced table. | REPRODUCED + MODEL-DERIVED | One day (21 Aug 2023), 3 timestamps, 14 outdoor assets. SOLWEIG was not re-run. No field Tmrt/UTCI. | "In this pilot, the choice of thermal method changed one in three screening outcomes." |
| E2 | Divergence by time of day | Reclassification rate was 64.3% at 12:00, **0.0% at 15:00** and 35.7% at 18:00. | Same table. The aggregate is in `outputs/tables/proxy_vs_physical_comparison.csv`. | Recomputed from the reproduced per-row table. **No committed script generates the aggregate CSV**; only its values were checked. | REPRODUCED + MODEL-DERIVED | Three discrete hours on one day. There is no interpolation between them. | "The two methods agreed at the hottest hour and diverged at the shoulder hours of that day." Not a general daily pattern. |
| E3 | Uncertainty classification | Of the 42 outdoor decisions, 35 were ROBUST, 6 BOUNDARY and 1 UNSTABLE (A24 at 18:00) under the *tested* perturbations. | `src/phase2_2_decision_confidence.py` → `data/processed/phase2_2_decision_confidence.csv` | Re-run and matched. | REPRODUCED + MODEL-DERIVED | Stability is measured only against solar-forcing realisations and targeted canopy geometry. These labels are not accuracy. The two perturbation input tables were taken as given, because they need SOLWEIG. | "Each decision carries an explicit stability label." Never "validated" or "accurate". |
| E4 | Constraint-first screening | An ordered gate chain (open → reachable → thermal limit → evidence → meaningful improvement) gives each candidate exactly one first-failing exclusion reason. There is no composite score. | `src/phase3_candidate_screening.py`, `src/phase3_scenarios.py` | Code inspected. Outputs re-run and matched: 208 scenario rows, 81 candidate rows. | IMPLEMENTED + REPRODUCED | Straight-line distance, not a walking network. Rules and thresholds were fixed by the project. | Demonstrates traceable, auditable decision logic. |
| E5 | Divergence from a proximity baseline | In **3 of 8** historical scenarios (S2, S6, S8), the "nearest open option" baseline picked a candidate that the screening excludes (`OUTDOOR_EXPOSURE_TOO_HIGH`, meaning outdoor and modelled hotter than the source). | `outputs/tables/phase3_hati_vs_baseline.csv`, `data/processed/phase3_scenarios.csv` | Re-run and matched. The modelled differences were inspected per case (see below). | REPRODUCED + MODEL-DERIVED | **S2 turns on a +0.1 °C difference, and the two uncertainty envelopes overlap.** S6 is +1.3 °C, also with overlapping envelopes. S8 is +5.3 °C, with separated envelopes. Only one case is clearly outside the tested uncertainty. | "Two selection procedures give different answers under the study's rules." **Not** evidence that any real decision was wrong or that risk was avoided. |
| E6 | Candidate-set change | The screening changed the candidate set compared with the baseline pool in **7 of 8** scenarios; 23 open-in-radius candidates were removed in total. | Same tables. | Re-run and matched. | REPRODUCED + MODEL-DERIVED | Adding filters to a pool removes items almost by construction, so this shows that the filters are active, not that they are better. | Context only. Never presented as superiority. |
| E7 | Explicit "no defensible alternative" | S8 (Parque del Retiro, 15:00, 500 m) has no surviving candidate. At 800 m two candidates appear, and at 1200 m seven. | `data/processed/phase3_scenarios_summary.csv`, `outputs/tables/phase3_accessibility_sensitivity.csv` | Re-run and matched. | REPRODUCED + MODEL-DERIVED | The result depends on the radius. The source was already the coolest outdoor asset nearby (38.6 °C modelled). | Demonstrates that the method can abstain instead of forcing a recommendation. |
| E8 | Abstention under evidence insufficiency (Layer B) | For the pedestrian-route comparison, Gate 3B returned **ABSTAIN / NO ROBUST DIFFERENCE**. The Route A−B sign reverses under justified perturbations, and no route is established as cooler. | `docs/research/pedestrian-heat/gate3b/GATE3B_DECISION.md` | **Documentary check only.** Not re-executed (it needs SOLWEIG and Catastro inputs). | MODEL-DERIVED (not reproduced here) | Frozen research. One OD pair, one day. | Demonstrates evidence-sufficiency discipline. **Never** a routing recommendation. |
| E9 | Opening-hours gate | Open/closed status per asset and timestamp. | `src/phase3_build_catalog.py` → `data/processed/phase3_asset_catalog.csv` | Re-run and matched. The script's internal verification checks printed "ALL VERIFY PASS". | IMPLEMENTED + REPRODUCED | Opening hours recorded in 2026 were applied to the 2023 study day. | Method demonstration only. |
| E10 | Indoor refuge state | Indoor assets are treated as thermally buffered. | `src/phase3_candidate_screening.py` (`INDOOR_NOT_MODELLED`) | Code inspected. | HYPOTHETICAL (assumption) | Air conditioning, queueing and approach exposure are not verified. | Must always be stated as an assumption. |
| E11 | Reproducible pipeline | The analysis-environment chain regenerates the same tables from committed inputs. | [`reproduce_screening.py`](reproduce_screening.py) | Executed, PASS. A negative control confirmed the comparator detects perturbations. | REPRODUCED | Python 3.14.0rc2 used, while the reference environment is 3.14.5 (package pins matched exactly). One OS (Linux). | "Selected results are independently re-executable." |
| E12 | Field validation, visitor behaviour, business impact | — | — | None exists. | PENDING | — | Cannot be claimed in any form. |
| E13 | Commercial demand, client use, pricing | — | — | None exists. The business scenario is hypothetical. | PENDING | — | Cannot be claimed in any form. |
| E14 | Current or forecast conditions | — | All thermal results describe 21 Aug 2023 (Layer A) or 24 Aug 2023 (Layer B). | — | PENDING | Historical only. | Never presented as current Madrid conditions. |

### Per-case detail for E5 (modelled UTCI, °C; envelope = tested uncertainty range)

| Scenario | Source (baseline pick) | Source UTCI [envelope] | Baseline pick UTCI [envelope] | Difference | Envelopes overlap? |
|---|---|---|---|---|---|
| S2 · 15:00 | A15 Fuente de Cibeles → A18 Palacio de Cibeles | 44.4 [42.4–44.5] | 44.5 [43.6–44.6] | +0.1 | **Yes** |
| S6 · 18:00 | A17 Estatua de Goya → A16 Fuente de Neptuno | 43.9 [42.9–44.6] | 45.2 [43.9–45.9] | +1.3 | Yes |
| S8 · 15:00 | A20 Parque del Retiro → A22 Palacio de Cristal | 38.6 [38.6–38.7] | 43.9 [43.0–43.9] | +5.3 | No |

The exclusion rule `OUTDOOR_EXPOSURE_TOO_HIGH` fires on any positive difference. The
improvement rule, by contrast, requires at least 0.8 °C. This asymmetry is part of the
locked method and is disclosed here, not changed.

## The three strongest demonstrated capabilities

1. **Traceable constraint-first screening (E4, E5, E7).** Every candidate gets exactly
   one recorded reason, the pipeline re-executes to identical tables, and the method can
   return "no defensible alternative".
2. **Sensitivity of a decision to the thermal representation (E1, E2).** The analysis
   shows that the choice of how "hot" is measured is itself a decision variable.
3. **Explicit uncertainty and evidence sufficiency (E3, E8).** Stability labels are
   bounded to the tested dimensions, and abstention is a first-class outcome.

## Data defect discovered during reproduction (flagged, not fixed)

The descriptive column `utci_category` in `data/processed/phase2_asset_thermal_exposure.csv`
and the column `utci_category_official` in `data/processed/phase2_2_decision_confidence.csv`
are shifted one band upward relative to the Bröde et al. (2012) categories that the
project's own `docs/PHASE2_UTCI_METHOD.md` documents. As a result, 34 rows with UTCI
38.4–45.4 °C carry the label "Extreme heat stress" (correct: "Very strong", 38–46 °C), and
8 rows with 32.4–37.6 °C carry "Very strong" (correct: "Strong").

**The decision variables are not affected.** The feasibility thresholds (32/46 °C),
`decision_state`, `thermal_stress_state` and the category comparison in
`phase3_scenarios.py` all use the correct numeric edges. The mislabelled column is not
cited in the manuscript, supplementary material, figures or app.

Because these files belong to the `RELEASE_LOCKED` layer, they are left unchanged. Any
correction is an owner decision under `PROJECT_STATUS.md` §A.5. Until then, **do not
quote those label columns in professional material**; quote UTCI values instead.
