# PHASE4_0_TO_PHASE4_1_HANDOFF.md — HATI-Madrid

Version 1.0 · 2026-08-17. Read this file first in any new conversation
starting Phase 4.1 (implementation). It is a pointer document — follow the
references for full detail. Read `docs/PHASE3_TO_PHASE4_HANDOFF.md` too; it
still governs everything about the science underneath this UI.

**Phase 0–3 science is immutable.** **Phase 4.0 design decisions are the
implementation contract** — Phase 4.1 builds exactly what Phase 4.0
specified, not a reinterpretation of it. The UI must never recompute or
silently alter any scientific classification. No new scores, ranking logic,
routing, ML, agents, or live-data claims may be introduced at any point in
Phase 4.1 or beyond, without an explicit new user-chartered phase.

## 1. Current project status

Thermal model locked (Phase 2.2), decision engine validated (Phase 3), and
visual/information architecture approved (Phase 4.0). **Nothing has been
implemented.** Phase 4.1 is the first phase authorized to write application
code, and only within the scope this handoff defines.

## 2. Completed phase gates through Phase 4.0

| Phase | Verdict | Doc |
|---|---|---|
| Phase 0 | GO WITH MODIFICATIONS | `docs/FEASIBILITY_GATE.md` |
| Phase 1 | REVISE BASELINE | `docs/PHASE1_GATE.md` |
| Phase 1.1 | REVISE BASELINE AGAIN | `docs/PHASE1_1_GATE.md` |
| Phase 1.2 | GO TO SOLWEIG / UTCI | `docs/PHASE1_2_SHADE_EVIDENCE_GATE.md` |
| Phase 2 | PHYSICAL MODEL ADDS DECISION VALUE | `docs/PHASE2_GATE.md` |
| Phase 2.1 | MODEL NEEDS REVISION | `docs/PHASE2_1_GATE.md` |
| Phase 2.2 | **MODEL LOCKED** | `docs/PHASE2_2_GATE.md` |
| Phase 3 | **DECISION ENGINE VALIDATED** | `docs/PHASE3_GATE.md` |
| **Phase 4.0** | **VISUAL ARCHITECTURE APPROVED** | `docs/PHASE4_0_GATE.md` |

## 3. The three approved primary views

1. **Territorial / Time View** — map of the pilot area, all 27 assets, a
   3-position timestamp selector (12:00/15:00/18:00, fixed date
   2023-08-21). Default landing view.
2. **Asset Decision View** — opens as a side panel on marker click, map
   stays visible. Full audit trail for one asset's decision.
3. **Alternative / Trade-off View** — surviving candidates side-by-side, no
   ranking; excluded candidates on demand; hosts the S8 state and the
   baseline-comparison toggle.

Navigation is drill-down (map → panel → trade-off), not tab switching. A
4th "scenario library" view was explicitly rejected — S1–S8 are shortcut
entry points into these 3 views, not a separate destination. Full spec:
`docs/PHASE4_0_INFORMATION_ARCHITECTURE.md`.

## 4. Locked information hierarchy

Six fields must never be collapsed into one score or one shared visual
signal: `thermal_state`, `decision_state`, `decision_confidence`,
`evidence_confidence`, `exclusion_reason`, and alternative trade-off
dimensions (indoor/outdoor, distance, experience type, UTCI delta). Full
field → view mapping: `docs/PHASE4_0_INFORMATION_ARCHITECTURE.md` §6.

## 5. Locked visual semantics

Five channels, none reused across concepts:

| Concept | Channel |
|---|---|
| `decision_state` | fill color (categorical: rust = `AVOID_PROLONGED_OUTDOOR_EXPOSURE`, teal = `INDOOR_REFUGE`) |
| `decision_confidence` | marker ring style (solid/dashed/dotted/none) |
| `evidence_confidence` | border weight / opacity, panel only |
| `thermal_state` | interior icon/glyph + explicit text label, always |
| `exclusion_reason` | desaturation + dedicated icon badge, neutral gray-scale, never severity-coded |

