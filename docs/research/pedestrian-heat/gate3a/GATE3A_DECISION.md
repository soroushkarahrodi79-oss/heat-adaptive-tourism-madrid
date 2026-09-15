# GATE3A_DECISION — pipeline falsification verdict

**Version 1.2 · 2026-09-15 (updated after the execution-semantics review).**
Numbers below are the **fully corrected** results: global-chainage sampler (AMENDMENT_002,
v = 1.1 m/s) + **stateful single-call SOLWEIG** and **hardened fail-closed Catastro**
(AMENDMENT_003; `GATE3A_STATEFUL_CORRECTION.md`). Both correction passes left the
interpretation unchanged.

> **v1.2 correction summary.** (1) SOLWEIG now runs as ONE stateful `calculate()` over a
> continuous 72-step 15-min sequence (00:00→17:45) — thermal state is carried, not reset per
> timestamp; only the 8 frozen decision fields feed metrics. (2) Catastro acquisition is
> fail-closed with structural GML parsing (rings/multipart, dedup) → building coverage
> 32.03 %→30.14 %; DSM/CDSM regenerated. Corrected baseline A−B: **14:00 −0.042**, **17:00
> −0.367** (was −0.048 / −0.365) — ordering and trade-off preserved.

## Baseline outcome label (3A.8 — no scientific winner)

# BASELINE DIFFERENCE OBSERVED

Small and sign-consistent, with the two metric families pointing to **different routes**
(a trade-off, preserved — not collapsed). **No route is declared scientifically
preferred**; that requires the frozen uncertainty/perturbation experiment in Gate 3B.

| | 14:00 departure | 17:00 departure |
|---|---|---|
| **THERMAL INTENSITY** — mean UTCI (A / B) | 40.345 / 40.387 °C → **A cooler by 0.042** | 42.246 / 42.613 °C → **A cooler by 0.367** |
| **EXPOSURE DURATION** — trip minutes (A / B) @1.1 m/s | 40.3 / 35.8 → **B shorter by 4.4** | 40.3 / 35.8 → **B shorter by 4.4** |
| minutes in very-strong+extreme (A / B) | 33.8 / 32.5 | 40.3 / 35.8 → **B fewer** |

(Speed-robustness QA at the other frozen value 1.4 m/s: A−B intensity = −0.077 / −0.387;
sign unchanged. Corrected sampler: A = 532 samples, B = 474; Σ represented length = route
length; Σ M4 minutes = M1 exactly.)

Route A (open Prado/Recoletos axis) has marginally **lower mean intensity**; Route B
(Alfonso XII park-edge) is **shorter** and so accumulates **fewer high-stress minutes**.
Intensity favours A, duration favours B → **the metrics disagree**, exactly the
intensity/duration trade-off the freeze anticipated. Per the frozen decision rule this
disagreement is preserved (it would support NO ROBUST DIFFERENCE / ABSTAIN), not resolved
into a winner. Differences are small (intensity ≤ 0.41 °C; whole corridor sits in
"very strong heat stress"), so their robustness is undetermined until perturbations run.

## Verdict

# GATE3A_CORRECTED_GO_TO_3B

The sampling correction was applied; all frozen artifacts revalidated; the corrected
metrics **preserve the A−B ordering** (Route A lower mean UTCI at both departures and both
frozen speeds) and **preserve the intensity/duration trade-off**. The interpretation is
unchanged (BASELINE DIFFERENCE OBSERVED, no winner). Not
`GATE3A_CORRECTION_CHANGED_INTERPRETATION` (nothing reversed) and not
`STOP_INVALID_PIPELINE` (pipeline produces coherent, invariant-satisfying output).

### Requirements check
| Requirement | Status |
|---|---|
| Reproducible thermal fields | MET — 3 scripts, fixed inputs, 22 artifact SHA-256; SOLWEIG 0.1.0b92 |
| No unresolved physical/model artefact invalidating comparison | MET — 0% out-of-range; edge SVF effect confined to the 150 m buffer (no route sample in it); 15% unclassified-tall logged as non-invalidating refinement |
| Valid time-resolved route sampling | MET — 8 fields @ Δt 15 min; traversal timestamps; 0 off-raster, 0 nan; ±7.5 min QA does not flip ordering |
| Frozen metrics computable for both routes | MET — M1–M5 for A and B at both departures; intensity/duration separated |
| No frozen assumption silently changed | MET — two documented amendments: AMENDMENT_001 (terrain MDT 2019→2023, user-approved pre-thermal) and AMENDMENT_002 (baseline speed 1.25→frozen 1.1 m/s, from the audit); neither silent, neither chosen by A/B contrast |
| Limitations compatible with Path B | MET — no accuracy/comfort/behaviour/health/dose claim; ABSTAIN remains first-class |

### Why GO and not MODIFY
MODIFY would require a repair that must precede the uncertainty experiment. The one repair
needed (terrain source) is **already made and ratified** (AMENDMENT_001); the remaining
items (15% unclassified-tall classification refinement; segment-level shadow timing) are
**improvements carried into** the robustness gate, not blockers to starting it. The
temporal-discretization QA explicitly did not flip the ordering, so no method change is
forced.

### Why not STOP_INVALID_PIPELINE
The pipeline produced interpretable, physically coherent outputs, and the only frozen-input
change was **forced by data availability and openly amended**, not made opportunistically
to obtain a result. No frozen assumption was bent to rescue an output.

## Carried into Gate 3B (robustness experiment)
1. **Run the full perturbation matrix** E-P1 (forcing), E-P2 (canopy — dominant), E-P4
   (building), E-P5 (side-of-street), E-P6 (speed 1.1/1.4). The baseline intensity gap
   (0.1–0.4 °C) is small enough that ≥1 perturbation could flip it → the decision rule may
   well return **ABSTAIN / NO ROBUST DIFFERENCE**; that is a legitimate outcome.
2. **Unclassified-tall (15%) is a fixed baseline limitation, NOT a refinement to tune.**
   Any classification change must come only through the frozen E-P2 (canopy) / E-P4
   (building) geometry-source perturbations, or a new amendment — never an ad-hoc
   reclassification chosen to stabilise the A/B ordering.
3. **Near-boundary watch (NC6)** — route max UTCI reached 45.5–45.6 °C, just below the
   +46 °C "extreme" cut-point; perturbations could push category metrics across it.
4. **AMENDMENT_001** stands as the ratified terrain source for 3B.
5. Wind/radiation remain uniform/modeled (unobserved in-corridor) — unchanged limitations.

## Prohibitions honoured
No perturbation matrix run; no route re-optimised after seeing fields; no route called
scientifically preferred; no physiological-dose claim; 21 Aug 2023 not used as validation
(study day is 24 Aug 2023, reusing no locked thermal result).

*Gate 3A ends here. The full research decision (ROBUST / NO ROBUST DIFFERENCE / ABSTAIN)
is not made until Gate 3B.*
