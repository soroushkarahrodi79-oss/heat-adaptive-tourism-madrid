# PHASE5_1_NOVELTY_AUDIT.md — HATI-Madrid Phase 5.1

Version 1.0 · 2026-08-18. Targeted novelty-threat audit for the A+B hybrid paper.
Based on a focused 2024–2026 literature search (logged in
`docs/PHASE5_1_LITERATURE_MATRIX.csv`). Classifies competitors, states the
routing/accessibility boundary (Task 3), and audits citation gaps (Task 9). No
new modelling; no Phase 0–4.1 output modified.

---

## 1. The contribution being defended

The exact combination claimed (from `docs/PHASE5_0_PAPER_CHARTER.md`):

> time-specific screening of **urban tourism opportunities** by **physically
> based thermal exposure (SOLWEIG/UTCI)** through a **constraint-first candidate
> filter** with **explicit uncertainty / evidence-confidence** and **surviving
> alternative identification**, benchmarked against a simple proxy and a naive
> nearest-open baseline, with **no behavioural claim** — plus the empirical
> finding that **thermal-method choice materially changes the screening
> outcome**.

No single retrieved study performs this whole combination. The audit below is
organised by how close each body of work comes.

## 2. Competitor classification

### DIRECT PRECEDENT (would invalidate the contribution)
**None found.** No retrieved study screens *tourism opportunities* by *physical
UTCI* through a *constraint-first candidate filter* with *explicit uncertainty*
and *alternative identification*. The claim survives.

### CLOSE ADJACENT (does much of the pipeline, different object or missing pieces)
- **UTCI-adjusted pedestrian accessibility** (Sustainable Cities and Society,
  2026) — defines "UTCI-adjusted reach" (how many destinations a pedestrian can
  reach under heat-stress-adjusted walking distance). Closest to HATI's
  accessibility idea, but it is an **urban-design reachability metric for a
  tropical climate**, not a tourism-opportunity *screen*; no constraint-first
  candidate filter, no evidence-confidence, no proxy-vs-physical decision
  sensitivity, no alternatives-that-survive output. Must be distinguished
  explicitly (§3).
- **Sidewalk-level urban heat-risk assessment** (Environment and Planning B,
  Colaninno et al., 2025) — couples UTCI hazard with pedestrian mobility to map
  heat risk at critical destinations. Method-adjacent, but resident/critical-
  facility oriented, risk-mapping not opportunity-screening, no uncertainty-graded
  decision fields.

### METHOD PRECEDENT (methods we build on or must distinguish from)
- **SOLWEIG** (Lindberg et al., Int J Biometeorol, 2008) and **WRF-UCM-SOLWEIG**
  city-scale thermal-comfort mapping (Sustainable Cities and Society, 2024) — the
  physical-modelling method; we *use* it, we do not claim it.
- **Tourism/Holiday Climate Index tradition** (HCI/TCI inter-comparison,
  Atmosphere 2016; reliability/usability of tourism climate indices, Earth
  Perspectives 2016; Hungarian HCI/TCI, Int J Biometeorol 2025) — the **weighted
  composite** suitability paradigm HATI is explicitly the constraint-first
  alternative to. Central contrast in Methods/Discussion.
- **GIS-MCDA with uncertainty/sensitivity** (participatory-GIS under uncertainty,
  IJGIS 2025; GIS-MCDA sensitivity mapping) and **Monte-Carlo UTCI/PET reliability**
  (Scientific Reports 2025) — the uncertainty-in-spatial-decision tradition we sit
  beside; we differ by keeping fields *separate and categorical* rather than
  propagating into one composite.
- **Heat-aware routing** — **Cool Routes** (Building and Environment, 2026),
  **CoolWalks** (Scientific Reports, 2025) — a saturated frontier we complement,
  not compete with (§3).

### CONTEXT PRECEDENT (establishes the problem, not the method)
- **Heat risk action planning for tourism** (Annals of Tourism Research, 2026) —
  governance framework to embed tourism in Heat Action Plans; qualitative,
  destination-management level; motivates our operational-screening layer, does
  not provide it.
- **Barcelona climate-shelter accessibility / mobility justice** (Cities, 2025) —
  resident-oriented cool-refuge accessibility; supports both our "proximity alone
  is insufficient" limitation and our visitor-vs-resident distinction.
- **Southern-Europe tourist heat adaptation & substitution** (Sustainability 2026;
  CaixaBank Research 2025; "extreme heat reshapes urban mobility", 2025) —
  establishes that heat reshapes tourism *in aggregate*; we make **no** such
  behavioural claim, so these bound our scope rather than threaten it.
- **Sevilla & Madrid historical-plaza thermal comfort** (Env Sci Pollut Res, 2022)
  — Madrid-specific outdoor-comfort evidence; local grounding.

### SUPPORTING ONLY (cited once, background)
- **UTCI foundations** (Bröde et al., 2012); **SOLWEIG Tmrt validation ranges**
  (Urban Climate, 2019 — RMSE ≈ 4.7 °C); **"Beyond LST" explainable ML** (2026,
  LST ≠ comfort); **tourism exposure to weather-extremes gridded dataset** (ERL,
  2024). One-line uses.

