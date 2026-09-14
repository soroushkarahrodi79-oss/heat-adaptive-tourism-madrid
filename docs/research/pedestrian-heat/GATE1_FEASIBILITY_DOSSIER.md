# GATE1_FEASIBILITY_DOSSIER — Pedestrian Heat-Exposure Decision-Reliability Extension

**Gate 1 — bounded feasibility study. Version 0.1 · 2026-09-14.**
**Verdict (full justification in `GATE1_DECISION.md`): MODIFY.**

> **Scope guard.** This document does *not* run SOLWEIG/URock, does *not* compute UTCI,
> does *not* build a recommender/dashboard, does *not* optimise routes on thermal results,
> and does *not* download large raster/LiDAR/remote-sensing datasets. It answers exactly
> one question: *can we assemble ONE pre-specified pedestrian route comparison in the
> Atocha–Prado–Retiro corridor with sufficiently auditable open data to justify a later
> robustness / abstention experiment?*

---

## GATE1_EVIDENCE_CORRECTION_2026-09-14

An adversarial evidence-correction pass verified three municipal open-data sources against
authoritative Ayuntamiento de Madrid / datos.madrid.es / geoportal.madrid.es descriptions.
Several Gate-1 statements were wrong, incomplete, or overclaimed and are corrected below.
This pass ran **before** any thermal output and changes no Gate-0 decision.

**What previous statements were wrong or incomplete**

1. **"NO hourly in-city observation is obtainable" (L02, §0 table, §1C) — FALSE / OBSOLETE.**
   Madrid publishes *Datos meteorológicos. Datos horarios desde 2019* (municipal network,
   operational since 2018; hourly by year). **Escuelas Aguirre** — an urban air-quality
   station on Calle de Alcalá at O'Donnell, only a few hundred metres from OD1's Puerta de
   Alcalá destination — reports at least hourly **air temperature and relative humidity**.
   An independent *urban* hourly Ta/RH check adjacent to OD1 therefore exists.
2. **E-P1's "+0.5 °C Retiro daily-max offset applied to the diurnal cycle" — STATISTICALLY
   UNJUSTIFIED and removed.** A daily-*maximum* difference does not license a constant hourly
   offset across the whole diurnal curve. It is replaced by an *empirical hourly*
   urban-minus-Barajas difference (now computable from Escuelas Aguirre) or, where that
   station is incomplete for the chosen day/hours, forcing uncertainty becomes an ABSTAIN
   condition — never an invented offset.
3. **Geometry over-reliance on PNOA 2008–2015 (L03/L04) — improvable.** Madrid **MDS 2023**
   (2023 aerial survey, ~100 pts/m², 10 cm tiles / 1 m COG) and municipal **MDT 2019** give a
   near-contemporaneous surface/terrain pair for a 2023+ study day, materially better than
   the 2008–2015 vintage for buildings/terrain.
4. **Path A "no pedestrian-level measurements exist and none is obtainable" (§1D) —
   OVERCLAIMED.** Impossibility was not demonstrated. Corrected to *NOT CURRENTLY AVAILABLE*:
   "no suitable independent pedestrian-level Tmrt/UTCI measurements have yet been identified
   for this corridor/date."

**Authoritative evidence used (verified 2026-09-14)**

- datos.madrid.es dataset 300352 *Datos meteorológicos. Datos horarios desde 2019*; municipal
  meteorology network description (airedemadrid.madrid.es *Red de meteorología*): the **six**
  full stations (Moratalaz, Villaverde, Hortaleza, Z.I. Fuencarral, EDAR La China, Centro
  Municipal de Acústica) measure wind, Ta, RH, pressure, **solar radiation**, precipitation;
  air-quality stations (e.g. Escuelas Aguirre, JMD Centro) report a **subset** — Ta/RH — and
  Escuelas Aguirre does **not** register wind.
