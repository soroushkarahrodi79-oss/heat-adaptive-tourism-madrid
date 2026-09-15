# GATE3B_DECISION_STABILITY — per-perturbation A−B and sign stability

**Version 1.0 · 2026-09-15.** Route A − Route B time-weighted mean UTCI (M2, °C) across the
frozen perturbations (A−B < 0 ⇒ Route A cooler). Baseline = Gate-3A (v = 1.1 m/s).

## 14:00 departure

| Perturbation | A−B (°C) | sign vs baseline |
|---|---|---|
| EP0 baseline | −0.048 | — |
| EP1b forcing (EA) | −0.045 | same |
| **EP2b canopy PNOA** | **+0.227** | **REVERSED** |
| **EP2c canopy tree-inv** | **+0.006** | **REVERSED** |
| EP2d canopy TCD | −0.100 | same |
| EP4b building PNOA | −0.021 | same |
| **EP5 side −12 m** | **+0.180** | **REVERSED** |
| EP5 side +12 m | −1.307 | same (large) |
| EP6 speed 1.4 | −0.077 | same |
| **range** | **−1.307 … +0.227 (spans 0)** | |

## 17:00 departure

| Perturbation | A−B (°C) | sign vs baseline |
|---|---|---|
| EP0 baseline | −0.365 | — |
| EP1b forcing (EA) | −0.370 | same |
| EP2b canopy PNOA | −0.066 | same (near 0) |
| EP2c canopy tree-inv | −0.185 | same |
| EP2d canopy TCD | −0.359 | same |
| EP4b building PNOA | −0.292 | same |
| **EP5 side −12 m** | **+0.377** | **REVERSED** |
| EP5 side +12 m | −0.230 | same |
| EP6 speed 1.4 | −0.387 | same |
| **range** | **−0.387 … +0.377 (spans 0)** | |

## Findings
1. **Intensity ordering is NOT robust.** The sign of the A−B mean-UTCI difference **reverses**
   under ≥1 justified perturbation at **both** departures — at 14:00 under the **canopy**
   states EP2b (PNOA) and EP2c (tree-inventory) and under side-of-street; at 17:00 under
   side-of-street. The dominant E-P2 canopy dimension flips the 14:00 ordering on its own.
2. **Magnitudes are within modeled uncertainty.** Baseline A−B is 0.05 °C (14:00) / 0.37 °C
   (17:00); the perturbation ensemble spans zero at both times. The difference is not
   separable from geometry/side uncertainty.
3. **Intensity and duration disagree.** Thermal intensity (M2) marginally favours Route A;
   exposure duration (M1, M4) favours Route B (shorter: 35.8 vs 40.3 min at 1.1 m/s → fewer
   high-stress minutes). The families point to different routes — a preserved trade-off.
4. **Category-boundary proximity (NC6).** Route point-max UTCI (M3max) sits at 45.0–45.9 °C
   across perturbations — just below the +46 °C "extreme heat stress" cut-point (EP1b, EP4b,
   EP5 reach 45.8–45.9) — i.e. the fields hug a category boundary.

**Per the frozen decision rule, sign reversal under ≥1 justified perturbation + metric
disagreement + boundary proximity ⇒ ABSTAIN / NO ROBUST DIFFERENCE.**
