# PHASE5_2E_INTRODUCTION_AUDIT.md — HATI-Madrid Phase 5.2E

Version 1.0 · 2026-08-18. Audit of the Introduction draft
`manuscript/01_INTRODUCTION_v0.1.md` against the locked Phase 5.0–5.2D record and the
Phase 5.1 introduction logic. No Phase 0–4.1 output was modified; no new analysis was
performed; no literature outside the locked Phase 5.1 corpus was introduced.

Sources consulted: `docs/PHASE5_0_PAPER_CHARTER.md`,
`docs/PHASE5_0_PROXY_DEFINITION.md`, `docs/PHASE5_1_NOVELTY_AUDIT.md`,
`docs/PHASE5_1_INTRO_LOGIC.md`, `docs/PHASE5_1_LITERATURE_MATRIX.csv`,
`docs/PHASE5_1_JOURNAL_FIT.md`, and the four approved manuscript sections
(`03_METHODS`, `04_RESULTS`, `05_DISCUSSION`, `06_LIMITATIONS`).

---

## 1. Tourism-management problem established early; no generic climate opening

The opening sentence is operational and tourism-anchored ("In the tourism cities of
Southern Europe, extreme-heat episodes now recur through the core of the summer
season, and they fall on precisely the outdoor places and midday-to-afternoon hours
that urban visitors use most"). Paragraph 1 frames heat as a destination-management
decision problem ("For destination management this is an operational problem rather
than only a long-run climatic one"), consistent with Intro-Logic Step 1. No generic
climate-change opener; scan for "climate change is one", "greatest challenge" →
none. ✓

## 2. Composite-index literature treated fairly

Paragraph 2 states TCI/HCI "remain useful for their intended purpose" and frames the
limitation as "one of spatial and temporal scale and of decision purpose, not of
validity." No "obsolete", "invalid", or "traditional indices are obsolete" language
(scanned clean). The weight-sensitivity point is attributed to the literature
(reliability of tourism climate indices, 2016), matching Intro-Logic Step 2. ✓

## 3. Physical modelling not framed as more accurate

Paragraph 3 uses the required framing: SOLWEIG/UTCI "provide a different
representation of the thermal environment, resolving additional physical dimensions
relevant to pedestrian exposure," and are explicitly "not, on their own and without
in-situ measurement, a validated ground truth against which a simpler method can be
called wrong." It then states the paper's question directly: "not which thermal
method is correct, but whether the choice of thermal representation materially
changes a tourism-screening decision." Scan for "more accurate"/"superior" → none;
"ground truth" occurs only in the negation above. This preserves the field-validation
boundary (Methods §3.4/§3.9; Limitations §6.1) and the decision-sensitivity frame
(Discussion §5.1). ✓

## 4. Routing / accessibility boundary explicit and correctly hedged

Paragraph 4 states the three decision stages accurately — routing (given O+D, which
path?), accessibility (given a destination set, which are reachable?), and the
upstream screening question (which opportunities should remain eligible candidates at
a given hour) — and labels the routing/accessibility methods "complementary" and
operating "at a downstream decision stage," each of which "presupposes the candidate
set." It uses "upstream" and "distinct decision stage," and explicitly notes a
downstream method "would consume" the surviving set. It does not claim the routing
literature is insufficient in general, and the phrase "routing ignores destination
selection" does not appear. This is the required strong-mitigation-not-denial
treatment (Novelty Audit §3; Reviewer-Attack-Map R4; Discussion §5.2). ✓

## 5. Gap conservative and literature-supported

Paragraph 5 opens with the required hedged form: "Among the closest approaches
identified in a targeted review of this literature, we found that routing,
accessibility, thermal mapping, and composite climate suitability are each addressed
separately, and none screens individual tourism opportunities by explicit
physical-thermal, accessibility, and evidence constraints at a specific hour…." No
"no previous study", "the first", "unprecedented", "completely novel" (scanned
clean). The gap is stated as an under-served, defensible screening stage, matching
Intro-Logic Step 5 and `RESEARCH_GAP.md` framing. ✓

## 6. No Results leakage

Scan for the Tier-1 statistics (`33.3`, `64.3`, `35.7`, `7/8`, `3/8`, `23 `,
`one-third`) → no matches. The contribution is described qualitatively; no
reclassification rate, scenario count outcome, or robustness figure appears. ✓

## 7. No product / dashboard framing

"HATI" does not appear. The framework is referred to as "a constraint-first,
uncertainty-aware architecture," "the proposed screening framework"/"the study," and
"the architecture." Scan for `dashboard`, `mvp`, `interface`, `digital twin`,
`software`, `app` → none. ✓ (Reviewer-Attack-Map R10)

## 8. Final paragraph: contribution + RQ1–RQ3

Paragraph 5 states the contribution as "an applied, reproducible decision-support
architecture together with a case-based demonstration of whether thermal-method
choice is decision-relevant," explicitly noting it "does not rest on either thermal
method being validated, and it makes no claim about tourist behaviour, flows, or
outcomes." It closes with the three research questions. Substantive meaning matches
the locked RQs (charter §4b); only light grammatical/style edits were applied, and
the proxy is described (not named "LST/shade/canopy") per the Intro proxy-wording
rule. ✓

## 9. Proxy wording

The comparator is described once, in Paragraph 5, as "a simple operational proxy —
combining ambient air-temperature hazard thresholds with nearby tree-presence
information," and in RQ1 as "the simple air-temperature-and-tree-presence proxy." No
"LST proxy", "shade proxy", "canopy proxy", or "satellite proxy" appears. ✓
(`PHASE5_0_PROXY_DEFINITION.md` §10)

## 10. Behavioural / outcome non-claim

Paragraph 5 states the contribution "makes no claim about tourist behaviour, flows,
or outcomes." Scan for `redistribut`, `optimis`, `improves safety`, `safer` → none.
✓ (charter §4; C14; R9)

## 11. Word count

Body prose (excluding markdown headings): **1,347 words** (1,350 including headings).
Target 1,200–1,600, preferred 1,350–1,500, not to exceed 1,700. At the lower edge of
the preferred band. ✓

## 12. Citation count and traceability

**23 distinct citations**, within the 15–25 target, distributed across the five
logic steps without stacking: P1 (7) tourism heat governance/context — extreme-heat
mobility 2025, heat risk action planning 2026, OECD 2026, Southern-Europe adaptation
2026, demand under climate change 2025, tourism exposure ERL 2024, Madrid/Sevilla
plaza comfort 2022; P2 (4) composite indices — HCI/TCI 2016, Hungarian HCI/TCI 2025,
tourism-climate-index reliability 2016, GIS-AHP 2011; P3 (5) physical modelling —
Lindberg et al. 2008, Bröde et al. 2012, WRF-UCM-SOLWEIG 2024, beyond LST 2026, Gál &
Kántor 2019; P4 (5) routing/accessibility — Cool Routes 2026, CoolWalks 2025,
UTCI-adjusted accessibility 2026, Colaninno et al. 2025, Barcelona climate shelters
2025; P5 (2) uncertainty-aware decision support — participatory GIS 2025, Monte-Carlo
UTCI/PET 2025. Every entry is present in `PHASE5_1_LITERATURE_MATRIX.csv`; no
citation was invented and none falls outside the locked corpus. ✓

## 13. Paragraph / logic structure

Five paragraphs mapping to the five Intro-Logic steps: P1 heat as a tourism-management
problem (Step 1); P2 limits of coarse/composite assessment (Step 2); P3 physical
modelling adds different information, with the field-validation boundary preserved
(Step 3); P4 routing/accessibility boundary (Step 4); P5 gap, contribution, and RQs
(Step 5). ✓

---

## INTRODUCTION GATE

The draft reads as tourism/destination-management research from its first sentence;
the novelty boundary against routing and accessibility is explicit and hedged as
complementary/upstream without denying the adjacent literature; the thermal-method
question is framed as decision sensitivity rather than accuracy, with the
field-validation boundary preserved; the composite-index tradition is treated as
scale-and-purpose limited, not invalid; the gap is stated conservatively with the
required hedge; the contribution fits the claim ceiling as an applied, reproducible
architecture plus a case-based method-sensitivity test; no behavioural, outcome, or
superiority claim appears; no Results statistics leak; and word count and citation
count are within target with every citation traceable to the locked corpus.

**INTRODUCTION DRAFT APPROVED**
