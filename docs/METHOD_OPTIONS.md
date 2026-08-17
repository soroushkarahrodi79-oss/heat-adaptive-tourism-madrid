# METHOD_OPTIONS.md — HATI-Madrid

Comparison of three methodological architectures. Version 0.1 · 2026-08-17

The recommendation was held open until the evidence was gathered. The evidence has now landed. This document compares three realistic designs on eight dimensions and recommends one, with reasons a reviewer would accept.

A shared foundation applies to all three options and is not itself a differentiator: pedestrian-scale thermal exposure is estimated from open geometry (Spanish Cadastre + PNOA LiDAR building/tree heights) and canopy (Urban Atlas Street Tree Layer / HRL Tree Cover Density / local arbolado) via an open radiation model (SOLWEIG for mean radiant temperature and UTCI), driven and anchored by AEMET station observations, with Landsat LST used only as a coarse surface-hazard cross-check. All options separate hazard, exposure, comfort, accessibility, and tourism value as distinct layers. What differs is **how those layers are combined into a decision**.

---

## Option A — Weighted composite "Heat-Adaptive Tourism Suitability Index" (MCDA)

Each site-hour receives a single score by normalising and weighting the layers (exposure, shade, water/shelter proximity, POI value, accessibility) and summing them, typically with AHP- or expert-derived weights.

- **Scientific strength:** Low–moderate. Familiar and easy to communicate, but the central number conflates a *hazard* with a *value*, and the ranking is known to be sensitive to weights that have no ground-truth. The composite-indicator literature (Ecological Indicators 2017; JRSS-A 2008) shows nominal weights rarely equal real importance.
- **Data requirements:** Moderate; all layers, plus a defensible weighting procedure (which is itself contestable).
- **Implementation complexity:** Low. This is the fastest to build.
- **Validation requirements:** Heavy *if done honestly* — mandatory uncertainty and sensitivity analysis on weights and normalisation, or the result is indefensible.
- **Novelty:** Low. "Another weighted tourism-suitability index" is exactly the framing a reviewer rejects.
- **Reproducibility:** High mechanically, but low epistemically — reproducing an arbitrary choice is not the same as justifying it.
- **Risk:** High. Invites the "arbitrary weights" and "you conflated comfort with value" critiques; explicitly cautioned against in the project brief.
- **Publication potential:** Low as a stand-alone claim.

## Option B — Constraint-first / threshold-based screening with Pareto trade-off surfacing (RECOMMENDED)

No single score. Instead, each site-hour is first tested against **explicit, separately-justified constraints** (e.g., modelled UTCI below a stated thermal-stress threshold; a cool alternative within a stated walking time; operating hours cover the time-slice). Options that pass are *feasible*; those that fail are excluded *with a stated reason*. Among feasible options, remaining objectives (lower exposure, higher tourism value, shorter access to cooling) are presented as a **Pareto trade-off set**, not collapsed into one number. Every input carries an uncertainty band and an evidence-confidence grade.

- **Scientific strength:** High. Keeps hazard/comfort/value separate; decisions are auditable ("excluded because UTCI > threshold at 16:00, confidence medium"); no hidden weighting. Thresholds are contestable but *explicit and testable*, which is the point.
- **Data requirements:** Same layers as A, plus defensible thresholds (from biometeorological literature) and uncertainty characterisation.
- **Implementation complexity:** Moderate. Constraint logic is simple; the Pareto step and uncertainty propagation add work.
- **Validation requirements:** Environmental validation of the exposure layer (vs AEMET/field) + sensitivity of the feasible set to threshold choices. Tractable and honest.
- **Novelty:** Moderate and *real* — the contribution is the decision architecture and epistemic transparency, not a metric. It sidesteps the saturated routing frontier by acting upstream (which options are candidates) rather than downstream (best path).
- **Reproducibility:** High, mechanically and epistemically — thresholds and confidence grades are stated and can be varied.
- **Risk:** Moderate. Main risk is threshold justification, which is manageable by citing established UTCI/PET thresholds and reporting sensitivity.
- **Publication potential:** Good for a solid applied/regional or urban-climate/tourism venue, precisely because it is defensible rather than flashy.

## Option C — Multi-objective network optimisation / heat-aware routing (with optional ML)

Model the pedestrian network and solve for thermally-optimal routes or itineraries across POIs, optionally learning exposure or preferences from data.

- **Scientific strength:** Moderate in principle, but **the frontier is saturated** (CoolWalks 2025 on Barcelona/Valencia; Transactions in GIS 2025; CEUS 2025; Building and Environment 2026). A Madrid entry would be incremental.
- **Data requirements:** High — good sidewalk network, reliable heights, and, for any ML, a supervised target with ground truth that HATI does not have.
- **Implementation complexity:** High.
- **Validation requirements:** Very high; routing/model validation plus, for ML, labelled data that does not exist here. Introducing ML without a defined prediction task and validation labels is excluded by the brief and would be method theatre.
- **Novelty:** Low-to-none as routing; the novel behavioural version needs mobility data HATI cannot access.
- **Reproducibility:** Moderate; ML components reduce transparency.
- **Risk:** High — direct collision with recent published work and with the no-behavioural-claim and no-ML constraints.
- **Publication potential:** Low unless it does something the frontier has not, which the available data does not enable.

---

## Comparison summary (qualitative, 1 = weak, 5 = strong for the project's goals)

| Dimension | A: Weighted index | B: Constraint-first (Pareto) | C: Routing/ML |
|---|---|---|---|
| Scientific strength | 2 | 4 | 2 |
| Data requirements (fit to available data) | 4 | 4 | 2 |
| Implementation simplicity | 5 | 3 | 2 |
| Validation tractability | 2 | 4 | 1 |
| Novelty (defensible) | 1 | 3 | 1 |
| Reproducibility (epistemic) | 2 | 5 | 3 |
| Risk control | 2 | 4 | 1 |
| Publication potential | 2 | 4 | 2 |

## Recommendation

**Adopt Option B — a constraint-first, threshold-based screening with Pareto trade-off surfacing, full uncertainty propagation, and per-input evidence-confidence grading.** It is the only option that is simultaneously (a) supportable by the accessible open data, (b) defensible against the "arbitrary weights" and "conflation" critiques, (c) clear of the saturated routing frontier, and (d) honest about behaviour. Option A may be retained *only* as a deliberately-labelled baseline whose weight-sensitivity is demonstrated in order to motivate B; it must never be the headline result. Option C is out of scope for Phase 1 and would only be reconsidered if genuine tourist-mobility data ever became accessible — which the inventory says it is not.