- geoportal.madrid.es *Modelo digital de superficies (MDS) 2023* and *MDS 2019 / MDT 2019*.
- datos.madrid.es dataset 300761 *Arbolado en parques y zonas verdes de Madrid (detalle)* —
  individually inventoried municipal trees (location + height attribute), 2025/2026 releases.

**What changed**

- L02 rewritten: hourly urban Ta/RH check now AVAILABLE near OD1; roles separated into
  MODEL FORCING / INDEPENDENT URBAN CHECK / REGIONAL CONTEXT.
- E-P1 rewritten (empirical-hourly or ABSTAIN; the +0.5 °C offset is deleted).
- L03/L04 rewritten to a hybrid architecture (MDT 2019 terrain · MDS 2023 surface/building ·
  MDS 2023 + tree-inventory canopy audit · PNOA retained as cross-check/fallback); new ledger
  rows L15 (MDS 2023 / MDT 2019) and L16 (tree inventory).
- §1D Path A downgraded from "impossible" to "not currently available."
- §1B study-day protocol gains a geometry-alignment rule and now **prefers a fresh 2023/2024
  heat day**; 2021-08-14 is demoted (it predates MDS 2023).

**What did NOT change**

- The **MODIFY** verdict (justification refined in `GATE1_DECISION.md`).
- Path B remains the operative claim ceiling (robustness / sensitivity / abstention).
- **L05/L06 remain MISSING** — the pedestrian network and access/crossing audit are still the
  binding precondition; nothing here fetches a network.
- **Corridor-local wind and solar radiation remain NOT locally observed** — only the six
  peripheral met stations measure them; GHI at OD1 stays modeled (clear-sky).
- Gate-0 protocol (`RESEARCH_PROTOCOL_V0.1.md`) — no amendment required.
- Literature log — unaffected (this pass concerns data provenance, not novelty).
- 2023-08-21 stays prohibited as independent validation of the locked HATI output.

**Is the MODIFY verdict still justified?** Yes. The two GO-blockers are unchanged: pedestrian
validation is still unavailable (Path B), and the routes are still not auditable (L05/L06).
The correction *strengthens* the feasibility case (a real urban hourly check; better geometry
vintage) but removes neither blocker, so the verdict remains **MODIFY** — now a stronger
MODIFY whose primary residual barrier to GO is Path B, not the independent check.

---

## 0. Repository forensics (what HATI has, and has NOT, established)

The extension inherits a mature, `RELEASE_LOCKED`, publicly-archived project. The single
most important forensic discipline here is separating *implemented / modeled* from
*independently validated*. The repository is unusually honest about this itself; the table
below is a compression of `PROJECT_STATUS.md`, `docs/PHASE2_VALIDATION_REPORT.md`,
`docs/PHASE1_2_TEMPORAL_ALIGNMENT.md`, `docs/PHASE1_1_SENSITIVITY_REPORT.md` and
`docs/RESEARCH_GAP.md`.

| Claim class | What is actually true in-repo |
|---|---|
| **Implemented / reproducible** | Operational-proxy classification (AEMET hazard bands + OSM tree-count exposure); constraint-first screening logic; the 33.3% proxy-vs-physical reclassification count; 8 decision scenarios; read-only replay app. |
| **Modeled (only)** | SOLWEIG Tmrt and the UTCI derived from it — for 21 Aug 2023, 3 timestamps (12/15/18). |
| **Independently validated** | **Nothing thermal.** No field Tmrt/UTCI measurement (globe thermometer, 6-directional radiometer, or any in-situ reading) exists anywhere in the project. AEMET validates *forcing inputs* (Ta/RH/wind/pressure) only — it cannot validate the radiant field. |
| **Independent check available** | **Corrected 2026-09-14.** An independent *urban hourly* Ta/RH check adjacent to OD1 **does** exist (Escuelas Aguirre, municipal *Datos horarios desde 2019*). Retiro official daily-max/monthly-mean remain a coarse cross-check. **Corridor-local wind and solar radiation are still not observed** (only six peripheral met stations measure them). Phase 1.1's "no hourly in-city" finding concerned AEMET Retiro specifically and is superseded for the municipal network. |
| **Geometry vintage** | PNOA-LiDAR **1st coverage ~2008–2015**. Canopy geometry is repeatedly flagged as the single largest, direction-changing uncertainty. No geolocated 2023 tree inventory exists. |
| **Solar forcing** | Modeled (pvlib Ineichen clear-sky), not measured. |
| **Published** | Preprint on Zenodo (DOI `10.5281/zenodo.22707470`) + ResearchGate; non-peer-reviewed; no journal selected. |
| **Proposed / not built** | A pedestrian *routable network*. Every OSM pull to date fetched POIs/buildings/trees/water/transit — **never the walkable path graph**. |

