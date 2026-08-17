# PHASE2_2_METHOD.md — HATI-Madrid Phase 2.2

Version 1.0 · 2026-08-17. Bounded revision spike addressing exactly the two
weaknesses `docs/PHASE2_1_GATE.md` and `docs/PHASE2_1_TO_PHASE2_2_HANDOFF.md`
identified, and nothing broader. Phase 0–2.1 results, docs and processed data
are treated as **immutable, read-only inputs** (handoff §11).

---

## 1. Scope (exactly two objectives; everything else out of scope)

1. **Task A — targeted geometry re-check** of the three flagged garden assets
   A23, A24, A27 (`docs/PHASE2_1_GEOMETRY_CONFIDENCE.md`), prioritising A24;
   resolve or quantify the vegetation-vintage uncertainty using the strongest
   recent spatially-explicit evidence readily available.
2. **Task B — evidence-derived decision uncertainty**: replace false precision
   at the hard 32/46 °C decision thresholds with an uncertainty envelope and a
   decision-confidence field derived from *observed* model sensitivity — **not**
   an arbitrary ±2 °C band, and **without** altering the official UTCI
   thermal-stress categories.

**Explicitly NOT done** (handoff §9, task restrictions): no Phase 3, no
dashboard, no routing, no ML, no CFD/URock, no city-wide expansion, no
full-pilot vegetation rebuild, no new literature/data discovery, no new model
complexity, no composite index, no synthetic field-validation.

## 2. What was and was not modified

- **Read-only inputs (never edited):** `data/interim/solweig/{dem,dsm,cdsm}_2m5.tif`
  (Phase 2 locked geometry), `data/processed/phase2_asset_thermal_exposure.csv`
  (Phase 2), `data/processed/phase2_1_*.csv` (Phase 2.1), `outputs/maps/*.tif`,
  all Phase 0–2.1 docs. Verified post-run: the original CDSM is byte-identical
  (max 47.0 m / mean 4.68 m unchanged); the corrected variant differs in only
  **43 of 474 117 pixels**, all inside the A23/A27 30 m neighbourhoods.
- **New, separately-stored artefacts (this phase):**
  - `data/interim/solweig_phase2_2/{narrow,central,wide}/` — corrected-canopy
    geometry variants (Task A).
  - `data/interim/solweig_cache_phase2_2/` — SOLWEIG runs for those variants.
  - `data/processed/phase2_2_geometry_evidence.csv`,
    `phase2_2_corrected_geometry_utci.csv`, `phase2_2_decision_confidence.csv`.
  - `outputs/tables/phase2_2_geometry_changes.csv`,
    `phase2_2_robustness_changes.csv`.
  - `src/phase2_2_*.py` (five scripts).

## 3. Environment

Identical to Phase 2/2.1 (handoff §7). Two interpreters, as in every prior
phase:
- **Main Python 3.14** (geopandas/rasterio/rasterstats) — evidence query,
  CDSM construction, extraction, confidence computation.
- **`.venv_solweig` Python 3.12** (`solweig==0.1.0b92`) — the SOLWEIG runs.
- `PROJ_LIB`/`PROJ_DATA` set to rasterio's bundled `proj_data`; new rasters
  re-tagged `EPSG:25830` to defeat the known malformed-`LOCAL_CS` quirk
  (`docs/PHASE2_SOLWEIG_METHOD.md`).

## 4. Task A method — localized, reproducible, real-data-only

**Evidence step** (`src/phase2_2_geometry_evidence.py`). For each of A23/A24/A27,
at radii 10/20/30 m, count Madrid official-inventory trees and — crucially —
read their **real per-tree height** `altura_m`, a field Audit 2 did not use (it
only counted trees). Cross-read Copernicus TCD 2018, OSM green coverage, and
the locked LiDAR CDSM. Output: `data/processed/phase2_2_geometry_evidence.csv`.
Per-asset verdict rule (documented before inspection): a garden is judged
**MATERIALLY STALE** if newer sources show abundant *tall* canopy (multiple
inventoried trees > 3 m and TCD high) where LiDAR reads near-zero;
**PARTIALLY STALE** if newer evidence exceeds LiDAR only modestly / only
outside the immediate point neighbourhood; **REPRESENTATIVE** if the strongest
spatially-explicit source (per-tree inventory *with heights*) agrees with the
near-zero LiDAR reading. Full interpretation: `docs/PHASE2_2_GEOMETRY_RECHECK.md`.

