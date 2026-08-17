# PHASE2_2_GEOMETRY_RECHECK.md — HATI-Madrid Phase 2.2, Task A

Version 1.0 · 2026-08-17. Targeted re-check of the three geometry-flagged
garden assets from `docs/PHASE2_1_GEOMETRY_CONFIDENCE.md`. This **resolves or
quantifies** the vegetation-vintage uncertainty; it does not rebuild vegetation
for the rest of the pilot. The Phase 2 LiDAR CDSM is preserved unchanged; a
separate corrected variant is built only where the evidence defensibly supports
it.

---

## 1. The decisive new evidence: real per-tree heights

Audit 2 (Phase 2.1) only *counted* Madrid-inventory trees. The inventory also
carries a real **height attribute (`altura_m`)** per tree. Phase 2.2 exploits
it, at 10/20/30 m radii, because canopy from trees just outside the 10 m buffer
still shades pixels inside it. Source table:
`data/processed/phase2_2_geometry_evidence.csv`.

| Asset | canopy trees (>3 m) 10 m / 20 m / 30 m | median · max canopy height 30 m | LiDAR CDSM mean · max 10 m | TCD 2018 | Green cov. |
|---|---|---|---|---:|---:|
| A23 Jardines de Cecilio Rodríguez | 2 / 2 / 4 | 12 m · 20 m | 0.62 m · 4.0 m | 49.2% | 100% |
| A24 La Rosaleda | **0 / 0 / 0** | — · — | 0.10 m · 3.0 m | 26.2% | 100% |
| A27 Jardines del Arquitecto Herrero Palacios | 0 / 9 / 25 | 11–13 m · 14 m | 0.88 m · 8.0 m | 65.5% | 100% |

## 2. Per-asset findings

### A23 — Jardines de Cecilio Rodríguez → **PARTIALLY STALE**
Real inventoried canopy exists but is modest at the immediate point (2 trees
~4 m within 10 m; taller 12–20 m trees appear only at 20–30 m). Notably the
LiDAR CDSM *max* within 10 m (4.0 m) already matches those two 4 m trees, so
LiDAR is not blind here — it modestly understates a genuinely semi-open formal
garden ("densely-planted, well-shaded (cedars)" per the asset note; TCD 49%).
- **Bias direction:** SOLWEIG **overestimates** heat (understated canopy).
- **Decision-relevant?** Marginally. Baseline UTCI 44.4 °C at 15:00 (the tighter
  case); correction moves it *away* from the 46 °C threshold.

### A24 — La Rosaleda → **REPRESENTATIVE (near-zero canopy is genuine)**
This is the headline geometry finding. The strongest, most spatially-explicit
source — the per-tree inventory *with heights* — finds **zero** canopy trees of
any height within 10, 20, **or 30 m**. The asset is a rose garden
("shrub-height roses rather than closed tree canopy", pilot note; the lowest
TCD of the three, 26.2%). The Audit 2 "POSSIBLY STALE" flag was driven by
green-polygon coverage (100% — but that only means the point sits inside a
mapped *garden polygon*, not under canopy) and moderate TCD; the height-aware
inventory overturns it. The near-zero LiDAR canopy is **correct**, not stale.
- **Bias direction:** none — LiDAR represents reality here.
- **Decision-relevant?** Yes, but in the *opposite* way to what was feared: A24
  was the project's single most fragile asset, flagged by **two** independent
  audits (solar + geometry). Phase 2.2 **de-flags its geometry**, leaving only
  the genuine solar-boundary case at 18:00. No correction is applied (inserting
  canopy the inventory says is absent would be fabrication).

### A27 — Jardines del Arquitecto Herrero Palacios → **MATERIALLY STALE**
The clearest stale case. Abundant real tall canopy nearby (9 inventoried
canopy trees within 20 m, 25 within 30 m, median 11–13 m, max 14 m; highest
TCD, 65.5%; "mature tree cover" per the asset note) where LiDAR reads near-zero
(0.88 m mean). The 0-within-10 m count is a point-placement artefact (the asset
point sits in a path/clearing) — the surrounding mature canopy would shade the
10 m buffer at the relevant sun angles.
- **Bias direction:** SOLWEIG **overestimates** heat (materially understated canopy).
- **Decision-relevant?** Yes; baseline UTCI 43.5 °C at 15:00, correction moves
  it further below 46 °C.

