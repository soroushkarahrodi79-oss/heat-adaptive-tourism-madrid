# PHASE5_2B_RESULTS_AUDIT.md — HATI-Madrid Phase 5.2B

Version 1.0 · 2026-08-18. Audit of the Results draft
`manuscript/04_RESULTS_v0.1.md` against the locked source files and the Phase 5.0
claim ceiling. No Phase 0–4.1 output was modified; no new analysis or recalculation
was performed beyond reading locked values back from their source files for
verification.

Sources of truth consulted: `docs/PHASE5_0_EVIDENCE_MATRIX.csv`,
`docs/PHASE5_0_RESULTS_HIERARCHY.md`, `docs/PHASE5_0_PAPER_CHARTER.md`,
`docs/PHASE5_2A_METHODS_AUDIT.md`, and the six locked data files below.

---

## 1. Every number verified against its locked source file

Each figure in the draft was read directly from the named file at audit time.

| # | Draft statement | Source file | Verified value | Status |
|---|---|---|---|---|
| 1 | 42 outdoor observations (14×3) | charter §5 | 42 | ✓ |
| 2 | Same state in 28, differ in 14; 33.3% (14/42) | `proxy_vs_physical_comparison.csv` | overall_reclassification_rate_pct = 33.3, n=42 | ✓ |
| 3 | 9 more restrictive / 5 less restrictive | `proxy_vs_physical_comparison.csv` | direction_count 9.0 / 5.0 | ✓ |
| 4 | 12:00 = 64.3% (9/14), 15:00 = 0.0% (0/14), 18:00 = 35.7% (5/14) | `proxy_vs_physical_comparison.csv` | by_timestamp 64.3 / 0.0 / 35.7, n=14 each | ✓ |
| 5 | Morphology all 33.3%: 3/9, 6/18, 4/12, 1/3 | `proxy_vs_physical_comparison.csv` | by_morphology 33.3 for attraction_exterior n9, park_garden n18, plaza_hardscape n12, street_corridor n3 | ✓ |
| 6 | Noon air temp 34.2 °C, LOW hazard | `PHASE1_METHOD.md` §3.1 (locked) | 34.2 °C, LOW band | ✓ |
| 7 | Modelled UTCI ≥32 °C at 14/14 outdoor assets at 12:00 | `solar_forcing_sensitivity.csv`; Evidence-Matrix C3 | noon_finding_assets_above_32C 12:00 = 14 | ✓ |
| 8 | Candidate set changed 7/8; unchanged in S7 | `phase3_hati_vs_baseline.csv` | candidate_set_changed True ×7; S7 False | ✓ |
| 9 | Nearest-open pick failed in 3/8 (S2, S6, S8) | `phase3_hati_vs_baseline.csv` | baseline_pick_survives_hati False for S2, S6, S8 | ✓ |
| 10 | All three failures = `OUTDOOR_EXPOSURE_TOO_HIGH` | `phase3_hati_vs_baseline.csv` | exclusion = OUTDOOR_EXPOSURE_TOO_HIGH ×3 | ✓ |
| 11 | 23 options screened out on thermal/evidence grounds | `phase3_hati_vs_baseline.csv` | Σ n_removed_by_hati_thermal_or_evidence = 23 | ✓ |
| 12 | 7 scenarios ALTERNATIVES_FOUND; counts 4–9 | `phase3_scenarios_summary.csv` | n_alt = 9,6,4,8,7,9,6 (S1–S7); range 4–9 | ✓ |
| 13 | S8: Retiro, 15:00, 500 m; 26 rows, 0 survive; NO_DEFENSIBLE_ALTERNATIVE | `phase3_scenarios.csv` + `_summary.csv` | 26 rows all EXCLUDED; recommendation = NO_DEFENSIBLE_ALTERNATIVE; radius 500 | ✓ |
| 14 | Satellite forcing: 1/42 changed (2.4%) | `solar_forcing_sensitivity.csv` | decision_changes 1.0 / pct 2.4 (REAL_SATELLITE) | ✓ |
| 15 | −10% = 0, −20% = 0 changes | `solar_forcing_sensitivity.csv` | SENS_A 0.0, SENS_B 0.0 | ✓ |
| 16 | Single satellite change = A24 @ 18:00 (envelope to 46 °C) | `phase2_2_decision_confidence.csv` | A24 18:00 UNSTABLE, envelope_high 46.0, source REAL_SATELLITE | ✓ |
| 17 | Noon ≥32 °C persisted under all solar scenarios | `solar_forcing_sensitivity.csv` | noon 12:00 = 14 for REAL_SATELLITE, SENS_A, SENS_B | ✓ |
| 18 | Confidence: ROBUST 35 (83.3%), BOUNDARY 6 (14.3%), UNSTABLE 1 (2.4%) | `phase2_2_decision_confidence.csv` | Counter = {ROBUST:35, BOUNDARY:6, UNSTABLE:1}, n=42 | ✓ |
| 19 | UNSTABLE = A24 @ 18:00 | `phase2_2_decision_confidence.csv` | A24 18:00 | ✓ |
| 20 | 6 BOUNDARY at 15:00/18:00, envelope maxima 44.5–45.9 °C | `phase2_2_decision_confidence.csv` | A15/A16/A24/A25 @15:00, A15/A16 @18:00; env_high 44.5–45.9 | ✓ |
| 21 | A24 → INSUFFICIENT_EVIDENCE in S4; source-flagged in S7 | `phase3_scenarios.csv`; Evidence-Matrix C9 | consistent with locked record | ✓ |

