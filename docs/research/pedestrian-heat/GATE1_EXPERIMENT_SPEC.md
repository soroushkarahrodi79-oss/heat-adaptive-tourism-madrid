# GATE1_EXPERIMENT_SPEC — Minimal comparison / perturbation experiment (partially frozen)

**Version 0.3 · 2026-09-14. Status: PARTIALLY FROZEN specification of a FUTURE experiment.
NOT executed. See the explicit freeze boundary in §1.**

> **Revised 2026-09-14 (evidence correction + pre-merge consistency pass):** E-P1 constant-offset
> deleted (empirical-hourly or ABSTAIN); geometry now distinguishes *normalized surface height*
> (MDS 2023 − MDT 2019) from *building* and *canopy* height, which require an explicit,
> still-OPEN classification/mask step (§1, §3); the ∫UTCI dt single scalar is **removed** in
> favour of a transparent multi-metric description (§1.2); E-P3 wind is **demoted** from a frozen
> perturbation to an unresolved limitation / ABSTAIN trigger (§3); and a real FROZEN-vs-OPEN
> boundary is drawn (§1). See `GATE1_FEASIBILITY_DOSSIER.md` §GATE1_EVIDENCE_CORRECTION_2026-09-14.

> This is a pre-registration-style record written **before** any thermal output exists, so that
> route pair, day, metrics, perturbation ranges, and decision rules cannot be chosen after
> seeing results. Only the elements marked FROZEN below are locked; elements marked **OPEN** are
> explicitly not yet fixed and MUST be frozen (and hashed where applicable) before the first
> thermal output. Changing a FROZEN element, or freezing an OPEN one in a way that departs from
> these rules, requires an `AMENDMENT_00x.md`. No SOLWEIG/URock/UTCI is run in this document.

---

## 1. Freeze boundary

### 1.1 FROZEN now (locked; change requires an amendment)

| Element | Frozen value |
|---|---|
| **Research object** | Decision reliability / evidence sufficiency / uncertainty / abstention for *modeled* comparative pedestrian thermal exposure (Gate-0). |
| **O-D case** | OD1: Atocha (A09, 40.404557, −3.688683) → Puerta de Alcalá (A14, 40.419987, −3.688724). |
| **Two corridors (identity, not exact geometry)** | Alt A = Paseo del Prado / Recoletos monumental axis (open, low continuous canopy). Alt B = Real Jardín Botánico / Retiro western edge + Calle Alfonso XII (tree-lined). |
| **Claim ceiling** | Path B — robustness / sensitivity / decision-reversal / evidence sufficiency of *modeled* comparative exposure. No accuracy/comfort/behaviour/health claim. |
| **Selection rules** | O-D criteria (§1A) and study-day rules R1–R7 (§1B), fixed before any outcome inspection. |
| **Abstention logic** | ROBUST / NO ROBUST DIFFERENCE / ABSTAIN framework (§4) and negative controls NC1–NC7 (§5). |
| **Perturbation *dimensions*** | The *which* — forcing (E-P1), canopy (E-P2), building/shadow (E-P4), network/side-of-street (E-P5), walking speed (E-P6). (E-P3 wind is demoted — §3.) The *parameter values* are OPEN until justified. |

### 1.2 OPEN — MUST BE FROZEN (and hashed where applicable) BEFORE FIRST THERMAL OUTPUT

| Element | Why still open | How it will be frozen |
|---|---|---|
| **Study day** | Needs R1–R7 confirmation via small AEMET + municipal metadata queries. | Prefer a fresh 2023/2024 AEMET heat-warning day (≠ 21 Aug 2023); 2021-08-14 = PNOA-vintage alternative; 2023-08-21 = legacy stress-test only. |
| **Target hours** | Depend on confirmed clear-sky daylight envelope for the chosen day. | A small fixed set (e.g. one near solar noon + one late-afternoon), fixed before running. |
| **Route A polyline / Route B polyline** | L05 network not yet acquired. | Bounded Overpass fetch for the two corridors; frozen + hashed as versioned GeoJSON (EPSG:25830). |
| **Network / access audit** | L06 not done. | Manual walkability + crossing/gate audit; unresolved access → ABSTAIN control. |
| **Meteorological forcing source** | Barajas vs a municipal full-met station not yet chosen. | Fixed to one series, held identical across both routes. |
| **Independent urban check** | File-level coverage of Escuelas Aguirre for the chosen day/hours unconfirmed. | Escuelas Aguirre hourly Ta/RH (different series from forcing); if missing → E-P1 ABSTAIN. |
| **Building classification strategy** | MDS 2023 − MDT 2019 is *normalized surface height*, not a building raster; the footprint/classification source is not yet audited. | Classify normalized surface height to buildings using an independently auditable building-footprint source (candidate: Catastro; to be audited) — OPEN (see L15/L17). |
| **Vegetation / canopy strategy** | MDS-derived height is not canopy height without a vegetation mask; the mask source is not yet justified. | Independently justified vegetation/tree mask before MDS height is read as canopy height; bound via E-P2 states — OPEN (see L04/L16/L17). |
| **Justified perturbation *definitions*** | Parameter values/ranges must have a data or literature basis. | Freeze each E-P range from provenance/literature; anything unjustified is dropped, not invented. |
| **Outcome metrics** | Finalised metric set per §1.3 (no bespoke scalar). | Freeze the multi-metric set and the exact UTCI category boundaries before any thermal output. |