**Correction step** (`src/phase2_2_build_corrected_cdsm.py`). For the assets
judged stale, build a corrected CDSM by burning each **real** inventoried
canopy tree (> 3 m) within 30 m as a disc of its **real** `altura_m` height,
accumulated by maximum over the locked Phase 2 canopy (a correction only ever
*adds* the canopy stale LiDAR missed; it never removes captured canopy). Only
the crown *radius* is an assumption (height is real data); to avoid false
precision on that one assumption, three variants are produced and carried as a
bracket — crown radius R ∈ {2.0, 3.0, 4.0} m (narrow/central/wide). A24 is
**not** corrected (its geometry is representative — inserting canopy there
would be fabrication).

**Rerun + extract** (`src/phase2_2_run_solweig_corrected.py`,
`src/phase2_2_extract_corrected.py`). Rerun SOLWEIG on each variant with the
**exact Phase 2 baseline weather** (so only geometry differs from Phase 2), a
fresh SVF/shadow precompute (required because canopy changed), separate cache.
Extract the same pre-registered 10 m-buffer mean UTCI. A24 is carried as an
**unchanged control**: its extracted delta is 0.0 °C at every timestamp/variant,
confirming the localized edit did not perturb the rest of the grid.

## 5. Task B method — evidence-derived envelope & confidence

`src/phase2_2_decision_confidence.py`. For every one of the 42 outdoor
asset×timestamp rows, assemble all *actually-computed* SOLWEIG realizations:
- **Solar** (all 42 rows): Phase 2 clear-sky baseline, REAL_SATELLITE, −10%,
  −20% (Phase 2.1 Audit 1).
- **Geometry** (A23, A27 only): the three corrected-canopy variants (Task A).

The **uncertainty envelope** is `[min, max]` over those realizations —
inherently **asymmetric** (clear-sky GHI is near the physical upper bound of
radiation and canopy correction only adds shade, so both uncertainty sources
push UTCI *down*; the only upward excursion is the small real cloud-enhancement
REAL_SATELLITE captured at 18:00). No symmetric ± band is assumed anywhere.

**decision_confidence** (safety-critical boundary 46 °C = FEASIBLE WITH
CONDITIONS vs NOT RECOMMENDED; secondary 32 °C):
- **UNSTABLE** — a realization lands on the opposite side of the 46 °C boundary
  from the baseline (materially contradictory decision).
- **BOUNDARY** — no realization flips, but the envelope lies within the row's
  **own demonstrated sensitivity** `s = max|realization − baseline|` of a
  threshold (evidence-derived, per-row — this is the principled replacement for
  Phase 2.1's blanket ±2 °C).
- **ROBUST** — envelope is farther from every threshold than `s`, no realization
  flips.

**Architectural rule honoured:** thermal state and decision confidence are
never collapsed. The output carries separate fields `thermal_stress_state`
(official UTCI category, unchanged), `decision_state`, `decision_confidence`,
`uncertainty_reason`, plus the full envelope and its provenance. Full
derivation and honest limits: `docs/PHASE2_2_DECISION_UNCERTAINTY.md`.

## 6. Reproduce

```bash
# main Python (geo stack); PROJ_LIB/PROJ_DATA -> rasterio proj_data
python src/phase2_2_geometry_evidence.py
python src/phase2_2_build_corrected_cdsm.py
# venv_solweig (Python 3.12)
.venv_solweig/Scripts/python.exe src/phase2_2_run_solweig_corrected.py narrow central wide
# main Python
python src/phase2_2_extract_corrected.py
python src/phase2_2_decision_confidence.py
python src/phase2_2_summary_tables.py
```