No number required recalculation; all are read-backs of locked values.

## 2. RQ1–RQ3 coverage

- **§4.1 → RQ1 (method sensitivity):** reclassification rate, direction, timestamp
  breakdown, morphology invariance, and the noon LOW-hazard / UTCI ≥32 °C pattern.
  Closes with the bounded finding "sensitive to thermal-method choice, particularly
  at noon." ✓
- **§4.2 → RQ2 (decision-support value):** 7/8 candidate-set change, 3/8 nearest-open
  failures, 23 removed, surviving-set range, and the S8 no-survivor case. Closes with
  a bounded finding. ✓
- **§4.3 → RQ3 (robustness/traceability):** solar-forcing stability, noon persistence,
  separate confidence distribution, UNSTABLE propagation, and exclusion/no-recommendation
  traceability. Closes with a bounded finding. ✓

Each subsection maps to exactly one research question, in order.

## 3. Exact H1–H5 coverage

| Headline (Results Hierarchy Tier 1) | Where reported | Status |
|---|---|---|
| H1 — 33.3% reclassification; 9 more / 5 less | §4.1 ¶1 | ✓ exact |
| H2 — 12:00 64.3% / 15:00 0% / 18:00 35.7%; noon LOW vs UTCI ≥32 at 14/14 | §4.1 ¶2 + ¶4 | ✓ exact |
| H3 — 7/8 changed; 3/8 fail (OUTDOOR_EXPOSURE_TOO_HIGH); 23 removed | §4.2 ¶2–3 | ✓ exact |
| H4 — S8 26 evaluated, 0 survive, NO_DEFENSIBLE_ALTERNATIVE | §4.2 ¶4 | ✓ exact |
| H5 — satellite 1/42 (2.4%); ±10/±20% 0; noon persists | §4.3 ¶1 | ✓ exact |

All five headline findings are present and stated at their exact locked values.
The confidence distribution (supporting Tier-1/2 evidence, Evidence-Matrix C9) is
also reported at §4.3 ¶2 with exact values.

## 4. No unsupported accuracy / superiority claim

The draft never states either method is more accurate, correct, better, superior,
or validated. Automated scan for `superior`, `more accurate`, `better`, `prove`,
`safer`, `successful`, `ground truth`, `corrected the proxy`, `missed the true`,
and `the proxy is wrong` returned **zero matches**. Divergence is reported neutrally
("differed," "reclassified," "produced a more/less restrictive state"), and §4.1
attributes the noon pattern to the difference between the two inputs without ranking
them. The word "demonstrated" appears only in the locked technical term
"demonstrated sensitivity" (Phase 2.2), not as a superiority claim. ✓

## 5. No behavioural or causal claim

No statement about tourist choice, flow, redistribution, adoption, safety outcome,
or visitor optimisation appears. Scan for `redistribut`, `optimis`, `improve`,
`visitor flow`, and `tourist` in an outcome sense returned no behavioural usage;
"surviving alternatives" and "candidate set" are used throughout, and S8 is framed
as an output of the locked rules. ✓ (charter §4; Evidence-Matrix C14)

## 6. No inferential-statistics language

No p-value, confidence interval, significance label, effect-size term, or
inferential test appears. The opening paragraph states explicitly that the unit is
the locked observation/scenario comparison and that no inferential test is applied.
33.3% is never described as significant. All quantities are descriptive counts and
rates over the locked units. ✓

## 7. No Methods repetition beyond what Results requires

Method mentions are limited to the minimum needed to make each number legible (the
32/46 °C boundaries, the nearest-open comparator definition in one clause, the
evidence gate as the propagation path). No re-derivation of SOLWEIG parameters,
provenance, gate history, or the uncertainty construction is included; those remain
in §3. ✓

## 8. No Discussion leakage

Each subsection ends with a bounded, factual "the finding of this subsection is
limited to…" statement. No interpretation of why method choice matters, no
positioning against literature, no novelty/importance/contribution argument, and no
normative reading of S8 appears. The forbidden Discussion terms (`novel`,
`innovative`, `breakthrough`, `important contribution`) scan clean. ✓

## 9. Word count

Body prose (excluding markdown headings): **1,204 words** (1,222 including
headings). Target band 1,200–1,700, preferred 1,300–1,500. The draft sits within the
mandatory band, at its lower end **by design**: every required number plus the
morphology-invariance, surviving-set range, source-state readout, satellite-change
linkage, and BOUNDARY characterisation are reported, and further expansion would
require either Methods repetition or Discussion-style interpretation, both
prohibited here. Judged adequate rather than padded.

## 10. Table / figure references

Provisional references only, consistent with `PHASE5_0_FIGURE_PLAN.md` /
architecture §10: Table 3 and Fig. 2 (proxy-vs-physical centerpiece), Fig. 3 (noon
UTCI), Table 4 and Fig. 6 (baseline-vs-HATI scenarios incl. S8), Fig. 4
(uncertainty/robustness). No final numbering or captions were invented, and the text
is readable with the figures removed. ✓

---

## RESULTS GATE

Every headline statistic is exact and verified against its locked source file; the
three subsections map directly to RQ1–RQ3; method divergence is described without
any accuracy or superiority claim; S8 is reported correctly as a rule-produced
no-survivor outcome (26 evaluated, 0 survive, NO_DEFENSIBLE_ALTERNATIVE); uncertainty
is reported without claiming physical validation; no behavioural, causal, or
Discussion-style statement appears; and the word count is within the mandatory band.

**RESULTS DRAFT APPROVED**