**Forensic conclusion.** Evidence does not exist merely because a file or feature exists.
The locked pilot proves a *screening decision architecture* and demonstrates that
*thermal-method choice changes the screening outcome* — it proves **nothing** about
pedestrian-level UTCI accuracy, and it built no route network. The extension therefore
starts from: a validated-input / unvalidated-output thermal model, stale-but-auditable
geometry, and a **missing** route graph.

---

## GATE 1A — Candidate decision cases

### Selection criteria (fixed BEFORE selecting; no thermal output inspected)

Each criterion is scored 1 (weak) – 3 (strong). Weights are equal and stated; no weight was
tuned to favour an outcome.

| # | Criterion | Rationale |
|---|---|---|
| C1 | Tourism relevance | A trip a real visitor would plausibly make on foot. |
| C2 | ≥2 genuinely plausible, non-artificial alternatives | Alternatives must be distinct corridors, not offset variants of one geometry. |
| C3 | Geometric / shade contrast | Enough structural difference that a future thermal comparison *could* be informative (informativeness, not a known answer). |
| C4 | Network auditability | Can both routes be traced on a real, checkable walkable network and legally walked? |
| C5 | Manageable extent / duration | Walkable pilot scale (roughly 10–30 min), inside the corridor box. |
| C6 | Independence from HATI's locked outputs | Endpoints may reuse asset *coordinates*; the case must not reuse any locked thermal/asset-ranking *result* as evidence. |

### Candidate O-D pairs (endpoints from `data/processed/pilot_assets.csv`)

| ID | Origin → Destination | Alt A | Alt B | C1 | C2 | C3 | C4 | C5 | C6 | Σ |
|---|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **OD1** | **Atocha (A09) → Puerta de Alcalá (A14)** | **Paseo del Prado monumental axis (open, low canopy)** | **Calle Alfonso XII / Retiro–Botánico western edge (tree-lined)** | 3 | 3 | 3 | 2 | 2 | 3 | **16** |
| OD2 | Reina Sofía (A02) → Retiro Estanque (A20/A26) | Prado axis then enter at Alcalá | Calle Alfonso XII park-edge street | 3 | 3 | 3 | 2 | 2 | 3 | 16 |
| OD3 | Prado (A01) → Palacio de Cristal (A22) | Retiro interior shaded paths | Perimeter streets | 2 | 2 | 2 | 2 | 2 | 3 | 13 |
| OD4 | Thyssen (A03) → Puerta de Alcalá (A14) | Paseo del Prado (open) | Recoletos sidewalk (open) | 2 | 1 | 1 | 3 | 3 | 3 | 13 |
| OD5 | Atocha (A09) → Reina Sofía (A02) | Direct Ronda de Atocha | Glorieta detour | 2 | 1 | 1 | 3 | 3 | 3 | 13 |

