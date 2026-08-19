# PHASE5_2G_FULL_MANUSCRIPT_CONSISTENCY_AUDIT.md — HATI-Madrid Phase 5.2G

Version 1.0 · 2026-08-18. Whole-paper consistency audit of the six gate-approved
sections read as one manuscript. No new analysis, no new literature, no locked number
changed, no modelling reopened. Two surgical consistency edits were made (recorded in
§12). Assembled body: `manuscript/MANUSCRIPT_v0.1.md`, 8,748 body words.

Sources also consulted: `docs/PHASE5_0_PAPER_CHARTER.md`,
`docs/PHASE5_0_PROXY_DEFINITION.md`, `docs/PHASE5_0_EVIDENCE_MATRIX.csv`,
`docs/PHASE5_0_REVIEWER_ATTACK_MAP.md`, `docs/PHASE5_1_NOVELTY_AUDIT.md`.

---

## 1. Central-argument crosswalk

| Section | Strongest one-sentence argument implied | Same paper? |
|---|---|---|
| Introduction | Screening tourism opportunities under heat is a distinct upstream stage; a constraint-first, uncertainty-aware architecture can occupy it and test whether thermal-method choice changes feasibility. | ✓ |
| Methods | Defines a proxy baseline, a physically based configuration, an uncertainty treatment, and a constraint-first screen so their differences can be compared without validating either method. | ✓ |
| Results | Method choice reclassified one third of outdoor observations (both directions, time-concentrated); screening changed the candidate set in 7/8 scenarios and returned an explicit no-survivor state once; decisions were stable under tested forcing. | ✓ |
| Discussion | Different thermal representations can materially change which opportunities are treated as feasible; a constraint-first architecture makes this auditable; method sensitivity, not accuracy. | ✓ |
| Limitations | The comparison is method sensitivity not accuracy; evidence is one bounded pilot with partial uncertainty and no behavioural or field validation. | ✓ |
| Conclusion | Thermal representation is a substantive modelling choice for heat-adaptive tourism screening; bounded to one pilot, no field/behavioural validation. | ✓ |

**Verdict:** all six support the single locked claim — *thermal-method choice can
materially alter tourism-screening outcomes, and a constraint-first, uncertainty-aware
architecture makes those effects auditable, without claiming physical-model
superiority or behavioural outcomes.* No section implies a stronger or different paper.

## 2. RQ crosswalk

| RQ | Introduction | Methods | Results | Discussion | Conclusion |
|---|---|---|---|---|---|
| RQ1 method sensitivity | stated | §3.3–3.5 (proxy, physical, comparison) | §4.1 | §5.1 | P1 |
| RQ2 decision-support value | stated | §3.7–3.8 (screen, baseline, scenarios) | §4.2 | §5.2 (+§5.3 for the no-survivor case) | P1–P2 |
| RQ3 robustness/traceability | stated | §3.6 (uncertainty), §3.7 (traceability) | §4.3 | §5.4 | P2–P3 |

Every RQ is answered; every Results subsection maps to one RQ; no Results item is
orphaned; no Discussion or Conclusion claim exceeds its RQ. The Intro RQ wording is
substantively identical to the charter §4b RQs (proxy described, not named — per the
proxy-wording rule).

## 3. Terminology inconsistencies