No red/yellow/green ramp, no gauge charts, no KPI counters, no magic
percentages, no decorative/AI visual elements. Full spec + rationale:
`docs/PHASE4_0_VISUAL_SEMANTICS.md`.

## 6. Uncertainty treatment

`decision_confidence` (ROBUST/BOUNDARY/UNSTABLE/INDOOR_BYPASS) is drawn
directly on the map marker at default zoom — never hover/tooltip-only. Each
value carries a fixed plain-language gloss (spec §6 of
`docs/PHASE4_0_VISUAL_SEMANTICS.md`). **A24 @ 18:00** is the canonical
UNSTABLE worked example and must render with an explicit "genuine
solar-boundary case, not a data artefact" annotation, visually distinct
from ordinary BOUNDARY rows — never softened into the same bucket.

## 7. S8 / `NO_DEFENSIBLE_ALTERNATIVE` treatment

Canonical case: Parque del Retiro (A20) @ 15:00, 500 m radius, 0 survivors.
When a scenario resolves to zero `CANDIDATE_ALTERNATIVE` rows, the
Alternative/Trade-off View renders a dedicated `NoDefensibleAlternativePanel`
— not a generic empty state: verdict headline ("No defensible alternative
found — this is the correct result of the screening, not a missing
feature"), evaluated/survived tally, full excluded-candidates list expanded
by default, fixed methodological line. No retry button, no auto-expand-
radius action. Full spec: `docs/PHASE4_0_INTERACTION_SPEC.md` §6.

## 8. Baseline-comparison mode

One explicit, off-by-default toggle inside the Alternative/Trade-off View,
scoped to the currently open scenario: "Compare to conventional baseline."
Reads pre-computed rows from `outputs/tables/phase3_hati_vs_baseline.csv`
only — **never recomputes a baseline live**. Not a global app mode, not a
permanent split-screen default. Full spec:
`docs/PHASE4_0_INTERACTION_SPEC.md` §7.

## 9. Permanent scientific limitations that must remain visible

Two-tier disclosure (never a footer nobody reads):

- **Tier 1 (always visible, context-sensitive strip):** e.g. "Thermal
  values are modelled (SOLWEIG/UTCI), not field-measured"; "Opening hours
  are 2026-documented values applied to the 2023 study date"; "Distances
  are straight-line; walking-route heat exposure is not modelled."
- **Tier 2 (expandable drawer):** full permanent-limitations list —
  (1) no field validation of Tmrt/UTCI exists anywhere in this project;
  (2) A24 @ 18:00 is a genuine, irreducible solar-boundary UNSTABLE case;
  (3) tested uncertainty covers only solar forcing + 2-asset geometry, not
  humidity/wind/model-structural uncertainty; (4) accessibility is
  straight-line only, no walking-exposure modelling; (5) no behavioural
  claim — screening only, not prediction of tourist choice; (6) indoor
  refuge assumes thermal buffering without verified A/C or queue-exposure
  modelling — plus the full opening-hours temporal-alignment caveat. Spec:
  `docs/PHASE4_0_INTERACTION_SPEC.md` §8.

## 10. Approved component inventory

Full list with fields/states in `docs/PHASE4_0_COMPONENT_INVENTORY.md`.
Highlights: `MapCanvas` / `AssetMarker` / `MapLegend` (View 1);
`ConfidenceIndicator` / `EvidenceConfidenceIndicator` / `ExclusionReasonRow`
/ `ViewAlternativesButton` (View 2); `AlternativeCard` / `TradeoffSortControl`
/ `ExcludedCandidatesList` / `NoDefensibleAlternativePanel` /
`BaselineComparisonPanel` (View 3); shared: `ConfidenceRingGlyph`,
`ExclusionTokenPill`, `LimitationsStrip`, `LimitationsDrawer`. Build exactly
these; do not invent new components that merge fields the spec keeps
separate.

## 11. Recommended Dash implementation approach

**Dash** (Plotly), recommended over Streamlit and custom React/MapLibre —
full comparison and rationale in
`docs/PHASE4_0_IMPLEMENTATION_RECOMMENDATION.md`. Reasons: same Python/CSV
stack as the locked `src/phase3_*.py` pipeline (no data-export/API layer,
so the UI cannot silently drift from the immutable CSVs); callback model
supports the required "map stays open, panel updates in place" interaction;
sufficient CSS control to avoid generic-dashboard chrome. Map layer:
`dash-leaflet` or Plotly `scattermapbox`/`scattermap` — point markers with
custom styling only, no continuous thermal raster/heatmap (no validated
continuous surface exists). **No package has been installed yet.**

## 12. Exact Phase 3 data files the UI may read

```
data/processed/phase3_asset_catalog.csv
data/processed/phase3_candidate_screening.csv
data/processed/phase3_scenarios.csv
data/processed/phase3_scenarios_summary.csv
outputs/tables/phase3_exclusion_reasons.csv
outputs/tables/phase3_hati_vs_baseline.csv
outputs/tables/phase3_accessibility_sensitivity.csv
```

These are the entire data surface for Phase 4.1. Read-only. No new columns,
no derived scores, no re-aggregation that produces a value not already
present in these files.

## 13. Files the UI must never modify

Every file under `data/processed/`, `outputs/tables/`, `outputs/maps/`, and
every `docs/PHASE0*`–`docs/PHASE3*` document. Also never modify or
re-execute `src/phase3_*.py` or any earlier-phase script as part of the UI
build — the UI is a read-only consumer of already-generated outputs, not a
re-runner of the pipeline. New Phase 4.1 code lives in its own path (e.g.
`app/` or `src/phase4_*`), never inside the Phase 0–3 `src/` outputs it
reads.

## 14. Phase 4.1 implementation restrictions

- Do not reopen SOLWEIG, UTCI, thresholds, scenario definitions, candidate
  logic, or baseline-comparison methodology.
- Do not introduce a composite/weighted score, a single "HATI score," or a
  ranked "best option" anywhere in the UI.
- Do not add ML, LLM ranking, agents, personas, or behavioural prediction.
- Do not perform heat-aware route optimisation or real routing (straight-
  line only, explicitly labelled as such).
- Do not expand beyond the pilot geography or the 27-asset catalog.
- Do not imply real-time/live data — always show the fixed
  12:00/15:00/18:00 selector with its "not live" caption, fixed date
  2023-08-21.
- Do not treat opening hours as verified-for-2023 fact.
- Do not silently deviate from the approved views, channel mapping, or
  component inventory (§3, §5, §10) without flagging the deviation to the
  user first — Phase 4.0 is the contract, not a suggestion.
- Do not skip the two-tier limitations disclosure (§9) to save UI space.

## 15. Acceptance criteria for the built MVP

The built prototype passes Phase 4.1 review only if, reproducing the
Phase 4.0 gate checks against the running app:

1. A user can reach all three views via the drill-down described in §3,
   using only the 3 approved timestamps.
2. On the map, `decision_state`, `decision_confidence`, and `thermal_state`
   are simultaneously legible per the channel mapping in §5 — none inferred
   from another.
3. `evidence_confidence` and `exclusion_reason` are visible in the Asset
   Decision / Alternative views without requiring a tooltip as the only
   access path.
4. A24 @ 18:00 renders with its distinct UNSTABLE treatment, verifiable by
   opening that specific asset at that specific timestamp.
5. Loading S8's scenario (A20 @ 15:00, 500 m) renders the dedicated
   `NoDefensibleAlternativePanel`, not an empty grid or error.
6. The baseline-comparison toggle, when switched on for any scenario,
   shows the exact pre-computed row from `phase3_hati_vs_baseline.csv` —
   no live recomputation.
7. The Tier-1 limitations strip is present and context-correct on all
   three views; the Tier-2 drawer contains the full permanent-limitations
   list verbatim.
8. No screen, tooltip, or exported view contains a single synthesized
   score, star rating, or ranked-"best" label anywhere in the app.
9. No copy anywhere describes the data as live, real-time, current, or
   forecast.
10. `git diff`/file-hash check confirms no file listed in §13 was modified
    by the implementation work.

Any failed criterion blocks sign-off and routes back to Phase 4.1 rework,
not a re-litigation of Phase 4.0's design decisions.