Notes: OD1 and OD2 tie numerically; OD1 is selected (see 1A decision) because its endpoints
are the corridor's two canonical termini (a real arrival-to-icon walk), its two alternatives
are maximally distinct (a wide sun-exposed civic axis vs. a tree-lined park-edge street),
and Puerta de Alcalá is an *outdoor* endpoint (so the comparison is not dominated by an
indoor-refuge endpoint). **OD4 and OD5 are deliberately retained as negative-control seeds**
(§1F): their low geometric contrast is a feature — a sound method should *not* confidently
separate them.

### 1A decision

**Primary Gate 1 case: OD1 — Atocha (A09, 40.404557, −3.688683) → Puerta de Alcalá
(A14, 40.419987, −3.688724).**

- **Alt A (Prado axis):** north up the Paseo del Prado / Paseo de Recoletos civic axis past
  Neptuno and Cibeles to Alcalá. Wide, monumental, hard-paved, intermittent plane-tree
  alignment; high sky-view, low continuous canopy.
- **Alt B (park-edge):** north-east along the Real Jardín Botánico / Parque del Retiro
  western edge and Calle Alfonso XII, rejoining Alcalá from the park side. Tree-lined
  street plus park-margin canopy; lower sky-view in stretches.

Both are ~1.5–1.9 km, ~20–25 min walk, fully inside the corridor box, and (subject to the
network audit that Gate 1 flags as still-required) legally walkable.

### Rejected candidates + reasons

- **OD3** rejected: contrast is *inside-park vs street*, strongly dependent on which park
  gate is used and on gate opening hours (adds an avoidable access confound at Gate 1).
- **OD4, OD5** rejected *as primary* (kept as negative controls): both alternatives are
  open, low-canopy sidewalks — little geometric contrast, so a confident thermal separation
  would be a red flag, not a result.
- **OD2** rejected *as primary* only on the tie-break above (indoor-ish museum origin,
  Estanque endpoint slightly less canonical than Alcalá); it is the designated **backup**.

---

## GATE 1B — Historical hot-day selection protocol

**21 Aug 2023 is NOT auto-selected.** Per protocol it may only be retained later as a
*legacy stress-test*, never as independent validation of this extension.

### Selection rules (fixed before any day is chosen; reproducible)

A candidate day is admissible only if it satisfies **all** of R1–R5; among admissible days,
prefer higher R6 and R7.

| Rule | Requirement | Why |
|---|---|---|
| R1 | Genuine high-heat event: AEMET official daily-max ≥ the AEMET *aviso* threshold for Madrid (heat warning in effect), independently attributable from AEMET *avance climatológico* / METEOALERTA, not from this project's own model. | The comparison is only interesting under real heat stress. |
| R2 | Complete hourly forcing coverage (Ta/RH/wind/pressure) for the full daylight envelope at the forcing station, no gaps at target hours. | SOLWEIG needs uninterrupted hourly forcing. |
| R3 | Confirmed clear-sky (or documented sky state) at target hours, so the modeled-GHI clear-sky assumption is defensible (station `coco`/weather code). | The only available radiation is a clear-sky estimate; it is valid only when the sky was actually clear. |
| R4 | Temporal compatibility with the chosen urban geometry (see R7): no major undocumented construction/canopy event between the geometry vintage and the study day. | Keeps the geometry-vintage gap bounded and stated. |
| R5 | An **independent urban hourly** meteorological cross-check exists for that day — corrected 2026-09-14: municipal *Datos horarios desde 2019* provides hourly Ta/RH at Escuelas Aguirre (adjacent to OD1) from Jan 2019 onward; Retiro daily-max and ERA5-Land remain coarse/regional cross-checks. | Every study day needs at least one non-forcing check; an urban hourly one is now attainable only for days in 2019+. |
| R6 (preference, not gate) | Availability of the diurnal variables a departure-time comparison would later need. | Supports the optional time-shift analysis. |
| **R7 (added 2026-09-14)** | Prefer a day whose vintage aligns with the best available geometry: municipal **MDS 2023** surface / **MDT 2019** terrain favour a **2023 or later** study day; a pre-2019 day forfeits both the urban hourly check (R5) and MDS-2023 alignment. | Aligns forcing, geometry, and independent check to the same era; minimises the dominant canopy/geometry vintage gap. |

