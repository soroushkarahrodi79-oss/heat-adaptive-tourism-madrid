# PHASE2_1_SOLAR_SENSITIVITY.md — HATI-Madrid Phase 2.1, Audit 1

Version 1.0 · 2026-08-17.

---

## Real-data search log

Before building any synthetic sensitivity scenario, a real observed or
reanalysis solar-radiation source for Madrid, 2023-08-21, was sought:

| Source considered | Result |
|---|---|
| AEMET radiation observations | Not pursued via the OpenData API (requires a registered `api_key` — the same registration barrier already documented in `docs/PHASE1_1_BASELINE_HARDENING.md` Audit 1; not repeated here) |
| Copernicus/ERA5 radiation variables (direct CDS access) | Requires Copernicus Climate Data Store account registration — not performed on the user's behalf, per this project's standing operating constraints |
| **Open-Meteo historical archive API** | **Used.** Free, public, no API key or registration required. Serves real satellite-derived shortwave radiation for Europe from **EUMETSAT CM SAF SARAH3** — a geostationary-satellite radiation retrieval product (not a station pyranometer, but a genuine observational-satellite product, not a clear-sky model) |

**Source used:** `https://archive-api.open-meteo.com/v1/archive`, queried
for the study-area centroid (40.4125 N, -3.68675 E), 2023-08-21, hourly,
variables `shortwave_radiation, direct_radiation, diffuse_radiation,
direct_normal_irradiance, cloud_cover` (plus Ta/RH/wind/cloud for
cross-checking against the already-used Barajas archive). Access date:
2026-08-17. Raw response preserved at
`data/raw/openmeteo_radiation/madrid_2023-08-21_radiation.json`.

This is **not fabricated observed radiation** — it is a real, named,
citable, third-party-operated satellite product, used exactly as served,
with its provenance stated at every use.

## Baseline vs. real-satellite comparison

| Local time | BASELINE (clear-sky, Phase 2) GHI | REAL_SATELLITE GHI | Delta | Real cloud cover at this hour |
|---|---:|---:|---:|---:|
| 12:00 | 722.8 W/m² | 651.0 W/m² | **−71.8 W/m² (−9.9%)** | 10% |
| 15:00 | 861.9 W/m² | 868.0 W/m² | +6.1 W/m² (+0.7%) | 15% |
| 18:00 | 497.7 W/m² | 553.0 W/m² | **+55.3 W/m² (+11.1%)** | 15% |

**A genuine finding in its own right:** the satellite data shows real,
non-zero cloud cover (10–15%) at all three target hours, whereas the
station-based weather code used to justify Phase 2's clear-sky assumption
(Meteostat's categorical `coco=1`, "clear") is a coarser summary that did
not capture this. The clear-sky assumption was reasonable given what was
available at the time, but the real satellite data shows it was not exact
— documented here, not smoothed over.

## Sensitivity scenario definitions

| Scenario | GHI construction |
|---|---|
| SENS_A_minus10pct | BASELINE GHI × 0.90, at every timestamp |
| SENS_B_minus20pct | BASELINE GHI × 0.80, at every timestamp |

Both are explicitly labelled, throughout every output row
(`data/raw/phase2_1_solar_scenarios.csv` `source_note` column), as
**UNCERTAINTY SCENARIOS, not observations**.

## SOLWEIG results by scenario (whole-grid means)

| Scenario | 12:00 Tmrt / UTCI | 15:00 Tmrt / UTCI | 18:00 Tmrt / UTCI |
|---|---|---|---|
| BASELINE (Phase 2, locked) | 47.5 / 36.1 °C | 53.4 / 42.1 °C | 49.6 / 42.4 °C |
| REAL_SATELLITE | 46.6 / 35.9 °C | 53.5 / 42.1 °C | 50.6 / 42.7 °C |
| SENS_A (−10%) | 46.6 / 35.9 °C | 52.4 / 41.8 °C | 48.6 / 42.2 °C |
| SENS_B (−20%) | 45.4 / 35.6 °C | 51.3 / 41.5 °C | 47.6 / 41.9 °C |

Whole-grid mean UTCI moves by at most ≈1.0 °C across all three alternative
scenarios and all three timestamps — a narrow, bounded range.

## Decision-level impact (pre-registered 10 m buffer-mean per asset, n=14 outdoor assets × 3 timestamps = 42 rows)

| Scenario | Rows where feasibility_state changed vs. Phase 2 baseline | UTCI delta (mean / max absolute) |
|---|---|---|
| REAL_SATELLITE | **1 / 42 (2.4%)** | −0.01 °C / 1.1 °C |
| SENS_A (−10%) | **0 / 42 (0.0%)** | −0.35 °C / 1.1 °C |
| SENS_B (−20%) | **0 / 42 (0.0%)** | −0.74 °C / 2.3 °C |

**The single decision change:** A24 (La Rosaleda), 18:00, under
REAL_SATELLITE — baseline UTCI 45.4 °C (FEASIBLE WITH CONDITIONS) becomes
46.0 °C (NOT RECOMMENDED) under the real, slightly-higher-than-clear-sky
satellite radiation at that hour. This is a genuine boundary case: a
±0.6 °C shift crossing an exact 46.0 °C cutoff. It is carried into Audit 3
as UNSTABLE, and is additionally geometry-flagged (see
`docs/PHASE2_1_GEOMETRY_CONFIDENCE.md`) — two independent uncertainty
sources converge on the same asset.

## The 12:00 finding, re-tested

Phase 2's central finding — substantial outdoor heat stress already present
at 12:00, before the regional air-temperature warning threshold is reached
— was re-tested explicitly:

| Scenario | Outdoor assets with UTCI ≥ 32 °C ("Strong heat stress" or worse) at 12:00 |
|---|---|
| BASELINE | 14 / 14 |
| REAL_SATELLITE | **14 / 14** (min 32.5 °C, max 39.8 °C) |
| SENS_A (−10%) | **14 / 14** (min 32.5 °C, max 39.8 °C) |
| SENS_B (−20%) | **14 / 14** (min 32.6 °C, max 39.0 °C) |

**The finding survives completely and without exception under every tested
solar-forcing scenario, including the real satellite data.** This is
expected on physical grounds: the finding's mechanism (solar elevation, and
therefore radiant load, peaking earlier in the day than regional air
temperature) is a function of solar geometry and the real, independently
observed air-temperature trajectory — not of the specific radiation
magnitude assumption, which only shifts the margin, not the qualitative
conclusion, within the tested range.
