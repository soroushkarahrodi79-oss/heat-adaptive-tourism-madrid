# PHASE3_TO_PHASE4_HANDOFF.md — HATI-Madrid

Version 1.0 · 2026-08-17. Read this file first in any new conversation
continuing this project. It is a pointer document, not a replacement for the
underlying phase docs — follow the references for full detail.

**Phase 0–3 numerical and scientific outputs are immutable historical inputs.**
Any future phase extends, audits, or visualises them; it must never edit their
content, regenerate their files with different values, or alter their stated
verdicts.

---

## 1. Current project status

HATI-Madrid has run a complete, reproducible pipeline: open-data proxy baseline
(Phase 1) → real SOLWEIG/UTCI physical model (Phase 2) → robustness audit
(Phase 2.1) → targeted geometry correction + evidence-derived uncertainty
(Phase 2.2, **MODEL LOCKED**) → constraint-first tourism opportunity screening
(Phase 3, **DECISION ENGINE VALIDATED**). The project has a validated science
core (thermal modelling) and a validated decision-support core (screening
logic) but **no visual/product layer yet**. Phase 4 is expected to be the first
phase where a visual system is considered — this handoff exists to brief that
work without re-deriving the science.

## 2. Completed phases and their final gates

| Phase | Verdict | Doc |
|---|---|---|
| Phase 0 | GO WITH MODIFICATIONS | `docs/FEASIBILITY_GATE.md` |
| Phase 1 (proxy baseline) | REVISE BASELINE | `docs/PHASE1_GATE.md` |
| Phase 1.1 (baseline hardening) | REVISE BASELINE AGAIN | `docs/PHASE1_1_GATE.md` |
| Phase 1.2 (shade-proxy evidence) | GO TO SOLWEIG / UTCI | `docs/PHASE1_2_SHADE_EVIDENCE_GATE.md` |
| Phase 2 (SOLWEIG physical spike) | PHYSICAL MODEL ADDS DECISION VALUE | `docs/PHASE2_GATE.md` |
| Phase 2.1 (robustness audit) | MODEL NEEDS REVISION | `docs/PHASE2_1_GATE.md` |
| **Phase 2.2 (targeted revision)** | **MODEL LOCKED** | `docs/PHASE2_2_GATE.md` |
| **Phase 3 (opportunity screening)** | **DECISION ENGINE VALIDATED** | `docs/PHASE3_GATE.md` |

## 3. Locked scientific findings — do NOT reopen

- **Study area**: Prado–Retiro–Atocha, ~3.5 km², EPSG:25830. **Episode**:
  2023-08-21 (a **Monday in August**), 12:00/15:00/18:00 CEST.
- **SOLWEIG adds real decision value**: 33.3% physical-vs-proxy reclassification,
  robust at 33.3–35.7% under every tested solar scenario, **unchanged at 33.3%**
  after Phase 2.2 geometry correction.
- **The 12:00 finding is robust and central**: substantial radiant heat stress
  (UTCI ≥32 °C, all 14 outdoor assets) precedes the regional air-temperature
  warning threshold — survived every solar scenario AND the corrected canopy
  geometry (min 35.8 °C).
- **Geometry (Phase 2.2)**: A24 La Rosaleda's near-zero canopy is
  **REPRESENTATIVE** (confirmed genuine — 0 canopy trees within 30 m; it is a
  rose garden). A23 and A27 were **corrected** (real inventory tree heights
  burned into a separate CDSM variant); UTCI fell 0.1–1.8 °C; **no decision
  flipped**.
- **Decision confidence (Phase 2.2)**: ROBUST 83.3% (35/42), BOUNDARY 14.3%
  (6/42), UNSTABLE 2.4% (1/42 — **A24 @ 18:00 only**, a genuine solar-boundary
  case, not a geometry artefact). Confidence is derived from each row's own
  demonstrated sensitivity, not a fixed ±band.
- **No direct field validation of Tmrt/UTCI exists anywhere in this project.**
  Permanent limitation.
- **MODEL LOCKED means** "sufficiently robust for the intended decision-support
  architecture," **not** "physically validated ground truth."

## 4. Phase 3 decision architecture (must be preserved, not redesigned)

Constraint-first gate chain, first-failure-wins, nothing silently dropped:

```
OPEN? → ACCESSIBLE? (straight-line, 800 m primary / 500–1200 m sensitivity)
  → THERMAL LIMIT OK? → EVIDENCE SUFFICIENT? → MEANINGFUL THERMAL IMPROVEMENT?
  → CANDIDATE_ALTERNATIVE
```