**Explicit anti-cherry-pick rule:** the day is chosen on R1–R7 (heat + data quality + vintage
alignment) **only**.
It is prohibited to choose a day because it maximises the Alt A – Alt B route difference. The
route difference must never be inspected before the day is fixed.

### Distinction (these are NOT automatically one dataset)

- **Weather-event selection** — attribution of "this was a real heat event" (AEMET official
  daily-max / warning record).
- **Model forcing** — the hourly series driving SOLWEIG (Barajas 08221, or a municipal full-met
  station; both are outside the corridor, so neither is the *urban* check below).
- **Independent urban meteorological checking** — a *different*, corridor-adjacent hourly record
  used to bound forcing representativeness: **Escuelas Aguirre hourly Ta/RH** (municipal *Datos
  horarios desde 2019*). It must not be the same series as the forcing. Retiro official summaries
  and ERA5-Land are the coarser **regional context** tier, not this urban check.

### Candidate dates + sources (selection stops here — no large download)

From material already in-repo plus small metadata:

| Candidate day | Evidence | R1 heat | R5 urban hourly (2019+) | R7 MDS-2023 align | Notes |
|---|---|---|---|---|---|
| A fresh **2023 or 2024** AEMET heat-warning day (≠ 21 Aug 2023) | AEMET OpenData + municipal *Datos horarios desde 2019* (small queries) | To select | **Yes** (Escuelas Aguirre) | **Yes** | **Preferred** after the 2026-09-14 correction: aligns forcing, urban hourly check, and MDS-2023 geometry. |
| 2021-08-14 | `data/raw/extreme_aug2021_barajas_raw.csv`; AEMET avance 202108 PDF | Yes (42.7 °C official) | Partial (2021 has municipal hourly, but predates MDS 2023) | No | **Demoted**: predates MDS 2023, so geometry reverts to PNOA 2008–2015. Retain as an alternative only. |
| 2023-08-21 | Barajas hourly + AEMET avance 202308 PDF | Yes (40.5 °C) | Yes | Yes | **Legacy stress-test only** — prohibited as independent validation of the locked HATI run; usable only as a *separately forced/reconstructed* case if circularity is fully avoided. |

**Provisional recommendation (to be frozen at Gate 2 start, not now):** shortlist a **fresh
2023/2024 AEMET heat-warning day (not 21 Aug 2023)** as primary — it aligns the Barajas/municipal
hourly forcing, the Escuelas Aguirre urban hourly check, and MDS-2023 geometry to one era —
with 2021-08-14 as a PNOA-vintage alternative. Do **not** pick a day on expected route
contrast. Final selection needs only small AEMET + municipal metadata queries to confirm
R2/R3/R5 — no bulk download.

---

## GATE 1C — Input feasibility ledger

The full structured ledger is `GATE1_INPUT_LEDGER.csv` (16 essential inputs after the
2026-09-14 correction added L15/L16, each with source/publisher/product/URL/vintage/
resolution/CRS/licence/role/status/independence/direction-risk/limitations/Gate-2 treatment).
Status summary:

| Status | Inputs |
|---|---|
| **ACCEPT** | L07 timestamps/timezone; L08 vintage register; L09 licensing; L14 O-D endpoints. |
| **ACCEPT WITH UNCERTAINTY** | L01 Barajas forcing; L02 independent urban check (now hourly Ta/RH near OD1; wind/radiation still not corridor-local); L03 buildings/terrain; L04 canopy; L10 departure-time support; L11 solar GHI; L13 wind; **L15 Madrid MDS 2023 / MDT 2019 (added)**; **L16 municipal tree inventory (added)**. |
| **MISSING** | **L05 pedestrian network**; **L06 route access/crossing plausibility**; L12 land cover (package default — non-blocking). |
| **REJECT** | none. |

