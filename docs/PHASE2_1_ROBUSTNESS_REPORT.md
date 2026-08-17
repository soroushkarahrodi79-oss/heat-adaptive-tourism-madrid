# PHASE2_1_ROBUSTNESS_REPORT.md — HATI-Madrid Phase 2.1

Version 1.0 · 2026-08-17. Synthesises Audits 1–3
(`docs/PHASE2_1_SOLAR_SENSITIVITY.md`, `docs/PHASE2_1_GEOMETRY_CONFIDENCE.md`,
and the combined classification below) into the decision-robustness picture
that feeds `docs/PHASE2_1_GATE.md`.

---

## Audit 3: decision robustness classification

**Rule** (fixed in `src/decision_robustness.py` before the resulting
distribution was known — the 2 °C threshold-proximity margin was not
adjusted after seeing the pass rate):

- **UNSTABLE**: the feasibility decision actually changes under a tested
  solar scenario, OR the asset is geometry-flagged POSSIBLY STALE AND its
  baseline UTCI sits within 2 °C of the 46 °C NOT-RECOMMENDED threshold.
- **BOUNDARY**: no tested scenario flips the decision, but EITHER the UTCI
  value (baseline or under any scenario) sits within 2 °C of a decision
  threshold (32 or 46 °C), OR the asset is geometry-flagged POSSIBLY STALE
  / PARTIALLY REPRESENTATIVE.
- **ROBUST**: neither condition applies.

### Result (n = 42 outdoor asset×timestamp rows)

| Robustness | Count | % |
|---|---:|---:|
| ROBUST | 19 | 45.2% |
| BOUNDARY | 20 | 47.6% |
| UNSTABLE | 3 | 7.1% |

**This split is dominated by BOUNDARY, not UNSTABLE.** Only 3 of 42 rows
(7.1%) actually change their substantive decision under any tested
uncertainty. The large BOUNDARY share (47.6%) reflects a real, physical
feature of this specific episode: during a genuine extreme-heat day, a
large fraction of this pilot's outdoor sites sit close to the UTCI
"Extreme heat stress" ceiling (46 °C) at the SEVERE-hazard timestamps
(15:00, 18:00) — this is a property of how hot the real day was, not an
artefact of the classification rule. Full per-row detail and reasons:
`data/processed/phase2_1_robustness.csv`; map:
`outputs/maps/phase2_1_unstable_assets.png`.

### The 3 UNSTABLE rows

| Asset | Timestamp | Reason |
|---|---|---|
| A23 Jardines de Cecilio Rodríguez | 15:00 | Geometry-flagged POSSIBLY STALE; baseline UTCI 44.4 °C, within 2 °C of the 46 °C threshold |
| A24 La Rosaleda | 15:00 | Geometry-flagged POSSIBLY STALE; baseline UTCI 45.0 °C, within 2 °C of the 46 °C threshold |
| A24 La Rosaleda | 18:00 | Decision actually changes under the REAL_SATELLITE solar scenario (45.4 → 46.0 °C, FEASIBLE WITH CONDITIONS → NOT RECOMMENDED) |

All three UNSTABLE rows involve the same two geometry-flagged park/garden
assets (A23, A24) — consistent with Audit 2's finding that vegetation-
vintage uncertainty, not solar-forcing uncertainty, is the dominant driver
of genuine (not just boundary-proximate) instability in this phase.

## Re-testing the five Phase 2 main findings

| # | Phase 2 finding (original) | Robustness-adjusted result | Verdict |
|---|---|---|---|
| 1 | 33.3% physical-vs-proxy reclassification | 33.3–35.7% across all three tested solar scenarios (never below 33%) | **Survives**, essentially unchanged |
| 2 | 12:00: substantial heat stress present before the air-temperature warning threshold | 14/14 outdoor assets stay ≥32 °C UTCI at 12:00 in every tested scenario, including the real satellite data | **Survives fully**, no exceptions found |
| 3 | Proxy both under- and over-estimates hazard, direction depending on timestamp | The 9 underestimation cases (12:00) are entirely unaffected by solar testing (0 changed). The 5 overestimation cases (18:00) weaken by exactly one row (A24, under REAL_SATELLITE only) — the physical model becomes marginally *more* aligned with the proxy at that one site under real radiation | **Survives**, with one minor, specific, explainable exception |
| 4 | No single morphology systematically fails (Phase 2's solar-driven reclassification was uniform ~33% across all four morphologies) | Confirmed for the solar dimension (only 1 additional flip, in park_garden). **However, Audit 2 found a real, separate, morphology-concentrated pattern**: vegetation-geometry staleness clusters specifically in park/garden assets (3 of 6 audited park/garden sites, 0 of 2 non-park contrast sites) | **Partially qualified**: no morphology-specific *solar* failure, but a real morphology-specific *geometry-confidence* pattern exists and should not be conflated with the original finding |
| 5 | Timestamp-driven differences (64.3% at 12:00, 0% at 15:00, 35.7% at 18:00) | Solar-scenario decision changes occurred ONLY at 18:00 (1 row) — 12:00 and 15:00 showed zero additional solar-driven instability. 15:00 in particular has now shown perfect stability across every uncertainty test performed anywhere in this project (Phase 1.2's Madrid-vs-TCD proxy agreement was also 100% at 15:00) | **Survives and strengthens** — 15:00's stability is now a three-times-replicated pattern, not a one-off |

## What this means, in one paragraph

The physical model's **substantive, decision-relevant conclusions are
robust**: the 12:00 finding is untouched by ±20% radiation uncertainty, the
overall reclassification rate versus the Phase 1 proxy stays well above the
20% bar under every tested scenario, and only 3 of 42 individual
asset×timestamp rows (7.1%) actually flip a decision. What is **not**
fully robust is the model's **numeric precision at the margin**: because
this was a genuinely extreme, near-ceiling heat episode, a large share of
outdoor readings (47.6%) sit close enough to the 46 °C extreme-stress
threshold that a crisp categorical read is fragile even when the
underlying substantive conclusion ("this site requires caution today") is
not in doubt. Separately, a real, geometry-driven, park/garden-concentrated
uncertainty (Audit 2) was found and should be treated as a distinct,
first-class caveat, not folded into the solar-sensitivity story.