No weighted score, no ranking into one number. Exclusion vocabulary (machine-
readable): `OUTSIDE_PILOT_SCOPE`, `CLOSED_AT_TIMESTAMP`,
`ACCESSIBILITY_CONSTRAINT`, `THERMAL_LIMIT_EXCEEDED`, `INSUFFICIENT_EVIDENCE`,
`NO_MEANINGFUL_THERMAL_IMPROVEMENT`, `OUTDOOR_EXPOSURE_TOO_HIGH`.
Pre-registered thermal-improvement margin Δ = 0.8 °C (median Phase 2.2
per-row demonstrated sensitivity — evidence-derived, not invented). Full
spec: `docs/PHASE3_DECISION_ARCHITECTURE.md`.

## 5. The 8 validated scenarios

See `docs/PHASE3_SCENARIOS.md` for full detail;
`data/processed/phase3_scenarios_summary.csv` for the machine-readable table.

| # | Source @ time (radius) | Source state | Outcome | Class |
|---|---|---|---|---|
| S1 | A16 Neptuno @15:00 (800 m) | BOUNDARY | 9 alternatives | exposed monument → indoor |
| S2 | A15 Cibeles @15:00 (800 m) | BOUNDARY | 6 alternatives | multiple trade-offs |
| S3 | A14 Puerta de Alcalá @18:00 (800 m) | ROBUST | 4 alternatives | exposed → shaded outdoor |
| S4 | A26 Alfonso XII @18:00 (800 m) | ROBUST | 8 alternatives | candidate excluded (A24, low evidence) |
| S5 | A19 Observatorio @15:00 (800 m) | **closed (Monday)** | 7 alternatives | source closed |
| S6 | A17 Estatua de Goya @18:00 (800 m) | ROBUST | 9 alternatives | nearest indoor closed at 18:00 |
| S7 | A24 La Rosaleda @18:00 (800 m) | **UNSTABLE (source itself)** | 6 alternatives | uncertain source, robust alternatives found |
| S8 | A20 Retiro @15:00 (**500 m**) | ROBUST | **0 — NO_DEFENSIBLE_ALTERNATIVE** | correctly no recommendation |

## 6. Strongest baseline-vs-HATI findings

Compared against a naive "nearest open tourism asset in radius" baseline
(no thermal/evidence screening): candidate set changed in **7 of 8** scenarios;
in **3 of 8** the baseline's nearest pick **fails** HATI screening (each time
because it is another hot outdoor site — `OUTDOOR_EXPOSURE_TOO_HIGH`); 23
open-in-radius options were removed on thermal/evidence grounds in total; 0
obviously-unsuitable survivors slipped through (guardrail check).
**Strongest single result: S8** — the baseline confidently sends a heat-stressed
visitor to another hot outdoor site 152 m away; HATI instead correctly declines
to recommend anything. Full detail: `outputs/tables/phase3_hati_vs_baseline.csv`,
`docs/PHASE3_VALIDATION_REPORT.md`.

## 7. Permanent scientific limitations (carry into every future phase)

1. No field validation of Tmrt/UTCI exists or is created by any phase to date.
2. A24 (La Rosaleda) @ 18:00 remains a genuine, irreducible solar-boundary
   UNSTABLE case.
3. Uncertainty envelopes (Phase 2.2) cover only tested uncertainty (solar
   forcing + corrected geometry for 2 assets) — not humidity, wind, or
   model-structural uncertainty.
4. Phase 3 accessibility is straight-line distance only — no routing, and
   **no modelling of heat exposure incurred while walking to an alternative**.
5. Phase 3 makes **no behavioural claim** — it screens options; it does not
   predict, model, or assert tourist choice, flow, or adoption.
6. Indoor "refuge" assumes thermal buffering without verified A/C status or
   modelled approach/queue exposure (Phase 1 caveat, still unresolved).

## 8. Opening-hours temporal-alignment caveat (explicit)

