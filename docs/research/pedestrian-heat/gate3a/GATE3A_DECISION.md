# GATE3A_DECISION — pipeline falsification verdict

**Version 1.0 · 2026-09-15.**

## Baseline outcome label (3A.8 — no scientific winner)

# BASELINE DIFFERENCE OBSERVED

Small and sign-consistent, with the two metric families pointing to **different routes**
(a trade-off, preserved — not collapsed). **No route is declared scientifically
preferred**; that requires the frozen uncertainty/perturbation experiment in Gate 3B.

| | 14:00 departure | 17:00 departure |
|---|---|---|
| **THERMAL INTENSITY** — mean UTCI (A / B) | 40.43 / 40.52 °C → **A cooler by 0.10** | 42.27 / 42.68 °C → **A cooler by 0.41** |
| **EXPOSURE DURATION** — trip minutes (A / B) | 35.4 / 31.5 → **B shorter by 3.9** | 35.4 / 31.5 → **B shorter by 3.9** |
| minutes in very-strong+extreme (A / B) | 28.2 / 27.9 | 33.2 / 30.2 → **B fewer** |

Route A (open Prado/Recoletos axis) has marginally **lower mean intensity**; Route B
(Alfonso XII park-edge) is **shorter** and so accumulates **fewer high-stress minutes**.
Intensity favours A, duration favours B → **the metrics disagree**, exactly the
intensity/duration trade-off the freeze anticipated. Per the frozen decision rule this
disagreement is preserved (it would support NO ROBUST DIFFERENCE / ABSTAIN), not resolved
into a winner. Differences are small (intensity ≤ 0.41 °C; whole corridor sits in
"very strong heat stress"), so their robustness is undetermined until perturbations run.

## Verdict

# GO_TO_ROBUSTNESS_EXPERIMENT

### Requirements check
| Requirement | Status |
|---|---|
| Reproducible thermal fields | MET — 3 scripts, fixed inputs, 22 artifact SHA-256; SOLWEIG 0.1.0b92 |
| No unresolved physical/model artefact invalidating comparison | MET — 0% out-of-range; edge SVF effect confined to the 150 m buffer (no route sample in it); 15% unclassified-tall logged as non-invalidating refinement |
| Valid time-resolved route sampling | MET — 8 fields @ Δt 15 min; traversal timestamps; 0 off-raster, 0 nan; ±7.5 min QA does not flip ordering |
| Frozen metrics computable for both routes | MET — M1–M5 for A and B at both departures; intensity/duration separated |
| No frozen assumption silently changed | MET — only deviation is AMENDMENT_001 (MDT 2019→2023), documented and user-approved before any thermal output |
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
2. **Classification refinement** — reduce the 15% unclassified-tall nSH (tighten Catastro
   footprint edges / vegetation mask) to cut omitted-shadow uncertainty.
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
