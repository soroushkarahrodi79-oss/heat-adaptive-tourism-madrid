# GATE3A_SAMPLING_CORRECTION — audit fix of the route sampler

**Version 1.0 · 2026-09-15.** Corrects a Gate-3A implementation mismatch against the frozen
Gate-2 sampling spec (`GATE2_METRIC_SPEC.md` §0). **Thermal rasters (SOLWEIG geometry +
forcing) were NOT re-run** — only the sampling/metrics layer changed. Baseline compared
against commit `675f2e5663b476d196c210664e890de2ea816d4c`.

## 1. Defect
The old `densify()` reset 5 m spacing **inside each original OSM segment**
(`n=max(1,int(seg//DS)); f=k/n`), so sample spacing depended on vertex geometry — not true
fixed chainage — and every sample was assumed to represent exactly 5 m (equal-weight M2/M3;
undercounted M4). Observable: A had 498 samples (×5 m = 2490 m ≠ 2657.8 m); M4 minutes summed
to ~33.2 min while M1 = 35.44 min.

## 2. Fix
- **True global chainage:** intervals [0,5),[5,10),…,[k·5, L] measured continuously from the
  route origin (final partial interval included); sample at each interval **midpoint**.
- **Represented length (dwell weight)** carried per sample = interval length.
- **M2** = represented-length-weighted mean; **M3** = weighted percentiles; **M4** minutes =
  represented_length / v per category; **M1** = L / v.
- Baseline speed corrected to **1.1 m/s** (frozen E-P6; AMENDMENT_002; the 1.25 m/s midpoint
  was unauthorised).

## 3. Invariants / tests (`tests/pedestrian_heat/test_gate3a_sampling.py`, 5/5 PASS)
- Σ represented length == route length (A 2657.81 m, B 2365.67 m) ✓
- Σ M4 category minutes == M1 exactly (all samples classified) ✓
- weighted M2 reproduces a constant synthetic field exactly ✓
- identical synthetic route with different vertex segmentation → identical M2/M3/M4 ✓
- interior sample spacing == 5 m in chainage; n = ceil(L/5) ✓

## 4. Old vs corrected (n_samples, spacing, metrics)

| Quantity | OLD (commit 675f2e5; v=1.25, per-vertex) | CORRECTED (v=1.1, global chainage) |
|---|---|---|
| n_samples A / B | 498 / 453 | **532 / 474** ( = ⌈L/5⌉ ) |
| represented spacing | variable (per-segment restart) | fixed 5 m (last partial 2.8 m A / 0.7 m B) |
| Σ rep_len A / B | 2490 / 2265 m (≠ L) | **2657.81 / 2365.67 m (= L)** |
| M4 Σ vs M1 | 33.2 vs 35.44 (mismatch) | **equal (exact)** |
| **M2 A / B — 14:00** | 40.43 / 40.52 | 40.497 / 40.545 |
| **M2 A−B — 14:00** | −0.10 | **−0.048** |
| **M2 A / B — 17:00** | 42.27 / 42.68 | 42.182 / 42.547 |
| **M2 A−B — 17:00** | −0.41 | **−0.365** |
| M3 IQR A (14:00 / 17:00) | 3.49 / 4.52 | 3.56 / 4.45 |
| M3 IQR B (14:00 / 17:00) | 2.83 / 2.70 | 2.80 / 2.80 |
| M1 A / B (min) | 35.44 / 31.54 (@1.25) | 40.27 / 35.84 (@1.1) |
| very-strong+extreme min A / B — 17:00 | 33.2 / 30.2 | 40.27 / 35.84 |

Speed-robustness QA (frozen 1.4 m/s, not the perturbation matrix): M2 A−B = **−0.077**
(14:00), **−0.387** (17:00).

## 5. Does the A−B ordering change?
**No.** Route A retains the **lower mean UTCI** (cooler intensity) at **both** departures and
**both** frozen speeds (A−B negative throughout: −0.048/−0.365 at 1.1 m/s; −0.077/−0.387 at
1.4 m/s). Route B remains **shorter** with **fewer** high-stress minutes. The correction
shifted magnitudes slightly (notably the 14:00 gap shrank to ~0.05 °C) but **reversed no
ordering**.

## 6. Does the intensity/duration trade-off survive?
**Yes.** THERMAL INTENSITY still favours A (cooler mean UTCI); EXPOSURE DURATION still favours
B (shorter trip, fewer high-stress minutes). The families still point to different routes; the
trade-off is preserved, not collapsed. No composite score.

## 7. Interpretation status
The correction did **not** change the Gate-3A interpretation: **BASELINE DIFFERENCE OBSERVED**,
trade-off preserved, no route declared preferred. The 14:00 intensity gap is now very small
(~0.05 °C), reinforcing that the robustness gate may legitimately return
ABSTAIN / NO ROBUST DIFFERENCE. → verdict **GATE3A_CORRECTED_GO_TO_3B**.