## 3. Localized correction — implemented for A23 & A27, not A24

A defensible, reproducible correction **was constructed and run** for A23 and
A27 (`src/phase2_2_build_corrected_cdsm.py`): 29 real inventoried canopy trees
(heights 4–20 m) burned into a copy of the locked CDSM at their real positions
and heights, bracketed by crown radius R ∈ {2, 3, 4} m. SOLWEIG was rerun on
all three variants with Phase 2 baseline weather. Corrected 10 m-buffer UTCI:
`data/processed/phase2_2_corrected_geometry_utci.csv`;
`outputs/tables/phase2_2_geometry_changes.csv`.

| Asset | timestamp | UTCI baseline | UTCI corrected (narrow / central / wide) | Δ central | decision |
|---|---|---:|---:|---:|---|
| A23 | 12:00 | 39.4 | 39.3 / 39.1 / 39.0 | −0.3 | unchanged (FWC) |
| A23 | 15:00 | 44.4 | 44.1 / 44.0 / 43.7 | −0.4 | unchanged (FWC) |
| A23 | 18:00 | 41.9 | 41.8 / 41.8 / 41.6 | −0.1 | unchanged (FWC) |
| A27 | 12:00 | 37.6 | 36.8 / 36.5 / 35.8 | −1.1 | unchanged (FWC) |
| A27 | 15:00 | 43.5 | 43.3 / 43.1 / 42.7 | −0.4 | unchanged (FWC) |
| A27 | 18:00 | 42.2 | 42.1 / 41.8 / 41.6 | −0.4 | unchanged (FWC) |
| A24 | all | (uncorrected) | control Δ = 0.0 at every timestep | 0.0 | unchanged (FWC) |

**Key results:**
- The correction confirms the Phase 2.1 directional hypothesis with real
  magnitudes: canopy correction lowers UTCI at both stale assets (A23 up to
  −0.7 °C, A27 up to −1.8 °C at the wide bracket), i.e. the LiDAR-based model
  **overestimated** heat there, as predicted.
- **No decision flips** under any variant or timestamp — every corrected value
  remains FEASIBLE WITH CONDITIONS. The correction cannot create new
  NOT-RECOMMENDED decisions because it only adds shade.
- The previously-UNSTABLE A23 15:00 row moves *further from* the 46 °C
  threshold, resolving the concern that made it fragile.
- The A24 control delta is exactly 0.0 everywhere — a clean check that the
  localized edit is genuinely localized.

## 4. Can the corrected geometry be constructed reproducibly? — Yes (A23/A27)

The correction uses only real municipal per-tree positions and heights; the
sole assumption (crown radius) is explicitly bracketed and carried into the
decision-uncertainty envelope (`docs/PHASE2_2_DECISION_UNCERTAINTY.md`) rather
than hidden as a point value. For A24 the honest, evidence-based action is the
opposite of correction: retain the original geometry and **reduce** its geometry
uncertainty, because the strongest evidence confirms it.

## 5. Residual geometry uncertainty after Phase 2.2

- A23/A27: **resolved** in the decision-relevant direction (corrected, no flip,
  moved away from threshold).
- A24: geometry **confirmed representative**; its remaining fragility is solar,
  not vegetation.
- The unaudited-in-Audit-2 plaza/attraction assets (A14–A16, A18, A22, A26) are
  predominantly hardscape with little on-site vegetation and are not implicated;
  no systematic, across-the-board geometry failure exists (consistent with
  Audit 2). Crown radius remains an assumption (bracketed), and no field survey
  of actual 2023 canopy was performed — stated as a bounded residual, not a
  claim of exactness.
