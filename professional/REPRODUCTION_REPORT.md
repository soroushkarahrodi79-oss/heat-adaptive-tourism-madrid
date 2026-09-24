# HATI-Madrid — Reproduction report: thermal extraction → constraint-first screening

**Executed:** 2026-09-24 · **Repository base:** commit `c69688e` (`main`)
**Selected analysis:** Option B, constraint-first tourism-opportunity screening, extended
upstream to the thermal-method comparison (Option A) because the same committed inputs
make that possible without re-running SOLWEIG.

This report records what was actually executed. It does not add or change any scientific
result. All locked Layer A files in this repository were left untouched, and the
pipeline ran in a disposable copy outside the repository.

## 1. What was and was not re-executed

| Stage | Script (unmodified) | Inputs | Re-executed? |
|---|---|---|---|
| SOLWEIG Tmrt/UTCI simulation | `src/run_solweig.py`, `src/phase2_2_run_solweig_corrected.py` | LiDAR geometry, meteorological forcing | **No.** Out of scope by design. The committed rasters `outputs/maps/{tmrt,utci}_{1200,1500,1800}.tif` were used as given. |
| Solar-forcing and geometry perturbation runs | `src/run_solweig_scenarios.py` and related | as above | **No.** `phase2_1_solar_scenario_assets.csv` and `phase2_2_corrected_geometry_utci.csv` were used as given. |
| Per-asset thermal extraction, proxy vs physical | `src/extract_asset_thermal_exposure.py` | UTCI/Tmrt rasters, `pilot_assets.csv`, `pilot_classifications.csv`, `shade_proxy_comparison.csv` | **Yes** |
| Decision confidence | `src/phase2_2_decision_confidence.py` | outputs above + perturbation tables | **Yes** |
| Opening-hours harvest | `src/phase3_extract_opening_hours.py` | committed OSM extracts (`data/raw/osm/*.json`) | **Yes** |
| Asset catalogue | `src/phase3_build_catalog.py` | opening hours + institutional hours recorded in the script | **Yes** |
| Context-free screening | `src/phase3_candidate_screening.py` | catalogue + decision confidence | **Yes** |
| 8 scenarios + nearest-open baseline | `src/phase3_scenarios.py` | screening + catalogue | **Yes** |
| Accessibility sensitivity (500/800/1200 m) | `src/phase3_validation.py` | scenario outputs | **Yes** |
| Headline-number assertions | `render_fig02.py`, `render_fig04.py`, `render_fig05.py` | reproduced tables | **Yes.** Each script asserts its locked numbers before saving. |
| Layer B, Gate 3A/3B pedestrian-route experiment | `src/gate3*` | SOLWEIG, Catastro | **No.** Frozen research, checked documentarily only. |

## 2. Environment

| Item | Reference (REPRODUCIBILITY.md) | This execution |
|---|---|---|
| OS | Windows (inferred from the `.venv_solweig/Scripts/` paths and CRLF output files) | Linux 6.18 |
| Python | 3.14.5 | **3.14.0rc2** (the only 3.14 build available through `uv` here; this is a declared deviation) |
| numpy / pandas / geopandas | 2.4.6 / 2.3.3 / 1.1.3 | identical |
| rasterio / rasterstats / shapely / pyproj | 1.5.0 / 0.21.0 / 2.1.2 / 3.7.2 | identical |
| matplotlib / pillow | 3.10.9 / 12.2.0 | identical |

## 3. Commands executed

```bash
# isolated environment (outside the repository)
uv venv -p 3.14 <scratch>/venv314
VIRTUAL_ENV=<scratch>/venv314 uv pip install -r requirements.txt

# full re-execution + comparison (copies the repo, never writes into it)
<scratch>/venv314/bin/python professional/reproduce_screening.py --workdir <scratch>/run1 --keep

# existing integrity tests, on the repository itself (read-only)
<scratch>/venv314/bin/python -m pytest tests/test_outputs.py -q -p no:cacheprovider
```

On Windows the equivalent command is
`py -3.14 professional\reproduce_screening.py --workdir C:\temp\hati_repro --keep`,
run inside a virtual environment built from `requirements.txt`. The script is plain
Python and needs no Bash. **It has not been executed on Windows in this session.**

## 4. Results

