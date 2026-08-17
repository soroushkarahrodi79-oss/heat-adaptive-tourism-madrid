# PHASE2_1_GATE.md — Phase 2.1 robustness gate decision

Version 1.0 · 2026-08-17. Thresholds reproduced **exactly as predefined in
the task specification, before any robustness result was inspected**, and
not altered by this document.

---

## Predefined criteria, evaluated in order

**MODEL LOCKED** requires ALL of:

| Condition | Result | Met? |
|---|---|---|
| ≥80% of asset×timestamp decisions are ROBUST | **45.2%** (19/42) | **No** |

Fails on the first condition alone — MODEL LOCKED is ruled out regardless
of the remaining conditions.

**MODEL CONDITIONALLY LOCKED** requires 60–79% ROBUST plus supporting
conditions:

| Condition | Result | Met? |
|---|---|---|
| 60–79% of decisions are ROBUST | **45.2%**, below the 60% floor | **No** |

Also ruled out on the ROBUST-percentage criterion alone.

**MODEL NEEDS REVISION** applies if ANY of the following hold:

| Condition | Result | Triggers? |
|---|---|---|
| Fewer than 60% of decisions are ROBUST | **45.2%** | **Yes** |
| The principal 12:00 result collapses | Survives fully — 14/14 assets ≥32 °C UTCI in every tested scenario (`docs/PHASE2_1_SOLAR_SENSITIVITY.md`) | No |
| Physical-vs-proxy reclassification falls below 20% under reasonable uncertainty | Stays at 33.3–35.7% under every tested solar scenario | No |
| Stale geometry systematically drives decision-critical results | 3 of 8 audited assets flagged POSSIBLY STALE (concentrated in park/garden, not universal); directly implicated in only 3 of 42 total rows | Partial — real and concentrated, not "systematic" in the all-encompassing sense, but non-trivial |

One condition (ROBUST <60%) is independently sufficient to trigger this
verdict per the task's "if any of" wording. The result is unambiguous on
that basis alone.

## Verdict

# MODEL NEEDS REVISION

## What this verdict does and does not mean

**This is not a rejection of the physical-modelling approach, and it does
not overturn `docs/PHASE2_GATE.md`'s "PHYSICAL MODEL ADDS DECISION VALUE"
finding.** Read alongside `docs/PHASE2_1_ROBUSTNESS_REPORT.md`, the
picture is specific and bounded, not general:

- Only **3 of 42 rows (7.1%)** are UNSTABLE — an actual decision flip under
  tested uncertainty. The 45.2% ROBUST figure is low almost entirely
  because **47.6% of rows are BOUNDARY** (close to a threshold, decision
  unchanged), which is a real, physically-grounded feature of auditing a
  genuinely extreme, near-ceiling heat episode, not evidence the model's
  substantive conclusions are wrong.
- The two substantive claims this project has built toward — that
  significant outdoor radiant heat stress precedes the regional
  air-temperature warning (the 12:00 finding) and that physical modelling
  materially improves on the simple proxy baseline (≥20% reclassification)
  — **both survive every tested uncertainty without exception**.
- The revision this gate calls for is specifically to **how the decision
  architecture handles numeric proximity to its own thresholds**, and to
  **closing the vegetation-vintage gap for the park/garden assets Audit 2
  flagged** — not to the modelling approach itself.

## What "needs revision" concretely means for the next phase

Per the task's own framing for the CONDITIONALLY LOCKED tier (whose spirit
applies even though the strict ROBUST-percentage threshold sorts this
result into NEEDS REVISION): **uncertainty must become an explicit,
first-class component of the decision-support system**, specifically:

1. **Replace the crisp 46 °C / 32 °C cutoffs with an uncertainty band** (e.g.
   a ±2 °C amber zone reported as "borderline — treat as elevated risk"
   rather than a silent binary flip) before any operational or dashboard
   use of these thresholds. This directly addresses why BOUNDARY dominates
   this result.
2. **Prioritise closing the vegetation-geometry gap for the three flagged
   assets** (A23, A24, A27) specifically — not a city-wide LiDAR
   reacquisition, but a targeted check (e.g. current aerial/orthophoto
   canopy inspection, or a newer regional LiDAR coverage if one becomes
   accessible) for these named, decision-relevant sites before their
   results are treated as final.
3. **Do not proceed to a dashboard or operational deployment** using the
   current crisp-threshold architecture without addressing (1) — consistent
   with this phase's own restriction against dashboard work, and a
   forward-looking recommendation for whatever phase follows.

## What was NOT found

No evidence emerged that the physical model produces systematically wrong
directional conclusions, that solar-forcing uncertainty threatens the
project's headline findings, or that vegetation staleness affects the
majority of assets. The verdict is a call for the *precision and
uncertainty-handling* of the decision architecture to mature to match the
*substantive* robustness the modelling itself has now twice demonstrated
(Phase 2 and this phase) — not a call to abandon or redo the physical
modelling work.