### 1.3 Outcome metrics (revised 2026-09-14 — ∫UTCI dt removed)

The raw cumulative integral **∫ UTCI dt is removed** as the (sole) primary statistic: no
published method was identified (Gate-1 targeted search) that validates integrating an
equivalent-temperature stress index through time into a physiological/generic "dose" for a
comparative route decision, and the claim ceiling forbids a physiological-dose reading. The
route comparison is instead described by a transparent, pre-declared **multi-metric** set,
each reported with its modeled-uncertainty interval:

1. **Trip duration** (per walking-speed alternative).
2. **Time-weighted mean modeled UTCI** along the route.
3. **Along-route distribution / range** of modeled UTCI (e.g. IQR, min–max).
4. **Minutes and proportion of the trip within each pre-declared standard UTCI stress
   category** (the categorical, boundary-meaningful metric).
5. **Maximum / high-percentile modeled UTCI** — reported only as a descriptor, used in the
   decision **only if** a specific method justifies it before results.

No metric is labelled "heat dose" or "physiological dose". If different legitimate metrics
disagree on route ordering, that disagreement **supports ABSTAIN / NO ROBUST DIFFERENCE**, it
is not reconciled into one number. Sampling uses the buffer-mean (not raw centroid) per the
locked pilot's own validated choice.

## 2. Preconditions that MUST be satisfied before any thermal run (from Gate 1)

- **P-A:** L05 pedestrian network acquired for the two routes via a bounded Overpass query
  (two corridors only — not city-wide) and stored as versioned GeoJSON in EPSG:25830.
- **P-B:** L06 access/crossing audit: both routes verified legally + physically walkable
  end-to-end on the study day; every controlled crossing and park gate (with opening hours)
  recorded. Any unresolved access → the case moves to an ABSTAIN negative control, not a run.
- **P-C:** Study day frozen on R1–R7; forcing (Barajas or a municipal met station) and the
  independent **urban** check (Escuelas Aguirre hourly Ta/RH) are **different** series.
- **P-D:** Both route polylines frozen and hashed before any UTCI field is generated.
- **P-E (added 2026-09-14; revised — MDS semantics):** Geometry evidence architecture, obtained
  by **bounded bbox clip to OD1 only** (not a city-wide raster download):
  - **Terrain** = Madrid MDT 2019 (subject to provenance/compatibility checks).
  - **Normalized surface height** = MDS 2023 − MDT 2019 — a top-of-everything surface field,
    **not** by itself a building or canopy raster.
  - **Building height** = normalized surface height classified with an **independently auditable
    building-footprint source** — this classification source is **OPEN** (candidate: Catastro,
    to be audited; L15/L17).
  - **Vegetation/canopy height** = normalized surface height only where an **independently
    justified vegetation/tree mask** says vegetation — the mask is **OPEN** (L04/L16/L17).
  - **PNOA 2008–2015** retained as an independent cross-vintage geometry sensitivity source.
  Classification of buildings and vegetation is a **Gate-2 precondition**, not assumed here.

## 3. Perturbation dimensions (dimensions FROZEN; exact parameter values OPEN — §1.2)

The *dimensions* below are frozen. The exact parameter **values/ranges** are OPEN until each is
justified from data provenance or literature (per §1.2) and frozen before the first thermal
output; anything that cannot be justified is dropped, **never invented**. Each dimension is
included **only** because it can change the *decision*.

