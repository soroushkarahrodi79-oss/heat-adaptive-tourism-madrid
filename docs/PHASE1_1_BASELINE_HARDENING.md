# PHASE1_1_BASELINE_HARDENING.md — HATI-Madrid Phase 1.1

Version 1.0 · 2026-08-17. Gate in effect at start: **REVISE BASELINE**
(`docs/PHASE1_GATE.md`). This document is a stress-test of the Phase 1 baseline,
not a rebuild: no SOLWEIG, UTCI, dashboard, ML, or city-wide expansion was
started. All four audits below use only real, currently-accessible data.

Companion documents: `docs/PHASE1_1_SENSITIVITY_REPORT.md` (the quantitative
tables), `docs/PHASE1_1_GATE.md` (the final verdict).

---

## Audit 1 — Meteorological station consistency (Retiro vs. Barajas)

**Question:** the heat episode is justified by Madrid-Retiro's official daily
figures, but the hourly hazard input is Madrid-Barajas. Can real Retiro hourly
data be obtained to close that gap?

**Attempt log (all real, dated 2026-08-17):**

| Source | Result |
|---|---|
| AEMET OpenData API, `valores/climatologicos/diarios/datos/.../estacion/3195` | Anonymous request returns HTTP 401: `"JWT strings must contain exactly 2 period characters. Found: 0"`. Requires a registered `api_key`. Registering an account on the user's behalf without explicit authorisation is outside this project's scope (see operating constraints); email-verified registration is not completable synchronously in any case. |
| datosclima.es (third-party AEMET-data reseller) | Retiro hourly data is available only via a manual email request to a named mailbox plus a EUR 2.50 payment per batch of up to 3 stations. Not a programmatic, reproducible source; not a purchase this project makes unilaterally. |
| x-y.es (aggregator, `est-3195-madrid-retiro`) | Publishes a monthly page with a "Calendario" section for Retiro, but day-level detail renders as a non-interactive chart with no scrapable hourly table or per-day URL found. |
| Meteostat hourly file, station id `08222` (co-located with Retiro) | Already identified and rejected in Phase 1 (`data/raw/README.md`): the station's own inventory metadata shows `hourly: {start: null}` while `model: {start: "2021-01-01"}` matches the served file's start date exactly - i.e. the values are reanalysis-interpolated, not observed. |

**Determination: Retiro hourly data is UNAVAILABLE** through any free,
programmatic, immediately-reproducible channel. Per the task specification,
Retiro hourly values are **not fabricated or interpolated**.

**What was done instead:**
1. Barajas remains the sole hourly hazard input, now carrying an explicit,
   machine-readable `station_representativeness_note` field in every output row
   (`src/build_classifications.py`).
