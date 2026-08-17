# PHASE1_2_SHADE_EVIDENCE_GATE.md — HATI-Madrid Phase 1.2

Version 1.0 · 2026-08-17. Gate in effect at start: **REVISE BASELINE AGAIN**
(`docs/PHASE1_1_GATE.md`), whose sole open condition was shade/exposure-proxy
robustness (Phase 1.1 Audit 4: 71% of outdoor assets proxy-sensitive across
tree-count / green-coverage / building-density).

**Core question:** do independent, defensible shade/vegetation proxies
produce sufficiently similar tourism-feasibility classifications for the
Prado–Retiro–Atocha pilot? If yes, retain the simpler architecture. If no,
stop proxy refinement and recommend SOLWEIG/Tmrt/UTCI.

---

## 1. The four proxy families

### P0 — OSM tree-count baseline (frozen historical reference)

Exact Phase 1 computation, unmodified: real OSM `natural=tree` points within
a 50 m buffer (or the asset's own polygon+15 m for the 8 park/garden assets).
Reused verbatim from `data/processed/pilot_classifications.csv` — **not
recomputed or improved in this phase**, per the task specification.

### P1 — Madrid official tree inventory

| Field | Value |
|---|---|
| Dataset | "Arbolado en parques y zonas verdes de Madrid (detalle)" (CKAN id `300761-0-arbolado-especies`), accessed via its live backing service, `MEDIO_AMBIENTE/ARBOLADO` ArcGIS MapServer, `sigma.madrid.es` |
| Owner | Ayuntamiento de Madrid, Dirección General de Gestión del Agua y Zonas Verdes |
| Dataset date | Best available evidence: published 2025-07-09, last updated 2026-07-27 (CKAN metadata); no confirmed per-record date field — see `docs/PHASE1_2_TEMPORAL_ALIGNMENT.md` |
| Access date | 2026-08-17 |
| Licence | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| Geometry type | Point (one record per real, individual tree) |
| Attributes used | `NOMBRE_ESPECIE` (species), `NOMBRE_COMUN`, `ALTURA` (height, m), `NOMBRE_DISTRITO`, `NOMBRE_BARRIO` |
| Spatial coverage (this project) | Study-area bounding box only, queried directly (not a city-wide download) |
| Records retrieved | 40,840 real trees — 6,089 from layer 11 "Arbolado de alineación y Zonas Verdes" (street/alignment + green-zone) and 34,751 from layer 8 "Arbolado Parques Históricos" (historic/singular parks, covers Retiro) |
| Limitations | (a) No confirmed 2023 vintage exists as geometry — see §Temporal below; (b) **administrative coverage gap**: the Real Jardín Botánico (CSIC/national institution, not municipally maintained) has **zero** municipal tree records within 100 m of its OSM-derived asset point despite being a real, densely-planted botanical garden — confirmed by checking radii out to 300 m, where hundreds of trees appear just outside the garden's walls in the surrounding municipal streets/park. This is a genuine administrative-boundary effect of "municipal maintenance" as the inventory's inclusion criterion, not a data quality defect. |

Full attempt log for why a true 2023 archive was not used (a 2023-dated
resource exists but is a species-count summary table, not geolocated
per-tree data): `docs/PHASE1_2_TEMPORAL_ALIGNMENT.md`.

**Not treated as measured shade** — this is an improved tree-*presence*
inventory (real point locations, real species, sometimes real height), not a
canopy or shadow measurement.

### P2 — Copernicus HRL Tree Cover Density

| Field | Value |
|---|---|
| Product | High Resolution Layer, Tree Cover Density, reference year **2018** |
| Reference year | 2018 (the newest vintage reachable without account registration — see attempt log below) |
| Resolution | 10 m native |
| CRS | Exported in WGS84 (EPSG:4326) via on-the-fly reprojection from the source service's Web Mercator (EPSG:3857) storage |
| Value semantics | Unsigned 8-bit, 0–100 = percent tree canopy cover per pixel; observed range in the exported clip: 0–100, mean 23.4%, mode 0 (non-treed surface, expected for a study area dominated by plazas/streets/water) |
| Source | EEA public ImageServer, `image.discomap.eea.europa.eu/arcgis/rest/services/GioLandPublic/HRL_TreeCoverDensity_2018/ImageServer` — no authentication required |
| Access date | 2026-08-17 |
| Licence | Copernicus/EEA standard open licence (free, full, open access; attribution required) |
| Preprocessing | `exportImage` clip to the exact study-area bounding box (210×225 px at 10 m), nearest-neighbour resampling, no reclassification or smoothing applied |
| Known urban limitations | 10 m pixels blur individual tree crowns into their surroundings at street scale; the product measures canopy presence from an overhead/satellite viewing angle and carries no information about sun angle, time of day, or ground-level shadow — explicitly **not** used or described as instantaneous shade anywhere in this project |

**Attempt log — why 2018, not 2023:** the task's stated preference (2023
status layer via the current VLCC/GeoVille infrastructure,
`geoserver.vlcc.geoville.com`) was attempted first: the connection timed out
(21 s, `Could not connect to server`) from this project's network
environment. The official CLMS product page returned HTTP 401 to automated
access. The EEA's public, no-login ImageServer catalogue
(`image.discomap.eea.europa.eu`) was enumerated in full; its newest Tree
Cover Density product is 2018. This is the **largest temporal gap in this
comparison (5 years)** and is treated as a first-class caveat throughout this
document, not a footnote — see §5 and §7.

