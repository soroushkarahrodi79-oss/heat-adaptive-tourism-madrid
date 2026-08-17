# PHASE2_INPUT_FEASIBILITY.md — HATI-Madrid Phase 2, Step 0

Version 1.0 · 2026-08-17. Gate in effect at start: **GO TO SOLWEIG / UTCI**
(`docs/PHASE1_2_SHADE_EVIDENCE_GATE.md`). This document is the mandatory Step
0 audit, run **before** any SOLWEIG execution, per the task specification's
explicit "STOP and report the blocking input" instruction. No input below
was silently substituted with a weaker proxy — every acquisition is a real,
checked, cited source, and every gap is stated.

**Outcome: no critical input was found unobtainable. The gate did not need
to invoke STOP.** All geometry and meteorological inputs below are real data.

---

## Required-input checklist

| Input | Status | Source | Resolution |
|---|---|---|---|
| Digital Surface Model (buildings) | **Obtained** | IGN/CNIG MDS WCS, normalized building height model | 2.5 m native |
| Digital Terrain Model (bare earth) | **Obtained** | IGN/CNIG MDT WCS | 5 m native, resampled to 2.5 m |
| Building heights | **Obtained** | Same MDS building layer (height above ground, LiDAR-derived) | 2.5 m native |
| Tree/canopy heights | **Obtained** | IGN/CNIG MDS WCS, normalized vegetation height model | 2.5 m native |
| Vegetation representation | **Obtained** | Same layer, used directly as SOLWEIG's CDSM | 2.5 m native |
| Land-cover/surface representation | **Not acquired — documented simplification, not a blocker** | SOLWEIG's package default (no custom `land_cover` grid) | n/a |
| Meteorological forcing (Ta, RH, wind, pressure) | **Obtained (real observations)** | AEMET/Barajas, already used throughout Phase 1/1.1/1.2 | Hourly, real values at exact target timestamps |
| Meteorological forcing (solar irradiance) | **Obtained (estimated, not measured)** | pvlib Ineichen clear-sky model, real solar geometry, justified by confirmed clear-sky station weather codes | Instantaneous, computed per timestamp |
| CRS compatibility | **Resolved (required a fix)** | All IGN/CNIG WCS layers projected to EPSG:25830 | n/a |
| Temporal correspondence | **Assessed, gaps documented, none blocking** | See table below | n/a |

## Geometry sources — detail

### Digital Terrain Model (DEM)

