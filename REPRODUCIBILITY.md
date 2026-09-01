# Reproducibility — HATI-Madrid

This documents the **actual** workflow used to produce the locked results and publication
figures. There is **no single one-command reproduction**; the pipeline runs as an ordered
sequence of scripts across two Python environments. All derived files regenerate from the
open-data inputs under `data/raw/`.

## Environments

Two interpreters are used (as in every phase of the project):

1. **Analysis / figures environment — Python 3.14.5.** Geospatial stack + plotting. Used for
   the study-area build, proxy classification, extraction, screening, validation, and all
   publication figures. Pinned packages in `requirements.txt`.
2. **SOLWEIG environment — Python 3.12** (`.venv_solweig/`, git-ignored). Required only for
   the physical modelling, because the `solweig` package caps at `Requires-Python <3.14`.
   Key packages: `solweig==0.1.0b92`, `rasterio`, `numpy`, `pyproj`, `shapely`, and `pvlib`
   (clear-sky irradiance estimate). The exact SOLWEIG build is recorded in each run's
   `run_metadata.json` and in `docs/PHASE2_SOLWEIG_METHOD.md`.

Neither virtual environment is committed; recreate them from `requirements.txt` (analysis)
and `pip install solweig==0.1.0b92 pvlib` under Python 3.12 (SOLWEIG).

## Required external data

Inputs under `data/raw/` are open data (see `docs/DATA_SOURCE_INVENTORY.csv` and
`docs/PHASE1_DATA_PROVENANCE.md`): AEMET episode/threshold records, IGN/CNIG LiDAR-derived
geometry, OpenStreetMap extracts, and Madrid municipal tree inventory. If any raw layer is
absent, the corresponding fetch/build script under `src/` documents how it was obtained
(e.g. `src/fetch_madrid_arbolado.py`, `src/build_solweig_geometry.py`).

## Workflow (ordered)

**A. Study area, assets, proxy baseline (analysis env):**
```
python src/define_study_area.py
python src/build_pilot_assets.py
python src/build_supporting_layers.py
python src/build_green_polygons.py
python src/build_classifications.py        # -> data/processed/pilot_classifications.csv (proxy)
```

**B. Physical thermal modelling (SOLWEIG env, Python 3.12):**
```
python src/build_solweig_geometry.py       # DEM/DSM/CDSM at 2.5 m (analysis env)
python src/build_met_forcing.py            # Ta/RH/wind + clear-sky GHI (pvlib)
.venv_solweig/Scripts/python src/run_solweig.py          # Tmrt/UTCI rasters -> outputs/maps/
python src/extract_asset_thermal_exposure.py             # -> phase2_asset_thermal_exposure.csv
```

**C. Uncertainty / geometry recheck (both envs):**
```
python src/phase2_2_geometry_evidence.py
python src/phase2_2_build_corrected_cdsm.py
.venv_solweig/Scripts/python src/phase2_2_run_solweig_corrected.py narrow central wide
python src/phase2_2_extract_corrected.py
python src/phase2_2_decision_confidence.py               # -> phase2_2_decision_confidence.csv
python src/extract_solar_sensitivity.py                  # -> solar_forcing_sensitivity.csv
```

**D. Constraint-first screening (analysis env):**
```
python src/phase3_extract_opening_hours.py
python src/phase3_build_catalog.py
python src/phase3_candidate_screening.py
python src/phase3_scenarios.py             # -> phase3_scenarios*.csv, phase3_hati_vs_baseline.csv
python src/phase3_validation.py
```

**E. Publication figures (analysis env):**
```
python outputs/publication/figures/render_fig01.py   # study design + architecture
python outputs/publication/figures/render_fig02.py   # thermal-method divergence
python outputs/publication/figures/render_fig04.py   # -> FIG03 screening consequence
python outputs/publication/figures/render_fig05.py   # -> FIG04 tested uncertainty
python outputs/publication/figures/render_fig03.py   # -> SFIG01 UTCI field (supplementary)
python outputs/publication/graphical_abstract/render_graphical_abstract.py
```
Each figure script re-reads the locked source tables and **asserts** the headline numbers
(e.g. 42/14/9/5; 7/8, 3/8, 23; 1/0/0; 35/6/1) before writing PDF/SVG/PNG.

**F. Integrity checks:**
```
python -m pytest tests/test_outputs.py
```

## Expected outputs

- `data/processed/` — proxy classifications, physical thermal exposure, decision confidence,
  screening catalog and scenarios.
- `outputs/tables/` — locked result tables (proxy-vs-physical comparison, solar sensitivity,
  HATI-vs-baseline, exclusion reasons, etc.).
- `outputs/maps/` — SOLWEIG Tmrt/UTCI rasters.
- `outputs/publication/` — figures (FIG01–FIG04, SFIG01) and the graphical abstract.
- `manuscript/`, `supplementary/`, `submission/` — manuscript, tables, references, highlights.

## Known limitations (reproducibility scope)

- SOLWEIG runs require the dedicated Python 3.12 environment; results are numerically stable
  but GPU auto-dispatch may vary by machine (spatially-averaged statistics are used, which
  are robust to single-pixel variation).
- No field measurements of Tmrt/UTCI exist; the pipeline reproduces the *modelled* values,
  not a validation of them.
- Opening hours were documented in 2026 and applied to the 2023 study day (temporal
  alignment limitation; see the manuscript Limitations section).
- Large public geodata (Madrid arbolado, ≈13 MB each) are currently vendored into the
  repository for a self-contained snapshot; they may later be excluded in favour of a documented
  download step to keep the repository lightweight.