**Not treated as instantaneous shade** — canopy-cover density is reported
strictly as canopy-cover density.

### P3 — Green-polygon coverage (retained from Phase 1.1, unchanged model)

Percent of the asset's buffer covered by real OSM `leisure=park/garden` +
`natural=wood` + `landuse=forest` polygons (161 polygons, full geometry,
study-area extent). Recomputed at the Phase 1.2 pre-registered 50 m buffer
using the identical function from `src/audit4_shade_proxy_test.py`, per the
task's instruction to retain this proxy as-is.

**Building density excluded from this comparison.** Phase 1.1 Audit 4 already
demonstrated it is conceptually unsuitable for park interiors (zero buildings
correctly indicates "deep in parkland," not "poor shade" — it inverted for 5
of the pilot's best-documented shaded gardens). It remains archived at
`data/processed/audit4_proxy_comparison.csv` for historical record but plays
no role in this phase's gate decision, per the task specification.

## 2. Common spatial unit

**Pre-registered before any proxy value was computed** in
`src/shade_proxy_prereg.py` (see that file's docstring for the full,
timestamped rationale): a uniform **50 m circular buffer** around each
outdoor asset's representative point, applied identically to P1, P2, and P3.
P0 is exempt (frozen historical method, see §1). 25 m and 100 m buffers were
also run as a **documented sensitivity check only** — never used to select a
more favourable buffer after seeing results (see §5, buffer sensitivity).

## 3. Normalisation / classification

No composite score or weighting anywhere. Each proxy's raw value is
translated to LOW / MODERATE / HIGH exposure by an **empirical tercile split
of that proxy's own distribution across the 14 outdoor pilot assets** — the
same method used throughout Phase 1/1.1, explicitly labelled here (again) as
an empirical sensitivity-grade category, not a physically justified
threshold, because no literature threshold exists for "trees per 50 m" or
"% canopy per 50 m" as a shade-sufficiency criterion for a tourism POI. P0
and P3 reuse their already-published cutpoints verbatim; only P1 and P2 have
fresh cutpoints (computed once, at the pre-registered buffer, before results
were inspected): P1 q1=6.33, q2=68.67 trees; P2 q1=25.08%, q2=36.85%. Every
proxy's exposure_state feeds the identical, unmodified
`feasibility_decision()` logic from Phase 1/1.1 (meteorological hazard gate;
adaptation indicator remains demoted). Real 2023-08-21 timestamps
(12:00/15:00/18:00 local) — no new episode introduced.

## 4. Temporal honesty

Full table and attempt logs: `docs/PHASE1_2_TEMPORAL_ALIGNMENT.md`. Summary:
meteorology is exact (0-year gap, real historical archive); P0/P3 (OSM) carry
a ~3-year gap already documented in Phase 1; P1 (Madrid trees) carries an
estimated ~2-3 year gap (exact vintage not confirmable, bounded above by the
dataset's 2025-07-09 publication date); **P2 (Copernicus TCD) carries a
5-year gap**, the largest of any layer, because no 2021+ vintage was
reachable without account registration.

## 5. Agreement analysis

Full detail: `outputs/tables/shade_proxy_agreement.csv`,
`data/processed/shade_proxy_comparison.csv`. Outdoor rows: n=42 (14 assets ×
3 timestamps).

**1. Raw percentage agreement (feasibility_state), all pairs:**

| Pair | Agreement | Cohen's κ |
|---|---:|---:|
| OSM vs Madrid | 81.0% | 0.616 |
| OSM vs TCD | 81.0% | 0.616 |
| OSM vs green | 81.0% | 0.616 |
| **Madrid vs TCD** | **71.4%** | **0.423** |
| Madrid vs green | 81.0% | 0.616 |
| TCD vs green | 81.0% | 0.616 |

κ=0.423 falls in the "moderate" band (Landis & Koch); κ=0.616 in "substantial."
None reach "almost perfect" (>0.80). Kappa is reported alongside, not relied
on alone, per the task specification.

**2. Confusion matrix, Madrid vs TCD (the gate-critical pair):**

```
TCD                        FEASIBLE  FEASIBLE WITH CONDITIONS  NOT RECOMMENDED
Madrid FEASIBLE                   6                          3                0
Madrid FEASIBLE WITH COND.        3                         22                3
Madrid NOT RECOMMENDED            0                          3                2
```

**3. Per-asset instability:** **8 of 14 outdoor assets (57.1%)** have a
feasibility classification that differs between at least two of the four
proxy families at at least one timestamp: A14 (Puerta de Alcalá), A16
(Fuente de Neptuno), A17 (Estatua de Goya), A18 (Palacio de Cibeles), A19
(Real Observatorio), A21 (Real Jardín Botánico), A25 (Jardín del Parterre),
A26 (Monumento a Alfonso XII). Map: `outputs/maps/shade_proxy_instability.png`.

**4. Direction of disagreement:** **0 of 42 rows** show a MAJOR disagreement
(a 2-level jump spanning FEASIBLE ↔ NOT RECOMMENDED). All 16 disagreeing rows
are MINOR (adjacent levels only, e.g. FEASIBLE ↔ FEASIBLE WITH CONDITIONS, or
FEASIBLE WITH CONDITIONS ↔ NOT RECOMMENDED). This is a genuine point in the
baseline's favour and is not minimised: **no asset was ever called clearly
safe by one proxy and clearly unsafe by another.**

**5. Agreement by morphology (Madrid vs TCD):**

| Morphology | Agreement | n |
|---|---:|---:|
| street_corridor | 100.0% | 3 |
| park_garden | 77.8% | 18 |
| plaza_hardscape | 66.7% | 12 |
| attraction_exterior | 55.6% | 9 |

Disagreement is not confined to one morphology — it is present, at varying
rates, in every category except the single-asset street_corridor group
(n=3, one asset, too small to generalise). Park interiors, the pilot's
best-vegetated sites, still show 22.2% disagreement even in their best
pairing.

**6. Timestamp-specific disagreement (Madrid vs TCD):** 12:00 → 57.1%,
**15:00 → 100.0%**, 18:00 → 57.1%. Agreement is not stable across the day;
it happens to peak exactly at the one timestamp (15:00, ELEVATED hazard)
where the feasibility rule table's own branching is least discriminating
(§`src/thresholds.py` rule 4/5) — i.e. the apparent 15:00 agreement is partly
an artefact of the decision rules collapsing more inputs to the same output
at that hazard level, not evidence the proxies agree better there.

**Systematic vs. random:** disagreement rates by morphology (44–67% across
three of four categories, only the 3-row street_corridor group at 0%
disagreement) show a **diffuse, not localised, pattern** — no single
morphology is uniquely responsible while the others are clean. This rules
out "fix one problem case type" as a viable next step; the disagreement is
spread across the pilot's structural diversity.

**Buffer sensitivity (not the gate decision):** Madrid vs TCD agreement at
25 m = 81.0%, at the pre-registered primary 50 m = **71.4%**, at 100 m =
81.0%. The pre-registered choice happens to show the *most conservative*
(lowest) agreement of the three — direct evidence against any suspicion that
50 m was chosen, consciously or not, to produce a favourable result. Critically,
**even the more favourable sensitivity buffers (81.0%) remain below the
predefined 85% threshold**, so the gate conclusion is robust to this choice
either way.

## 6. Predefined decision gate — evaluated exactly as specified in advance

| Condition | Threshold | Result | Met? |
|---|---|---|---|
| Agreement, Madrid tree inventory vs. Copernicus TCD | ≥85% | 71.4% (primary, pre-registered buffer); 81.0% (both sensitivity buffers) | **No**, at every buffer tested |
| No important outdoor asset differs by more than one feasibility level | 0 MAJOR jumps | 0 / 42 rows MAJOR | **Yes** |
| Outdoor assets materially proxy-sensitive | ≤20% | 57.1% (8/14) | **No** |
| No clear systematic failure for a particular morphology | — | Diffuse across plaza/park/attraction (44–67%); not localised to one type | Ambiguous, but moot (see below) |

The gate requires **BOTH** principal improved proxies (Madrid tree inventory
and Copernicus TCD) to satisfy **ALL** listed conditions. Two of four
conditions fail outright (agreement, proxy-sensitivity), by wide margins, at
every buffer size tested, including the two sensitivity buffers that were
not part of the pre-registered decision. Per the task's explicit rule: *"If
any major robustness condition fails, do NOT create additional proxy
families merely to rescue the baseline. The gate must become GO TO SOLWEIG /
UTCI."*

## 7. Verdict

# GO TO SOLWEIG / UTCI

Simple, open-data vegetation/shade proxies — even after acquiring two
genuinely independent, official/authoritative improvements over the original
OSM-tree-count baseline (a municipal per-tree inventory and a continental
satellite-derived canopy product) — do **not** converge closely enough to
support the tourism-feasibility decisions this project's constraint-first
architecture is meant to make. Madrid-vs-TCD agreement (71.4% at the
pre-registered buffer, 81.0% even under a more favourable sensitivity buffer)
falls well short of the predefined 85% bar, and well over half of outdoor
assets are materially proxy-sensitive. That instability is itself the Phase
1.2 result, exactly as the task specification anticipated it might be — it
is reported as a finding, not an obstacle to route around with a fifth proxy
family (which the task specification explicitly forbids doing).

One genuine point of reassurance survives: disagreement is consistently
*minor* (adjacent feasibility levels), never *major* (no asset swings from
uncontroversially safe to uncontroversially unsafe between proxies). This
bounds the practical severity of the instability, but does not satisfy the
predefined gate, which set its bar at overall agreement and asset-sensitivity
rate, not just at worst-case severity.

## 8. What SOLWEIG is expected to resolve that no further proxy can

The two candidate "improved" proxies disagree with each other not because
one is obviously wrong, but because a tree count and a canopy-density raster
are measuring genuinely different physical quantities (individual stems vs.
area-averaged cover) at genuinely different spatial and temporal
resolutions, neither of which encodes sun position, shadow geometry, or
building massing. No further point-count or coverage-fraction proxy can
adjudicate between them — only a model that ingests real geometry (building
and tree heights, canopy shape, solar path) and computes actual radiant
exposure, i.e. SOLWEIG-class Tmrt/UTCI modelling, can. This conclusion is
earned by the two real, good-faith proxy acquisitions and comparisons in this
phase, not asserted in place of doing them.
