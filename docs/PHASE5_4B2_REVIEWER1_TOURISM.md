# PHASE5_4B2_REVIEWER1_TOURISM.md — Reviewer 1 (Tourism / Destination Management)

Adversarial review of `manuscript/MANUSCRIPT_TMP_v0.2.md` for *Tourism Management
Perspectives*. I judge the manuscript that exists, not the effort behind it.

## Overall verdict: MAJOR REVISION (borderline reject on fit)

The paper is timely and honest, but as written it reads as an **urban-environmental
decision-support method demonstrated on tourism assets**, not as a tourism-management
contribution. The tourism content is in the *application layer* (curated attractions,
opening hours, experience types); the *contribution* — thermal-method sensitivity + a
constraint-first filter — is domain-agnostic. For a TMP readership that expects a
management insight, the "so what for a destination manager?" is underdeveloped.

## Top 3 criticisms

**1. The management contribution is thin relative to the machinery. [MAJOR]**
- *Evidence:* §4.5 states the contribution as "an applied decision-support contribution
  rather than a new metric or algorithm," and the four "distinct inputs" it keeps visible
  are all technical fields (thermal state, constraints, evidence, uncertainty). The
  Discussion engages tourism *governance* (Scott, 2026) and *refuge equity* (Mombelli et
  al., 2025) only lightly, and offers no destination-management theory, no visitor-experience
  framing, and no concrete managerial action beyond "screen options."
- *Required action:* reframe the Introduction and Discussion around a management decision a
  DMO/operator actually faces (e.g., which attractions to flag/deprioritise at 12:00 vs
  18:00, and how to justify it), using existing scenarios. No new data.
- *Not:* a demand study, a visitor survey, or behavioural data (scope creep).

**2. "Tourism opportunity screening" risks being accessibility/constraint filtering
renamed. [MAJOR]**
- *Evidence:* the screen's tourism-specific gates are "open at timestamp" and asset
  curation; the thermal and accessibility gates are generic. RQ2's comparator is a
  proximity tool. A skeptical reader sees a spatial constraint filter with a tourism label.
- *Required action:* make the tourism decision *stage* explicit and defend why it is
  distinct from routing/accessibility for a manager (the manuscript already argues this in
  §4.2 — surface it earlier and tie it to a management workflow).

**3. The empirical base is one city, one day, 27 hand-curated assets. [MAJOR — but bounded]**
- *Evidence:* §2.1, §5.2. The 27 assets are "purposively selected"; no representativeness
  is claimed (good), but a TMP reviewer will ask what a single extreme afternoon in one
  3.5 km² box tells destination management generally.
- *Required action:* this is honestly disclosed; keep it, but strengthen the "why a bounded
  pilot is the right first step" argument and the transferable-architecture framing. Do NOT
  add a second city (scope creep / not required to avoid a fatal flaw).

## Answers to the reviewer questions

1. *Tourism paper or urban-climate model with labels?* Currently closer to the latter in
   emphasis; fixable by reframing (MAJOR).
2. *Insight beyond "heat matters"?* Yes but narrow: "the thermal method you pick changes
   which attractions you'd flag." That is a real, non-obvious operational point — it just
   is not developed into management guidance.
3. *Meaningful decision stage or accessibility renamed?* A genuine upstream stage exists
   (candidate eligibility before routing), but the manuscript under-sells it for managers.
4. *Assets justified?* Adequately (OSM tourism/heritage tags, Wikidata for 24/27), but
   small; the curation is manual and not scalable as presented.
5. *Nearest-open a credible comparator?* Weak (see Reviewer 3 / Critical Attack 2). It is a
   straw man; the interesting result is the auditable removal, not "we differ from
   proximity."
6. *Is NO_DEFENSIBLE_ALTERNATIVE managerially meaningful?* Partly — "the tool can decline"
   is a nice property, but as delivered it is a property of hard constraints under a
   hand-picked 500 m radius (S8), not a demonstrated management need.
7. *General enough for TMP despite one day/city?* Marginal.
8. *Too much architecture, too little management?* Yes — the central weakness for TMP.
9. *Discussion connects to tourism adaptation literature?* Lightly; more integration with
   destination-management/adaptation work would help (using already-cited sources).
10. *Recommendation:* **major revision**; a stricter colleague would reject on fit.

## Requests I would REFUSE as scope creep
- A tourist survey, revealed/stated-preference validation, or demand modelling.
- A second city or additional heatwave.
- Any behavioural-outcome claim.
