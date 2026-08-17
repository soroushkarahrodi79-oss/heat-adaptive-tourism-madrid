# PHASE2_UTCI_METHOD.md — HATI-Madrid Phase 2

Version 1.0 · 2026-08-17.

**UTCI (Universal Thermal Climate Index) is a model-derived thermal-stress
index, not a measured or directly observed quantity, and it is never
described as measured human comfort anywhere in this project.** It combines
four inputs — air temperature, relative humidity, wind speed, and mean
radiant temperature (Tmrt) — through a documented, published polynomial
approximation of a human heat-exchange model (the Fiala multi-node
physiological model), calibrated by Bröde et al. (2012, *International
Journal of Biometeorology*).

---

## Implementation used

SOLWEIG's own built-in `solweig._utci` module, invoked automatically as part
of `solweig.calculate(..., outputs=["utci", ...])` (see
`docs/PHASE2_SOLWEIG_METHOD.md`). This is **not** a separate package or a
project-written formula — it is the same, single, documented implementation
shipped with and version-pinned to the SOLWEIG package used throughout this
phase (v0.1.0b92), computed pixel-by-pixel from SOLWEIG's own Tmrt output
plus the same real Ta/RH/wind inputs already used for the Tmrt calculation
(§ Meteorological forcing, `docs/PHASE2_SOLWEIG_METHOD.md`).

## Inputs to the UTCI calculation, per pixel

| Input | Source |
|---|---|
| Air temperature (Ta) | Real Madrid/Barajas hourly observation, uniform across the raster (station-scale forcing — see Wind limitation below) |
| Relative humidity (RH) | Real Madrid/Barajas hourly observation, uniform across the raster |
| Wind speed | Real Madrid/Barajas hourly observation, uniform across the raster — **not** spatially resolved at street level (no CFD/URock this phase, per the task's explicit prohibition; documented in `docs/PHASE2_VALIDATION_REPORT.md`) |
| Mean radiant temperature (Tmrt) | SOLWEIG's own per-pixel physical model output for the same timestep — the one input that DOES vary spatially at 2.5 m resolution, and the reason this phase exists |

## Official UTCI thermal-stress categories (used for interpretation, not invented)

The published Bröde et al. (2012) category system, used throughout this
phase's outputs (`utci_category` field in
`data/processed/phase2_asset_thermal_exposure.csv`):

| UTCI range | Category |
|---|---|
| 9 – 26 °C | No thermal stress |
| 26 – 32 °C | Moderate heat stress |
| 32 – 38 °C | Strong heat stress |
| 38 – 46 °C | Very strong heat stress |
| > 46 °C | Extreme heat stress |

These are **physiological stress categories**, describing the level of
strain a standardised human body model experiences — they are not, by
themselves, a tourism-feasibility recommendation.

## Translation to feasibility_state (this project's own decision, clearly labelled)

To compare against Phase 1's `feasibility_state` architecture, this phase
defines its own translation rule — a project decision informed by, but not
identical to, the official UTCI categories:

```
UTCI >= 46 C   -> NOT RECOMMENDED           (official "Extreme heat stress")
32 <= UTCI < 46 -> FEASIBLE WITH CONDITIONS (official "Strong" / "Very strong" heat stress)
UTCI < 32 C    -> FEASIBLE                  (official "Moderate" or below)
```

This rule was **pre-registered in `src/phase2_prereg.py` before any Tmrt/
UTCI raster was inspected**, and is not retuned after seeing results. It
collapses "Strong" and "Very strong" into a single FEASIBLE WITH CONDITIONS
band for direct comparability with Phase 1's three-state architecture
(which also has no intermediate state between FEASIBLE WITH CONDITIONS and
NOT RECOMMENDED). Indoor assets are exempt (§ below).

**This translation is a project judgement, not an official recommendation.**
The official UTCI literature frames "Very strong heat stress" (38–46 °C) as
warranting limited exposure duration for vulnerable groups, not necessarily
outright avoidance for the general population — this project's choice to
still call it FEASIBLE WITH CONDITIONS (not NOT RECOMMENDED) reflects that
nuance and is stated explicitly here rather than silently implied to be an
official threshold.

## What this does NOT claim

- UTCI is **not** measured thermal comfort. It is a model output computed
  from one measured-and-uniform set of inputs (Ta/RH/wind) and one
  spatially-resolved modelled input (Tmrt).
- AEMET's real station observations validate the Ta/RH/wind/pressure inputs
  to this calculation (§ `docs/PHASE1_1_BASELINE_HARDENING.md` Audit 1) —
  **AEMET does not, and cannot, validate the modelled Tmrt or the resulting
  UTCI**, which are physical-model outputs with no independent field
  observation in this project (see `docs/PHASE2_VALIDATION_REPORT.md`,
  "Direct Tmrt validation").
- This project does not infer or claim anything about actual tourist
  physiological experience, individual acclimatisation, clothing, or
  behaviour from a UTCI value — UTCI's underlying human model is a
  standardised reference person, not any real individual.
- Indoor assets are **not** assigned a UTCI value in this phase — SOLWEIG
  models the outdoor environment only; indoor assets retain their Phase 1
  indoor-bypass `feasibility_state` unchanged (see
  `docs/PHASE2_VALIDATION_REPORT.md`).