**Two MISSING inputs are load-bearing for a *route* comparison** and are the headline Gate 1
finding: L05 (the routable pedestrian graph) and L06 (crossing/access plausibility). Neither
was ever assembled by HATI. Both are **acquirable within Gate-1 rules** (a bounded Overpass
query for the two fixed routes + a manual walkability audit — small, not a bulk download),
but until acquired and audited the "auditable routes" precondition for GO is **not met**.

Specific attention points (per Gate 1C; updated 2026-09-14):
- **Barajas vs central Madrid:** forcing is an airport ~13 km NE. An **independent urban
  hourly Ta/RH** check now exists adjacent to OD1 (Escuelas Aguirre) — so airport-vs-centre
  Ta/RH bias can be *measured hourly*, not just assumed differenced-out. **Wind and radiation
  remain non-corridor-local** (only the six peripheral met stations observe them).
- **Radiation & wind:** GHI at OD1 stays a clear-sky *estimate* (no corridor-local pyranometer;
  nearest radiation obs are peripheral municipal stations / AEMET Ciudad Universitaria, usable
  only as a regional check); wind is a single non-local station value. Both are perturbation
  dimensions, not validated fields.
- **Canopy vintage — reduced but still dominant:** PNOA 2008–2015 is no longer the only
  option. **MDS 2023** (L15) gives a 2023 surface, and the **municipal tree inventory** (L16)
  audits *current* tree presence/removals; both shrink the gap for a 2023+ study day. Canopy
  still leads the direction-changing risk because MDS is unclassified and gives no crown
  transmissivity or leaf state.
- **Crown geometry vs tree points:** neither PNOA height raster, MDS 2023 surface, nor the
  tree inventory provides crown polygons, per-hour shade, or leaf state — shadow extent stays
  approximated; the tree inventory is a *presence/removal audit*, not crown geometry.
- **Building geometry date:** MDS 2023 − MDT gives a **2023** building surface, materially
  better than the 2008–2015 building nDSM; OSM incompleteness / side-of-street ambiguity still
  unmodelled — the network audit (L06) must resolve which sidewalk each route uses.
- **Crossings / pedestrian restrictions & historical opening hours:** required if a
  time-shift comparison is later attempted; 2026 hours applied to a historical day is a
  stated mismatch.
- **Sentinel-2:** never used as a thermal sensor or LST source (guardrail restated).

Do not confuse source resolution with pedestrian-scale *accuracy*: MDS 2023 is 1 m and
~contemporaneous **yet unclassified and photogrammetric** (no building/canopy separation, no
sub-canopy structure); the PNOA canopy raster is 2.5 m **and** ~decade-stale simultaneously.

---

## GATE 1D — Claim ceiling

**Path A (independent pedestrian-level thermal measurements exist): NOT CURRENTLY AVAILABLE
(corrected 2026-09-14 — not "impossible").**
No field Tmrt/UTCI exists in-repo, and **no suitable independent pedestrian-level Tmrt/UTCI
measurement has yet been identified** for this corridor/date. Impossibility is **not**
demonstrated: a future in-situ campaign (globe/six-directional radiometer transect along the
two OD1 routes) is conceivable and would reopen Path A, but is out of scope and unfunded here.
Until such data are identified or collected, the study operates on Path B.

**Path B (no such measurements currently available): OPERATIVE.**

Therefore the **maximum honest claim ceiling** for this extension is:

> **Robustness, sensitivity, decision-reversal behaviour, and evidence sufficiency of
> *modeled* comparative pedestrian thermal exposure — including a first-class ABSTAIN /
> NO-EVIDENCE outcome — for one auditable tourism O-D case.**

