# GATE3A_METHOD — First thermal experiment / pipeline falsification

**Version 1.0 · 2026-09-15.** First permitted thermal computation. Purpose: determine
whether the frozen Gate-2 evidence stack produces a reproducible, internally coherent,
time-resolved modeled comparison **without violating the Path-B claim ceiling** — NOT to
prove a route cooler. Baseline only; no perturbation matrix; no path optimisation; no
scientific winner.

## Inputs (frozen Gate-2, + AMENDMENT_001)
- **Routes:** frozen `OD1_Route_A_epsg25830.geojson` (2657.8 m) and
  `OD1_Route_B_epsg25830.geojson` (2365.7 m) — hashes verified (3A.1).
- **Study day / departures:** 2023-08-24; **14:00 and 17:00 Europe/Madrid as departure
  times.**
- **Forcing:** Barajas 08221 hourly, linearly interpolated to each field timestamp;
  clear-sky GHI via pvlib Ineichen. Independent check: Escuelas Aguirre (representativeness).
- **Geometry (frozen architecture):** nSH = **MDS 2023 − MDT 2023** (AMENDMENT_001:
  terrain MDT 2019→2023, user-approved, pre-thermal); building height = nSH within
  **Catastro INSPIRE footprints**; canopy height = nSH within a vegetation mask (OSM green
  + municipal tree buffers + Copernicus TCD ≥ 30 %), outside footprints.
- **Wind:** uniform station wind (E-P3 demoted). **Radiation:** modeled clear-sky.

## Model
`solweig` 0.1.0b92 (UMEP-dev standalone), Python 3.12 (`.venv_solweig`); UTCI computed by
SOLWEIG from Tmrt. Same package/version as the locked pilot.

## Spatial domain (3A.2)
EPSG:25830 bbox x[440996, 441736] y[4472668, 4474830]; **370 × 1081 px @ 2 m**. Bounded to
Route A + Route B + a **150 m shadow buffer** (justified: ≤ ~50 m heritage-core building at
the 17:45 solar altitude ~36° → ~70 m shadow; 150 m is conservative), fixed **before** any
thermal output. **Not** city-wide. Resolution 2 m: sidewalk-scale, SVF-tractable over the
domain; fixed before results. MDS/MDT COG tiles read **windowed via `/vsicurl`** (not
bulk-downloaded).

## Time-resolved traversal (3A.3, frozen Gate-2 §0.1)
Thermal fields at **Δt = 15 min**: 14:00/14:15/14:30/14:45 and 17:00/17:15/17:30/17:45
(8 SOLWEIG runs; SVF computed once). Each route densified to **Δs = 5 m**; segment
traversal time `t_k = departure + cumulative_distance / v` at baseline **v = 1.25 m/s**
(midpoint of the frozen E-P6 1.1/1.4 range); UTCI/Tmrt sampled from the field **nearest
t_k** via a **10 m buffer-mean** (locked-pilot PRIMARY_BUFFER_M). Solar geometry/shadows
therefore evolve along the trip. A single static field is **not** applied to the whole
walk. ±7.5 min discretization uncertainty is QA'd (`GATE3A_QA_REPORT.md`).

## Metrics (3A.7, frozen Gate-2)
Computed exactly per `GATE2_METRIC_SPEC.md`, with **THERMAL INTENSITY** (M2 time-weighted
mean UTCI, M3 distribution, M5 p95 descriptor) reported **separately** from **EXPOSURE
DURATION** (M1 trip duration, M4 minutes/proportion per UTCI stress category). No composite
score; nothing labeled a physiological dose; a shorter route is not called thermally
superior. UTCI categories per Bröde et al. 2012 (+26/+32/+38/+46 °C).

## Reproducible pipeline
1. `py src/gate3a_build_geometry.py` → dem/dsm/cdsm (2 m) + masks + provenance.
2. `(.venv_solweig) python src/gate3a_run_solweig.py` → forcing + 16 Tmrt/UTCI rasters.
3. `py src/gate3a_sample_metrics.py` → baseline metrics + temporal QA.
All three set `PROJ_DATA`/`PROJ_LIB`/`GDAL_DATA` to the interpreter's bundled rasterio
data (system PostGIS/pyproj PROJ are version-incompatible). Hashes in
`GATE3A_MODEL_PROVENANCE.json`. Large rasters are gitignored; hashes + windowed-acquisition
commands recorded instead.
