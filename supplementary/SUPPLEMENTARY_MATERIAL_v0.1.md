# Supplementary Material

**Thermal representation as a decision variable in heat-adaptive tourism opportunity
screening: evidence from a Madrid pilot**

All values below are exact, drawn from the locked project outputs; none is recalculated.
Each item is included because it supports reproducibility or supplies exact detail behind a
main-text figure, without distracting from the tourism-management argument.

---

## Figure S1. Model-derived UTCI field at 12:00, 15:00 and 18:00

Three-timestamp small-multiple of the **model-derived** UTCI field (SOLWEIG/UTCI, 2.5 m),
on a single shared colour scale, with the 32 °C and 46 °C category breaks contoured and the
14 outdoor assets overlaid. Illustrates that the modelled radiant field is spatially and
temporally structured, and that at 12:00 the field is ≥ 32 °C everywhere modelled (the
mechanism behind the noon divergence in Figure 2). UTCI is model-derived, never observed.
File: `outputs/publication/figures/SFIG01_UTCI_FIELD_v0.1.{pdf,svg,png}`. (Moved from the
main text because the outdoor feasibility category is single-valued at the pre-registered
10 m buffer-mean, so the spatial texture is not the decision variable.)

---

## Table S1. Thermal-method reclassification — exact rates

Source: `outputs/tables/proxy_vs_physical_comparison.csv`. Unit: outdoor asset × timestamp
observation (n = 42).

| Breakdown | Group | Value | n |
|---|---|---|---|
| Overall reclassification rate | all | 33.3% | 42 |
| Direction | physical more restrictive than proxy | 9 | 42 |
| Direction | physical less restrictive than proxy | 5 | 42 |
| Direction | agreement (unchanged) | 28 | 42 |
| By timestamp | 12:00 | 64.3% | 14 |
| By timestamp | 15:00 | 0.0% | 14 |
| By timestamp | 18:00 | 35.7% | 14 |
| By morphology | attraction exterior | 33.3% | 9 |
| By morphology | park or garden | 33.3% | 18 |
| By morphology | plaza or hardscape | 33.3% | 12 |
| By morphology | street corridor | 33.3% | 3 |

"More/less restrictive" denotes the direction of classification divergence between the two
methods, not the correctness of either; neither method is field-validated.

---

## Table S2. Decision confidence and tested-uncertainty detail

Sources: `outputs/tables/solar_forcing_sensitivity.csv`,
`data/processed/phase2_2_decision_confidence.csv`. Envelope = [min, max] UTCI (°C) over the
tested realizations.

**(a) Solar-forcing sensitivity (decisions changed vs clear-sky baseline, of 42):**

| Realization | Decisions changed | % |
|---|---|---|
| Satellite-derived irradiance (EUMETSAT CM SAF) | 1 | 2.4% |
| −10% GHI | 0 | 0.0% |
| −20% GHI | 0 | 0.0% |

**(b) Confidence distribution (of 42 outdoor observations):** ROBUST 35 (83.3%),
BOUNDARY 6 (14.3%), UNSTABLE 1 (2.4%).

**(c) The six BOUNDARY and one UNSTABLE observations (near the 46 °C boundary):**

| Asset | Timestamp | Class | Envelope (°C) |
|---|---|---|---|
| A15 | 15:00 | BOUNDARY | 42.4–44.5 |
| A16 | 15:00 | BOUNDARY | 43.7–45.1 |
| A24 | 15:00 | BOUNDARY | 44.1–45.1 |
| A25 | 15:00 | BOUNDARY | 44.0–45.0 |
| A15 | 18:00 | BOUNDARY | 42.8–45.2 |
| A16 | 18:00 | BOUNDARY | 43.9–45.9 |
| A24 | 18:00 | **UNSTABLE** | 44.2–46.0 |

Tested uncertainty covers solar forcing (four realizations, all rows) plus targeted canopy
geometry (two assets); it is a lower bound on total uncertainty and is not a validation of
the modelled field.

---

## Table S3. Exclusion-reason frequency across the eight scenarios

Source: `outputs/tables/phase3_exclusion_reasons.csv`. Every excluded candidate carries
exactly one machine-readable reason (defined in Table 2).

| Exclusion reason | Count across scenarios |
|---|---|
| `ACCESSIBILITY_CONSTRAINT` | 93 |
| `CLOSED_AT_TIMESTAMP` | 43 |
| `OUTDOOR_EXPOSURE_TOO_HIGH` | 20 |
| `NO_MEANINGFUL_THERMAL_IMPROVEMENT` | 2 |
| `INSUFFICIENT_EVIDENCE` | 1 |

The 23 options reported in the main text as removed "on thermal/evidence grounds" are the
`OUTDOOR_EXPOSURE_TOO_HIGH` + `NO_MEANINGFUL_THERMAL_IMPROVEMENT` + `INSUFFICIENT_EVIDENCE`
removals attributable to each scenario's source-relative screen (Table 3); accessibility and
opening-hours exclusions are counted separately above.

---

## Table S4. Opening-hours provenance (summary)

Source: `data/processed/phase3_osm_opening_hours_raw.csv`, `src/phase3_build_catalog.py`
(`DOCUMENTED_HOURS`). Of 27 assets, opening hours were harvested from OpenStreetMap tags for
11 and filled from documented institutional schedules for 16; each carries a source string
and an evidence-completeness flag. Hours were documented in 2026 and applied to the 2023
study day (temporal-alignment limitation, Section 5.5). Real Monday-in-August closures used
include Museo Naval, Antropología and Artes Decorativas, Real Fábrica de Tapices, Thyssen
(16:00 close), and the Real Observatorio (guided visits Fri–Sun only). A per-asset table with
source strings is available in the repository.

---

## S5. Software and reproducibility

Physical modelling used the official standalone `solweig` package (version 0.1.0b92) under a
dedicated Python 3.12 environment; the geospatial and screening pipeline ran under the
project's main Python. UTCI was computed by the package's own built-in module. All reported
tables and figures regenerate from the locked inputs via the project scripts
(`src/*.py`; figure scripts in `outputs/publication/figures/`), with per-figure numeric
assertions and SHA-256 hashes recorded in `docs/PHASE5_3B_RENDER_MANIFEST.csv`. Model
parameters were left at documented package defaults (Section 2.4); no parameter was tuned to
a target result. [PUBLIC REPOSITORY URL / RELEASE DOI TO VERIFY.]
