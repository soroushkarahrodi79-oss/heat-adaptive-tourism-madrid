# PHASE2_1_ROBUSTNESS_METHOD.md — HATI-Madrid Phase 2.1

Version 1.0 · 2026-08-17. Gate in effect at start: **PHYSICAL MODEL ADDS
DECISION VALUE** (`docs/PHASE2_GATE.md`). This phase tests whether that
verdict, and the specific findings behind it, survive the two most
important unresolved input uncertainties identified in
`docs/PHASE2_VALIDATION_REPORT.md`: solar-radiation forcing and
vegetation-geometry vintage. **The Phase 2 baseline is locked and was not
modified or re-run** — every comparison below is against the original,
unchanged `data/processed/phase2_asset_thermal_exposure.csv`.

No SOLWEIG parameter was tuned. No new model sophistication (CFD, URock,
custom land cover) was introduced. No city-wide vegetation rebuild was
attempted.

---

## Audit 1 — solar-forcing robustness

**Real-data search performed before any synthetic scenario was built**, per
the task's explicit preference for measured/reanalysis data over invented
sensitivity numbers. Result: a real, free, no-registration source was
found — see `docs/PHASE2_1_SOLAR_SENSITIVITY.md` for the full search log
and source detail. Four scenarios were run:

| Scenario | Radiation source | Nature |
|---|---|---|
| BASELINE | Phase 2's original pvlib Ineichen clear-sky estimate | **Not re-run** — the original, locked Phase 2 result |
| REAL_SATELLITE | Open-Meteo historical archive, EUMETSAT CM SAF SARAH3 satellite retrieval | Real observational-satellite product, genuinely independent of the clear-sky model |
| SENS_A_minus10pct | BASELINE × 0.90 | Synthetic **uncertainty scenario**, not an observation |
| SENS_B_minus20pct | BASELINE × 0.80 | Synthetic **uncertainty scenario**, not an observation |

All three non-baseline scenarios were run through the identical, unmodified
SOLWEIG surface geometry (`SurfaceData.prepare()` reused Phase 2's own
cached SVF/shadow matrices — geometry was not re-prepared or altered).
**Only `global_rad` changed between scenarios and versus Phase 2's
baseline**; Ta, RH, wind speed, and pressure were held identical to Phase 2
in every run, per the task's "do not change other model inputs between
runs" instruction. `src/build_solar_scenarios.py` builds the four-scenario
forcing table; `src/run_solweig_scenarios.py` executes the 9 new SOLWEIG
runs (3 scenarios × 3 timestamps; BASELINE's 3 runs are Phase 2's own,
reused unchanged); `src/extract_solar_sensitivity.py` extracts the same
pre-registered 10 m buffer-mean statistic (`src/phase2_prereg.py`, Phase 2's
own pre-registration, reused unchanged) for all 14 outdoor assets in every
scenario.

## Audit 2 — vegetation-geometry vintage confidence audit

**Not a rebuild.** Eight outdoor assets were selected (not all 14, per the
task's "targeted... approximately 6-8" instruction), prioritising: park/
garden morphology with strong vegetation-Tmrt sensitivity (A20, A21, A23,
A24, A25, A27) plus two additional Phase 1.2 proxy-sensitive assets of other
morphologies for contrast (A17, A19). For each, the Phase 2 LiDAR CDSM
(locked, unmodified) was compared against three independent, already-
acquired, newer real data sources — **no new vegetation data was fetched
for this audit**; every comparison source was already sitting in
`data/interim/`/`data/raw/` from Phase 1.2:

1. Madrid official tree inventory (Phase 1.2 P1: live ArcGIS service, real
   per-tree points, current as of the 2026 query date)
2. Green-polygon coverage (Phase 1.2 P3: real OSM park/garden polygons)
3. Copernicus HRL Tree Cover Density (Phase 1.2 P2: 2018 vintage — itself
   pre-dates the 2023 episode, but post-dates the LiDAR's 2008–2015
   vintage, so it is a genuine intermediate-age cross-check, not a
   contemporaneous one)

Each asset was assigned REPRESENTATIVE / PARTIALLY REPRESENTATIVE /
POSSIBLY STALE by a documented, non-arbitrary rule (full detail and the
per-asset table: `docs/PHASE2_1_GEOMETRY_CONFIDENCE.md`). **The Phase 2
CDSM raster itself was never edited** — flags are recorded as a separate
confidence layer (`data/processed/phase2_1_geometry_confidence.csv`) and
fed into Audit 3, not substituted into the locked geometry.

## Audit 3 — decision robustness classification

Every one of the 42 outdoor asset×timestamp rows from the locked Phase 2
baseline is assigned ROBUST / BOUNDARY / UNSTABLE by combining Audit 1
(does the feasibility decision actually change under any tested solar
scenario?) and Audit 2 (is the asset geometry-flagged, and if so, is the
baseline UTCI close enough to the 46 °C threshold that a plausible canopy
correction could matter?). The exact rule, its 2 °C threshold-proximity
margin, and why it was fixed *before* the overall pass rate was known, are
documented in full in `src/decision_robustness.py`'s module docstring and
reproduced in `docs/PHASE2_1_ROBUSTNESS_REPORT.md`. The margin was not
adjusted after seeing the resulting ROBUST/BOUNDARY/UNSTABLE split.

## Reproducibility chain

```
data/raw/openmeteo_radiation/madrid_2023-08-21_radiation.json   (real satellite data)
data/raw/phase2_met_forcing.csv                                  (Phase 2, locked)
        |
        v  src/build_solar_scenarios.py
data/raw/phase2_1_solar_scenarios.csv
        |
        v  src/run_solweig_scenarios.py  (reuses Phase 2's cached geometry)
data/interim/solweig_cache_phase2_1/{REAL_SATELLITE,SENS_A_minus10pct,SENS_B_minus20pct}/run_*/
        |
        v  src/extract_solar_sensitivity.py
data/processed/phase2_1_solar_scenario_assets.csv
        |
        v  (combined with) src/geometry_confidence_audit.py
data/processed/phase2_1_geometry_confidence.csv
        |
        v  src/decision_robustness.py
data/processed/phase2_1_robustness.csv, outputs/tables/decision_robustness.csv
        |
        v  src/make_maps.py (map_phase2_1_robustness)
outputs/maps/phase2_1_unstable_assets.png
```
