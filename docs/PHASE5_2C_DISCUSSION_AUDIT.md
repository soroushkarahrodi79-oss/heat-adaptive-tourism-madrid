# PHASE5_2C_DISCUSSION_AUDIT.md — HATI-Madrid Phase 5.2C

Version 1.0 · 2026-08-18. Audit of the Discussion draft
`manuscript/05_DISCUSSION_v0.1.md` against the locked Phase 5.0–5.2B record. No
Phase 0–4.1 output was modified; no new analysis was performed; no literature was
added beyond the locked Phase 5.1 corpus.

Sources consulted: `manuscript/03_METHODS_v0.1.md`, `manuscript/04_RESULTS_v0.1.md`,
`docs/PHASE5_0_PAPER_CHARTER.md`, `docs/PHASE5_0_EVIDENCE_MATRIX.csv`,
`docs/PHASE5_0_REVIEWER_ATTACK_MAP.md`, `docs/PHASE5_1_NOVELTY_AUDIT.md`,
`docs/PHASE5_1_DISCUSSION_MAP.md`, `docs/PHASE5_1_LITERATURE_MATRIX.csv`,
`docs/PHASE5_2A_METHODS_AUDIT.md`, `docs/PHASE5_2B_RESULTS_AUDIT.md`.

---

## 1. Every interpretation traced to locked evidence and its fixed frame

The Discussion Map fixes an allowed interpretive frame per finding. Each was checked.

| Finding | Draft location | Discussion-Map frame | Status |
|---|---|---|---|
| H1 (33.3%, both directions) | §5.1 ¶1 | method sensitivity; two-directional ⇒ decision variable, not offset | ✓ frame held |
| H2 (noon 64.3%; LOW vs UTCI ≥32) | §5.1 ¶2 | mechanism: radiant load high before air-temp warning crossed; not measured/validated | ✓ frame held |
| H (both directions, 9/5) | §5.1 ¶1 + ¶4 | not one-way bias; representation is a decision input; own-lineage proxy non-convergence | ✓ frame held |
| H3 (7/8; 3/8; 23 removed) | §5.2 | upstream screening changes option set; complementary to routing | ✓ frame held |
| H3b (nearest-open fails 3/8) | §5.2 ¶3 | failure mode of proximity-only guidance; governance lever; no outcome claim | ✓ frame held |
| H4 / S8 (0/26; NO_DEFENSIBLE_ALTERNATIVE) | §5.3 | architectural ability to decline; refuge-accessibility parallel; no moralising | ✓ frame held |
| H5 (1/42; 0; 0; noon persists; 83.3/14.3/2.4) | §5.4 | stable under tested forcing; categorical/separated uncertainty; not validation | ✓ frame held |

Numbers used are minimal and consistent with the locked Results (§4) — no figure
contradicts a source value, and no new statistic was introduced.

## 2. No accuracy / superiority drift (most dangerous criticism: R1+R3)

The standing rule (Discussion-Map: "method sensitivity, never accuracy validation")
holds throughout. The opening paragraph states the non-accuracy claim explicitly
("does not establish that the physically based configuration is correct and the
proxy wrong; neither representation was field-validated"). §5.1 ¶3 explicitly frames
the AEMET warning scale and UTCI as different constructs, "not two competing
measurements of the same quantity," and rules out the four forbidden readings (AEMET
understated; proxy failed to detect real heat; SOLWEIG corrected the proxy; UTCI as
ground truth). Automated scan: `more accurate`, `superior`, `corrected the proxy`,
`ground truth` (except in negation), `better model`, `safer` → **no offending
matches**. "validated" appears only as "field-validated here" (negated). ✓

## 3. No behavioural or causal claim

