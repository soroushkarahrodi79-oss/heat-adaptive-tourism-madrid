# PHASE5_2D_LIMITATIONS_AUDIT.md — HATI-Madrid Phase 5.2D

Version 1.0 · 2026-08-18. Audit of the Limitations draft
`manuscript/06_LIMITATIONS_v0.1.md` against the locked Phase 5.0–5.2C record. No
Phase 0–4.1 output was modified; no new analysis was performed; no new literature was
introduced.

Sources consulted: `manuscript/03_METHODS_v0.1.md`, `manuscript/04_RESULTS_v0.1.md`,
`manuscript/05_DISCUSSION_v0.1.md`, `docs/PHASE5_0_PAPER_CHARTER.md`,
`docs/PHASE5_0_REVIEWER_ATTACK_MAP.md`, `docs/PHASE5_0_EVIDENCE_MATRIX.csv`,
`docs/PHASE5_1_DISCUSSION_MAP.md`, `docs/PHASE5_2A/2B/2C` audits.

---

## 1. Field-validation absence appears prominently

The physical-model validation boundary is §6.1, the first domain, and opens by naming
it "the most consequential boundary." It states Tmrt and UTCI were model-derived, that
no direct field measurements were collected, that station observations support the
forcing and "not the modelled radiant field: they constrain the inputs, not the
output," and that SOLWEIG was assessed by plausibility and sensitivity "not against
in-situ radiant or comfort measurements." It explicitly refuses the compensating move:
"precedent for the model in general does not certify the specific configuration used
here." This satisfies R1 and the Reviewer-Attack-Map "most dangerous criticism"
requirement (R1+R3), and the limitation is not weakened anywhere. ✓

## 2. Method divergence not framed as accuracy

§6.1 ¶2 states the required boundary directly: "the proxy-versus-physical comparison
evaluates decision sensitivity to the choice of thermal method, not the accuracy of
either method against ground truth," and "it does not show that one representation is
correct and the other wrong." Automated scan: `more accurate`, `ground truth`,
`superior`, `validated the`, `proves` → matches occur **only inside negations** (e.g.
"does not… assert that the physical configuration is the more accurate account").
No accuracy or superiority drift. ✓ (Discussion-Map standing rule; charter §6)

## 3. Single-day / single-city scope explicit

§6.2 states one city, one ≈3.5 km² pilot, one documented extreme-heat day, three
timestamps, 27 assets, 42 outdoor comparisons — each verified against Methods §3.1 and
charter §5. It explicitly denies seasonal, climatological, city-wide, cross-city, and
cross-regime inference, and states the assets are "not a statistically representative
sample," with "the reported rates … properties of this configuration rather than
population estimates." ✓ (R2)

## 4. Tested uncertainty distinguished from total uncertainty

§6.3 names what was propagated (solar forcing across all outdoor rows; targeted
geometry for two assets) and what was not (wind, humidity, air-temperature, full
vegetation, model-structural, radiation errors), consistent with Methods §3.6 and
Discussion §5.4. It carries the canopy-vintage limitation and states the correction was
localised, not a full canopy reconstruction. The interpretive boundary is explicit: a
"ROBUST, BOUNDARY, or UNSTABLE classification expresses robustness to the tested
uncertainty space, not total certainty," the per-row sensitivity is "a lower bound on
the true uncertainty," and "robust against what was tested, not validated." ✓
(Discussion-Map H5 forbidden list respected)

## 5. Behavioural non-claim explicit

§6.4 ¶2 states the framework used "no behavioural response data, observed no visitor
substitution, and was not validated against revealed or stated preferences," and does
not predict tourist choice, following of alternatives, flow redistribution, or exposure
/ health outcomes ("outside the evidence and are not claimed"). ✓ (R9; C14)

## 6. Accessibility limitation explicit

§6.4 ¶1 states accessibility is straight-line distance with "no pedestrian route
geometry," "no thermal exposure during travel," and "no slope or walking-cost model,"
a "lower bound on true walking distance." ✓ (R6)

## 7. Indoor-refuge assumption explicit