Explicitly **excluded** from the ceiling (restated from protocol §5): observed tourist
exposure; validated pedestrian UTCI accuracy; subjective comfort; behaviour; physiological
stress; health/adaptation benefit. None of {another model run, ERA5-Land, the same forcing,
the locked HATI output} counts as independent validation of pedestrian UTCI.

This lowered ceiling is **not** a project failure: the Gate-0 research object *is* decision
reliability + evidence sufficiency + abstention, which lives entirely inside Path B.

---

## GATE 1E — Minimal perturbation set (designed, NOT executed)

Full frozen spec in `GATE1_EXPERIMENT_SPEC.md`. Summary of the smallest defensible set —
each dimension included **only** because it can change the *decision* and each range has a
data/literature justification (no arbitrary parameter sweeps):

| Dim | Uncertainty source | Justified alternatives | Why it can flip the decision |
|---|---|---|---|
| E-P1 (revised 2026-09-14) | Meteorological forcing representativeness | Barajas as-is vs an **empirical hourly** Escuelas-Aguirre-minus-Barajas Ta/RH difference at the target hours. If the urban station is incomplete for the chosen day/hours, forcing uncertainty becomes an **ABSTAIN** condition — the discarded +0.5 °C constant-offset is **not** reinstated. | Airport-vs-centre bias, now measured hourly; a daily-max offset was statistically invalid for the diurnal cycle. |
| E-P2 (revised 2026-09-14) | **Canopy / vegetation geometry** | Bounding canopy states: PNOA 2008–2015 nDSM vs **MDS 2023** surface-derived canopy height vs **municipal tree-inventory** presence audit (removals/additions) vs Copernicus TCD 2018 density | The dominant risk: canopy change can add/remove the shade separating Alt A from Alt B; MDS 2023 + inventory bound it far better than one stale raster. |
| E-P3 | Wind treatment | Uniform station wind vs a simple open-vs-canyon adjustment (no CFD) | Plaza-vs-canyon cooling could differentially favour one route. |
| E-P4 (revised 2026-09-14) | Building/shadow representation | **MDS 2023 − MDT 2019** building surface (2023) vs PNOA 2008–2015 building nDSM as cross-check | Building edits alter cast shadow on one route; the 2023 surface is the preferred base, PNOA the fallback/cross-check. |
| E-P5 | Pedestrian network representation | Two independently-audited route traces (e.g. sidewalk side A vs side B where ambiguous) | Side-of-street choice changes exposure along the same corridor. |
| E-P6 | Walking speed / pauses | 1.1 vs 1.4 m/s; optional queue/pause at endpoints | Changes cumulative exposure integral and could reorder near-ties. |

**Decision framework — no invented °C threshold.** The literature check (below and in
`GATE1_LITERATURE_LOG.md`) found **no** defensible universal "material UTCI difference"
threshold for *this* comparison type, but a **mature rank-reversal / decision-stability
formalism** (pairwise-comparison robustness under uncertainty bounds). The comparison is
therefore framed on decision stability, not on a magic number:

- **ROBUST COMPARISON** — the *direction* of the paired Alt A − Alt B difference is
  preserved across all justified perturbations (E-P1…E-P6) and the difference sits clear of
  any UTCI category boundary.
- **NO ROBUST DIFFERENCE** — the routes are statistically/materially indistinguishable, or
  the sign is stable but the magnitude is within the modeled uncertainty interval.
- **ABSTAIN / NO EVIDENCE** — the decision *reverses* under at least one justified
  perturbation, OR an essential input is MISSING/near a category boundary, OR the
  uncertainty interval spans the decision.

Statistical significance is explicitly **not** conflated with practical/physiological
relevance (no physiological claim is made at all).

---

## GATE 1F — Negative controls (pre-specified)

A method that confidently resolves any of these has **failed** its evidence-sufficiency
logic and must ABSTAIN:

1. **NC1 — effectively identical routes:** OD4 / OD5 seeds (two open low-canopy sidewalks).
2. **NC2 — missing network link:** a route deliberately traced across an unmapped/again-to-
   verify connection (tests L05 gap handling).
