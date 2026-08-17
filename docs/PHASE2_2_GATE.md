# PHASE2_2_GATE.md — Phase 2.2 microclimate gate decision

Version 1.0 · 2026-08-17. Gate outcomes and their criteria are reproduced
**exactly as predefined in the Phase 2.2 task specification, before any Phase
2.2 result was inspected**, and are not altered by this document. Phase 0–2.1
verdicts and data are untouched (`docs/PHASE2_1_TO_PHASE2_2_HANDOFF.md` §11);
this gate evaluates only the Phase 2.2 revision built on top of them.

---

## Inputs to the decision

| Quantity | Phase 2.1 | Phase 2.2 | Source |
|---|---:|---:|---|
| ROBUST | 45.2% (19/42) | **83.3% (35/42)** | `phase2_2_decision_confidence.csv` |
| BOUNDARY | 47.6% (20/42) | **14.3% (6/42)** | " |
| UNSTABLE | 7.1% (3/42) | **2.4% (1/42)** | " |
| Rows changing confidence | — | 17/42 (40.5%) | `phase2_2_robustness_changes.csv` |
| Physical-vs-proxy reclassification | 33.3% | **33.3%** (unchanged; 0 corrected realizations flip a feasibility_state) | `phase2_2_summary_tables.py` |
| 12:00 finding (outdoor UTCI ≥ 32) | 14/14 | **14/14**, incl. corrected geometry (min 35.8 °C at wide bracket) | " |
| Substantive tourism decision changes | — | **0** from geometry correction; the 1 pre-existing solar case (A24 18:00) persists | " |

## Predefined criteria, evaluated in order

**MODEL LOCKED** requires ALL of:

| Condition | Result | Met? |
|---|---|---|
| Substantive Phase 2 findings remain intact | Reclassification 33.3% (≥20%); 12:00 finding 14/14; both directions of proxy error preserved | Yes |
| UNSTABLE rows ≤ 10% | 2.4% | Yes |
| The 12:00 finding survives | Survives, including under corrected canopy | Yes |
| Physical-vs-proxy reclassification ≥ 20% | 33.3% | Yes |
| No unresolved systematic geometry failure remains | Geometry issue was localized to 3 assets; A23/A27 corrected (no flip), A24 confirmed representative — none unresolved, none systematic | Yes |

Every MODEL LOCKED condition is satisfied. Per the pre-registered gate, this is
sufficient and dispositive: the verdict is **MODEL LOCKED**. The gate is applied
exactly as pre-registered; the permanent limitations recorded below are carried
*inside* the locked model, not used to downgrade the pre-registered verdict.

**MODEL NEEDS FURTHER REVISION** applies only if any of: geometry correction
materially overturns the physical-model result; the 12:00 finding collapses;
reclassification < 20%; or unresolved uncertainty is systematic.

| Condition | Result | Triggers? |
|---|---|---|
| Geometry correction materially overturns the result | 0 decisions flip; correction only *reduced* modelled heat at 2 assets, confirming the prior directional caveat | No |
| 12:00 finding collapses | Survives 14/14 | No |
| Reclassification < 20% | 33.3% | No |
| Unresolved uncertainty is systematic | It is localized (1 asset×timestamp) and explicitly represented | No |

NEEDS FURTHER REVISION is ruled out on every condition.

## Verdict

# MODEL LOCKED

All pre-registered MODEL LOCKED conditions are met and none of the NEEDS
FURTHER REVISION conditions is triggered. The gate is decided strictly on the
pre-registered criteria evaluated above; no post-hoc caveat is permitted to
move it.

## What "model locked" means here (and does not)

MODEL LOCKED here means **"sufficiently robust for the intended
decision-support architecture"** — i.e. the SOLWEIG/UTCI physical model, its two
substantive findings, and the decision-confidence architecture are stable
enough, against every uncertainty this project has actually tested, to be
treated as a settled foundation for a subsequent (separately-gated) phase. It
does **not** mean "physically validated ground truth": the model has not been
checked against measured Tmrt/UTCI, and lock is a statement about
decision-architecture robustness, not field accuracy.

## Permanent scientific limitations (carried inside the locked model)

These are recorded as standing limitations of the locked model, not as reasons
to alter the verdict:

1. **No direct field validation of Tmrt/UTCI** exists anywhere in this project,
   and none is created by this phase (handoff §3). Lock is decision-architecture
   robustness, not measured accuracy.
2. **A24 (La Rosaleda) 18:00 remains a genuine solar-boundary case**: it flips
   FEASIBLE WITH CONDITIONS → NOT RECOMMENDED under real satellite radiation at
   the exact 46.0 °C cutoff. Task A confirmed A24's near-zero canopy is
   *representative*, so this is a real solar-forcing boundary, not a geometry
   artefact a correction could remove. It is retained as a permanent
   first-class UNSTABLE flag, not smoothed away.
3. **Uncertainty envelopes cover tested uncertainties only** — solar forcing
   (four realizations) and, for the two stale assets, corrected-canopy geometry
   (three crown-radius brackets). They do not incorporate air-temperature,
   humidity, wind, or model-structural uncertainty; a ROBUST label means "robust
   against every uncertainty actually tested", not "certain".
4. **The Phase 2.2 confidence percentages are not directly comparable** to Phase
   2.1's: the improvement from 45.2% to 83.3% ROBUST comes substantially from
   replacing Phase 2.1's blanket ±2 °C proximity margin with each row's own
   demonstrated sensitivity (`docs/PHASE2_2_DECISION_UNCERTAINTY.md`). The
   change is a like-for-unlike methodological refinement, so the two ROBUST
   figures must not be read as a single trend line.

MODEL LOCKED thus records that the physical-modelling architecture and its
substantive findings are **validated and stable for the decision-support
architecture**, the residual uncertainty is **localized and explicitly
represented**, and the one remaining asset-level fragility (A24 18:00) is
**carried transparently within the locked model** rather than resolved away.

## What this verdict does and does not authorise

- **Does:** treat the SOLWEIG/UTCI physical model, the 12:00 finding, and the
  ≥20% reclassification as settled load-bearing results; treat the
  decision-confidence architecture (separate thermal state, decision state,
  confidence, uncertainty reason) as the interface any later phase builds on.
- **Does not:** authorise Phase 3, a dashboard, or operational deployment here.
  Any such phase is separately scoped and separately gated, must keep BOUNDARY/
  UNSTABLE as first-class outputs, must carry the A24 18:00 caveat, and should
  still treat a genuine Tmrt/UTCI field-validation campaign as the highest-value
  next investment (`docs/PHASE2_GATE.md`, `docs/PHASE2_1_TO_PHASE2_2_HANDOFF.md`
  §3).

## What was NOT found

No corrected-geometry realization overturned any tourism decision; no evidence
emerged that the physical model is systematically wrong in direction; the
geometry staleness proved real but localized and, where real, corrigible in the
*less-hazard* direction. The one asset whose decision remains genuinely
uncertain was, if anything, better understood after this phase, not worse.
