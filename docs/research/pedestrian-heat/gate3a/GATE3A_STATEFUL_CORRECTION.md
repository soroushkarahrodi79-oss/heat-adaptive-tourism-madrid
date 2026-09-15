# GATE3A_STATEFUL_CORRECTION — SOLWEIG temporal-state + Catastro hardening (review fix)

**Version 1.0 · 2026-09-15.** Corrects two execution defects found in Gate-3A review
(AMENDMENT_003). **No** route, resolution, metric, decision rule, perturbation, or UTCI
boundary changed. Compared against commit `8a1597a` (the sampling-corrected baseline).

## Defects corrected
1. **Non-stateful SOLWEIG (BLOCKER).** Old runner called `calculate()` once per timestamp →
   fresh `ThermalState` each time → no 15-min surface/wall heat-storage continuity. **Fix:** a
   single `calculate(surface, weather=[72×15-min list 00:00→17:45])` stateful call; only the 8
   frozen decision fields extracted. Ran 72 timesteps in one series (35.6 s); no memory failure
   (RESOURCE_BLOCKED not triggered).
2. **Fail-open Catastro (BLOCKER).** Old `catastro_footprints()` swallowed per-subtile errors
   and regex-counted every `gml:posList` as a polygon. **Fix:** `src/catastro_bu.py` — every
   subtile must succeed (HTTP/exception/parse errors raise → build aborts), EPSG:25830 direct,
   structural GML parse (exterior/interior rings, multipart), dedup by `gml:id`, per-subtile
   provenance+hashes.

## Geometry impact
Building-footprint coverage **32.03 % → 30.14 %** (interior courtyards/holes no longer filled,
duplicates removed, multipart handled). `dsm_2m` sha `4fdb7f3c…`→`5a909578…`; `cdsm_2m`
`9d1d8894…`→`84f0efde…`; `dem_2m`/`veg_mask` unchanged. The corrected geometry is used for the
corrected thermal run.

## OLD vs CORRECTED — decision fields (domain-mean, °C)
| label | Tmrt old | Tmrt new | ΔTmrt | UTCI old | UTCI new | ΔUTCI |
|---|---|---|---|---|---|---|
| 14:00 | 57.54 | 56.80 | −0.74 | 40.37 | 40.20 | −0.18 |
| 14:15 | 57.91 | 57.11 | −0.80 | 40.84 | 40.65 | −0.19 |
| 14:30 | 58.29 | 57.48 | −0.80 | 41.31 | 41.12 | −0.19 |
| 14:45 | 58.68 | 57.92 | −0.76 | 41.78 | 41.61 | −0.18 |
| 17:00 | 56.57 | 56.57 | −0.00 | 43.02 | 43.02 | −0.00 |
| 17:15 | 55.78 | 55.84 | +0.06 | 42.76 | 42.77 | +0.01 |
| 17:30 | 54.85 | 54.94 | +0.08 | 42.38 | 42.39 | +0.02 |
| 17:45 | 54.02 | 54.08 | +0.06 | 42.01 | 42.02 | +0.01 |

Stateful preconditioning lowers the **midday** fields ~0.75 °C Tmrt / ~0.18 °C UTCI; the
**late-afternoon** fields are essentially unchanged (state converged). The shift is domain-wide.

## OLD vs CORRECTED — route metrics (v = 1.1 m/s)
| metric | OLD (8a1597a) | CORRECTED |
|---|---|---|
| M2 A / B — 14:00 | 40.497 / 40.545 | 40.345 / 40.387 |
| **M2 A−B — 14:00** | **−0.048** | **−0.042** |
| M2 A / B — 17:00 | 42.182 / 42.547 | 42.246 / 42.613 |
| **M2 A−B — 17:00** | **−0.365** | **−0.367** |
| M3max A / B — 17:00 | 45.50 / 45.44 | 45.53 / 45.48 |
| very-strong+ext min A / B — 17:00 | 33.2 / 30.2 → (v=1.1: 40.3 / 35.8) | 40.3 / 35.8 |
| n_samples A / B | 532 / 474 | 532 / 474 |
| off-raster / nan | 0 / 0 | 0 / 0 |
| temporal ±7.5 min sign flip | no | no (14:00 −0.07/−0.04/−0.09; 17:00 −0.38/−0.37/−0.30) |

## Because the shift is common-mode, A−B is preserved
The stateful + geometry corrections move **both** routes near-identically, so the decision-bearing
Route A − Route B difference is essentially unchanged (14:00 −0.048→−0.042; 17:00 −0.365→−0.367).
Route A retains the marginally lower mean UTCI at both departures; Route B remains shorter
(intensity/duration trade-off preserved); M3max still 43–45.5 °C (below the +46 °C extreme
boundary). **The Gate-3A interpretation does not change.**

## Verdict
**GATE3A_CORRECTED_GO_TO_3B** — chosen from corrected evidence, not by preserving the old
conclusion.