2. Retiro's **official** (not this project's own) daily/monthly figures are used
   as an independent cross-check, quantified for the first time in Phase 1.1:
   - Daily max, 2023-08-21: Retiro 40.0°C (official) vs. Barajas 40.5°C (this
     project's own hourly extract) → **+0.5°C**, Barajas warmer, consistent with
     an open airport apron vs. a shaded urban park.
   - Monthly mean, August 2023: Retiro 28.0°C (official) vs. Barajas 28.11°C
     (this project's own 744-hour extract) → **+0.11°C**, close agreement.
   - This is a real, quantified representativeness bound at daily/monthly
     scale. It is explicitly **not** evidence of hourly-scale agreement, which
     remains unverified and is stated as such in every output row.
3. **Terminology correction:** the gate is renamed, consistently, from "hazard
   gate" to **METEOROLOGICAL HAZARD gate** throughout `src/thresholds.py`
   (function `meteorological_hazard_state()`, column
   `meteorological_hazard_state`) and this documentation. An explicit scope
   statement was added to `src/thresholds.py` stating the gate classifies
   station-measured ambient air temperature against an official civil-protection
   warning scale, and must never be read as, or substituted for, UTCI/PET/WBGT.
   No prior Phase 0/1 document was found to mischaracterise AEMET thresholds as
   comfort thresholds (checked by grep across `docs/*.md`), so this is a
   forward-looking precision fix, not a correction of a prior error.

**Files changed:** `src/thresholds.py`, `src/build_classifications.py`,
`src/make_maps.py`, `tests/test_outputs.py`. **Files added:**
`data/raw/extreme_aug2021_barajas_raw.csv` is unrelated to this audit (see
Audit 2); no new raw file was added for Audit 1 since the negative result did
not produce a dataset.

---

## Audit 2 — EXTREME-hazard branch validation

**Question:** AEMET's red/EXTREME threshold (≥42°C) was implemented but never
empirically exercised by the Phase 1 baseline's three fixed 2023-08-21
timestamps (max reached: 40.5°C, SEVERE). Does a real observation exist that
crosses it, and does the branch behave sensibly when exercised?

**Real observation found:** **14 August 2021**, part of an AEMET-documented
"intensa ola de calor" spanning 11–15 August 2021
(`data/raw/aemet_official_pdfs/AEMET_avance_climat_MAD_202108.pdf`, official
AEMET Delegación Territorial en Madrid monthly report). AEMET's own account: "el
día 14 cuando se registraron las temperaturas máximas más elevadas... los 42.7°C
de Barajas... nuevas efemérides" (a new station record at the time). This
project's own real hourly extract for Barajas that day
(`data/raw/extreme_aug2021_barajas_raw.csv`, same station/source pipeline as the
Phase 1 episode) independently shows 42.4°C at 18:00 local (UTC+2) — a 0.3°C gap
from the official figure, consistent with the same small, expected
methodology-vs-continuous-sensor discrepancy already documented for the
2023-08-21 episode (40.5 vs. 40.0°C).

**Test design:** `src/audit2_extreme_stress_test.py` runs the *unmodified*
Phase 1 architecture (`compute_site_metrics`, `feasibility_decision`,
`evidence_confidence`) against this real day, using the **identical** three
canonical clock times (12:00/15:00/18:00 local) for direct comparability:
12:00→33.2°C (LOW), 15:00→39.5°C (SEVERE), 18:00→42.4°C (EXTREME). This is
explicitly labelled an **architecture stress test**, not a second adopted
episode: the exposure/adaptation spatial layers remain the current (2026) OSM
snapshot, not 2021 conditions — the same temporal-mismatch caveat already
carried by the Phase 1 baseline's own 2023-08-21 episode, three years larger.

**Result: the branch behaves sensibly.** At the real EXTREME reading, **all 14
outdoor assets → NOT RECOMMENDED, unconditionally** (rule 1 fires regardless of
exposure or adaptation state — verified explicitly for well-shaded, well-served
sites like Real Jardín Botánico and Jardines de Cecilio Rodríguez, which are
excluded exactly the same as the open plazas, confirming rule 1's intended
unconditional precedence). All 13 indoor assets → FEASIBLE WITH CONDITIONS,
consistent with the indoor rule. Across the full synthetic-free 3-timestamp
run: 0 excluded at LOW, 5 at SEVERE, 14 at EXTREME — a monotonic escalation
identical in shape to the Phase 1 baseline's own 2023-08-21 pattern.

**Determination: the EXTREME branch is now empirically VALIDATED** (not merely
implemented) via a real, independently-confirmed AEMET reading, and it behaves
as designed. `tests/test_outputs.py::test_extreme_branch_validated_by_stress_test`
pins this result going forward.

**Files added:** `data/raw/extreme_aug2021_barajas_raw.csv`,
`data/raw/aemet_official_pdfs/AEMET_avance_climat_MAD_202108.pdf`,
`src/audit2_extreme_stress_test.py`,
`data/processed/extreme_branch_stress_test_2021-08-14.csv`.

---

## Audit 3 — Adaptation-resource gate discrimination test

**Question:** Phase 1 found `adaptation_state` was GOOD/LIMITED for all 27
pilot assets, never POOR, so its exclusion rule never fired
(`docs/PHASE1_VALIDATION_REPORT.md` §3). Does it add real discrimination, or is
it decorative?

**Test A — threshold sensitivity** (`src/audit3_adaptation_gate_test.py`,
Part A): grid-searched water/transit distance thresholds from the baseline
(250 m / 400 m) down to very tight values. POOR does not appear for ANY of the
27 core assets until thresholds are tightened to 250 m water / **100 m**
transit or tighter — well below any cited walkability standard (the
literature range used throughout this project is 250–400 m; sub-100 m has no
citation basis here). Full grid in `docs/PHASE1_1_SENSITIVITY_REPORT.md`.

**Test B — small bounded ring extension** (`src/audit3_adaptation_gate_test.py`,
Part B): 6 additional real, named OSM assets just beyond the study-area box,
still Retiro/Atocha-adjacent (Plaza Niño Jesús, Jardines Doce de Octubre,
Parque Daoíz y Velarde, La Casa Encendida, Jardín de Palestina, Casa de
Cervantes — **not** added to the adopted pilot set, kept as a separate
discrimination-test sample), chosen specifically to be more peripheral than the
core 27. Evaluated against a correspondingly widened real water/transit point
set (201 water points, 276 transit points in the ring bbox). **All 6 ring
assets were also GOOD or LIMITED — none POOR.** Removing the adaptation-based
exclusion rule changed **0 of 18** ring-asset feasibility rows. Re-testing the
core 27 against the wider water/transit set (a superset of the original)
changed **0 of 27** `adaptation_state` values.

**Determination: the gate is non-discriminatory** at any defensible distance
threshold, confirmed by three independent real-data checks (Phase 1's original
27, the threshold grid, and the 6-asset ring). Per the task's explicit
instruction, it is **demoted, not silently kept**:
- The exclusion rule ("SEVERE hazard + adaptation==POOR → NOT RECOMMENDED") is
  **removed** from `src/thresholds.py:FEASIBILITY_RULES_OUTDOOR` and
  `src/build_classifications.py:feasibility_decision()`.
- `water_dist_m`, `transit_dist_m`, and `adaptation_state` remain computed and
  reported in every output row as real, useful practical context — they are
  simply no longer decision-relevant.
- Removing the rule changed **0 of the 81 Phase 1 pilot rows** (confirmed by
  re-running the full pipeline and comparing feasibility-state counts before/
  after: 41 FEASIBLE WITH CONDITIONS / 35 FEASIBLE / 5 NOT RECOMMENDED,
  unchanged), because the rule had never fired on real data in the first place.

**Files added:** `data/raw/osm/query_ring*.overpassql`,
`data/raw/osm/osm_ring_raw.json`, `osm_ring_water_raw.json`,
`osm_ring_transit_raw.json`, `src/audit3_adaptation_gate_test.py`,
`data/processed/audit3_ring_extension.csv`. **Files changed:**
`src/thresholds.py`, `src/build_classifications.py`,
`tests/test_outputs.py` (added `test_adaptation_gate_stays_demoted`).

---

## Audit 4 — Shade-proxy sensitivity audit

**Question:** the exposure gate relies on OSM tree-point count within a
buffer. How sensitive is the resulting classification to that specific proxy
choice, tested against real alternatives?

**Two alternative real-data proxies built** (`src/audit4_shade_proxy_test.py`,
full methodology and per-proxy limitations in its module docstring and
`docs/PHASE1_1_SENSITIVITY_REPORT.md`):

- **Proxy 2 — green-polygon coverage fraction**: % of a uniform 50 m buffer
  around each asset covered by real OSM park/garden/wood/forest polygons
  (161 polygons fetched with full geometry for the whole study area, not just
  the 8 pilot-asset parks). Approximates vegetated/permeable land cover
  (evapotranspirative cooling potential), not overhead canopy specifically.
- **Proxy 3 — building density**: count of real OSM building centroids within
  the same 50 m buffer, as a structural street-canyon/enclosure proxy.
  Explicitly **not** a shadow model (no building-height data available in this
  area, consistent with `docs/DATA_SOURCE_INVENTORY.csv`) — a genuinely
  different physical mechanism (built shade) from proxies 1/2 (vegetation).

**Result: substantial, non-uniform disagreement.**

| Comparison | Outdoor-asset-timestamp agreement (n=42) |
|---|---:|
| Proxy 1 (tree count) vs. Proxy 2 (green coverage) | 81.0% (34/42) |
| Proxy 1 (tree count) vs. Proxy 3 (building density) | 57.1% (24/42) |

**10 of 14 outdoor assets (71%)** have a feasibility classification that
changes under at least one proxy pair at at least one timestamp
(`data/processed/audit4_unstable_assets.csv`,
`outputs/maps/05_audit4_unstable_assets.png`).

**A specific, diagnosable failure mode was found in Proxy 3**, not just
generic noise: building density is mapped so that *more* buildings implies
*more* potential shade (for comparability with proxies 1/2, where more
vegetation implies more shade) — but this inverts incorrectly for genuine park
interiors. Five of the pilot's best-documented shaded gardens (Real Jardín
Botánico, Jardines de Cecilio Rodríguez, La Rosaleda, Jardín del Parterre,
Jardines del Arquitecto Herrero Palacios) have **zero** buildings within 50 m
precisely *because* they are deep inside parkland — Proxy 3 misreads this as
"poor shade" (bottom tercile) rather than recognising it as strong evidence of
a well-vegetated interior. This is a proxy-design limitation discovered
empirically by cross-checking against a second, independent real signal, and
is reported as a specific finding, not folded anonymously into an aggregate
disagreement percentage. Proxy 2 (green coverage), by contrast, correctly
scores all five of those same gardens at or near 100% coverage.

**Determination:** the Phase 1 baseline's exposure classification is **not
robust to the choice of simple, non-physical shade proxy** — even between the
two most comparable, both-legitimate vegetation proxies (1 and 2), a real 19%
of outdoor-asset-timestamps disagree. This is reported as a genuine, load-bearing
finding for the Phase 1.1 gate decision (`docs/PHASE1_1_GATE.md`), not
minimised. No proxy was judged "more correct" than another except where a
specific, explicable failure mode (Proxy 3's park-interior inversion) could be
identified — reconciling proxies 1 and 2's residual disagreement would require
real canopy/shadow geometry, i.e. exactly the class of analysis SOLWEIG
provides and this Phase 1.1 pass explicitly does not start.

**Files added:** `data/raw/osm/query_all_green_polygons.overpassql`,
`data/raw/osm/osm_all_green_polygons_raw.json`,
`src/build_all_green_polygons.py`, `data/interim/all_green_polygons.geojson`,
`src/audit4_shade_proxy_test.py`,
`data/processed/audit4_proxy_comparison.csv`,
`data/processed/audit4_unstable_assets.csv`,
`outputs/maps/05_audit4_unstable_assets.png`. **Files changed:**
`src/make_maps.py`.

---

## Summary of code/data changes (audit trail)

| Change | Reason | Audit |
|---|---|---|
| `hazard_state` → `meteorological_hazard_state` (function + CSV column, everywhere) | Terminological precision; prevent any future reading as a comfort index | 1 |
| Added `station_representativeness_note`, quantified Barajas-vs-Retiro gap | Real spatial-representativeness limitation, explicit and quantified rather than asserted | 1 |
| Added `extreme_branch_stress_test_2021-08-14.csv` | Empirical validation of a previously-implemented-but-untested branch | 2 |
| Removed adaptation-based exclusion rule (old rule 3); kept `adaptation_state`/distances as reported context | Demonstrated non-discriminatory at any defensible threshold across 33 real assets | 3 |
| `METHOD_VERSION` bumped to `phase1.1-baseline-hardening-v1.1` | Version the rule-set change | 1, 3 |
| No change to hazard thresholds, exposure tercile method, or the EXTREME/SEVERE/ELEVATED/LOW band definitions | Not implicated by any audit finding | - |

Re-running `src/build_classifications.py` after all changes reproduces
identical Phase 1 feasibility counts (41 FEASIBLE WITH CONDITIONS / 35
FEASIBLE / 5 NOT RECOMMENDED) — Phase 1.1 corrected the architecture's honesty
and closed two validation gaps without silently altering the Phase 1 result
set. The one genuinely new empirical finding that changes the overall picture
is Audit 4's proxy sensitivity, which is a new fact, not a correction of a
Phase 1 error.