| Dim | Perturbation | Intended (to-be-frozen) alternatives | Justification of the range |
|---|---|---|---|
| E-P1 (revised 2026-09-14) | Forcing representativeness | (a) Barajas as-is; (b) an **empirical hourly** Escuelas-Aguirre-minus-Barajas Ta/RH difference at the target hours. **If** the urban station is incomplete for the chosen day/hours → forcing uncertainty is an **ABSTAIN** condition. | Airport-vs-centre bias measured hourly from a real corridor-adjacent station. **The former +0.5 °C daily-max constant offset is DELETED** — a daily-max gap does not license a constant hourly offset. |
| E-P2 (revised 2026-09-14) | **Canopy geometry** | (a) PNOA veg nDSM (2008–2015); (b) MDS 2023 **normalized surface height masked to vegetation** (mask OPEN — L17); (c) **municipal tree-inventory** presence/removal audit; (d) Copernicus TCD 2018 density. | Four *real, independent* canopy states bound the change; note (b) is only canopy *after* an audited vegetation mask, not before. |
| ~~E-P3~~ (DEMOTED 2026-09-14) | Wind treatment | **Removed from the frozen perturbation set.** No specific published canyon-multiplier method/parameterisation was identified for this context, so no multiplier is invented. Spatial wind heterogeneity is kept as an **unresolved limitation / possible ABSTAIN trigger** (uniform station wind is the only justified treatment now). | A physically based wind treatment is deferred to Gate 2 **only if** wind is shown decision-critical AND suitable inputs/evaluation exist — never URock added merely to rescue this. Complexity is not evidence. |
| E-P4 (revised 2026-09-14 — MDS semantics) | Building/shadow geometry | (a) MDS 2023 − MDT 2019 **normalized surface height classified to buildings via an audited footprint source** (classification OPEN — L17); (b) PNOA 2008–2015 building nDSM as an independent cross-vintage check. | Raw MDS − MDT is *surface* height, not a building raster; buildings require classification. PNOA tests geometry-source/vintage sensitivity. IGN 2nd-coverage pull only if (a)/(b) still leave the pair fragile. |
| E-P5 | Network / side-of-street | Two audited traces where sidewalk side is ambiguous (side A vs side B). | Side-of-street changes sun/shade exposure along the identical corridor. |
| E-P6 | Walking speed / pauses | 1.1 m/s vs 1.4 m/s; optional endpoint pause. | Standard pedestrian speed range; changes trip duration and the time-weighted / in-category metrics (§1.3) and can reorder near-ties. |

**Explicitly excluded** (would violate scope or add complexity without changing the
decision): CFD/URock wind fields, city-wide modelling, future-climate scenarios, land-cover
refinement (unless a route crosses a strongly contrasting surface, per L12), any ML.

## 4. Decision rule (frozen — no invented threshold)

Framed on decision stability (pairwise rank-reversal robustness), **not** a fixed °C cut, and
evaluated **per metric** across the §1.3 set. UTCI category boundaries are applied **only** to
the category-meaningful metrics (time-weighted mean UTCI and minutes/proportion-in-category),
**never** to an integrated ∫UTCI dt value (removed):

- **ROBUST COMPARISON** — the sign of the Alt A − Alt B difference agrees across the §1.3
  metrics AND is preserved across **all** justified perturbations (E-P1, E-P2, E-P4, E-P5,
  E-P6) AND the category-based metrics sit clear of a UTCI category boundary.
- **NO ROBUST DIFFERENCE** — routes indistinguishable, or sign stable but magnitude inside the
  modeled uncertainty interval, or **legitimate metrics disagree on ordering**.
- **ABSTAIN / NO EVIDENCE** — the sign **reverses** under ≥1 justified perturbation, OR an
  essential input is MISSING (L05/L06) or its classification is unresolved (L17), OR a
  category-based metric straddles a UTCI category boundary, OR spatial wind is shown
  decision-critical while unresolved (demoted E-P3), OR the uncertainty interval spans the
  decision.

A "material difference" threshold will be adopted **only** if the Gate-2 literature update
finds a defensible, comparison-specific value; otherwise the stability formulation above
governs. (Gate 1 found none — see `GATE1_LITERATURE_LOG.md`.)

## 5. Negative controls that MUST return ABSTAIN

NC1–NC7 (`GATE1_FEASIBILITY_DOSSIER.md` §1F) are run alongside OD1. If the method confidently
resolves any negative control, the evidence-sufficiency logic has failed and the method — not
the control — is rejected.

## 6. What this experiment will and will not output

- **Will:** a ROBUST / NO-ROBUST-DIFFERENCE / ABSTAIN label for OD1 with its perturbation
  audit trail; negative-control behaviour; an explicit statement of the vintage each result
  rests on.
- **Will NOT:** a validated UTCI accuracy figure, a comfort/behaviour/health claim, a
  recommender, a dashboard, a city-wide map, or a route "recommendation" derived from thermal
  output.
