# PROJECT CHARTER — HATI-Madrid

**Heat-Adaptive Tourism Intelligence for Madrid**
Phase 0 — Research, Data Feasibility, and Scientific Novelty Gate
Version 0.1 (Draft for gate review) · 2026-08-17

> This charter is deliberately conservative. It is written to survive an examiner and a peer reviewer, not to sound novel. Where the ambition of the original brief exceeds what the data can defend, this document narrows the claim rather than the evidence.

---

## 1. Problem

Extreme heat is now a recurring, lethal summer condition in Madrid, not an anomaly. Heat was associated with tens of thousands of excess deaths across Europe in summer 2024, and Madrid-specific work documents a long, rising temperature–mortality signal in the city. Tourism, meanwhile, concentrates visitors in exactly the times (mid-afternoon) and places (open, hard-surfaced, low-shade monumental spaces) where outdoor heat stress peaks, and visitors are a population with low local knowledge of where to find shade, water, and cool indoor refuge.

Existing tools address fragments of this. Municipal heat-health plans target residents and vulnerable groups, not visitors. Commercial routing and tourism apps optimise for distance, rating, or popularity, not thermal exposure. The recent academic wave of "heat-aware pedestrian routing" optimises a walking path but does not decide *which tourism opportunities are suitable in the first place*, does not incorporate indoor cool alternatives or cooling-resource accessibility, and rarely propagates uncertainty or labels the confidence of its own evidence.

The problem HATI-Madrid addresses is therefore narrower and more specific than "heat and tourism": **there is no transparent, reproducible, uncertainty-aware method to screen and compare tourism opportunities in Madrid by their thermal suitability and their access to adaptation resources during specific extreme-heat hours, without over-claiming about human comfort or tourist behaviour.**

## 2. Scope (what HATI-Madrid Phase 1 will do)

- Define a **spatiotemporal decision-support framework** (a method + a reproducible computational pipeline), not a product, for a bounded study area (central tourist Madrid) and a bounded period (one or more recent extreme-heat episodes in summer).
- Integrate **openly accessible** environmental, urban-form, cooling-resource, and tourism-POI data into an explicit, documented representation of *heat hazard*, *thermal exposure proxy*, and *adaptation-resource accessibility* — keeping these conceptually and computationally separate.
- Produce, for candidate tourism opportunities (both outdoor sites and indoor/shaded alternatives), a **transparent suitability screening** that says *why* an option is or is not thermally suitable at a given hour, with explicit thresholds, explicit uncertainty, and an explicit evidence-confidence label per input.
- Deliver **environmental validation** of the heat/exposure layer against independent station and, where feasible, field or literature-reported reference measurements.

## 3. Non-scope (what HATI-Madrid Phase 0/1 will NOT do)

- It will **not** claim to change, redistribute, or predict actual tourist behaviour or flows. No behavioural or mobility outcome will be asserted, because no tourist-specific intra-urban mobility data of adequate quality is accessible (see Data Inventory).
- It will **not** treat Land Surface Temperature (LST) as human thermal comfort, nor as air temperature, nor as UTCI/PET. LST is used, if at all, only as a *surface hazard/relative-exposure proxy* with stated error.
- It will **not** produce a single composite "heat-adaptive tourism score" with arbitrary weights as its primary output (see Method Options; a constraint-first design is preferred).
- It will **not** build a dashboard, production application, agent, digital twin, or LLM layer in Phase 0 or early Phase 1.
- It will **not** generate synthetic visitor data or infer tourism behaviour from environmental data.
- It will **not** claim causality without a causal design, nor treat remote sensing as ground truth.
- It will remain **independent of the SNTO codebase** during Phase 0; no SNTO code is reused or duplicated.

## 4. Intended contribution

The honest contribution is **not** a new heat metric, a new routing algorithm, or a claim about behaviour. All three are either saturated or unsupported (see Research Gap). The defensible contribution is:

1. **A constraint-first, uncertainty-aware, reproducible decision-support framework** that couples thermal-exposure proxies with tourism suitability *and* cooling-resource accessibility for a real Southern-European destination, with a documented separation between hazard, exposure, comfort, and behaviour — and with an explicit "what this cannot claim" boundary.
2. **A transferable, fully open-data feasibility template and reference implementation** for Madrid that others can reproduce and re-point to another city, including an evidence-confidence scheme that grades each input rather than hiding weak data inside a composite index.

This is an **integration, transparency, and reproducibility** contribution positioned against a fragmented literature — a realistic target for a solid applied/regional journal, not a claim of methodological breakthrough.

## 5. Unit of analysis

Primary unit: **a (tourism opportunity × time-slice) pair** — a candidate site or indoor alternative evaluated at a specific hour of a specific extreme-heat day. Supporting spatial units: the pedestrian street segment / small grid cell (for exposure) and the walkable catchment around cooling resources (for accessibility). The tourist as an individual is explicitly *not* a unit of analysis, because we have no individual-level data and make no individual behavioural claim.

## 6. Provisional research questions

- **RQ1 (descriptive/environmental):** How does modelled pedestrian-level thermal exposure vary across central Madrid's tourism spaces across the hours of an extreme-heat day, using open data, and how well does that variation validate against independent reference measurements?
- **RQ2 (methodological):** Can a *constraint-first* screening framework (explicit thresholds + Pareto-style trade-offs) classify tourism opportunities by thermal suitability and cooling-resource access more transparently and reproducibly than a weighted composite index, and with quantified sensitivity to its own assumptions?
- **RQ3 (feasibility/transferability):** Which claims does the accessible open-data landscape support and which does it forbid — i.e., where is the boundary between a defensible environmental-suitability statement and an unsupported behavioural one?

## 7. Hypotheses (only where justified)

Formal hypotheses are stated **only for RQ1**, where a testable quantity exists:

- **H1:** Modelled pedestrian thermal-exposure proxy differs significantly across tourism microsites within the study area at peak heat hours (i.e., the spatial signal is real, not noise). *Testable against independent reference data.*
- **H2:** The rank ordering of sites by suitability is materially sensitive to threshold and weighting choices under a composite-index design, and materially *less* sensitive under a constraint-first design. *Testable via sensitivity analysis.*

No hypothesis is offered for behaviour, because no confirmatory behavioural data exists. RQ2 and RQ3 are answered by demonstration and audit, not hypothesis testing — this is stated deliberately rather than dressed up as inferential science.

## 8. Expected outputs (Phase 1, subject to gate approval)

A documented, version-controlled, reproducible pipeline; a validated pedestrian heat-exposure layer for the study area and period; a constraint-first suitability classification with full sensitivity and uncertainty reporting and per-input evidence-confidence labels; and a written methods paper whose central figures are the exposure surface, the constraint-satisfaction map, and the sensitivity/uncertainty analysis. A visual prototype/dashboard is a *later* deliverable, explicitly gated behind successful environmental validation.