**Every step exited 0, and all 10 regenerated tables matched their locked references.**

| Table | Rows | Structural + numeric match | Byte-level |
|---|---|---|---|
| `data/processed/phase2_asset_thermal_exposure.csv` | 81 | MATCH | identical except CRLF→LF |
| `data/processed/phase2_2_decision_confidence.csv` | 42 | MATCH | identical except CRLF→LF |
| `data/processed/phase3_osm_opening_hours_raw.csv` | 27 | MATCH | identical except CRLF→LF |
| `data/processed/phase3_asset_catalog.csv` | 27 | MATCH | identical except CRLF→LF |
| `data/processed/phase3_candidate_screening.csv` | 81 | MATCH | identical except CRLF→LF |
| `data/processed/phase3_scenarios.csv` | 208 | MATCH | identical except CRLF→LF |
| `data/processed/phase3_scenarios_summary.csv` | 8 | MATCH | identical except CRLF→LF |
| `outputs/tables/phase3_exclusion_reasons.csv` | 5 | MATCH | identical except CRLF→LF |
| `outputs/tables/phase3_hati_vs_baseline.csv` | 8 | MATCH | identical except CRLF→LF |
| `outputs/tables/phase3_accessibility_sensitivity.csv` | 8 | MATCH | identical except CRLF→LF |

"Identical except CRLF→LF" means that once line endings are normalised the files are
character-for-character equal, including every printed decimal. The only byte
difference is the Windows vs Linux line terminator written by `pandas.to_csv`.

**Headline numbers, recomputed from the reproduced tables (not read from the locked ones):**

| Result | Reproduced value | Matches published |
|---|---|---|
| Outdoor observations; reclassified by the thermal method | 42; 14 (9 more restrictive, 5 less) | yes |
| Reclassification rate at 12:00 / 15:00 / 18:00 | 64.3% / 0.0% / 35.7% | yes |
| Decision confidence ROBUST / BOUNDARY / UNSTABLE | 35 / 6 / 1 | yes |
| Scenarios whose candidate set changed vs baseline | 7/8 | yes |
| Scenarios whose nearest-open pick is excluded by the screening | 3/8 (S2, S6, S8; all `OUTDOOR_EXPOSURE_TOO_HIGH`) | yes |
| Open-in-radius candidates removed by thermal/evidence gates | 23 | yes |
| No-survivor scenario | S8 | yes |

**Existing tests:** `tests/test_outputs.py`, 14 passed, run both on the repository and on
the reproduced copy.

**Negative control on the comparator.** Three deliberate perturbations of a reproduced
table were each detected: +0.01 °C on one UTCI value, one changed confidence label, and
one dropped row. The PASS therefore reflects real agreement and does not come from a
comparator that always passes.

## 5. What this reproduction does and does not establish

**It establishes** that, from the committed SOLWEIG outputs and open-data inputs, the
committed code deterministically regenerates the locked extraction, confidence,
catalogue, screening, scenario and sensitivity tables, and the published headline
numbers.

**It does not establish:**

- that the SOLWEIG simulation itself reproduces, because it was not re-run;
- that the modelled UTCI matches real conditions. There is no field measurement, and
  reproducibility is not physical validation;
- anything about Layer B beyond a reading of its frozen decision record;
- behaviour on Windows or under Python 3.14.5 exactly.

## 6. Findings raised during reproduction

1. **UTCI category label shift (decision-neutral data defect).** Two descriptive label
   columns are one Bröde category too high. See
   [`EVIDENCE_MATRIX.md`](EVIDENCE_MATRIX.md#data-defect-discovered-during-reproduction-flagged-not-fixed).
   No decision, figure or manuscript statement depends on them. They are not fixed here
   because the files are `RELEASE_LOCKED`.
2. **Aggregate table without a generator.** `outputs/tables/proxy_vs_physical_comparison.csv`
   has no producing script in `src/`. Its values were checked against the reproduced
   per-row table, and they agree. Its provenance as a file is nonetheless undocumented.
3. **The 3/8 result is thin in one case.** In S2 the excluded baseline pick is modelled
   +0.1 °C hotter than the source, and the two tested uncertainty envelopes overlap. The
   method's exclusion rule has no margin (see `EVIDENCE_MATRIX.md`, E5). This is
   disclosed, not changed.
