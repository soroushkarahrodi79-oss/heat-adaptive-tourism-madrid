# PHASE1_METHOD.md — HATI-Madrid Phase 1 Thermal Feasibility Spike

Version 1.0 · 2026-08-17
Gate in effect: **GO WITH MODIFICATIONS** (`docs/FEASIBILITY_GATE.md`). This document
executes the bounded Phase 1 spike authorised under that gate; it does not reopen
Phase 0.

> **Phase 1.1 amendment note (2026-08-17):** a subsequent hardening pass
> (`docs/PHASE1_1_BASELINE_HARDENING.md`) renamed the hazard gate to
> "meteorological hazard gate" (§5.1), demoted the adaptation-resource gate
> from an exclusion rule to a reported indicator (§5.3), and found the
> exposure gate (§5.2) sensitive to the choice of shade proxy. §5.1, §5.3, and
> §5.4 below are updated in place to stay factually accurate; the rest of this
> document is preserved as the original Phase 1 record. See
> `docs/PHASE1_1_GATE.md` for the current gate verdict, which supersedes
> `docs/PHASE1_GATE.md`.

---

## 1. Purpose

Determine whether a scientifically defensible, spatially differentiated tourism
thermal-suitability classification can be produced for a small, real pilot in
central Madrid, using only real, open, already-existing data and a simple,
auditable constraint-first decision architecture — **not** a weighted composite
index, **not** SOLWEIG/UTCI, **not** ML.

## 2. Study area

**Prado – Retiro – Atocha**, a rectangular bounding box in WGS84:

| Edge | Value | Landmark reference |
|---|---|---|
| North | lat 40.4210 | just north of Puerta de Alcalá (40.4201, -3.6883) |
| South | lat 40.4040 | just south of Estación de Madrid-Puerta de Atocha's full building extent (OSM relation centroid 40.40456, -3.68868) |
| West | lon -3.6960 | west of CaixaForum Madrid / Paseo del Prado sidewalk (-3.6936) |
| East | lon -3.6775 | east of Retiro's Palacio de Cristal (-3.6823), into the park interior, as far as Jardines de Cecilio Rodríguez (real polygon centroid -3.67797) |

Area ≈ 3.5 km². Geometry generated reproducibly by `src/define_study_area.py`;
output at `data/processed/study_area.geojson`.

**Why this box, not a hand-drawn polygon:** a rectangle pinned to named,
independently verifiable landmarks is fully reproducible by a third party without
access to any proprietary boundary file, and is large enough to include a genuine
cross-section of adaptation conditions (open monumental plazas, the Prado–Thyssen–
Reina Sofía museum corridor, Atocha's transit hub, and a real slice of Retiro's
interior including two well-known shaded gardens) while staying small enough to
respect the explicit "do not expand city-wide" instruction and the feasibility
gate's "smallest publishable version" mandate.

**Self-correction during build:** an initial, tighter draft of this box (south
edge at lat 40.4055, east edge at lon -3.6790) was used to curate the pilot asset
list, but the reproducibility test suite (`tests/test_outputs.py`) caught that
three real, legitimately-curated assets — the Atocha station building, Jardines
de Cecilio Rodríguez, and Jardines del Arquitecto Herrero Palacios — had OSM
centroids just outside that draft box. This happens because Overpass reports a
way/relation's full-geometry centroid even when only part of the feature
intersects the query bounding box, so a polygon that just clips the box edge can
still report a centroid outside it. Rather than discard those real, legitimately
curated assets or leave the study-area polygon not actually containing the pilot
set it was drawn to represent, the box was widened by ~150 m on both affected
edges and every upstream OSM extract was re-fetched against the new box (see
`data/raw/osm/README.md`). This is reported here because it also had a welcome
side effect on data quality — see §5.2.

**What is deliberately excluded:** most of Retiro Park (this box's slice of the
park interior is real but partial), the Sol/Gran Vía retail core, and Salamanca
district. These are legitimate Phase 2+ expansion candidates, not omissions of
convenience.

## 3. Heat episode