## 3. Routing boundary (Task 3) — the critical distinction

The 2025–2026 heat-mobility literature is the sharpest novelty boundary. The
distinction below **is supported by the retrieved literature**: routing papers
(Cool Routes, CoolWalks) explicitly take origin+destination as *given*, and even
the accessibility papers (UTCI-adjusted reach, RUCS) take the *destination set*
as given and measure reachability — none produces or screens the candidate set
itself.

| Dimension | THERMAL ROUTING | THERMAL ACCESSIBILITY | **HATI (this paper)** |
|---|---|---|---|
| Question | Given O and D, which *path* is coolest? | Given a destination set, how many are *reachable* under heat? | **Which tourism opportunities should stay in the feasible candidate set at this hour, why, with what confidence, and what alternatives survive?** |
| Input assumed given | origin + destination | destination set | **nothing downstream — HATI produces the candidate set** |
| Core operation | least-thermal-cost path | heat-adjusted reach count | **constraint-first elimination + alternative identification** |
| Thermal role | path cost | distance penalty | **hard feasibility gate (physical UTCI)** |
| Uncertainty | rarely explicit | rarely explicit | **first-class per-row confidence + evidence gate** |
| Tourism role | none/agnostic | destinations agnostic | **curated tourism opportunities + experience type** |
| Output | a route | a reachability score | **a screened, traceable alternative set (or explicit none)** |
| Exemplars | Cool Routes 2026; CoolWalks 2025 | UTCI-adjusted reach 2026; RUCS | — |

**Positioning sentence:** routing and accessibility both operate *downstream of*
destination/candidate selection; HATI operates *upstream*, producing and
screening the candidate set that those methods presuppose. This is the single
most important boundary the manuscript must assert (and cite) in §2.

## 4. What remains novel (stated conservatively)

Even granting every adjacent work its full due, three things are not occupied:
1. **Tourism-opportunity screening as the object** (not routing, not reachability,
   not risk mapping) under explicit physical-thermal + evidence constraints.
2. **Thermal-method choice as a demonstrated decision variable** — the
   proxy-vs-physical reclassification result (33.3%; 64.3% at noon) is, in the
   retrieved literature, not something anyone has quantified *for tourism
   screening decisions*.
3. **Constraint-first + categorical uncertainty + explicit no-recommendation**,
   as an alternative to the weighted composite tourism-climate-index tradition.

If a reviewer produces a study combining all of items 1–3, the contribution
collapses to "a Madrid replication." No such study was found.

## 5. Citation-gap audit (Task 9)

Cross-checked against `docs/PHASE5_0_PAPER_CHARTER.md` and
`docs/PHASE5_0_MANUSCRIPT_ARCHITECTURE.md`.

**MUST ADD BEFORE DRAFTING**
- The **routing/accessibility boundary set** — Cool Routes (2026), CoolWalks
  (2025), UTCI-adjusted pedestrian accessibility (2026). Without these the R4
  "just another routing paper" attack is unanswered.
- The **composite tourism-climate-index tradition** — HCI/TCI inter-comparison +
  a tourism-climate-index reliability critique. Without these the constraint-first
  contribution has nothing to contrast against.
- The **tourism heat-governance context** — heat risk action planning for tourism
  (Annals of Tourism Research, 2026). Establishes the management gap HATI serves.
- **SOLWEIG Tmrt validation-range reference** (Urban Climate, 2019 or equivalent)
  — directly resolves the known Madrid/Mediterranean plausibility-range gap
  (below).

**USEFUL**
- Barcelona climate-shelter accessibility (2025); Southern-Europe adaptation/
  substitution (2026); Sevilla–Madrid plaza comfort (2022); Monte-Carlo UTCI/PET
  reliability (2025); "Beyond LST" (2026).

**OPTIONAL**
- OECD Tourism Trends 2026; ERL tourism-exposure gridded dataset (2024);
  hyperlocal POI activity under heat (2026 preprint).

**UNNECESSARY**
- ML/deep-learning UTCI prediction (e.g., GSM-UTCI) — cite at most once to say why
  ML is deliberately out of scope; otherwise excluded (charter forbids ML).
- General smart-tourism / digital-twin literature — out of scope, do not cite.

**Explicit check — Madrid/Southern-European Tmrt/UTCI plausibility-range gap
(flagged in `docs/PHASE2_VALIDATION_REPORT.md` §3):** the project could not, at
Phase 2, cite a city-specific Madrid Tmrt comparison figure. The literature
search **partially closes** this: SOLWEIG Tmrt-validation studies report RMSE
≈ 3.5–5.7 °C and sunlit urban Tmrt in the 60–70+ °C range for comparable
Mediterranean/warm climates (Urban Climate 2019; SOLWEIG 1.0 2008). This is
sufficient to support a *plausibility* statement ("modelled ranges are consistent
with published SOLWEIG-class values") — **not** a validation claim. It does
**not** require any new modelling. Gap status: **resolvable by citation; not a
blocker.**

**Conclusion:** no citation gap blocks drafting once the four MUST-ADD clusters
are in the reference list — all are now identified in
`docs/PHASE5_1_LITERATURE_MATRIX.csv`.
