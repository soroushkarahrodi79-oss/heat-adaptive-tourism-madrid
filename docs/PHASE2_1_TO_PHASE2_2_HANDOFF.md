# PHASE2_1_TO_PHASE2_2_HANDOFF.md — HATI-Madrid

Version 1.0 · 2026-08-17. Read this file first in any new conversation
continuing this project. It is a pointer document, not a replacement for
the underlying phase docs — follow the references for full detail.

---

## 1. Current scientific status

HATI-Madrid has run a real, reproducible pipeline from an open-data
constraint-first proxy baseline (Phase 1) through a real SOLWEIG physical
radiation model (Phase 2) to a robustness audit of that physical model
(Phase 2.1). The physical model **does add decision value** over the
simple proxy baseline, and its two central substantive findings (see §3)
are **robust** to the two most important tested input uncertainties. Its
**numeric precision near decision thresholds is not fully robust**,
because the real August 2023 episode was extreme enough that many readings
sit close to the UTCI "Extreme heat stress" ceiling. The current gate
verdict is **MODEL NEEDS REVISION** (`docs/PHASE2_1_GATE.md`) — a call to
harden the decision architecture's threshold-handling and close a specific,
identified geometry gap, **not** a rejection of the physical-modelling
approach.

## 2. Completed phases and their final gates

| Phase | Verdict | Doc |
|---|---|---|
| Phase 0 | GO WITH MODIFICATIONS | `docs/FEASIBILITY_GATE.md` |
| Phase 1 (proxy baseline) | REVISE BASELINE | `docs/PHASE1_GATE.md` |
| Phase 1.1 (baseline hardening audits) | REVISE BASELINE AGAIN | `docs/PHASE1_1_GATE.md` |
| Phase 1.2 (shade-proxy evidence gate) | GO TO SOLWEIG / UTCI | `docs/PHASE1_2_SHADE_EVIDENCE_GATE.md` |
| Phase 2 (SOLWEIG physical spike) | PHYSICAL MODEL ADDS DECISION VALUE | `docs/PHASE2_GATE.md` |
| **Phase 2.1 (robustness audit)** | **MODEL NEEDS REVISION** | `docs/PHASE2_1_GATE.md` |

## 3. Locked findings — do NOT reopen or re-derive

- **Study area**: Prado–Retiro–Atocha bounding box, ~3.5 km², EPSG:25830.
  Fixed since Phase 1. Do not expand city-wide.
- **Heat episode**: 2023-08-21, timestamps 12:00/15:00/18:00 local (CEST).
  AEMET-confirmed extreme episode. Fixed since Phase 1.
- **Meteorological anchor**: Madrid/Barajas (WMO 08221), with a documented,
  quantified representativeness gap vs. Retiro (+0.5 °C daily-max,
  +0.11 °C monthly-mean). Retiro hourly data is confirmed unobtainable
  (Phase 1.1 Audit 1) — do not re-attempt without a materially different
  access route.
- **Simple proxies are unstable**: OSM tree count, Madrid official tree
  inventory, and Copernicus TCD disagree on 19–43% of classifications
  (Phase 1.2). This is why SOLWEIG was started. Do not re-litigate.
- **SOLWEIG adds real decision value**: 33.3% physical-vs-proxy
  reclassification (Phase 2), robust at 33.3–35.7% under solar-forcing
  uncertainty (Phase 2.1).
- **The 12:00 finding is robust and central**: substantial outdoor radiant
  heat stress (UTCI ≥32 °C at all 14 outdoor assets) is present at 12:00,
  *before* the regional air-temperature warning threshold is crossed. This
  survived every tested solar scenario without exception, including real
  satellite radiation data. This is the project's strongest single result.
- **Solar-forcing uncertainty is NOT the project's main problem**: ≤2.4%
  decision change under real-satellite or ±10–20% synthetic radiation
  scenarios. Do not re-run this sensitivity without new cause.
- **No direct field validation of Tmrt/UTCI exists anywhere in this
  project.** AEMET validates meteorological forcing inputs only, never the
  modelled radiant environment. This is permanent until a field campaign is
  run.

## 4. Current unresolved problems (this is what Phase 2.2 or successor should address)