§5.2 ¶1 states the results are "statements about the option set, not about what any
visitor would do; no behavioural response is claimed or tested." §5.2 ¶3 and §5.3
explicitly decline outcome claims ("does not… show that using it changes any
realised management or visitor outcome"; "not empirical proof that the resulting
guidance improves management outcomes"). Scan for `redistribut`, `optimis`,
`improve tourist`, `flow`, `stay indoors` → no behavioural usage. ✓ (charter §4;
Evidence-Matrix C14; R9)

## 4. No routing-novelty overclaim (R4)

§5.2 draws the routing / accessibility / screening distinction and explicitly labels
the screening layer "a complementary upstream layer rather than a replacement," that
"does not eliminate the overlap with the routing literature," and notes a downstream
router "could in principle consume the surviving candidate set." Forbidden forms
("completely new paradigm", "first system ever", "routing cannot do this") are
absent. Novelty phrasing uses the required hedge ("Among the closest approaches
identified in the targeted review…"). ✓

## 5. Literature comparisons supported

Every cited work is in `PHASE5_1_LITERATURE_MATRIX.csv`, and each is used with the
role the matrix/Discussion-Map assigns: Gál & Kántor 2019 and WRF-UCM-SOLWEIG 2024
(radiant load driven by geometry, §5.1); "beyond LST" 2026 (air/surface ≠ comfort,
§5.1); HCI/TCI inter-comparison 2016 + tourism-climate-index reliability 2016
(composite weight-sensitivity, §5.1); Cool Routes 2026 + CoolWalks 2025 + UTCI-
adjusted accessibility 2026 (routing/accessibility boundary, §5.2); heat risk action
planning for tourism 2026 (governance, §5.2); Barcelona climate-shelter accessibility
2025 (proximity insufficient, §5.3); Monte-Carlo UTCI/PET reliability 2025 +
participatory-GIS-under-uncertainty 2025 (uncertainty framing, §5.4). Each major
result states whether it aligns with, extends, differs from, or complements the
comparison set. No fabricated contrast and no new citation were introduced. ✓

## 6. No false universality

Novelty-language scan (`the first`, `no previous`, `unprecedented`, `unique`,
`completely novel`) → no offending matches (`the first` appears only as "the first
constraint" / "first-failing-gate"). §5.1 closes qualified ("supports this on one
case rather than as a universal conclusion"). ✓

## 7. Transferability bounded

§5.5 ¶2 separates a potentially transferable architecture (constraint-first
elimination, explicit exclusions, separate confidence, method-sensitivity
comparison, no-survivor state) from non-transferable operational parameters
(thresholds, distances, assets, schedules, geometry, forcing, Madrid results), and
uses the required formulation almost verbatim: "the architecture is therefore
potentially transferable, whereas its operational parameters require local
calibration and validation." No "can be applied to any destination" language. ✓ (R2)

## 8. S8 not moralised

§5.3 frames S8 as "an architectural property rather than a normative recommendation"
and keeps the interpretation "narrow": explicit non-recommendation "preserves the
meaning of the constraints and prevents a weak option from being presented merely
because it is the least unsuitable candidate available." No `responsible AI`,
`ethical`, or `safer` language. ✓

## 9. Robustness not called validation

§5.4 ¶1 states the stability result "is a statement about stability under the tested
forcing, not a validation of the modelled radiant field, which remains unmeasured,"
and ¶3 states the treatment "is deliberately partial," covering only tested
dimensions, with confidence meaning "robust against what was tested, not certain."
The thermal-state / decision-confidence separation is interpreted via the A24 @ 18:00
UNSTABLE example without implying comprehensive uncertainty quantification. ✓
(Discussion-Map H5 forbidden list respected)

## 10. Product language controlled

"HATI" does not appear in the draft. The framework is referred to as "the proposed
framework," "the screening architecture," "the constraint-first approach," and "the
physical-model configuration." The visual prototype appears in exactly one
subordinate sentence (§5.5 ¶1: "a supplementary demonstration of implementation
feasibility and is not itself a result"). ✓ (R10)

## 11. No Introduction / Conclusion / Limitations leakage

No background-motivation build-up, no thesis restatement in conclusion register, and
no standalone Limitations subsection. Limitations are *anticipated* in one closing
paragraph (§5.5 ¶3) that explicitly defers full treatment ("set out in full in the
following section") and uses the required boundary framing ("These limitations bound
the interpretation to…") rather than the forbidden "despite these limitations, the
results prove…". ✓

## 12. Word count

Body prose (excluding markdown headings): **1,835 words** (1,871 including
headings). Target 1,800–2,400, not to exceed 2,500. Within band, favouring
analytical density over length. ✓

## 13. Structure

Five subsections: 5.1 thermal representation is decision-relevant (RQ1/H1/H2); 5.2
screening before routing (RQ2/H3); 5.3 explicit non-recommendation and traceability
(H4/S8); 5.4 robustness, uncertainty, and appropriate confidence (RQ3/H5); 5.5
contribution and transferability (cross-cutting synthesis + bounded transferability
+ limitations anticipation). Four substantive interpretive subsections plus a closing
synthesis, as directed. ✓

---

## DISCUSSION GATE

H1–H5 are interpreted without breaching the claim ceiling; the proxy-vs-physical
comparison is kept to method sensitivity and never becomes an accuracy comparison;
the routing boundary is asserted as a complementary upstream layer without
overclaim; uncertainty is presented as partial and tested-only, never as validation;
generalisation is bounded to a potentially transferable architecture with
locally-calibrated parameters; literature is integrated analytically with each work
in its locked role; no behavioural, redistribution, or tourism-outcome claim
appears; S8 is treated as an architectural property, not moralised; and the
contribution is stated as an applied, reproducible, case-based decision-support
architecture rather than a methodological breakthrough.

**DISCUSSION DRAFT APPROVED**
