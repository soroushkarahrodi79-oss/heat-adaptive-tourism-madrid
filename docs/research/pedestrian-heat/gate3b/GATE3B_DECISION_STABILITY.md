# GATE3B_DECISION_STABILITY — per-perturbation A−B and sign stability

**Version 2.0 · 2026-09-15 (CORRECTED: stateful SOLWEIG + hardened Catastro, AMENDMENT_003).**
Route A − Route B time-weighted mean UTCI (M2, °C); A−B < 0 ⇒ Route A cooler. Baseline =
corrected Gate-3A (stateful, v = 1.1 m/s). v1 (provisional, non-stateful) values shown for
comparison.

## 14:00 departure

| Perturbation | A−B CORRECTED | A−B (v1 provisional) | sign vs baseline |
|---|---|---|---|
| EP0 baseline | −0.042 | −0.048 | — |
| EP1b forcing (EA) | −0.042 | −0.045 | same |
| **EP2b canopy PNOA** | **+0.226** | +0.227 | **REVERSED** |
| EP2c canopy tree-inv | −0.025 | +0.006 | same (was borderline+) |
| EP2d canopy TCD | −0.091 | −0.100 | same |
| EP4b building PNOA | −0.018 | −0.021 | same |
| **EP5 side −12 m** | **+0.148** | +0.180 | **REVERSED** |
| EP5 side +12 m | −1.268 | −1.307 | same (large) |
| EP6 speed 1.4 | −0.072 | −0.077 | same |
| **range** | **−1.268 … +0.226 (spans 0)** | −1.307 … +0.227 | |

## 17:00 departure

| Perturbation | A−B CORRECTED | A−B (v1 provisional) | sign vs baseline |
|---|---|---|---|
| EP0 baseline | −0.367 | −0.365 | — |
| EP1b forcing (EA) | −0.372 | −0.370 | same |
| EP2b canopy PNOA | −0.067 | −0.066 | same (near 0) |
| EP2c canopy tree-inv | −0.181 | −0.185 | same |
| EP2d canopy TCD | −0.363 | −0.359 | same |
| EP4b building PNOA | −0.295 | −0.292 | same |
| **EP5 side −12 m** | **+0.366** | +0.377 | **REVERSED** |
| EP5 side +12 m | −0.282 | −0.230 | same |
| EP6 speed 1.4 | −0.385 | −0.387 | same |
| **range** | **−0.385 … +0.366 (spans 0)** | −0.387 … +0.377 | |

## Findings (unchanged by the correction)
1. **Intensity ordering NOT robust.** The A−B sign **reverses** under ≥1 justified perturbation
   at both departures — 14:00 under **E-P2b PNOA canopy** and **E-P5 side-of-street**; 17:00
   under **E-P5 side-of-street**. (E-P2c tree-inventory is now marginally negative rather than
   marginally positive — the point is that the canopy state at 14:00 sits on/across zero.)
2. **Within modeled uncertainty.** Baseline A−B 0.04 °C (14:00) / 0.37 °C (17:00); the
   perturbation ensemble spans zero at both times.
3. **Intensity vs duration disagree.** Intensity marginally favours A; duration favours B
   (shorter route, fewer high-stress minutes) — preserved trade-off.
4. **Category-boundary proximity (NC6).** Route point-max UTCI 45.0–45.9 °C across perturbations,
   just below +46 °C.

**Sign reversal under ≥1 justified perturbation + metric disagreement + boundary proximity ⇒
ABSTAIN / NO ROBUST DIFFERENCE (unchanged from the provisional run).**