**20–25 August 2023**, Comunidad de Madrid — designated by AEMET itself as an
"episodio de calor extremo" ("del día 20 al 25 de agosto hubo un episodio de calor
extremo, en el que tanto las temperaturas máximas como las mínimas fueron muy
elevadas"), in the official monthly climatological advance report for August 2023
(AEMET Delegación Territorial en Madrid, published 2023-09-11; archived at
`data/raw/aemet_official_pdfs/AEMET_ACM_MAD_202308_avance_climatologico.pdf`).

Within that window, **21 August 2023** is used as the representative day: AEMET's
own Retiro station (indicativo 3195, inside Retiro Park, ~1 km from the study
area's western edge) recorded its August monthly maximum of **40.0 °C** that day.
August 2023 as a whole was independently confirmed extremely anomalous: mean
monthly temperature at Retiro was the highest in a series dating to 1920, and the
month's mean-maximum anomaly (+2.4 °C over the 1991–2020 reference period) was the
warmest on record at that station since 1961.

**Why this episode qualifies as extreme heat, not an arbitrarily chosen hot day:**
it is an AEMET-designated episode (not a single spike this project labelled itself),
it is corroborated by two independent official metrics (Retiro's absolute daily max
and the region's monthly-mean anomaly), and it sits inside a month AEMET itself
classified "EXTREMADAMENTE CÁLIDO" for the whole Comunidad de Madrid.

### Timestamps

Three real, actually-observed hourly readings from **Madrid/Barajas** (AEMET /
WMO station 08221, ICAO LEMD), the nearest station with a genuine (non-modelled)
long-run hourly observation record — see `docs/PHASE1_DATA_PROVENANCE.md` for why
Retiro's own hourly series was not usable. All times are **Europe/Madrid local
time (CEST, UTC+2)** on 2023-08-21; the raw file's `hour_utc` column is UTC and is
converted by adding 2 hours.

| Local time | UTC hour | Air temperature | AEMET Madrid-Metropolitana hazard band |
|---|---|---|---|
| 12:00 | 10:00 | 34.2 °C | LOW (below 36 °C amarillo) |
| 15:00 | 13:00 | 38.8 °C | ELEVATED (36–39 °C, amarillo) |
| 18:00 | 16:00 | 40.5 °C | SEVERE (39–42 °C, naranja) |

These three clock times were fixed by the task specification (~12:00, ~15:00,
~18:00) before the data was pulled, so they were not cherry-picked to produce a
particular result. No timestamp in this triplet happened to reach AEMET's red
(≥42 °C) threshold, even though the day's true peak (40.5 °C, at 18:00 UTC+2 in
this station's series) came close — this is reported as a real limitation in
§7 below and in `docs/PHASE1_VALIDATION_REPORT.md`, not smoothed over.

## 4. Tourism assets

27 real, named locations inside the study area, every one sourced from
OpenStreetMap (ODbL) via the public Overpass API (query and raw JSON preserved at
`data/raw/osm/`, fetched 2026-08-17). No point was invented, relocated, or
estimated. Full list with real coordinates, categories, indoor/outdoor flag, exact
OSM source id, and curation rationale: `data/processed/pilot_assets.csv` (built by
`src/build_pilot_assets.py`, which fails loudly if a curated OSM id is missing from
the source extract).

| Category | Count | Examples |
|---|---:|---|
| museum_indoor | 8 | Prado, Reina Sofía, Thyssen, CaixaForum, Naval, Antropología, Artes Decorativas, Real Fábrica de Tapices |
| transit_hub / transit_hub_green | 5 | Atocha main station, Estación del Arte, Retiro & Banco de España metro, Atocha's indoor Jardín Tropical |
| monument_outdoor | 6 | Puerta de Alcalá, Fuente de Cibeles, Fuente de Neptuno, Estatua de Goya (Prado forecourt), Palacio de Cibeles, Real Observatorio |
| park_general / garden_outdoor / outdoor_pavilion_shaded / outdoor_attraction_mixed_shade | 8 | Parque del Retiro, Real Jardín Botánico, Palacio de Cristal, Jardines de Cecilio Rodríguez, La Rosaleda, Jardín del Parterre, Monumento a Alfonso XII, Jardines del Arquitecto Herrero Palacios |

13 indoor / 14 outdoor. This set was hand-curated (not a raw dump of all 483 OSM
elements in the box) specifically to span the brief's required adaptation
conditions: outdoor attractions, shaded outdoor spaces, green areas, indoor
attractions, transport-accessible alternatives, poor-shade sites, and
strong-vegetation sites. Which of these last two labels actually applies to each
site is **not** asserted by hand at curation time — it is computed in §5 from real
measured data, so the pilot-set design does not leak into the classification result.

## 5. Baseline decision architecture (constraint-first, Option B)

Per `docs/METHOD_OPTIONS.md`'s recommendation, this baseline uses **no weighted
composite score**. Every classification is the output of an ordered sequence of
explicit, separately justified pass/fail gates. Full threshold definitions and
citations are centralised in `src/thresholds.py` (imported by, not duplicated in,
the pipeline code) so there is a single source of truth for every number used.

### 5.1 Meteorological hazard gate

*(Renamed from "Thermal hazard gate" in Phase 1.1, Audit 1, for terminological
precision — the thresholds and logic below are unchanged from the original
Phase 1 run.)*

Input: real hourly air temperature, Madrid/Barajas station (§3). As of Phase
1.1, every output row also carries a `station_representativeness_note`
quantifying Barajas's agreement with Retiro's official figures (+0.5 °C at
daily-max, +0.11 °C at monthly-mean for the episode/month used here); real
Retiro hourly data was sought and found unobtainable — see
`docs/PHASE1_1_BASELINE_HARDENING.md` Audit 1 for the full attempt log.

Bands: **LOW / ELEVATED / SEVERE / EXTREME**, using AEMET's own official
Meteoalerta maximum-temperature warning thresholds for zone 722802 "Metropolitana y
Henares" (covers the city of Madrid): amarillo 36 °C, naranja 39 °C, rojo 42 °C.
Source: `data/raw/aemet_official_pdfs/AEMET_METEOALERTA_ANX1_Umbrales_y_niveles_de_aviso.pdf`.

This is an **ambient air-temperature meteorological hazard classification**,
classifying a station reading against an official civil-protection warning
scale — it is not, and must never be read as or substituted for, a
thermal-comfort index (UTCI, PET, WBGT). It does not account for radiation,
wind, or humidity — see §7. The EXTREME band was implemented but untested by
this baseline's three fixed timestamps; it is now empirically validated
against a real 2021-08-14 AEMET-confirmed reading in Phase 1.1 Audit 2
(`data/processed/extreme_branch_stress_test_2021-08-14.csv`).

### 5.2 Exposure gate (outdoor assets only)

Proxy variable: count of real OSM `natural=tree` points (n=1,353 in the study
area) within the asset's real extent — a 50 m radius buffer around the asset point
for monument/building-type assets, or the asset's actual OSM polygon (buffered
+15 m) for park/garden-type assets whose real footprint was fetched separately
(`data/raw/osm/osm_green_polygons_raw.json`, `src/build_green_polygons.py`).

Bands: **LOW / MODERATE / HIGH** exposure (well-shaded / moderate / poor-shade),
assigned by **tercile of the pilot sample's own measured tree_count distribution**
(q1 = 0.33, q2 = 3.67 trees). This is explicitly an empirical split of this
pilot's own data, not a literature constant — no published "trees per 50 m near a
tourism POI" shade-sufficiency threshold exists to cite. Sensitivity of this
choice is examined in `docs/PHASE1_VALIDATION_REPORT.md`.

**Safeguard rule (present in the code, did not need to fire in the final run):**
an explicit override exists for the case where a real, officially-tagged
park/garden polygon's on-site tree count lands in the bottom tercile despite the
site being a documented green space — the rule holds such a site at MODERATE
exposure with confidence downgraded to LOW rather than accepting an
implausible HIGH ("poor shade") reading at face value (`src/thresholds.py:
GREEN_LAND_USE_CATEGORIES`). This was written after an early build genuinely hit
the case (both Retiro gardens above returned zero mapped trees under the initial,
tighter study-area box in §2, before the widened re-fetch recovered their real
tree data — 4 and 22 trees respectively). In the final run reported here the
widened box resolved the underlying data gap directly, so the override rule did
not need to activate for any asset; it is kept in the pipeline as a documented
safeguard against the same class of problem recurring with different assets or
data updates, and its non-triggering is itself checked implicitly by
`tests/test_outputs.py`.

Indoor assets bypass this gate entirely (§5.4).

### 5.3 Adaptation-resource indicator

*(Demoted from "Adaptation-resource gate" in Phase 1.1, Audit 3: three
independent real-data tests found this input non-discriminatory at any
defensible distance threshold, so its exclusion rule was removed. The
computation below is unchanged and remains in every output row as real,
reported context — it is simply no longer decision-relevant. Full detail in
`docs/PHASE1_1_BASELINE_HARDENING.md` Audit 3 and
`docs/PHASE1_1_SENSITIVITY_REPORT.md` §3–4.)*

Inputs: real distance (metres, projected CRS EPSG:25830) from the asset to the
nearest OSM drinking-water/fountain point (n=139) and nearest OSM rail/metro/bus
transit point (n=107; `data/interim/water_points.geojson`,
`data/interim/transit_points.geojson`).

Bands: **GOOD** (water ≤250 m AND transit ≤400 m) / **LIMITED** (one of the two) /
**POOR** (neither). 400 m follows standard pedestrian-catchment practice (≈5-minute
walk at ~4.8 km/h, widely used for transit-stop and amenity-catchment analysis).
250 m for water is a tightened version of the same heuristic (≈3-minute walk),
reflecting the acute hydration urgency emphasised in regional heat-health guidance
during extreme-heat episodes. POOR never occurred for any of the 27 pilot assets,
nor for 6 additional real assets tested in a bounded ring extension beyond the
study area (Phase 1.1 Audit 3) — even tightening thresholds well below these
values across a grid search produced no POOR case until the transit threshold
fell to ≤100 m, below any cited walkability standard used in this project.

### 5.4 Tourism feasibility gate (final decision)

Applies the hazard/exposure/adaptation states through an ordered rule table (full
text, with every threshold value interpolated in, in `src/thresholds.py`;
implementation in `src/build_classifications.py:feasibility_decision()`). First
matching rule wins — this is a decision tree, not a score:

- **Indoor assets:** FEASIBLE unless hazard is SEVERE/EXTREME, in which case
  FEASIBLE WITH CONDITIONS (reason: A/C operational status is not verified in any
  source used — `docs/DATA_SOURCE_INVENTORY.csv` notes Madrid's museums open-data
  layer does not state A/C status — and outdoor approach/queueing exposure is a
  real residual risk not captured by an "indoor" flag alone).
- **Outdoor assets:** EXTREME hazard → NOT RECOMMENDED unconditionally. SEVERE
  hazard → NOT RECOMMENDED if exposure is HIGH (poor shade), else FEASIBLE WITH
  CONDITIONS. *(Phase 1.1: the previous "...or adaptation is POOR" clause was
  removed — see §5.3.)* ELEVATED hazard → always FEASIBLE WITH CONDITIONS.
  LOW hazard → FEASIBLE, or FEASIBLE WITH CONDITIONS if exposure is HIGH.
- **INSUFFICIENT EVIDENCE:** reserved for any row with a missing required input
  (defensive path; did not trigger for this complete 81-row pilot run — see
  `docs/PHASE1_VALIDATION_REPORT.md`).

### 5.5 Evidence-confidence

Categorical **HIGH / MEDIUM / LOW**, weakest-link rule (documented, not hidden):
MEDIUM by default (every input here is real but carries at least one caveat: the
hazard reading is real and direct but ~9 km displaced from the study area; the
exposure proxy is a real point count but a proxy for actual canopy/shadow; the
adaptation-resource network is real but its completeness is not independently
audited). Downgraded to LOW when (a) the row is an indoor asset at SEVERE/EXTREME
hazard (the unverified A/C assumption becomes decision-relevant), or (b) the
site's exposure reading required the safeguard override in §5.2 (did not trigger
in this run). **No row in this Phase 1 baseline reaches HIGH** — reported as a
finding, not a shortcoming, in `docs/PHASE1_VALIDATION_REPORT.md`.

## 6. Outputs

- `data/processed/study_area.geojson`
- `data/processed/pilot_assets.csv` (27 rows)
- `data/processed/pilot_classifications.csv` (81 rows = 27 assets × 3 timestamps)
- `outputs/maps/01_study_area.png` … `04_feasibility_by_timestamp.png`

Phase 1.1 additions (see `docs/PHASE1_1_BASELINE_HARDENING.md`):
`data/processed/extreme_branch_stress_test_2021-08-14.csv`,
`data/processed/audit3_ring_extension.csv`,
`data/processed/audit4_proxy_comparison.csv`,
`data/processed/audit4_unstable_assets.csv`,
`outputs/maps/05_audit4_unstable_assets.png`.

## 7. What this baseline does NOT claim

- It does **not** compute UTCI, PET, WBGT, or Tmrt. The hazard gate is ambient air
  temperature only, explicitly labelled as such throughout.
- It does **not** model shade, shadow geometry, or canopy cover. Tree count is a
  documented proxy, not a shadow simulation. Phase 1.1 Audit 4 quantified this
  proxy's fragility directly: swapping it for a different, equally defensible
  real-data proxy (green-polygon coverage) changes 19% of outdoor classifications,
  and 71% of outdoor assets are sensitive to proxy choice across three tested
  alternatives — see `docs/PHASE1_1_SENSITIVITY_REPORT.md` §5.
- It does **not** infer, predict, or claim anything about actual tourist behaviour,
  flows, or preferences.
- It does **not** claim the three chosen clock-times are the day's true hazard
  peak — the real hourly series shows the maximum at Barajas that day fell at
  18:00 local (40.5 °C), matching one of the three required timestamps, but the
  method did not search for the peak; it used the timestamps specified in the task.
- It uses **no machine learning** and **no LLM** in the decision logic.

## 8. Reproducibility

Every derived file is regenerable from `data/raw/` by running, in order:
`src/define_study_area.py` → `src/build_pilot_assets.py` →
`src/build_supporting_layers.py` → `src/build_green_polygons.py` →
`src/build_classifications.py` → `src/make_maps.py`. No manual editing of any
`data/processed/` or `data/interim/` file is required or expected.