1. **Threshold precision, not substance, is fragile.** 47.6% of the 42
   audited asset×timestamp rows are BOUNDARY (close to the 32 °C/46 °C UTCI
   cutoffs) even though only 7.1% are UNSTABLE (decision actually flips).
   The crisp categorical thresholds need an explicit uncertainty band
   before any operational/dashboard use (`docs/PHASE2_1_GATE.md` §"What
   'needs revision' concretely means").
2. **Vegetation-geometry vintage gap**, concentrated at 3 named assets (§5
   below), not resolved — only confidence-flagged.
3. Wind is not spatially resolved (station-scale only; no CFD/URock — this
   remains explicitly out of scope per every phase's restrictions).
4. No custom land-cover grid was used in SOLWEIG (package default only).

## 5. The three geometry-sensitive garden assets

Identified in Phase 2.1 Audit 2 (`docs/PHASE2_1_GEOMETRY_CONFIDENCE.md`) —
LiDAR canopy (CDSM, ~2008–2015 vintage) reads near-zero at these three real
gardens while all newer independent evidence (Madrid's live tree inventory,
OSM green-polygon coverage, Copernicus TCD 2018) indicates real, substantial
vegetation. Flagged **POSSIBLY STALE**, directional implication: SOLWEIG's
modelled Tmrt/UTCI at these three sites more likely **overestimates** real
2023 heat exposure than underestimates it.

| Asset ID | Name | LiDAR CDSM mean height in 10 m buffer |
|---|---|---:|
| A23 | Jardines de Cecilio Rodríguez | 0.62 m |
| A24 | La Rosaleda | 0.10 m |
| A27 | Jardines del Arquitecto Herrero Palacios | 0.88 m |

A24 (La Rosaleda) is the single most fragile asset in the whole project: it
is both geometry-flagged AND the one asset whose decision actually flips
under the real-satellite solar scenario (18:00, FEASIBLE WITH CONDITIONS →
NOT RECOMMENDED). Prioritise this asset first if pursuing targeted
geometry correction.

## 6. Repository structure and key files

Root: `C:\workspace\HEAT-ADAPTIVE-TOURISM-MADRID`. No git repository.

```
data/raw/            Immutable source extracts (AEMET, OSM, PNOA-LiDAR/IGN,
                      Madrid arbolado, Copernicus TCD, Open-Meteo radiation).
                      Each subfolder has its own README.md with provenance.
data/interim/         Derived layers before final processing (trees,
                      green polygons, SOLWEIG geometry rasters, etc.)
data/processed/       Final CSVs - pilot_assets.csv, pilot_classifications.csv
                      (Phase 1, LOCKED), phase2_asset_thermal_exposure.csv
                      (Phase 2, LOCKED), phase2_1_*.csv (Phase 2.1, LOCKED).
outputs/maps/          PNGs + Tmrt/UTCI GeoTIFFs (tmrt_*.tif, utci_*.tif).
outputs/tables/         Summary CSVs for each phase's agreement/robustness metrics.
src/                   All pipeline code, one script per build/audit step.
docs/                  All phase documentation (this file's siblings).
.venv_solweig/         Dedicated Python 3.12 venv for SOLWEIG - see §7.
```

Most load-bearing files to read next, in order: `docs/PHASE2_GATE.md`,
`docs/PHASE2_1_GATE.md`, `docs/PHASE2_1_ROBUSTNESS_REPORT.md`,
`src/phase2_prereg.py` (pre-registered method decisions),
`src/thresholds.py` (all decision thresholds, single source of truth).

## 7. Software/environment to reproduce SOLWEIG

- **Project's default Python is 3.14.5 — SOLWEIG will NOT install there.**
  Every published `solweig` PyPI release caps at `Requires-Python <3.14`.
- A working environment already exists: `.venv_solweig/` (Python 3.12.10),
  with `solweig==0.1.0b92`, `rasterio`, `pvlib`, `geopandas`-compatible
  deps installed. Activate via
  `.venv_solweig/Scripts/python.exe <script>.py` (Windows).
- **Required environment variable before any rasterio/SOLWEIG run**:
  `PROJ_LIB` and `PROJ_DATA` must point at rasterio's own bundled
  `proj_data` directory, or a conflicting system PostGIS PROJ install will
  break CRS handling. Example (adjust per venv):
  `export PROJ_LIB="<venv>/Lib/site-packages/rasterio/proj_data"; export PROJ_DATA="$PROJ_LIB"`.
  This bit both the venv and the main-Python environment during Phase 2/2.1
  and needed fixing both times.
- **Known CRS quirk**: both IGN/CNIG WCS services (used for DSM/DEM/CDSM)
  and SOLWEIG's own output rasters get tagged with a malformed generic
  `LOCAL_CS["ETRS89 / UTM zone 30N"]` string instead of proper EPSG:25830.
  Coordinate values are correct; only the tag is wrong. Fix by re-tagging
  (`rasterio.open(path, 'r+').crs = CRS.from_epsg(25830)`), not
  reprojecting — see `src/build_solweig_geometry.py` and
  `docs/PHASE2_SOLWEIG_METHOD.md`.
- SOLWEIG's own cached SVF/shadow matrices live in
  `data/interim/solweig_cache/` (Phase 2) — reusable via
  `SurfaceData.prepare(..., working_dir=...)` without recomputation, as
  Phase 2.1 did for its 9 additional runs.

## 8. Exact datasets already downloaded (do not re-fetch unless refreshing)

| Data | Location | Source |
|---|---|---|
| AEMET/Barajas hourly met (2023-08-21 episode + Aug 2021 extreme stress test) | `data/raw/episode_aug2023_barajas_raw.csv`, `data/raw/extreme_aug2021_barajas_raw.csv` | Meteostat-relayed AEMET |
| Real satellite radiation (2023-08-21) | `data/raw/openmeteo_radiation/madrid_2023-08-21_radiation.json` | Open-Meteo / EUMETSAT CM SAF SARAH3 |
| OSM trees, green polygons, buildings, transit, water | `data/raw/osm/`, `data/interim/*.geojson` | Overpass API |
| Madrid official tree inventory (40,840 real trees) | `data/raw/madrid_arbolado/`, `data/interim/madrid_arbolado_points.geojson` | Ayuntamiento de Madrid live ArcGIS service |
| Copernicus HRL Tree Cover Density (2018) | `data/raw/copernicus_tcd/tcd_2018_study_area.tif` | EEA public ImageServer |
| PNOA-LiDAR-derived DEM/DSM/CDSM | `data/raw/pnoa_lidar/`, `data/interim/solweig/*.tif` | IGN/CNIG public WCS (DEM 2ª cobertura vintage unstated; building/vegetation nDSM 1ª cobertura, ~2008–2015) |
| SOLWEIG outputs (Tmrt/UTCI, all scenarios) | `data/interim/solweig_cache/`, `data/interim/solweig_cache_phase2_1/`, `outputs/maps/*.tif` | Computed, this project |

## 9. Restrictions that remain active

No dashboard code. No routing. No ML. No agents. No behavioural/tourist-flow
claims. No causal-adaptation claims. No city-wide expansion. No CFD/URock.
No treating AEMET as validating Tmrt. No describing UTCI as measured
comfort. No synthetic field-validation data. No composite/weighted
indices. No new model complexity beyond what a specific, gated phase
justifies.

## 10. Recommended next phase

A bounded **Phase 2.2 — Threshold Uncertainty & Targeted Geometry
Correction** spike, addressing exactly the two items in §4.1–4.2 and
nothing broader:
1. Introduce an explicit uncertainty band around the UTCI 32 °C/46 °C
   decision thresholds (e.g. amber/borderline zone), replacing the crisp
   cutoff in the feasibility-translation rule.
2. A targeted correction or re-audit of canopy at the three named assets
   (§5) — e.g. current aerial/orthophoto inspection or a newer LiDAR
   coverage if one becomes accessible for just those sites — not a
   city-wide vegetation rebuild.

Only after both are addressed should the gate be re-evaluated against the
Phase 2.1 criteria, and only then would dashboard/operational work become
appropriate to consider — and even then, as its own separately-scoped and
separately-gated phase.

## 11. Historical results must not be rewritten

**Phase 0, Phase 1, Phase 1.1, Phase 1.2, Phase 2, and Phase 2.1 results,
docs, and processed data files are final and locked.** Any future phase
must treat them as read-only inputs — extend, audit, or build on top of
them, but never edit their content, regenerate their output files with
different values, or alter their stated verdicts. If a future finding
appears to contradict an earlier one, document the discrepancy explicitly
in a new phase's own docs; do not silently correct the historical record.
