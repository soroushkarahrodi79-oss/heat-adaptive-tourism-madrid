# PHASE4_1_TO_NEXT_PHASE_HANDOFF.md — HATI-Madrid

Version 1.0 · 2026-08-18. Read this first in any new conversation after
Phase 4.1. It is a pointer document — follow the references for detail. The
science (Phase 0–3) and the Phase 4.0 visual architecture remain the
immutable contract; Phase 4.1 built exactly that and is now closed (§11).

## 1. Current project status

Thermal model locked (Phase 2.2), decision engine validated (Phase 3),
visual architecture approved (Phase 4.0), and the Visual Decision-Support MVP
implemented and validated (Phase 4.1). A running, read-only Dash application
now presents the locked Phase 3 outputs as the three approved views. No Phase
5 work has been started.

## 2. Completed gates through Phase 4.1

| Phase | Verdict | Doc |
|---|---|---|
| Phase 0 | GO WITH MODIFICATIONS | `docs/FEASIBILITY_GATE.md` |
| Phase 1 / 1.1 / 1.2 | REVISE → GO TO SOLWEIG/UTCI | `docs/PHASE1*_GATE.md` |
| Phase 2 / 2.1 / 2.2 | **MODEL LOCKED** | `docs/PHASE2_2_GATE.md` |
| Phase 3 | **DECISION ENGINE VALIDATED** | `docs/PHASE3_GATE.md` |
| Phase 4.0 | **VISUAL ARCHITECTURE APPROVED** | `docs/PHASE4_0_GATE.md` |
| Phase 4.1 | **MVP IMPLEMENTATION VALIDATED** | `docs/PHASE4_1_GATE.md` |

## 3. Commits

- **Baseline scientific commit (immutable reference):**
  `901954e1dc8a07970715ff5be82634a9abcc270f`
  — "HATI-Madrid through Phase 4.0 — science and visual architecture locked".
  Per-file hashes: `docs/PHASE4_1_IMPLEMENTATION_BASELINE.md`.
- **Phase 4.1 implementation commit:** `5364f3f`
  — "Phase 4.1 — Visual Decision-Support MVP (Dash) over locked Phase 3 outputs".

## 4. Locked scientific findings (do not reopen)

- 27-asset Prado–Retiro–Atocha pilot; single historical heat episode
  **2023-08-21** at three modelled timestamps **12:00 / 15:00 / 18:00**.
- Two `decision_state` values: `AVOID_PROLONGED_OUTDOOR_EXPOSURE`,
  `INDOOR_REFUGE`. Two `thermal_state` values: `VERY_STRONG_HEAT_STRESS`,
  `INDOOR_NOT_MODELLED`.
- Four `decision_confidence` categories: `ROBUST` / `BOUNDARY` / `UNSTABLE` /
  `INDOOR_BYPASS` (categorical, derived per-row from demonstrated
  sensitivity — never percentages).
- Three `evidence_confidence` levels: `HIGH` / `MODERATE` / `LOW`
  (weakest-link of opening-hours and thermal evidence).
- Eight validated scenarios S1–S8 with pre-registered access radii
  (500/800/1200 m tested). Baseline (nearest-open) comparison pre-computed.
- The entire permitted data surface is seven CSVs (§9); these are read-only.

## 5. Validated UI behaviors

- Three views via drill-down (map → asset panel → trade-off), map stays the
  spatial anchor; S1–S8 jump chips are shortcuts, not a fourth view.
- Exactly three timestamps, fixed date shown, always-visible "not live"
  caption; switching timestamp keeps map pan/zoom and updates panels in place.
- Five concepts on five non-reused channels: decision_state = fill colour
  (rust/teal), decision_confidence = ring style (solid/dashed/dotted/none,
  drawn on the marker, not tooltip-only), evidence_confidence = opacity
  (panel), thermal_state = glyph + text, exclusion_reason = desaturation +
  neutral token badge with plain-language translation.
- Exclusions auditable: monospace token + fixed translation always shown,
  expandable to source-row values.
- Off-by-default baseline comparison reads the pre-computed
  `phase3_hati_vs_baseline.csv` row only; never recomputes.
- Radius sensitivity shown as a labelled read-only disclosure, never a retry.
- Two-tier limitations: context-sensitive Tier-1 strip on every view + full
  7-item Tier-2 drawer.
- No score, ranking, star, "best option", gauge, KPI wall, traffic-light
  ramp, or live/forecast wording anywhere. 14/14 automated contract+smoke
  tests enforce these. See `docs/PHASE4_1_VISUAL_QA.md`.

## 6. S8 and A24 @ 18:00 special states