§6.4 ¶3 states indoor status used a "refuge-bypass logic that assumes thermal
buffering," that indoor temperature, air conditioning, queue/entrance exposure, and
comfort "were not observed," and that indoor thermal evidence "was capped below the
highest confidence level by design." It concludes surviving indoor options should be
read "as assumed refuges under this logic, not as physically verified cool refuges."
✓ (R8)

## 8. Opening-hours temporal mismatch explicit

§6.5 states hours were "captured and documented at a later date and applied
retrospectively to the 2023 study day," sufficient for a reproducible demonstration
"but … not proof that every establishment kept the same schedule on 21 August 2023,"
and localises the effect to "a specific candidate's availability … not the thermal
modelling." ✓ (R7)

## 9. Transferability bounded

§6.6 separates the potentially transferable architecture (constraint-first screening,
first-failing-gate explanations, separate thermal state / confidence, explicit
exclusion reasons, explicit no-survivor state, thermal-representation comparison) from
setting-specific operational components (thresholds, radius, schedules, assets,
relevance, geometry, meteorology, adaptation resources), and uses the required
formulation: "The architecture is therefore potentially transferable, whereas its
operational parameters and empirical performance require local calibration and
validation before use in another setting." No "the model is transferable to other
destinations" language. ✓ (R2)

## 10. No defensive rhetoric

No generic opener ("like all studies…"), no compensating validation claim ("however,
SOLWEIG is widely validated…"), and no "despite these limitations, the results prove…"
construction — all three scanned clean. The closing synthesis (§6.6 final ¶) uses the
required boundary frame ("these limitations bound the interpretation to…") rather than
neutralising the limitations. ✓

## 11. No product / dashboard / development-history limitations

No dashboard, basemap, connectivity, software-version, or Phase-1/2/3 development
narrative appears (scanned: `dashboard`, `basemap`, `digital twin`, `agent`, `machine
learning` → none). Only limitations affecting scientific interpretation are included.
✓ (R10)

## 12. Future work

§6.7 is a single closing paragraph confined to tests that raise the evidence ceiling —
field Tmrt/UTCI measurement (named highest-value), multi-day/seasonal and additional
cities, route-level exposure, observed behaviour, verified indoor conditions — each
tied to a boundary named above. No new feature (ML, agents, digital twins,
optimisation) is promised. ✓

## 13. Word count

Body prose (excluding markdown headings): **1,180 words** (1,225 including headings).
Target 800–1,200, preferred 900–1,050. Within the mandatory band, in its upper portion
by design: five limitation domains plus a bounded transferability subsection and a
one-paragraph future-work close leave little compressible content without dropping a
required disclosure. Judged substantial-but-not-dominant, as directed. ✓

## 14. Consistency with Methods / Results / Discussion

Every limitation matches a boundary already stated in the locked sections: field
validation (Methods §3.4, §3.9; Discussion §5.1/§5.4), scope (Methods §3.1), tested
uncertainty (Methods §3.6; Discussion §5.4), accessibility and behaviour (Methods §3.8,
§3.9; Discussion §5.2), indoor refuge (Methods §3.9), opening hours (Methods §3.2), and
transferability (Discussion §5.5). No new limitation was invented and no contradiction
was introduced. ✓

## 15. Domain structure

§6.1 physical-model validation boundary · §6.2 spatial and temporal scope · §6.3 input
and uncertainty limitations · §6.4 tourism and accessibility limitations · §6.5
operational-data and retrospective-alignment limitations · §6.6 scope conditions and
transferability · §6.7 future work. Five limitation domains + transferability + a short
future-work close, ordered by consequence, as directed. ✓

---

## LIMITATIONS GATE

All permanent limitations are represented and none is rhetorically neutralised; the
field-validation boundary leads and is not weakened; the proxy-versus-physical
comparison is held to method sensitivity, never accuracy; single-day/single-city scope,
partial-uncertainty, behavioural non-claim, straight-line accessibility, indoor-refuge
assumption, and opening-hours mismatch are all explicit; the architecture-versus-
parameter transferability distinction is stated correctly; future work promises no
unsupported feature; and nothing contradicts the locked Methods, Results, or Discussion.

**LIMITATIONS DRAFT APPROVED**
