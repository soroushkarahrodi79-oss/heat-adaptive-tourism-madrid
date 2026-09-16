# AMENDMENT_002 — Gate-3A baseline walking speed governance

**Date:** 2026-09-15 · **Raised at:** Gate-3A sampling correction (external audit).
**Status:** APPLIED for Gate 3A (pipeline falsification).

## 1. Issue
Gate-3A originally used **v = 1.25 m/s** (a midpoint) as the baseline walking speed.
Gate 2 froze E-P6 at **1.1 and 1.4 m/s only** (`GATE2_PERTURBATION_SPEC.md`); 1.25 m/s
was **never a frozen value**. `GATE2_METRIC_SPEC.md` M1 defines v as "the E-P6
alternative", i.e. a frozen value — not an invented midpoint.

## 2. Resolution
The Gate-3A baseline is re-expressed at a **frozen** E-P6 value: **v = 1.1 m/s**, the
Gate-1/Gate-2 **tourist-representative** speed ("slow/tourist ≈ 1.1 m/s"). This is the
population of interest for a tourism heat-exposure study, so it is the principled baseline —
**not** chosen by A-vs-B contrast. The invented 1.25 m/s midpoint is withdrawn.

## 3. Why speed cannot bias the ordering
Walking speed is applied **identically to both routes**. It scales M1 (duration) and M4
(minutes) proportionally for A and B alike, so it cannot flip a duration ordering. It does
weakly affect which 15-min thermal field each segment samples (via traversal time), so M2/M3
are re-computed at 1.1 m/s. As a robustness check (not the E-P6 perturbation matrix), all
metrics were also computed at the other frozen value **1.4 m/s**: the sign of the M2
(intensity) A−B difference is preserved at both speeds and both departures (see
`GATE3A_SAMPLING_CORRECTION.md`). Speed governance therefore does not affect the Gate-3A
interpretation.

## 4. Scope
Baseline reporting only. The full E-P6 speed perturbation (1.1 vs 1.4 as a decision-stability
input) is still run in Gate 3B. No other frozen element changes.