- **Proxy:** described consistently as ambient air-temperature hazard thresholds +
  OSM tree-count / tree-presence exposure → constraint-first feasibility. No
  LST/satellite/canopy-fraction/shade-model attribution to the proxy anywhere;
  "land surface temperature" appears only as the *citation title* ("beyond land
  surface temperature," Intro/Discussion), and "surface-temperature/shadow" only
  inside the Methods negative definition. Intro simplification and Methods technical
  definition are compatible. ✓
- **One drift found and fixed (Methods §3.5):** reclassification direction had been
  phrased as "the baseline understated/overstated hazard," which implies a true
  hazard the proxy mis-stated and contradicts both the next paragraph of the same
  subsection and Discussion §5.1. Corrected to neutral "more/less restrictive than
  the proxy state" (edit 1, §12). No other terminology inconsistency remains.

## 4. Numerical cross-check

| Quantity | Locked value | Where it appears | Consistent? |
|---|---|---|---|
| Reclassification | 14/42 = 33.3% | Results §4.1 (14/42, 33.3%); Discussion "one-third"; Conclusion "one third" | ✓ |
| Direction | 9 more / 5 less restrictive | Results §4.1; Discussion "nine … five" | ✓ |
| By timestamp | 12:00 64.3% / 15:00 0.0% / 18:00 35.7% | Results §4.1 only; Discussion qualitative ("largest at midday, absent at 15:00, intermediate at 18:00") | ✓ |
| Noon UTCI ≥32 | 14/14 outdoor | Results §4.1 ("all 14 … 14 of the 14"); Discussion "all fourteen" | ✓ |
| Morphology | 33.3% each (3/9, 6/18, 4/12, 1/3) | Results §4.1 | ✓ |
| Candidate set changed | 7/8 (S7 exception) | Results §4.2 ("7 of the 8"); Discussion "seven of eight"; Conclusion "seven of eight" | ✓ |
| Nearest-open fails | 3/8 (S2,S6,S8), OUTDOOR_EXPOSURE_TOO_HIGH | Results §4.2; Discussion "in three" | ✓ |
| Options removed | 23 | Results §4.2 only | ✓ |
| Alternatives-found | 7/8 (S8 exception), counts 4–9 | Results §4.2 | ✓ |
| S8 | 26 evaluated, 0 survive, NO_DEFENSIBLE_ALTERNATIVE, Retiro 15:00 500 m | Results §4.2; Discussion §5.3 ("twenty-six"); Conclusion (descriptive) | ✓ |
| Solar forcing | satellite 1/42 (2.4%), −10% 0, −20% 0 | Results §4.3 only | ✓ |
| Confidence | ROBUST 35 (83.3%) / BOUNDARY 6 (14.3%) / UNSTABLE 1 (2.4%) | Results §4.3 only | ✓ |
| UNSTABLE case | A24 @ 18:00 | Results §4.3; Discussion §5.4; = the single satellite-forced change | ✓ |
| Study parameters | 3.5 km², 27 assets (13/14), 42 outdoor, 8 scenarios, hours 12/15/18, Ta 34.2/38.8/40.5 | Methods/Results consistent | ✓ |

No denominator conflict, no percentage-precision drift, verbal equivalents ("one
third", "seven of eight") match their numeric sources, and no headline number appears
in a section instructed to omit it (Methods/Limitations restate no Results statistic;
apparent `23 `/`26 ` tokens there are substrings of "2023"/"2026"). **Two distinct
7/8 facts coexist** — candidate-set-changed (exception S7) and alternatives-found
(exception S8); both are individually correct and labelled by different properties in
Results §4.2, and the Conclusion's single "seven of eight" refers unambiguously to the
candidate-set change. Flagged as a clarity watch-point, not a contradiction (§13).

## 5. Unit-of-analysis check

The five units stay distinct throughout: **27 assets** (13 indoor / 14 outdoor),
**42 outdoor asset × timestamp observations** (14 × 3), **8 decision scenarios**, and
**candidate rows within scenarios** (26 in S8). Results opens by defining "the unit is
the asset × timestamp observation or the scenario comparison," uses "observation"
only for the 42 rows and "scenario" only for the 8, and reserves "candidate rows" for
within-scenario evaluation. No sentence conflates assets, observations, scenarios, and
candidate alternatives. ✓

## 6. Claim-ceiling check

Supported claims only: method-choice sensitivity (not accuracy), candidate-set change,
explicit no-recommendation, stability under tested forcing, auditability. Forbidden
claims absent across all sections: `more accurate`/`superior`/`ground truth`/
`corrected the proxy` appear **only in negations or citation titles**; `proxy failed`
appears only in Discussion's explicit denial; no breakthrough/first/unprecedented; no
behavioural/redistribution/optimisation/safety claim. The most dangerous line (R1+R3,
"two unvalidated methods") is defended in Methods §3.4/§3.5, Discussion §5.1, and
Limitations §6.1. ✓

## 7. Routing-boundary check

Routing (O+D → path), thermal accessibility (destination set → reachability), and
screening (upstream candidate eligibility) are described consistently in Intro P4,
Discussion §5.2, and Conclusion P2. All three use "complementary"/"upstream"/"distinct
decision stage" and note downstream methods "would consume" the surviving set. None of
the forbidden forms (`routing is irrelevant`, `routing ignores`, `replaces routing`,
`no overlap`) appears. The boundary is asserted as strongly mitigated, not eliminated
(Novelty Audit §3; R4). ✓

## 8. Uncertainty-language check

`thermal state`, `decision confidence`, and `evidence confidence` are kept as distinct
concepts in Methods §3.6–3.7, Results §4.3, Discussion §5.4, and Limitations §6.3.
ROBUST/BOUNDARY/UNSTABLE is consistently defined as robustness to the *tested*
uncertainty space, never as accurate/certain/validated — Methods "robust against what
was tested, not certain"; Limitations "robust against what was tested, not validated …
lower bound on the true uncertainty"; Discussion "stability under the tested forcing,
not a validation." Uncertainty scope is consistently stated as partial (solar +
targeted geometry only). ✓

## 9. Transferability check

Discussion §5.5, Limitations §6.6, and Conclusion P3 all draw the same boundary:
architecture potentially transferable; operational parameters and empirical
performance require local calibration and validation. Discussion and Limitations use
the near-verbatim formulation. No universal-external-validity phrase exists ("any
destination" is a false positive from "m*any destination*s"). ✓

## 10. Behavioural / output-claim check

Every reference to behaviour is a non-claim: Discussion §5.2 ("no behavioural response
is claimed or tested"), Limitations §6.4 (redistribution/flows/outcomes "outside the
evidence and are not claimed"), Conclusion P3 ("without any observation of tourist
behaviour"). Architectural capability (the engine can decline; can change the option
set) is consistently distinguished from observed outcome (never asserted). ✓

## 11. Redundancy findings

- The routing/accessibility distinction appears three times (Intro P4, Discussion
  §5.2, Conclusion P2). This is **intentional reinforcement** of the novelty-critical
  boundary, not harmful duplication; each instance serves its section's function
  (set-up / interpretation / closing). Retained.
- Partial-uncertainty appears in Discussion §5.4 and Limitations §6.3 with different
  functions (interpretation vs boundary). Acceptable.
- Indoor-refuge caveat appears in Methods §3.9, Discussion §5.3-adjacent, and
  Limitations §6.4; consistent and non-duplicative in role.
- No paragraph reproduces another section wholesale; no Methods project-history
  narrative ("Phase 1/2/3") leaked. No redundancy materially harms quality.

## 12. Exact edits made

**Edit 1 — Methods §3.5 (accuracy-drift removal, authorised: "removing an accidental
superiority claim").**
- Before: "Reclassifications were characterised by direction — whether the physical
  model was more restrictive (the baseline understated hazard) or less restrictive
  (the baseline overstated hazard) — and were stratified by timestamp …"
- After: "Reclassifications were characterised by direction — whether the physically
  derived state was more restrictive or less restrictive than the proxy state — and
  were stratified by timestamp …"
- Reason: "understated/overstated hazard" implied a true hazard the proxy mis-stated,
  contradicting the same subsection's "two methods disagree, not that one is correct
  and the other wrong" and Discussion §5.1. Neutral directional wording restores the
  claim ceiling. No number changed.

**Edit 2 — Introduction opening sentence (unsupported-claim fix, authorised: "fixing
one unsupported opening sentence"; Audit 15).**
- Before: "…extreme-heat episodes now recur through the core of the summer season, and
  they fall on precisely the outdoor places and midday-to-afternoon hours that urban
  visitors use most. Open plazas … become heat-exposed at the same times that
  sightseeing concentrates there …"
- After: "…extreme-heat episodes increasingly overlap with the summer season and with
  the daytime, outdoor conditions under which much urban tourism takes place. Open
  plazas … become heat-exposed during these hours …"
- Reason: "the … hours that urban visitors use most" / "at the same times that
  sightseeing concentrates there" asserted tourist spatial-temporal usage the cited
  sources do not establish and edged toward a behavioural-timing claim (Intro-Logic
  Step 1 narrowing). Replaced with the conservative, source-supported framing.

No other edits were made; prose was not otherwise rewritten.

## 13. Unresolved issues

- **Two coexisting 7/8 facts (advisory, non-blocking).** Candidate-set-changed (7/8,
  exception S7) and alternatives-found (7/8, exception S8) both appear in Results §4.2.
  Both are correct and separately labelled; the Conclusion uses only the first. No
  contradiction, but a copy-editing pass before submission may add a half-clause to
  Results §4.2 making explicit that the two "seven of eight" statements concern
  different scenarios, to remove any reader ambiguity. Not required for consistency
  lock.
- No factual, terminological, numerical, unit, claim-ceiling, routing, uncertainty,
  transferability, behavioural, indoor, or transferability contradiction remains
  unresolved.

## 14. Manuscript narrative test (Audit 18)

Reading only the Introduction final paragraph + Results subsection headings +
Discussion first paragraph + Conclusion yields one coherent paper: a constraint-first,
uncertainty-aware screening architecture is proposed (Intro); its outputs are
thermal-method sensitivity, screening effects, and robustness/traceability (Results
headings); different thermal representations materially change feasibility and the
architecture makes this auditable without accuracy or behavioural claims (Discussion
opening); and the bounded implication is that thermal representation is a substantive
modelling choice (Conclusion). No divergence. ✓

---

## CONSISTENCY GATE

One central claim holds across all six sections; RQ1–RQ3 are fully aligned and each is
answered; the proxy definition does not drift and carries no LST/shade/canopy framing;
the physical-model superiority drift found in Methods §3.5 was corrected; no numerical
contradiction exists; the unit of analysis is unambiguous; the AEMET/UTCI construct
boundary is intact and explicit; the routing distinction is consistent and hedged;
uncertainty is partial/tested throughout; no behavioural claim appears; the indoor
assumption is correctly bounded; transferability is bounded to architecture-with-local-
calibration; and no unresolved contradiction remains between approved sections.

**MANUSCRIPT CONSISTENCY LOCKED**