- **Source:** IGN/CNIG public WCS, `https://servicios.idee.es/wcs-inspire/mdt`, coverage `Elevacion25830_5`.
- **Resolution:** 5 m native mesh, generated from PNOA-LiDAR (IGN's own product description: "Modelos Digitales del Terreno... procedentes de sensores LiDAR aerotransportados del proyecto PNOA-LiDAR").
- **Access:** No login required; public OGC WCS 2.0.1, standards-compliant, `GetCapabilities`/`DescribeCoverage`/`GetCoverage` all worked directly.
- **Access date:** 2026-08-17.
- **Licence:** IGN/CNIG open data (free reuse, attribution).
- **Clip:** Requested directly for the study-area bounding box in EPSG:25830 (`440941,4472831,442525,4474706`) — no city-wide download.
- **Real values obtained:** min 607 m, max 681 m elevation — consistent with Madrid city centre's known real elevation range.
- **File:** `data/raw/pnoa_lidar/dem_wcs_5m.tif`.

### Digital Surface Model components (building + vegetation)

- **Source:** IGN/CNIG public WCS, `https://wcs-mds.idee.es/mds`, coverages `mdsn_e025` (building, normalized/height-above-ground) and `mdsn_v025` (vegetation, normalized/height-above-ground).
- **Resolution:** 2.5 m native mesh.
- **Origin:** "Modelo Digital de Superficies normalizado (clase edificación y vegetación)... generados a partir del MDT-LIDAR 1ª cobertura" (IGN's own product description) — derived from the **first PNOA-LiDAR coverage** (nominally 2008–2015; see Temporal correspondence below).
- **Access:** No login required; same WCS mechanism as the DEM.
- **Access date:** 2026-08-17.
- **Licence:** IGN/CNIG open data (free reuse, attribution).
- **Real values obtained:** building height 0–65 m (27.4% of pixels >0.5 m, consistent with a mixed plaza/park/building study area); vegetation height 0–47 m (43.5% of pixels >0.5 m, consistent with Retiro's dominance of the study area).
- **Files:** `data/raw/pnoa_lidar/building_ndsm_025.tif`, `veg_ndsm_025.tif`.

**A newer product exists but was not used, for a documented, checked reason:**
a second-coverage (2015–2021) version of the same normalized building/
vegetation models exists on `centrodedescargas.cnig.es`
("MDSnV2,5"/"MDSnE2,5", segunda cobertura), but is distributed only as
individual MTN50-sheet downloads through an interactive catalogue with no
disclosed coordinate-based API — unlike the WCS used above, it cannot be
clipped directly to the pilot bbox without either browsing the interactive
map or guessing a sheet code. Given Step 0's explicit instruction to "clip
acquisition to the pilot area as early as technically possible" and avoid
unnecessary city-scale downloads, the WCS-served first-coverage product was
used as the pragmatic, real, zero-city-wide-download choice, and the
resulting ~8–15 year temporal gap is treated as a first-class limitation
(§ Temporal correspondence, `docs/PHASE2_VALIDATION_REPORT.md`), not hidden.

### CRS fix (documented, not a data-quality problem)

Both IGN/CNIG WCS services return GeoTIFFs tagged with a malformed generic
`LOCAL_CS["ETRS89 / UTM zone 30N"]` WKT string rather than a proper
`PROJCS`/EPSG:25830 definition, which SOLWEIG's CRS validator (correctly)
rejects as "not projected." This is a **metadata relabelling**, not a
reprojection: the numeric coordinate values returned by the WCS exactly
match the requested EPSG:25830 bounding box, confirmed by inspection. The
fix (`src/build_solweig_geometry.py:CRS_FIX`) explicitly re-tags the CRS to
`EPSG:25830` without altering any pixel value or coordinate.

### Composite DSM

SOLWEIG's `dsm` parameter (absolute-elevation ground+building surface) is
built as `DEM (resampled to 2.5 m) + building nDSM`, both from the sources
above — see `docs/PHASE2_SOLWEIG_METHOD.md` for the exact construction and
resolution justification. `dem` and `cdsm` (canopy height, "relative to
ground" convention) are passed to SOLWEIG separately, per its documented
API (`SurfaceData.prepare(dsm=..., cdsm=..., dem=..., cdsm_relative=True)`).

### Land cover (documented simplification)

SOLWEIG's `land_cover` parameter (albedo/emissivity by surface type) is
optional and was **not supplied** — no open, study-area-clipped land-cover
raster at matching resolution was acquired within this bounded spike. This
means SOLWEIG's package-default ground-surface assumption is used uniformly
across the study area rather than a site-specific pavement/grass/water
classification. This is stated explicitly as a simplification carried into
`docs/PHASE2_VALIDATION_REPORT.md`, not a silent omission — Step 0 judged it
non-blocking because `land_cover` is documented as optional in the
package's own API and its absence does not prevent Tmrt/UTCI calculation,
only refines it.

## Meteorological forcing — detail

Real observed inputs (air temperature, relative humidity, wind speed,
pressure) are the same Madrid/Barajas hourly archive already used and
fully documented throughout Phase 1/1.1/1.2
(`data/raw/episode_aug2023_barajas_raw.csv`) — no new station, no new
representativeness question beyond what Phase 1.1 Audit 1 already
established and quantified.

**Global horizontal irradiance (GHI)** is the one genuinely new forcing
variable this phase requires and the archive does not contain (Meteostat's
hourly bulk product has no pyranometer column — see `data/raw/README.md`).
It is **estimated**, not measured: pvlib's Ineichen clear-sky model, using
real solar geometry (true date/time/location) and pvlib's bundled real
Linke-turbidity climatology, justified by the archive's own confirmed
"clear" weather condition code (`coco=1`) at Madrid/Barajas for all three
target hours on 2023-08-21 — verified programmatically before use
(`src/build_met_forcing.py` asserts this). Full detail in
`docs/PHASE2_SOLWEIG_METHOD.md` §Meteorological forcing.

## Resolution justification

**Working resolution: 2.5 m.** This is within the task's target 2–5 m range
and is not the finest technically available (the source LiDAR point density,
5 pts/m² for the newest coverage, would in principle support sub-metre
rasters). 2.5 m is justified as the **minimum needed** to resolve:
- Building edges: real building footprints in this area (Prado/Retiro
  perimeter buildings, museum blocks) are tens of metres across — 2.5 m
  resolves their edges and orientation without needing to be sub-metre.
- Pedestrian open space: plazas and paths in the study area are typically
  several metres to tens of metres wide — fully resolved at 2.5 m.
- Meaningful tree-canopy structure: individual mature tree crowns in Retiro
  are typically 5–15 m across — resolvable at 2.5 m (a crown spans several
  pixels), whereas 5 m would only marginally resolve a single crown and 10 m
  would merge adjacent crowns.
- Shade differences relevant to outdoor tourism exposure: the 2.5 m choice
  additionally matches the **native** resolution of the two geometrically
  decisive inputs (building and vegetation normalized height models), so no
  resampling loss is introduced on the layers that most directly drive
  shadow-casting geometry — only the smoother, low-frequency DEM is
  upsampled (from its native 5 m).

A resolution-sensitivity check is reported in
`docs/PHASE2_VALIDATION_REPORT.md`.

## Temporal correspondence table

| Input | Reference vintage | Gap to episode (2023-08-21) |
|---|---|---|
| Meteorological forcing (Ta/RH/wind/pressure) | 2023-08-21, real hourly readings | 0 (exact) |
| Meteorological forcing (GHI) | Computed for the true date/time | 0 (astronomically exact; physically estimated, not measured — see above) |
| DEM (terrain) | PNOA-LiDAR-derived, exact campaign year not stated by the WCS service description | Terrain is stable over time; negligible practical gap expected |
| Building nDSM | PNOA-LiDAR 1ª cobertura (2008–2015) | ~8–15 years. Central Madrid's Prado–Retiro–Atocha core is a protected heritage zone with little large-scale new construction in this period — a real but likely small-impact limitation, stated not assumed away |
| Vegetation nDSM (CDSM) | PNOA-LiDAR 1ª cobertura (2008–2015) | ~8–15 years — the **largest and most consequential temporal gap in this phase**. Trees grow, are pruned, are removed, and are planted over a decade; canopy height and extent in 2023 almost certainly differ from this source in ways this project cannot quantify. Treated as a first-class limitation, not a footnote — see `docs/PHASE2_VALIDATION_REPORT.md` |

This continues the same temporal-honesty discipline established in
`docs/PHASE1_2_TEMPORAL_ALIGNMENT.md`: every input's vintage is stated, no
input is implied to represent August 2023 conditions unless it demonstrably
does.