3. **NC3 — uncertain pedestrian access:** a route using a park gate whose opening hours /
   legality on the study day is unresolved (tests L06).
4. **NC4 — unresolved canopy vintage:** a route whose Alt A/Alt B separation depends entirely
   on canopy pixels in the 2008–2015 nDSM that current arbolado points contradict.
5. **NC5 — missing meteorological variable:** a target hour with a forcing gap or non-clear
   sky (violates R2/R3) — the method must refuse, not interpolate silently.
6. **NC6 — category-boundary case:** a pair whose modeled UTCI difference straddles a UTCI
   stress-category boundary.
7. **NC7 — justified-assumption reversal:** any pair whose ordering flips between E-P2 canopy
   states — the canonical ABSTAIN trigger.

---

## GATE 1G — GO / MODIFY / NO-GO (rules + result)

Decision rules were fixed before scoring; the row-by-row evaluation is in
`GATE1_DECISION.md`. In one line: **GO** requires (among other things) auditable routes AND
usable forcing AND ≥1 independent check AND a legitimate ABSTAIN outcome AND a non-trivial
surviving question. Here forcing, ABSTAIN, and the surviving question hold; **auditable
routes are not yet in hand (L05/L06 MISSING)** and **pedestrian-level validation is not
currently available (Path B operative)**. That combination is the textbook **MODIFY**
trigger, not GO — and it is **not** NO-GO, because a genuine, non-saturated
evidence-sufficiency / abstention question survives the literature review and — after the
2026-09-14 correction — a genuine independent **urban hourly** check now exists (Escuelas
Aguirre Ta/RH), no longer merely a weak daily/monthly one.

**VERDICT: MODIFY** — proceed to Gate 2 with (a) the claim ceiling reduced to
robustness/sensitivity/abstention (Path B), and (b) two hard preconditions that must be
satisfied *before* any thermal run: acquire + manually audit the L05 pedestrian network and
L06 access/crossings for the two OD1 routes, and freeze the study day on R1–R7 (preferring a
fresh 2023/2024 heat day per the correction).

---

## Principal uncertainties (ranked)

1. **Canopy geometry** — still dominant and direction-changing, but **reduced** after the
   correction: MDS 2023 (L15) + tree inventory (L16) bound it far better than the 2008–2015
   raster alone; the residual (unclassified surface, no crown transmissivity, no leaf state)
   is why the ABSTAIN logic still centres here.
2. **No pedestrian-level validation (Path B operative)** — caps the claim while it holds;
   Path A is *not currently available*, not impossible.
3. **Missing route network + access audit (L05/L06)** — a precondition gap, resolvable but
   currently open.
4. **Corridor-local wind & radiation not observed** — only peripheral met stations measure
   them; GHI stays modeled and wind non-local. (Ta/RH is now checkable at OD1.)
5. **Forcing representativeness (Barajas airport)** — now testable via an empirical hourly
   Escuelas-Aguirre-minus-Barajas Ta/RH difference (E-P1), not merely assumed differenced-out.

## Unresolved blockers carried to Gate 2

- **B1:** L05 pedestrian network and L06 crossing/access plausibility are MISSING and must be
  acquired + manually audited before any thermal computation.
- **B2:** Study day not yet frozen (R1–R7 shortlist; a fresh 2023/2024 heat day preferred;
  small AEMET + municipal metadata queries pending).
- **B3:** A closely-adjacent 2026 paper ("How fine is fine enough? … heat-aware pedestrian
  routing") narrows the novelty envelope; Gate 2 framing must assert the abstention/
  evidence-sufficiency distinction sharply (see `GATE1_LITERATURE_LOG.md`).

---

*This dossier stops before thermal modeling by design. No SOLWEIG/URock/UTCI was run; no
large dataset was downloaded; no synthetic validation evidence was created.*