Opening hours used in Phase 3 are **point-in-time documented values** captured
2026-08-17 (current OSM tags + documented institutional schedules), evaluated
against the **2023-08-21 study date**. This is a **retrospective application of
present-day hours to a historical date** — real, closure-pattern-consistent
(museums plausibly follow stable weekly/seasonal schedules), but **not a
guarantee that 2023 hours were identical** to 2026 hours at every asset. Any
visual system must not present opening-hours-derived exclusions
(`CLOSED_AT_TIMESTAMP`) as verified-for-2023 fact; it should carry the same
caveat forward, and a production system would need actual 2023 hours or a
live/current-date feed rather than retrospective application. This is
independent from, and additional to, the general `evidence_completeness`
(COMPLETE/PARTIAL/MISSING) flag already carried per asset.

## 9. Repository structure and key Phase 3 files

Root: `C:\workspace\HEAT-ADAPTIVE-TOURISM-MADRID`. No git repository.

```
data/processed/phase3_asset_catalog.csv        27-asset decision records (hours, relevance, evidence)
data/processed/phase3_candidate_screening.csv  81 rows = 27 assets x 3 timestamps, context-free gates
data/processed/phase3_scenarios.csv            full per-candidate scenario detail
data/processed/phase3_scenarios_summary.csv    8-scenario summary
outputs/tables/phase3_exclusion_reasons.csv    exclusion-reason tallies
outputs/tables/phase3_hati_vs_baseline.csv     HATI vs nearest-open baseline, per scenario
outputs/tables/phase3_accessibility_sensitivity.csv  500/800/1200 m sensitivity
outputs/maps/phase3_scenario_map.png           8-panel scenario locator map
src/phase3_*.py                                pipeline: extract_opening_hours, build_catalog,
                                                candidate_screening, scenarios, make_map, validation
```

Most load-bearing docs to read next, in order: `docs/PHASE3_METHOD.md`,
`docs/PHASE3_DECISION_ARCHITECTURE.md`, `docs/PHASE3_SCENARIOS.md`,
`docs/PHASE3_VALIDATION_REPORT.md`, `docs/PHASE3_GATE.md`. For the thermal
foundation underneath: `docs/PHASE2_2_GATE.md`,
`docs/PHASE2_2_DECISION_UNCERTAINTY.md`.

## 10. Fields the future visual system MUST preserve separately

Never collapse these into one score or one color/icon that erases the others:

- `thermal_state` — official UTCI category (physiological stress band)
- `decision_state` — tourism action implied (e.g. `AVOID_PROLONGED_OUTDOOR_EXPOSURE`)
- `decision_confidence` — ROBUST / BOUNDARY / UNSTABLE (or INDOOR_BYPASS)
- `evidence_confidence` — HIGH / MODERATE / LOW (weakest-link of hours + thermal evidence)
- `exclusion_reason` — the machine-readable reason a candidate did NOT survive
- **alternative trade-offs** — indoor/outdoor, distance/walk-time, experience
  type, UTCI delta vs source — exposed side-by-side per surviving candidate,
  never merged into a single ranked "best" value

## 11. Visual/product requirements implied by the validated science

Any future visual system, when it is scoped, should be expected to:

- Render `decision_confidence` and `evidence_confidence` as visually distinct
  from `thermal_state`/`decision_state` (e.g. never fold confidence into color
  alone if color already encodes thermal severity).
- Represent `NO_DEFENSIBLE_ALTERNATIVE` as a valid, clearly-communicated
  outcome — not an empty/error state to be hidden or defaulted away.
- Show exclusion reasons on demand (auditability), not just survivors.
- Carry the opening-hours temporal-alignment caveat (§8) and the permanent
  scientific limitations (§7) into any user-facing surface, not just docs.
- Avoid implying behavioural prediction in any wording, iconography, or
  framing (no "tourists will go here", no popularity/flow language).
- Treat straight-line accessibility as a visible simplification (e.g. label
  distances as "straight-line," not "walking route").

None of this authorizes starting that visual system now — it is scoping input
for whenever Phase 4 is formally chartered.

## 12. Restrictions for Phase 4

Until explicitly re-scoped by the user:

- Do NOT reopen SOLWEIG or change any Phase 2.2 thermal value.
- Do NOT change Phase 3 screening logic, thresholds, or scenario outcomes.
- Do NOT start dashboard design or implementation.
- Do NOT add ML, LLM ranking, agents, personas, or behavioural prediction.
- Do NOT perform heat-aware route optimisation.
- Do NOT expand beyond the pilot geography or asset set.
- Do NOT introduce composite/weighted scores to rank candidates or assets.
- Do NOT treat opening hours as verified-for-2023 fact (see §8).
- Treat all Phase 0–3 docs, CSVs, and verdicts as read-only historical inputs.
