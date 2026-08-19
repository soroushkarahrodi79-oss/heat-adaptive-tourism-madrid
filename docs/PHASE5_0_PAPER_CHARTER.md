# PHASE5_0_PAPER_CHARTER.md — HATI-Madrid Phase 5.0

Version 1.0 · 2026-08-18. Locks the paper object, contribution, unit of
analysis, and claim ceiling for the A+B hybrid manuscript. Reports only locked
Phase 0–4.1 evidence; opens no gate and runs no new analysis. Wording obeys the
core-positioning constraints in the Phase 5.0 charter request and
`docs/PHASE5_0_PROXY_DEFINITION.md`.

---

## 1. Working paper object (one sentence)

The paper studies **whether the choice between a simple open-data environmental
proxy and physically based thermal-exposure modelling materially changes
heat-adaptive tourism-suitability screening decisions, and demonstrates a
transparent, uncertainty-propagating, constraint-first decision architecture
that exposes those differences and identifies feasible alternatives without
opaque composite scoring or behavioural assumptions**, on a single
extreme-heat-day pilot in central Madrid.

## 2. Primary contribution (exactly one)

> **A demonstration that thermal-*method* choice is a first-class decision
> variable in heat-adaptive tourism screening — a simple air-temperature +
> tree-count proxy and a physically based SOLWEIG/UTCI model disagree on a
> material and physically interpretable share of feasibility classifications —
> delivered through a constraint-first, uncertainty-aware decision architecture
> that makes each such difference auditable rather than hidden inside a
> composite score.**

The novelty is architectural and epistemic (constraint-first + uncertainty +
evidence-confidence + explicit non-claims, with method-sensitivity made
visible), not a new index, sensor, algorithm, or behavioural result.

## 3. Secondary contributions (max three)

1. **A constraint-first alternative to weighted composite suitability indices**
   for tourism heat-screening, with a machine-readable exclusion vocabulary and
   every exclusion traceable to one most-fundamental reason.
2. **An evidence-confidence and uncertainty-propagation scheme** that carries
   solar-forcing and geometry uncertainty into a per-row robustness class and an
   evidence gate, preserving explicit *no-recommendation* outcomes rather than
   forcing a pick.
3. **A fully reproducible, open-data reference implementation** (study-area,
   pipeline, decision fields, read-only visual prototype) that is transferable in
   principle to other destinations by re-running, not re-coding.

## 4. Non-contributions (attractive but unsupported — must be excluded)

- **No claim that SOLWEIG/UTCI is ground truth.** No field validation of
  Tmrt/UTCI exists in the project; the model is plausibility-checked only.
- **No claim the proxy is "wrong" in an accuracy sense.** Neither side is field-
  validated; the result is *divergence*, not *error*.
- **No behavioural claim** — no prediction, modelling, or assertion about tourist
  choice, flow, demand, adoption, or preference.
- **No redistribution / no improved observed tourism outcomes.**
- **No heat-aware routing novelty** — accessibility is a straight-line reach
  constraint; routing is explicitly out of scope and a saturated frontier.
- **No methodological-breakthrough claim** — this is an integration,
  transparency, and reproducibility contribution.
- **No automatic generalization** from the single Madrid pilot to other days,
  seasons, or cities.
- **No new metric, ML model, or composite score.**

## 4b. Research questions (max three; Task 3)

Each maps directly to locked evidence; no hypothesis is added beyond the
pre-registered logic (the project offered formal hypotheses only for the
environmental spatial-signal question, which is subsumed here).

- **RQ1 — Method sensitivity.** Does physically based thermal-exposure modelling
  (SOLWEIG/UTCI) materially alter tourism-feasibility classifications relative to
  the locked simple proxy baseline (air-temperature hazard × OSM tree-count),
  and is any difference physically interpretable? → C1–C4 (33.3% overall;
  64.3% at noon; both directions).
- **RQ2 — Decision-support value.** Does constraint-first heat-aware screening
  change the set of feasible tourism alternatives relative to a conventional
  nearest-open baseline, and does it decline to recommend when nothing accessible
  is materially better? → C5–C7, C10 (7/8 changed; 3/8 baseline fails; S8 none).
- **RQ3 — Robustness / traceability.** Do those decisions remain auditable and
  stable under the tested uncertainty (solar forcing, geometry, access radius)
  while preserving explicit no-recommendation outcomes? → C8–C11.

## 5. Unit of analysis

- **Study area:** Prado–Retiro–Atocha rectangular box, central Madrid, ≈ 3.5 km²
  (`data/processed/study_area.geojson`).
- **Date:** one AEMET-designated extreme-heat day, **2023-08-21** (inside the
  20–25 Aug 2023 official "episodio de calor extremo").
- **Timestamps:** three fixed local hours — **12:00 / 15:00 / 18:00** (CEST),
  air temperature 34.2 / 38.8 / 40.5 °C.
- **Assets:** 27 curated real tourism assets (13 indoor / 14 outdoor) from OSM.
- **Primary observation:** the **(tourism asset × timestamp) pair**. Thermal /
  reclassification analysis is on the **42 outdoor** pairs (14 × 3); indoor pairs
  bypass the outdoor thermal model by construction.
- **Scenarios:** **8 pre-registered decision scenarios (S1–S8)** for the
  screening layer, each a (source asset × timestamp × access radius) case with a
  nearest-open baseline comparator.

The individual tourist is explicitly **not** a unit of analysis.

## 6. Claim ceiling

**Strongest claim the evidence supports:**
On this pilot, the choice of thermal method materially and interpretably changes
tourism-feasibility classifications (33.3% of outdoor asset×timestamp rows
reclassified; 64.3% at noon, driven by air temperature understating modelled
midday radiant load), and a constraint-first architecture can expose these
differences, propagate the tested uncertainty into per-row confidence, change
the feasible-alternative set relative to a conventional nearest-open baseline
(7/8 scenarios; baseline pick fails in 3/8), and correctly return no
recommendation where nothing accessible is materially better (S8) — all with
every decision auditable and no behavioural claim.

**Strongest tempting claim the evidence does NOT support:**
That the physical model is *correct* and the proxy is *wrong* — i.e., that using
SOLWEIG/UTCI yields *more accurate* or *safer* real tourism decisions. Without
field-validated Tmrt/UTCI ground truth, the project can show the two methods
*differ* and that the difference is physically *interpretable*, but **cannot**
certify which is right, nor that adopting the model improves any real-world
outcome. The paper claims decision-relevant *sensitivity to method*, never
*validated superiority*.
