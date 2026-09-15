# GATE2_EVIDENCE_REPORT — Evidence Acquisition & Experiment Freeze

**Gate 2 — pre-modeling evidence gate. Version 1.0 · 2026-09-15.**
**Verdict (full justification in `GATE2_DECISION.md`): GO_TO_FIRST_THERMAL_EXPERIMENT.**

> **Scope guard.** No SOLWEIG was run; no UTCI/Tmrt computed; no thermal map,
> route-thermal difference, recommender, or future-climate scenario produced. This
> gate ends **before** the first thermal output. It resolves the Gate-1 OPEN
> preconditions and freezes a complete, auditable experiment specification. Frozen
> Gate-0 / Gate-1 decisions are not reopened or silently modified.

This report follows the Gate-2 task structure (2A–2J). Every acquired artifact has a
SHA-256 in `data/processed/pedestrian-heat/gate2_hash_manifest.json` and the freeze
values are in `GATE2_FREEZE_MANIFEST.json`.

---

## 2A — Pedestrian network acquisition

A **bounded** Overpass acquisition (corridor bbox `(40.4035,-3.6950,40.4210,-3.6820)`,
~2.1 km²), **not** a city-wide network. Preserved:
- **Query:** `data/raw/osm_pedestrian/query_od1_pedestrian.overpassql`
- **Raw response:** `data/raw/osm_pedestrian/osm_od1_pedestrian_raw.json`
  (SHA-256 `a3a616016a9646197bdbcff2c26a853f0179afb6ccf79b13209cf9e2c0ce2e8f`;
  2979 elements — 2262 ways, 717 nodes; 1147 footways, 53 pedestrian ways, 150 steps).
- **Acquisition timestamp:** 2026-09-14T19:46:20Z; **OSM base:** 2026-09-14T19:45:03Z.
- **Attribution:** © OpenStreetMap contributors, ODbL.
- **Provenance:** `data/raw/osm_pedestrian/acquisition_provenance.json`.

Candidate walkable traces were constructed from actual OSM ways (footways, pedestrian
streets, steps, service/living_street links), crossings, access tags and barriers.
**No thermal information was used in route construction.**

## 2B — Manual route / access audit

**Method.** A walkable graph was built from the fetched ways (highway ∈
{footway, path, pedestrian, steps, living_street, service, track, unclassified,
cycleway, residential} plus `foot=yes/designated/permissive` overrides; `access` in
{private,no,customers,permit,military} excluded unless a foot override; steps kept).
Each route is a **corridor-pinned shortest walkable path** (Dijkstra on walking
distance) through waypoints fixed by the **Gate-1 frozen corridor identities** —
never by any thermal output.

