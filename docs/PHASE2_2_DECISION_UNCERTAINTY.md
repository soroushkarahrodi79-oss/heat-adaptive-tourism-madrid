# PHASE2_2_DECISION_UNCERTAINTY.md — HATI-Madrid Phase 2.2, Task B

Version 1.0 · 2026-08-17. Replaces the false precision at the hard 32/46 °C
decision thresholds with an **evidence-derived** uncertainty envelope and a
separate decision-confidence field. The official UTCI thermal-stress categories
(Bröde et al. 2012) are **not** modified; no arbitrary ±2 °C band is used.

Source: `src/phase2_2_decision_confidence.py` →
`data/processed/phase2_2_decision_confidence.csv`;
`outputs/tables/phase2_2_robustness_changes.csv`.

---

## 1. The architectural separation (never one collapsed score)

Every row carries four independent fields:

| Field | Meaning | Source of truth |
|---|---|---|
| `thermal_stress_state` / `utci_category_official` | physiological stress band | **official UTCI categories, unchanged** |
| `decision_state` | tourism action (OUTDOOR_FEASIBLE / AVOID_PROLONGED_OUTDOOR_EXPOSURE / AVOID_OUTDOOR_EXPOSURE) | project decision layer on the baseline value |
| `decision_confidence` | ROBUST / BOUNDARY / UNSTABLE | the uncertainty analysis below |
| `uncertainty_reason` | plain-language derivation | computed per row |

Worked example (A16 Fuente de Neptuno, 18:00):
`thermal_stress_state = EXTREME_HEAT_STRESS`, `decision_state =
AVOID_PROLONGED_OUTDOOR_EXPOSURE`, `decision_confidence = BOUNDARY` (envelope
reaches 45.9 °C, 0.1 °C from the NOT-RECOMMENDED threshold). The thermal state
and the confidence are reported side by side, not multiplied together.

## 2. The uncertainty envelope (real realizations only, asymmetric)

For each of the 42 outdoor asset×timestamp rows the envelope is
`[min, max]` over all **actually-computed** SOLWEIG realizations:

- **Solar** (every row): Phase 2 clear-sky baseline; REAL_SATELLITE (EUMETSAT
  CM SAF SARAH3); −10%; −20% (Phase 2.1 Audit 1).
- **Geometry** (A23, A27 only): the three corrected-canopy variants (Task A).

The envelope is deliberately **asymmetric**, and this is physically grounded,
not a modelling convenience:
- Clear-sky GHI sits near the **physical upper bound** of surface radiation, so
  real-atmosphere realizations almost always reduce it (cloud). The lone upward
  excursion is the small real cloud-enhancement REAL_SATELLITE captured at
  18:00 — which is exactly the realization that drives the one UNSTABLE row.
- Canopy correction only **adds** shade, so geometry realizations for the stale
  assets push UTCI **down**.

Both tested uncertainty sources therefore widen the envelope mostly *below* the
baseline. We do not assume symmetry; we report the measured envelope. Each row
records `envelope_low/high/width`, the realization that produced each end
(`envelope_low_source`, `envelope_high_source`), and the number of geometry
realizations included.

## 3. From envelope to decision_confidence (the ±2 °C replacement)

Phase 2.1 flagged a row BOUNDARY if any value sat within a **blanket ±2 °C** of
a threshold. That constant was acknowledged as arbitrary and is the thing this
phase was asked to remove. The replacement is **per-row and evidence-derived**:

Let `s = max|realization − baseline|` be the row's **own demonstrated
sensitivity** (how much this specific site×hour actually moved across every
model run we performed). Then, with the safety-critical boundary at 46 °C
(FEASIBLE WITH CONDITIONS ↔ NOT RECOMMENDED) and a secondary boundary at 32 °C:

- **UNSTABLE** — at least one realization falls on the opposite side of the
  46 °C boundary from the baseline (a materially contradictory decision).
- **BOUNDARY** — no realization flips, **but** the envelope lies within `s` of a
  decision threshold (distance-to-nearest-threshold ≤ `s`). A crisp single
  number would misrepresent confidence because the site's *own demonstrated*
  model movement is as large as its margin to the threshold.
- **ROBUST** — the envelope stays farther from every threshold than `s`, and no
  realization flips.

This is not tuned to hit a target pass rate: `s` is a measured quantity per
row, the envelope endpoints are real model runs, and the rule was fixed before
the resulting distribution was read. Where `s` is small (a genuinely stable
site×hour) the ROBUST bar is *stricter* than the old 2 °C, not looser; where `s`
is large the row is held to BOUNDARY even if it would have passed a fixed band.

## 4. Result (n = 42 outdoor rows)

| Confidence | Phase 2.1 | Phase 2.2 |
|---|---:|---:|
| ROBUST | 19 (45.2%) | **35 (83.3%)** |
| BOUNDARY | 20 (47.6%) | **6 (14.3%)** |
| UNSTABLE | 3 (7.1%) | **1 (2.4%)** |

**17 of 42 rows (40.5%) change confidence state.** Transitions
(`outputs/tables/phase2_2_robustness_changes.csv`):
- **15 BOUNDARY → ROBUST**: rows the blanket 2 °C caught but whose own
  demonstrated sensitivity is smaller than their margin to a threshold (e.g. the
  12:00 park assets at ~33–34 °C with `s` ≈ 0.2 °C; several 18:00 assets ~2–3 °C
  clear of 46 °C).
- **A23 15:00 UNSTABLE → ROBUST**: the geometry correction (Task A) resolved the
  vegetation-vintage uncertainty that made it fragile; corrected values sit
  ~44 °C and move *away* from 46 °C.
- **A24 15:00 UNSTABLE → BOUNDARY**: geometry de-flagged (representative); the
  solar envelope 44.1–45.1 °C sits within `s` = 0.9 °C of 46 °C but never crosses
  it — genuine boundary, not instability.
- **A24 18:00 remains UNSTABLE**: REAL_SATELLITE pushes it to exactly 46.0 °C
  (baseline 45.4). Task A confirmed A24's geometry is *representative*, so this
  is a real solar-forcing boundary crossing, not a geometry artefact — the one
  genuinely fragile tourism decision left in the pilot.

The six BOUNDARY rows are the honest residue: A15/A16/A24/A25 at 15:00 and
A15/A16 at 18:00 — all sitting within their own demonstrated sensitivity of the
46 °C ceiling on a genuinely near-ceiling extreme-heat day (envelope highs
44.5–45.9 °C). They are reported as "borderline — treat as elevated risk",
exactly the first-class-uncertainty behaviour `docs/PHASE2_1_GATE.md` asked for.

## 5. Honest limits of this envelope (why it is not a full error bar)

The envelope reflects **tested** uncertainty only: solar forcing (four
realizations) plus, for two assets, corrected-canopy geometry (three crown-radius
brackets). It does **not** include air-temperature, humidity, wind, or SOLWEIG
structural uncertainty, and — per the permanent project caveat
(`docs/PHASE2_1_TO_PHASE2_2_HANDOFF.md` §3) — there is still **no field
validation of Tmrt/UTCI**. Consequently `s` is a lower bound on true
uncertainty, and a ROBUST label means "robust against every uncertainty this
project has actually tested", not "certain". This is why the gate
(`docs/PHASE2_2_GATE.md`), although formally **MODEL LOCKED** on the
pre-registered criteria, defines lock as "sufficiently robust for the intended
decision-support architecture" rather than "physically validated ground truth",
records the absence of Tmrt/UTCI field validation as a permanent limitation, and
retains the BOUNDARY/UNSTABLE categories as permanent first-class fields rather
than engineering them away.
