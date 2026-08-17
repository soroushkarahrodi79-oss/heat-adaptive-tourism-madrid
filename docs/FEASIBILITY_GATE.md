# FEASIBILITY_GATE.md — HATI-Madrid

Phase 0 gate decision. Version 0.1 · 2026-08-17

---

## VERDICT: GO WITH MODIFICATIONS

The project is feasible, defensible, and worth doing — **but only in a substantially narrowed form**. The original concept, taken at face value ("a framework that integrates heat, environment, attractiveness, adaptation resources and accessibility to identify lower-heat tourism alternatives that redistribute tourists"), contains one fatal ambiguity and one novelty hazard:

1. **Fatal if unmodified — the behavioural claim.** There is no accessible, tourist-specific, intra-urban mobility or field-observation dataset for Madrid. Any claim that the system *identifies alternatives tourists would take*, *redistributes* visitors, or changes behaviour is unsupportable and must be cut. Population-level MITMA mobility exists but mixes residents, commuters and visitors at district scale — it cannot isolate tourists at POI scale.
2. **Novelty hazard — the routing frame.** Heat-aware pedestrian routing is a saturated 2025–2026 frontier that already includes Spanish cities (CoolWalks: Barcelona, Valencia). Framing HATI as routing would make it a late, incremental entry.

With those two modifications — **drop behaviour, move upstream from routing to constraint-first suitability screening** — the project becomes a clean, publishable, reproducible contribution. Hence GO WITH MODIFICATIONS, not GO, and certainly not STOP.

## Scores (1–10) with interpretation

For dimensions where "low is good," the favourable direction is stated so the numbers are not read backwards.

| Dimension | Score | Direction | Justification |
|---|---:|---|---|
| Scientific novelty | 4 | higher = better | Real but incremental: novelty is in the decision architecture (constraint-first + uncertainty + evidence-confidence + explicit non-claims), not in any metric, sensor, or algorithm. Routing and index framings are not novel. |
| Data feasibility | 8 | higher = better | Environmental, urban-form, canopy, POI, and cooling-resource layers are all open and accessible (AEMET, Copernicus, LiDAR, Cadastre, OSM, Madrid Open Data). Only behaviour is infeasible. |
| Methodological defensibility | 7 | higher = better | High **if** Option B (constraint-first + sensitivity + uncertainty) is used; drops to ~4 under an arbitrary-weight composite index. |
| Visual / product potential | 8 | higher = better | Exposure surfaces, constraint-satisfaction maps and trade-off sets are highly visualisable — but the dashboard is explicitly deferred behind validation. |
| Publication potential | 6 | higher = better | Solid applied/regional or urban-climate/tourism venue is realistic. Top-tier is unlikely without behavioural validation or methodological breakthrough, neither of which the data supports. |
| Implementation difficulty | 6 | lower = easier | Moderate. The hard part is defensible pedestrian Tmrt/UTCI from LiDAR+canopy via SOLWEIG and its validation; the decision logic itself is simple. |
| Dependence on unavailable proprietary data | 3 | lower = better | Low. The core is fully open; proprietary visitor-flow data is explicitly excluded, not depended upon. |
| Risk of scope creep | 8 | lower = better | High. The concept invites bolt-ons (routing, ML, behaviour, dashboard, digital twin). This is the single biggest threat to completion and must be actively policed. |

**Overall read:** strong feasibility and defensibility, modest-but-real novelty, dangerous scope-creep risk. The gate passes on condition that scope is held to the smallest publishable version below.

## Validation plan (and its hard limits)

The brief's four validation types map onto HATI as follows:

1. **Environmental validation — POSSIBLE and required.** Validate the modelled pedestrian exposure (Tmrt/UTCI) against independent AEMET station observations and, ideally, a small targeted field-measurement campaign or literature-reported reference values, following the RS-plus-field approach in the 2025 "beyond LST" work. This is the project's empirical backbone.
2. **Routing/model validation — PARTIALLY POSSIBLE, deprioritised.** Since routing is not the object, only the exposure/shade model needs validating (as above). No path-optimality validation is claimed.
3. **Tourism-relevance validation — WEAK/DESCRIPTIVE ONLY.** Tourism value is represented by static, transparent POI proxies (openness, indoor/A-C alternative, cultural significance), not by observed attractiveness. This can be face-validated and expert-reviewed, but not empirically validated against behaviour.
4. **Behavioural validation — IMPOSSIBLE with available data.** Explicitly out of scope. Stated as a limitation, not a gap to be quietly filled.

**Claims that remain permanently impossible without tourist mobility or field observation:** that the tool changes, redistributes, or predicts tourist movement; that identified alternatives are the ones tourists actually prefer or choose; that any observed change in flows is attributable to the framework. These are declared non-claims in the charter.

## Smallest publishable version (the MVP that should actually be built)

> **A reproducible, open-data, constraint-first spatiotemporal screening of thermal suitability for tourism opportunities in central Madrid, across the hours of one recent extreme-heat episode, with environmental validation and full uncertainty/evidence-confidence reporting — and no behavioural claim.**

Concretely, the minimum that constitutes a paper:

- **One bounded study area** (central monumental tourism core, e.g. the Prado–Sol–Palacio axis) and **one extreme-heat episode** (a few days), not all of Madrid and not a whole summer.
- **One validated exposure layer**: pedestrian Tmrt/UTCI from LiDAR + canopy via SOLWEIG, anchored to AEMET, cross-checked against Landsat LST, validated against reference measurements.
- **A constraint-first classification** of a modest set of outdoor sites plus indoor/cool alternatives into feasible/infeasible per hour, each exclusion carrying a reason, an uncertainty band, and an evidence-confidence grade.
- **One sensitivity analysis** showing how the feasible set moves with thresholds, and a demonstration that a weighted-index baseline is more fragile.
- **The explicit "what this cannot claim" section** as a first-class result.

Everything else — routing, itinerary optimisation, city-wide coverage, the interactive dashboard, multi-summer analysis, any ML, any behavioural inference — is **Phase 2+**, gated behind this MVP.

## Recommended next steps (pending your approval of this gate)

1. **Approve the two modifications** (drop behaviour; constraint-first, not routing) or contest them.
2. **Lock the study-area boundary and the target heat episode** — a single decision that controls scope.
3. **Run a one-week data-acquisition spike**: pull AEMET for the episode, PNOA LiDAR + Cadastre for the area, Urban Atlas canopy, OSM network/POIs, Madrid Open Data (trees, water, museums, green areas), and attempt the climate-shelter assembly — confirming each source's real usability rather than its listed existence.
4. **Stand up a minimal SOLWEIG pipeline** on the study area for two or three heat hours and sanity-check the exposure surface before committing to full modelling.
5. **Pre-register the constraints and thresholds** (from UTCI/PET literature) *before* seeing results, to keep the screening honest.
6. **Only then** write Phase 1. Do not build any dashboard until environmental validation passes.

**Phase 1 is not authorised until you explicitly approve this gate.**
