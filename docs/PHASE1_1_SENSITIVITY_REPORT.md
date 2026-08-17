# PHASE1_1_SENSITIVITY_REPORT.md — HATI-Madrid Phase 1.1

Version 1.0 · 2026-08-17. Quantitative companion to
`docs/PHASE1_1_BASELINE_HARDENING.md`. All tables below are reproduced directly
from script output (`src/audit3_adaptation_gate_test.py`,
`src/audit4_shade_proxy_test.py`, `src/audit2_extreme_stress_test.py`) — no
numbers here are hand-edited from what those scripts printed.

---

## 1. Meteorological representativeness (Audit 1)

| Metric | Retiro (official, AEMET) | Barajas (this project's own hourly extract) | Gap |
|---|---:|---:|---:|
| Daily max, 2023-08-21 | 40.0°C | 40.5°C | +0.5°C |
| Monthly mean, Aug 2023 (n=744 hourly readings for Barajas) | 28.0°C | 28.11°C | +0.11°C |

No hourly-scale comparison is possible — that is the entire finding of Audit 1
(Retiro hourly data unobtainable; see `docs/PHASE1_1_BASELINE_HARDENING.md`
Audit 1 for the full attempt log). The two rows above are the only real,
quantified representativeness bounds available, and both are daily/monthly,
not hourly.

## 2. EXTREME-branch stress test (Audit 2)

Real Barajas hourly readings, 2021-08-14 (local Europe/Madrid, official AEMET
daily max 42.7°C):

| Local time | Temp (°C) | Meteorological hazard state |
|---|---:|---|
| 12:00 | 33.2 | LOW |
| 15:00 | 39.5 | SEVERE |
| 18:00 | 42.4 | EXTREME |

Feasibility outcome, all 27 pilot assets × 3 timestamps (n=81):

| Hazard state | FEASIBLE | FEASIBLE WITH CONDITIONS | NOT RECOMMENDED |
|---|---:|---:|---:|
| LOW | 22 | 5 | 0 |
| SEVERE | 0 | 22 | 5 |
| EXTREME | 0 | 13 | 14 |

At EXTREME: **all 14 outdoor assets → NOT RECOMMENDED** (including sites with
LOW/well-shaded exposure and GOOD adaptation access, confirming rule 1 fires
unconditionally as designed); **all 13 indoor assets → FEASIBLE WITH
CONDITIONS**.

## 3. Adaptation-gate threshold sensitivity grid (Audit 3, Part A)

27 core pilot assets, water/transit distance thresholds varied:

| water_thr (m) | transit_thr (m) | GOOD | LIMITED | POOR |
|---:|---:|---:|---:|---:|
| 250 | 400 (baseline) | 23 | 4 | 0 |
| 250 | 300 | 21 | 6 | 0 |
| 250 | 200 | 21 | 6 | 0 |
| 250 | 150 | 20 | 7 | 0 |
| 250 | 100 | 11 | 15 | **1** |
| 200 | 400 | 22 | 5 | 0 |
| 200 | 150 | 19 | 8 | 0 |
| 200 | 100 | 10 | 16 | **1** |
| 150 | 400 | 19 | 8 | 0 |
| 150 | 150 | 16 | 11 | 0 |
| 150 | 100 | 9 | 15 | **3** |
| 100 | 400 | 15 | 12 | 0 |
| 100 | 150 | 12 | 15 | 0 |
| 100 | 100 | 8 | 13 | **6** |
| 75 | 400 | 14 | 11 | **2** |
| 75 | 100 | 8 | 10 | **9** |
| 50 | 400 | 11 | 14 | **2** |
| 50 | 100 | 7 | 9 | **11** |

**Reading:** POOR is 0 for every threshold pair that keeps transit access at
150 m or looser, regardless of the water threshold. The first non-zero POOR
count appears only once the transit threshold is tightened to 100 m — under
half the baseline's already-tight 400 m (5-minute-walk) standard, and without
independent citation support in this project's source base.

## 4. Ring-extension test (Audit 3, Part B)

6 real assets beyond the study-area box, evaluated against a real, widened
water/transit point set (201 water points, 276 transit points):

| Asset | Type | Water dist (m) | Transit dist (m) | Adaptation state |
|---|---|---:|---:|---|
| Plaza Niño Jesús | outdoor | 121.1 | 15.5 | GOOD |
| Jardines Doce de Octubre | outdoor | 34.4 | 98.0 | GOOD |
| Parque Daoíz y Velarde | outdoor | 42.1 | 107.0 | GOOD |
| La Casa Encendida | indoor | 331.3 | 85.0 | LIMITED |
| Jardín de Palestina | outdoor | 17.3 | 92.9 | GOOD |
| Casa de Cervantes | indoor | 185.5 | 198.3 | GOOD |

0 of 6 are POOR. Re-scoring the core 27 against this same wider water/transit
set: 0/27 `adaptation_state` values changed from the original (narrower-set)
computation. Removing the adaptation exclusion rule changed 0/18 ring-asset
feasibility rows (isolated test with exposure forced to MODERATE so the rule
was actually reachable rather than short-circuited by the exposure rule — see
script comments in `src/audit3_adaptation_gate_test.py`).

## 5. Shade-proxy comparison (Audit 4)

Tercile cutpoints (empirical, this pilot's own distribution):

| Proxy | Metric | q1 | q2 |
|---|---|---:|---:|
| 1 (baseline) | tree_count in buffer/polygon | 0.00 | 2.00† |
| 2 | green-polygon coverage % (50 m buffer) | 48.27 | 100.00 |
| 3 | building count (50 m buffer) | 0.00 | 1.00 |

†Proxy 1's cutpoints as originally computed in `docs/PHASE1_METHOD.md`; reused
directly from `data/processed/pilot_classifications.csv` in this audit rather
than re-derived, so proxy 1 here is bit-for-bit identical to the Phase 1
baseline.

Per-asset proxy values (outdoor assets, n=14):

| Asset | P1 tree count | P1 state | P2 green % | P2 state | P3 buildings | P3 state |
|---|---:|---|---:|---|---:|---|
| Puerta de Alcalá (A14) | 0 | HIGH | 23.2 | HIGH | 1 | MODERATE |
| Fuente de Cibeles (A15) | 0 | HIGH | 11.0 | HIGH | 0 | HIGH |
| Fuente de Neptuno (A16) | 0 | HIGH | 15.4 | HIGH | 0 | HIGH |
| Estatua de Goya (A17) | 13 | LOW | 24.1 | HIGH | 0 | HIGH |
| Palacio de Cibeles (A18) | 3 | MODERATE | 0.0 | HIGH | 1 | MODERATE |
| Real Observatorio (A19) | 0 | HIGH | 96.6 | MODERATE | 2 | LOW |
| Parque del Retiro (A20) | 355 | LOW | 100.0 | MODERATE | 4 | LOW |
| Real Jardín Botánico (A21) | 55 | LOW | 100.0 | MODERATE | 0 | HIGH |
| Palacio de Cristal (A22) | 1 | MODERATE | 100.0 | MODERATE | 1 | MODERATE |
| Jardines de Cecilio Rodríguez (A23) | 4 | LOW | 100.0 | MODERATE | 0 | HIGH |
| La Rosaleda (A24) | 2 | MODERATE | 100.0 | MODERATE | 0 | HIGH |
| Jardín del Parterre (A25) | 2 | MODERATE | 100.0 | MODERATE | 0 | HIGH |
| Monumento a Alfonso XII (A26) | 0 | HIGH | 100.0 | MODERATE | 2 | LOW |
| Jardines del Arquitecto Herrero Palacios (A27) | 22 | LOW | 98.9 | MODERATE | 0 | HIGH |

**Note the Proxy 3 inversion**: A21, A23, A24, A25, A27 — five of the pilot's
best-documented shaded gardens — score `building_count_50m = 0` and are
therefore classified HIGH (poor shade) under Proxy 3's tercile split, while
Proxy 2 correctly scores all five at 98.9–100% green coverage. This is not
random noise; it is Proxy 3's core assumption (more buildings → more shade)
failing in exactly the terrain where it cannot hold (deep parkland has no
buildings by definition).

### Feasibility agreement (outdoor rows, n=42 = 14 assets × 3 timestamps)

**Proxy 1 vs. Proxy 2** — 81.0% agreement (34/42):

| Proxy1 \ Proxy2 | FEASIBLE | FEASIBLE WITH CONDITIONS | NOT RECOMMENDED |
|---|---:|---:|---:|
| FEASIBLE | 7 | 2 | 0 |
| FEASIBLE WITH CONDITIONS | 2 | 24 | 2 |
| NOT RECOMMENDED | 0 | 2 | 3 |

**Proxy 1 vs. Proxy 3** — 57.1% agreement (24/42):

| Proxy1 \ Proxy3 | FEASIBLE | FEASIBLE WITH CONDITIONS | NOT RECOMMENDED |
|---|---:|---:|---:|
| FEASIBLE | 3 | 6 | 0 |
| FEASIBLE WITH CONDITIONS | 3 | 19 | 6 |
| NOT RECOMMENDED | 0 | 3 | 2 |

### Unstable assets

**10 of 14 outdoor assets (71%)** have at least one timestamp where
feasibility differs between at least two of the three proxies:
A14, A17, A18, A19, A21, A23, A24, A25, A26, A27.
**Stable across all three proxies:** A15, A16, A20, A22 (4 of 14).

Full row-level detail: `data/processed/audit4_unstable_assets.csv`. Map:
`outputs/maps/05_audit4_unstable_assets.png`.

## 6. What this means for threshold/proxy robustness, in one paragraph

The meteorological hazard gate (official AEMET thresholds) and the exposure
gate's tercile-split *method* are not in question here — what Audit 4 shows is
that the specific *input variable* feeding the exposure gate (a raw tree
point count) is one defensible choice among several, and swapping it for
another defensible, real-data choice changes a material fraction of outdoor
classifications. Combined with Phase 1's own buffer-radius sensitivity finding
(`docs/PHASE1_VALIDATION_REPORT.md` §4: 1–7 of 14 assets shift under a ±20–25 m
radius change), the exposure gate is the least stable component of the entire
architecture — considerably less stable than the hazard gate (official,
externally fixed thresholds) or the now-demoted adaptation indicator.
