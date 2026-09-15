# GATE3B_METHOD — Robustness / uncertainty experiment

**Version 1.0 · 2026-09-15.** Executes the FROZEN Gate-2 pre-registered perturbation set and
the frozen decision-stability rule on the Gate-3A baseline. Path B; ABSTAIN is a first-class
outcome. Inherits AMENDMENT_001 (terrain MDT 2023) and AMENDMENT_002 (baseline speed 1.1 m/s).

## Design
For each frozen perturbation the modeled UTCI field is recomputed (or re-sampled) and the
Route A − Route B difference is evaluated **per metric**; the decision rule tests whether the
sign is preserved across **all** justified perturbations. Baseline geometry/forcing = Gate 3A.

| Dim | Perturbation states run | Implementation |
|---|---|---|
| E-P1 forcing | (a) Barajas [baseline]; (b) EA-adjusted (empirical hourly Escuelas-Aguirre − Barajas Ta/RH: +0.1/−0.1 °C Ta, +3 % RH) | new SOLWEIG run, baseline geometry |
| E-P2 canopy (dominant) | (a) MDS-2023 nSH masked-to-veg [baseline]; (b) PNOA veg nDSM 2008–2015; (c) municipal tree-inventory buffer mask × nSH; (d) Copernicus TCD ≥ 30 % mask × nSH | new SOLWEIG run per CDSM |
| E-P3 wind | demoted (uniform only) — not perturbed | — |
| E-P4 building | (a) MDS−MDT via Catastro footprints [baseline]; (b) PNOA building nDSM 2008–2015 | new SOLWEIG run, new DSM |
| E-P5 side-of-street | frozen trace vs ±12 m lateral offset (opposite kerb approximation) | re-sample baseline fields |
| E-P6 speed | 1.1 m/s [baseline] vs 1.4 m/s | re-sample (traversal-time field selection) |

Canopy coverage across E-P2 states spans **4.9 %–41 %** (tree-inventory → PNOA), directly
probing the dominant direction-changing uncertainty.

## Thermal computation
`solweig` 0.1.0b92 (`.venv_solweig`), same domain (370×1081 @ 2 m), Δt = 15 min fields
(8 timestamps per config), corrected global-chainage sampling (v = 1.1 m/s; 10 m buffer-mean).
Memory note: the run environment had ~1 GB free RAM, so each config's 8 timestamps were run
one-per-process (SVF cached once, reused) with a retry-fill loop for transient OOM — all
5 configs reached 8/8 rasters; this is an execution/logistics detail with no effect on values.

## Decision rule (frozen, GATE2_METRIC_SPEC §3)
- ROBUST: sign of A−B agrees across M1–M4 AND preserved across all perturbations AND category
  metrics clear of a UTCI boundary.
- NO ROBUST DIFFERENCE: metrics disagree / within uncertainty.
- ABSTAIN: sign reverses under ≥1 justified perturbation, OR boundary straddle, OR essential
  input missing, OR uncertainty spans the decision.

## Outputs
`GATE3B_PERTURBATION_RESULTS.csv` (A−B per metric per perturbation × departure);
`GATE3B_DECISION_STABILITY.md`; `GATE3B_NEGATIVE_CONTROLS.md`; `GATE3B_MODEL_PROVENANCE.json`;
`GATE3B_DECISION.md`. Reproduce: `src/gate3b_build_perturbation_geometry.py` →
`src/gate3b_run_one.py <config> [label]` (per config/timestamp) → `src/gate3b_analyze.py`.
Heavy rasters gitignored; hashes in provenance.