**Two audit findings drove the geometry:**
1. **Route B must not cut through Retiro.** The unconstrained shortest path entered
   the park via mapped gates (Puerta del Ángel Caído; Puerta de la Independencia,
   `opening_hours "Apr-Sep 06:00-24:00"`) and walked interior avenues (Paseo de
   Paraguay/Argentina) — i.e. the **rejected OD3 park-interior confound** (gate-hours
   dependence, NC3). Because the frozen Alt-B identity is the **street** ("Retiro
   western edge + Calle Alfonso XII"), park-gate nodes and Retiro-interior nodes were
   made impassable for auto-routing (destination-adjacent gate exempt). Keeping Route
   B on the street is faithful realisation of the frozen identity, **not** opportunistic
   repair. Result: **0 park gates on the frozen Route B.**
2. **Calle de Alfonso XII is a motor carriageway** (`highway=secondary/tertiary`,
   `foot=no` on one segment; sidewalks tagged mostly `right`/`both`). Pedestrians use
   the separate sidewalk footways. Route B is pinned to the **park-side (east)
   sidewalk** footway chain; the opposite sidewalk is the frozen **E-P5** perturbation.

**Frozen routes** (versioned GeoJSON, EPSG:25830; geometry must not change without an
amendment):

| Route | Identity | Length | Vertices | OSM ways | Mapped crossings | Park gates | SHA-256 |
|---|---|---|---|---|---|---|---|
| **A** | Paseo del Prado / Recoletos monumental axis (open) | 2657.8 m | 127 | 42 | 23 | 0 | `f2f9d8b4…4337dc9a6` |
| **B** | Real Jardín Botánico / Retiro western edge + Calle Alfonso XII (tree-lined, park-side sidewalk) | 2365.7 m | 115 | 38 | 13 | 0 | `fedf5ed4…52ba95f7` |

The two traces are spatially distinct (200–315 m E–W separation through the corridor
mid-section), sharing only the shared O and D. Files:
`data/processed/pedestrian-heat/OD1_Route_A_epsg25830.geojson` and
`…OD1_Route_B_epsg25830.geojson`.

**Segment audit** (`GATE2_ROUTE_AUDIT.csv`, 240 segments):

| Classification | Route A | Route B |
|---|---|---|
| VERIFIED | 111 | 99 |
| VERIFIED WITH UNCERTAINTY | 15 | 15 |
| REJECT | 0 | 0 |
| UNRESOLVED | 0 | 0 |

"VERIFIED WITH UNCERTAINTY" segments are (i) the two O-D endpoint access snaps
(Atocha concourse ~91 m; Alcalá monument island ~42 m — common to both routes) and
(ii) open plaza / axis desire-line segments (13 per route; monumental plazas
Emperador Carlos V, Cibeles, Independencia and the Salón del Prado) where the exact
walked line across open pavement is approximate. **No segment is REJECT or
UNRESOLVED**: both routes are continuously, legally walkable end-to-end with no
park-gate/opening-hour dependence. OD1 therefore **does not** move to the ABSTAIN
negative-control case; the backup OD2 is not invoked.

## 2C — Study-day freeze

Rules R1–R7 were applied **before** any thermal output. 21 Aug 2023 excluded (locked
pilot day). Candidate table (AEMET-documented extreme-heat episode 20–25 Aug 2023;
Barajas 08221 in-repo hourly):

| Day | Barajas Tmax °C | 24 h complete (R2) | Afternoon sky coco (R3) | Wind km/h | R1 | R5 urban | R7 MDS-align |
|---|---|---|---|---|---|---|---|
| 2023-08-20 | 39.0 | ✓ | 1 (clear) | 11.2 | ✓ | ✓ | ✓ |
| ~~2023-08-21~~ | 40.5 | ✓ | 1,2 | 14.8 | — | — | EXCLUDED (locked) |
| 2023-08-22 | 40.0 | ✓ | 1 (clear) | 14.8 | ✓ | ✓ | ✓ |
| 2023-08-23 | 39.5 | ✓ | 1 (clear) | 22.3 | ✓ | ✓ | ✓ |
| **2023-08-24** | **40.0** | ✓ | **1 (clear)** | 16.6 | ✓ | ✓ | ✓ |
| 2023-08-25 | 38.5 | ✓ | 1,2 | 33.5 | ✓ | ✓ | ✓ |

**Pre-declared selection rule (data-quality only, not route contrast):** among R1–R5
admissible days pick (i) fully-clear afternoon (coco=1 at target hours), (ii) complete
24 h forcing, (iii) highest heat tier, (iv) greatest temporal separation from the
excluded 21 Aug 2023 (to minimise circularity with the locked pilot). → **2023-08-24**
(top tier 40.0 °C, fully clear, Δ3 days from 21 Aug; 22 Aug is only Δ1). This was fixed
**before** any A-vs-B thermal difference could be inspected (none exists).

**Frozen:** study date **2023-08-24**; timezone **Europe/Madrid (CEST = UTC+2)**;
target hours **14:00 and 17:00 local** (12:00 and 15:00 UTC) — a near-solar-maximum
hour and a late-afternoon peak-heat hour, both confirmed clear-sky, chosen before any
thermal computation. These are **departure times**, not whole-trip static snapshots;
the time-resolved traversal method (Δt = 15 min fields; per-segment traversal
timestamps; explicit static-per-hour fallback that lowers the claim) is frozen in
`GATE2_METRIC_SPEC.md` §0.1.

- **R1** heat: AEMET *avance* designates 20–25 Aug 2023 an extreme-heat episode;
  Barajas (AEMET station) daily max 40.0 °C ≥ *naranja* threshold (39 °C, zone 722802).
- **R4** geometry compatibility: no undocumented construction/canopy event known
  between MDS-2023 vintage and the study day (heritage core, protected).
- **R6** diurnal-variable availability: full hourly forcing supports an optional
  time-shift analysis (not part of this freeze).

## 2D — Meteorological evidence (verified at file level)

Full ledger: `GATE2_METEOROLOGY_LEDGER.csv`.

- **Model forcing (frozen):** Madrid-Barajas 08221 (AEMET), hourly Ta/RH/wind/
  pressure/coco. **Verified complete at target hours (24 Aug 2023):** 14:00 = 37.0 °C
  / 17 % / 11.2 km/h / clear; 17:00 = 40.0 °C / 12 % / 6.0 km/h / clear. Solar GHI is
  pvlib Ineichen clear-sky (licensed by coco=1), applied identically to both routes.
  File `aemet_barajas_08221_hourly_202308.csv` (SHA-256 `ffd1ed05…bc025019`).
- **Independent urban check (verified at file level, NOT dataset description only):**
  **Escuelas Aguirre** (municipal *Datos horarios desde 2019*, dataset 300352, station
  8 / air-quality 28079008, ~0.5 km ENE of Puerta de Alcalá). Downloaded the Aug-2023
  monthly file and extracted station 8, day 24, magnitudes 83 (Ta) and 86 (RH): **all
  target-hour values present and flagged "V" (valid)** — Ta ≈ 35.3 °C (H14) / 37.1 °C
  (H15) around 14:00 and 39.8 °C (H17) / 39.9 °C (H18) around 17:00; RH 23→15 %. Ta
  tracks Barajas within ~0–2 °C. File
  `data/raw/madrid_meteo_municipal/meteo_municipal_202308.csv` (SHA-256
  `e3f933f8…30430fe5`); provenance JSON alongside. This is a genuine, independent,
  corridor-adjacent hourly Ta/RH record — the basis for E-P1 — and it is **not** the
  forcing series. It does **not** validate Tmrt/UTCI.
  - **Escuelas Aguirre measures Ta/RH only** — **not wind, not radiation.** Corridor-
    local wind and radiation remain unobserved (see 2F).
- **Regional context (kept in role):** AEMET *avance* (episode + Retiro daily max) and
  Meteoalerta thresholds. **Not** called pedestrian validation; ERA5-Land not used.
- **ABSTAIN rule (2D):** if the urban check were absent at a required timestamp,
  forcing uncertainty → ABSTAIN (no interpolation to preserve the experiment).
  **Not triggered** — coverage is complete and valid.

## 2E — Geometry evidence

Full ledger: `GATE2_GEOMETRY_LEDGER.csv`. Only **bounded OD1 clips / reproducible
acquisition** are used; large rasters are not committed — acquisition instructions +
hashes are recorded instead.

- **Terrain:** Madrid **MDT 2019** (geoportal.madrid.es, 10 cm COG tiles); IGN MDT 5 m
  (in-repo, WCS verified live) as cross-check. Bounded tile clip to OD1 at execution.
- **Normalized surface height:** **MDS 2023 − MDT 2019** — a *top-of-everything*
  surface field, **explicitly not** a building or canopy raster. Madrid MDS 2023
  (geoportal.madrid.es, 100 pts/m², 1 m COG tiles) confirmed obtainable; bounded clip.
- **Building classification (L17 building side — RESOLVED).** Building-footprint source
  **audited live (2026-09-15): Catastro INSPIRE Buildings WFS** returns
  `bu-ext2d:Building` features with **authoritative 2-D footprint polygons**
  (`gml:posList`), `currentUse`, `conditionOfConstruction`, `OfficialArea`. Decision:
  **use the footprint geometry to mask the normalized surface height into buildings;
  take building HEIGHT from the masked nSH, NOT from Catastro `numberOfFloorsAboveGround`**
  — that attribute is a floor-count proxy and is **frequently `nil="unpopulated"`** in
  the feed (confirmed in the audit). PNOA 2008–2015 building nDSM (in-repo) is the
  cross-vintage check (E-P4). Only after this masking is the nSH read as building height.
- **Vegetation classification strategy (stated as known / inferred / unresolved).**
  - **Known:** municipal tree inventory (dataset 300761; in-repo live GeoJSON) —
    individual tree **points** with species and ALTURA height; **1322 park + 1528
    street trees within the OD1 corridor** (one 139 m ALTURA outlier to drop).
    Copernicus TCD 2018 (in-repo) tree-cover density. PNOA veg nDSM 2008–2015 (in-repo)
    canopy height (stale). OSM green polygons (in-repo).
  - **Inferred:** canopy height = MDS-2023 nSH **only where a justified vegetation mask
    says vegetation** (mask = union of tree-inventory buffers + OSM green polygons +
    Copernicus TCD ≥ threshold).
  - **Unresolved:** crown transmissivity, leaf state, sub-canopy structure, per-hour
    shade, historical crown geometry. Tree points are **not** crown polygons; the
    inventory is a presence/removal audit, **not** historical canopy. Sentinel-2/optical
    is **never** used as temperature/LST — greenness only, for a mask.
  - **Compatibility with Path B / ABSTAIN condition:** the residual canopy ambiguity is
    bounded by the four-state E-P2 perturbation; **if the A-vs-B ordering flips across
    those canopy states, the case ABSTAINs (NC7)** rather than forcing a classification.

## 2F — Wind decision

- **Available observation:** single non-corridor station wind (Barajas 08221),
  target-hour values **11.2 km/h (3.1 m/s) at 14:00 and 6.0 km/h (1.7 m/s) at 17:00**.
  Escuelas Aguirre (the urban check) does **not** measure wind; only the six peripheral
  municipal full-met stations measure wind/radiation, **none in the corridor**.
- **How the eventual model consumes it:** SOLWEIG takes a single hourly wind speed
  applied **uniformly** across the grid, identically to both routes.
- **Decision — uniform wind only.** No open/canyon multiplier is invented; **URock is
  not introduced.** Gate-1 demoted spatial-wind perturbation (E-P3) and no published
  canyon-parameterisation specific to this context was found, so none is fabricated
  (complexity is not evidence). Uniform wind is acceptable under the Path-B claim
  ceiling because: (i) it is applied identically to both routes and cannot by itself
  flip a within-pair difference; (ii) target-hour wind is low (1.7–3.1 m/s), limiting
  canyon-channelling magnitude; (iii) the claim ceiling forbids any spatial-wind claim
  regardless.
- **Unresolved spatial heterogeneity is listed explicitly** and remains an **ABSTAIN
  trigger**: if the comparison is later shown decision-critical on spatial wind while
  it is unresolved, the case ABSTAINs. Wind uncertainty **alone** does not make OD1
  uninterpretable at these low speeds, so Gate 2 does not return MODIFY/ABSTAIN on wind.

## 2G — Frozen outcome metrics

Frozen in `GATE2_METRIC_SPEC.md`: M1 trip duration; M2 time-weighted mean modeled
UTCI; M3 along-route distribution/range; M4 minutes and proportion per UTCI stress
category; M5 max/95th-percentile **as a descriptor only, excluded from the decision**
(no comparison-specific justification — dropped from the decision before freezing).
The cumulative ∫UTCI dt scalar stays **removed**; no output is called a dose. Formulas,
Δs = 5 m sampling, buffer-mean, missing-pixel ABSTAIN rule, and the **authoritative
UTCI category boundaries** (+26/+32/+38/+46 °C; Bröde et al. 2012 / www.utci.org) are
all specified there. No composite score is formed after seeing results.

Three freeze-integrity points are made explicit in the spec (§0.1, §1.6, M2):
- **Route-length confound.** Metrics are split into **THERMAL-INTENSITY** {M2, M3, M5}
  (length-independent microclimate) vs **EXPOSURE-DURATION** {M1, M4} (length-dependent
  accumulated load), reported separately; a shorter route is **not** called cooler
  merely because it accumulates fewer minutes; an intensity/duration trade-off supports
  **NO ROBUST DIFFERENCE / ABSTAIN**, never a composite.
- **Departure-time, time-resolved traversal** (§0.1): 14:00/17:00 are departure times;
  Δt = 15 min SOLWEIG fields; per-segment traversal timestamps; hourly met interpolated;
  solar geometry/shadows evolve within the trip; explicit static-per-hour fallback that
  **lowers the claim** rather than faking time resolution.
- **UTCI category semantics** (M2/M4): sample-by-sample accounting (M4) is the
  boundary-meaningful metric; categorising the route-**average** (M2) is a descriptive
  band only, **not** a physiological classification of the journey.

## 2H — Frozen perturbation values

Frozen in `GATE2_PERTURBATION_SPEC.md`. E-P1 (forcing; empirical hourly urban−airport
Ta/RH, measured values recorded), E-P2 (canopy; four real independent states), E-P4
(building; MDS−MDT via Catastro footprints vs PNOA cross-vintage), E-P5 (side-of-street;
frozen vs opposite sidewalk), E-P6 (speed 1.1/1.4 m/s + optional pause) each have exact,
provenance/literature-justified values. **E-P3 (wind) is demoted** to an unresolved
limitation. Nothing is an arbitrary range; the boundary guard band is the
perturbation-ensemble interval (no invented °C guard).

## 2I — Negative controls (operationalised BEFORE the thermal experiment)

Pre-declared here, before any thermal output, with the **exact evidence condition that
forces ABSTAIN**. These test the evidence-sufficiency logic, not model accuracy; a
method that confidently resolves any of them has failed and must ABSTAIN.

| NC | Control | Operationalisation for OD1 | ABSTAIN evidence condition |
|---|---|---|---|
| **NC1** | Effectively identical routes | OD4 (Thyssen→Alcalá: Paseo del Prado vs Recoletos sidewalk) / OD5 (Atocha→Reina Sofía) seeds — two open low-canopy sidewalks, minimal geometric contrast. | Method returns a **confident** A≠B ordering (ROBUST) on a pair with no geometric basis → fail → must ABSTAIN / NO ROBUST DIFFERENCE. |
| **NC2** | Missing network link | A trace forced across a deliberately unmapped/again-to-verify connection (an OSM gap). | Any essential route link MISSING/unverified → ABSTAIN (never silently bridge). |
| **NC3** | Uncertain pedestrian access | A Route-B variant that **enters Retiro via a gate** (Puerta del Ángel Caído / de la Independencia, opening-hours dependent) — the park-interior option rejected in 2B. | Route depends on a gate whose legality/opening-hours on the study day is unresolved → ABSTAIN. |
| **NC4** | Unresolved canopy vintage | A pair whose A−B separation rests entirely on 2008–2015 PNOA canopy pixels that the 2025/2026 tree inventory contradicts (removals/additions). | Separation depends on canopy pixels contradicted by current inventory → ABSTAIN. |
| **NC5** | Missing meteorological variable | A target hour with a forcing gap or non-clear sky (violates R2/R3), or > 5 % missing UTCI pixels along a route. | Any target-hour forcing gap / non-clear sky / missing-pixel breach → refuse, do not interpolate → ABSTAIN. |
| **NC6** | Category-boundary case | A pair whose M2/M4 straddles a UTCI category cut-point (+26/+32/+38/+46 °C). | Perturbation-ensemble interval of a category metric **contains** a cut-point → ABSTAIN. |
| **NC7** | Justified-assumption reversal | The canonical trigger: A−B ordering flips between E-P2 canopy states (or any justified perturbation). | Ordering reverses under ≥ 1 justified perturbation → ABSTAIN. |

Controls are fixed now and will **not** be reselected after observing the primary
result.

## 2J — Final pre-modeling freeze

`GATE2_FREEZE_MANIFEST.json` records: OD1 identity; Route A/B hashes; study day; target
hours; timezone; forcing source + hash; independent-check source + hash; terrain,
normalized-surface, building-classification, vegetation-classification and tree-audit
sources/methods; wind treatment; outcome metrics; UTCI categories; walking assumptions;
perturbation alternatives; negative controls; and the Path-B claim ceiling. Every
mutable local artifact used has a SHA-256 (`gate2_hash_manifest.json`, 14 entries;
`route_freeze_hashes.json`).

---

## Unresolved limitations carried forward (honest ledger)

1. **Canopy classification residuals** — no crown transmissivity / leaf state / sub-
   canopy / historical crown geometry; bounded by E-P2, ABSTAIN if it flips the order
   (dominant residual uncertainty).
2. **Spatial wind unobserved in-corridor** — uniform wind only; E-P3 demoted; ABSTAIN
   if later shown decision-critical.
3. **Corridor-local radiation unobserved** — GHI stays modeled clear-sky (valid only at
   the confirmed clear hours), applied identically to both routes.
4. **MDS 2023 semantics** — normalized surface height is building/canopy only after the
   frozen classification/mask steps; raw nSH is never read as either.
5. **No pedestrian-level thermal validation (Path B)** — caps the claim; Path A is *not
   currently available*, not impossible.
6. **Open-plaza desire-lines & endpoint snaps** — 13 approximate open-space segments per
   route + O-D access snaps (common to both routes; VERIFIED WITH UNCERTAINTY).
7. **Municipal H-column convention** — Escuelas Aguirre Hnn is hour-ending local time;
   the ±1 h bracket is recorded (does not affect the extreme-heat confirmation).

None of these makes the A-vs-B ordering uninterpretable **before** modeling; each is
either bounded by a frozen perturbation or wired to an explicit ABSTAIN condition.

*Gate 2 stops here — before the first thermal output. No SOLWEIG/UTCI/Tmrt was run.*
