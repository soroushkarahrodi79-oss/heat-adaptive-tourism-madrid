# PHASE5_2H_ABSTRACT_AUDIT.md — HATI-Madrid Phase 5.2H

Version 1.0 · 2026-08-18. Audit of `manuscript/00_ABSTRACT_v0.1.md` against the locked
manuscript body (`manuscript/MANUSCRIPT_v0.1.md`) and, for numerical verification,
`docs/PHASE5_0_EVIDENCE_MATRIX.csv` and `docs/PHASE5_0_PAPER_CHARTER.md`. No citations,
no new literature, no new analysis. The Abstract was drafted from the locked manuscript,
not from memory.

---

## 1. Word count

**240 words** (excluding the "# Abstract" heading). Target 210–240; hard limits
190–250. Within target, at the upper edge. ✓

## 2. No citations

The Abstract contains no author-year references, no bracketed citations, and no
literature titles. ✓

## 3. Problem in the first two sentences

Sentence 1 states the management problem and the gap: "Extreme heat is a time- and
place-sensitive management problem for urban tourism, yet climate-suitability indices,
thermal routing, and heat-adjusted accessibility largely address downstream stages and
leave open the upstream question of which tourism opportunities should remain feasible
candidates at a given hour." Problem and gap are established before the approach. ✓

## 4. Tourism-management identity preserved

Opens on urban-tourism management, frames the contribution as "heat-adaptive tourism
decision support," and treats SOLWEIG/UTCI as an input to a tourism-screening question
rather than as the subject. Reads as a tourism/destination-management abstract, not an
urban-climate-methods or software abstract. ✓

## 5. Proxy defined correctly

"a simple operational proxy combining ambient air-temperature hazard thresholds and
nearby tree-presence information." No LST, satellite-temperature, shade-proxy, or
canopy-proxy language. Matches `PHASE5_0_PROXY_DEFINITION.md` §10 allowed wording. ✓

## 6. No physical-model superiority

SOLWEIG/UTCI is "physically based … modelling," never validated, accurate, superior,
or ground truth. The mandatory boundary sentence is present verbatim in intent: "The
analysis evaluates decision sensitivity to thermal-method choice rather than the
accuracy of either method against ground truth." Scan: `more accurate`, `superior`,
`validated` → absent; `ground truth` appears only inside that boundary sentence. ✓

## 7. No AEMET-vs-UTCI construct error

The dangerous noon framing was omitted entirely (permitted by the task). The Abstract
makes no statement that ambient temperature underestimated heat, that the warning state
was wrong, or that the physical model corrected it. The reclassification is reported
neutrally as method sensitivity "in both directions." No construct-boundary violation
is possible because the noon juxtaposition is not stated. ✓

## 8. Unit of analysis correct

The 33.3% figure is tied to the correct denominator: "reclassified one third of outdoor
asset-time observations (33.3%, 14 of 42)." Assets (27) and scenarios (8) are named
separately and not conflated with observations (42). No denominator drift from
observations to assets. ✓

## 9. Maximum four headline quantitative results

Four, matching the required hierarchy: (A) 33.3% (14 of 42) reclassification; (B) 7 of
8 candidate-set change; (C) 3 of 8 nearest-open failures; (D) one no-defensible-
alternative outcome. The optional solar-robustness result and the full confidence
distribution were omitted to stay within length and avoid overload. No forbidden
numbers (64.3, 35.7, 83.3/14.3/2.4) appear. ✓

## 10. Numerical verification against the locked manuscript

| Abstract figure | Manuscript source | Match |
|---|---|---|
| 33.3%, 14 of 42, outdoor asset-time observations | Results §4.1 "reclassification rate of 33.3% (14/42)"; "42 outdoor asset × timestamp observations" | ✓ |
| both directions | Results §4.1 (9 more / 5 less restrictive) | ✓ |
| 7 of 8 candidate-set change | Results §4.2 "differed from the nearest-open set in 7 of the 8 scenarios" | ✓ |
| 3 of 8 nearest-open failures | Results §4.2 "did not satisfy the locked screening constraints in 3 of the 8 scenarios (S2, S6, S8)" | ✓ |
| no-defensible-alternative when none qualified | Results §4.2 (S8, NO_DEFENSIBLE_ALTERNATIVE) | ✓ |
| 27 assets, three times of day | Methods §3.1 | ✓ |

No new rounding; all figures match the locked values exactly.

## 11. No behavioural claim

No prediction of tourist choice, redistribution, adoption, flow optimisation, safety,
or health outcome. Scan for `redistribut`, `optimis`, `safer`, `improves safety`,
`behaviour` → none. The contribution is stated as architectural/analytical. ✓

## 12. One concise limitation boundary

Exactly one closing clause: "Results are limited to a single Madrid pilot without
direct field validation of Tmrt/UTCI or observed tourist behaviour." The Limitations
section is not reproduced. ✓

## 13. No product language

"HATI", "dashboard", "platform", "application", "tool", and "MVP" are all absent. The
object is "the proposed … architecture"/"the framework." ✓

## 14. No unsupported novelty claim

Scan for `first`, `novel`, `unprecedented`, `unique`, `groundbreaking` → none ("first"
occurs only inside the compound "constraint-first"). Verbs used are "develops,"
"tests," "indicate," consistent with the allowed set; "shows" is not used for model
accuracy. ✓

## 15. Style

One continuous paragraph, seven sentences, no semicolons, no internal terminology
("Phase," "gate," "locked," "audit"), no long inventory sentence, no promotional
adjectives. A tourism reader can follow the management contribution without SOLWEIG
expertise. ✓

## 16. Consistency with MANUSCRIPT_v0.1.md

Every claim compresses a claim already in the locked body: gap (Introduction), design
and proxy/physical comparison (Methods §3.1–3.5), the four results (Results §4.1–4.2),
the method-sensitivity-not-accuracy boundary (Methods §3.5 / Discussion §5.1), the
implication (Discussion §5.5 / Conclusion), and the limitation (Limitations §6.1). No
figure, claim, or framing conflicts with the body. ✓

---

## ABSTRACT GATE

The Abstract is 240 words in one coherent paragraph moving problem → approach → results
→ implication; the four headline numbers are exact and correctly denominated; the proxy
is described without LST/shade/canopy framing; the physical model is not framed as
accurate or superior and the method-sensitivity-not-accuracy boundary is explicit; no
AEMET-vs-UTCI construct error is possible because the noon juxtaposition is omitted; no
behavioural or product claim appears; one compact limitation clause protects the
empirical claim; no citations; and the compression is faithful to the locked
manuscript.

**ABSTRACT DRAFT APPROVED**