- **S8** (`A20` Parque del Retiro, 15:00, 500 m): zero survivors →
  dedicated `NoDefensibleAlternativePanel` (verdict headline, "26 candidates
  evaluated within 500 m · 0 survived", methodological line, all excluded
  expanded by default). Not an empty grid, error, retry, or radius-expansion.
- **A24 @ 18:00** (`La Rosaleda`): the one canonical `UNSTABLE` source case,
  rendered distinctly from `BOUNDARY` with an "irreducible boundary case"
  flag — "genuine solar-boundary case, not a data artefact". Never softened.

## 7. Permanent scientific limitations (must stay visible; Tier-2 drawer)

1. No field validation of modelled Tmrt/UTCI anywhere in the project.
2. A24 @ 18:00 is a genuine, irreducible solar-boundary UNSTABLE case.
3. Tested uncertainty covers only solar forcing + 2-asset geometry (not
   humidity/wind/model-structural uncertainty).
4. Accessibility is straight-line only; no walking-route heat exposure.
5. No behavioural claim — screening only, not prediction of tourist choice.
6. Indoor refuge assumes thermal buffering without verified A/C or
   queue-exposure modelling.
7. Opening hours are 2026-documented values applied to the 2023 study date,
   not verified for 2023.

## 8. Protected-file integrity status

`git diff` vs baseline `901954e` over `data/processed/`, `outputs/tables/`,
`outputs/maps/`, `docs/PHASE0–3*`, and `src/` is **empty**; the seven
data-contract SHA-256s match the baseline. Protected Phase 0–3 artifacts are
**unchanged**. Re-verify at any time with the command in
`docs/PHASE4_1_IMPLEMENTATION_BASELINE.md` §4 and the test
`tests/phase4_1/test_contract.py::test_protected_file_hashes`.

## 9. Current app structure and environment

- Code under `app/` only (`constants.py`, `data_loader.py`, `app.py`,
  `components/`, `assets/style.css`). Tests under `tests/phase4_1/`. Full map:
  `docs/PHASE4_1_IMPLEMENTATION_REPORT.md`.
- Dedicated venv **`.venv_app`, Python 3.12.10** — separate from the main
  3.14 geo interpreter and from `.venv_solweig`. Git-ignored.
- Pinned: `dash==4.4.1`, `dash-leaflet==1.1.3`, `pandas==2.3.3`,
  `pytest==8.4.2` (`app/requirements.txt`; lock in `requirements.lock.txt`).
- Run from repo root: `.venv_app/Scripts/python -m app.app` →
  `http://127.0.0.1:8050/`.
- The seven readable files:
  ```
  data/processed/phase3_asset_catalog.csv
  data/processed/phase3_candidate_screening.csv
  data/processed/phase3_scenarios.csv
  data/processed/phase3_scenarios_summary.csv
  outputs/tables/phase3_exclusion_reasons.csv
  outputs/tables/phase3_hati_vs_baseline.csv
  outputs/tables/phase3_accessibility_sensitivity.csv
  ```

## 10. Remaining UX limitation(s)

- Basemap tiles (CartoDB Positron) require network access at runtime; offline,
  all decision content still renders but the map imagery is blank.
- Tablet is a readability fallback only (stacked column ≤ ~1000px); no phone
  breakpoint, per Phase 4.0 scope.
- Confidence "why" (per-row demonstrated sensitivity) is a click/expand
  detail, by design; only the headline confidence category is on the marker.

## 11. Phase 4.1 is CLOSED

Phase 4.1 is complete and validated. Do **not** reopen it without a concrete,
reproducible defect (a specific failing behavior, a broken test, or a proven
mismatch between the app and a Phase 4.0 spec). "Polish", "add one summary
indicator", or general redesign are **not** defects and do not reopen 4.1 —
they belong to a new, explicitly-chartered phase. Any change must keep the 14
contract/smoke tests green and leave the protected artifacts unchanged from
`901954e`.

## 12. Two possible next directions (do not begin either)

Both require a new user charter before any work starts.

**A. Presentation / demo polish.** Tighten the existing MVP for live
demonstration: visual refinement within the locked channel mapping, optional
offline/basemap fallback, screenshot/GIF capture, a scripted demo path
through S1–S8, and packaging for easy launch. Constraint: no new scientific
claim, score, ranking, view, or channel — strictly cosmetic/operational.

**B. Research-paper packaging.** Assemble the Phase 0–4 record into a
publishable methods/results narrative: figures from `outputs/`, the scenario
and uncertainty tables, the decision-architecture and validation framing, and
the permanent-limitations statement. Constraint: reports the existing locked
findings only; runs no new analysis and reopens no gate.

Neither direction is authorized by this document. Await an explicit charter.
