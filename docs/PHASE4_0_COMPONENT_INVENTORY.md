# PHASE4_0_COMPONENT_INVENTORY.md — HATI-Madrid

Version 1.0 · 2026-08-17. Specification artifact only — component list for
implementation planning, not code.

Each entry: purpose, data fields consumed, states/variants, notes tying it
back to the Visual Semantics / Interaction Spec docs.

## Navigation / shell

**`ScenarioTimeSelector`**
Purpose: choose among the 3 validated timestamps.
Fields: fixed set (`12:00`,`15:00`,`18:00`) + fixed date.
States: one of 3 selected. Always renders the "not live" caption beneath it.

**`ScenarioJumpChip`** (×8, optional)
Purpose: shortcut into a validated scenario (S1–S8).
Fields: `scenario`, `source_id`, `timestamp`, `access_radius_m`.
States: default / hover / active.

**`LimitationsStrip`**
Purpose: Tier-1 always-visible caveat (Interaction Spec §8).
Fields: context-dependent caveat text (map / hours-dependent / distance).
States: one of several pre-written strings, chosen by current view/content.

**`LimitationsDrawer`**
Purpose: Tier-2 full caveat list.
Fields: static text from handoff §7/§8; optional doc-link footnotes.
States: collapsed / expanded.

## Map (View 1)

**`MapCanvas`**
Purpose: render pilot-area basemap + asset markers for the selected
timestamp.
Fields: asset locations, per-asset `decision_state`, `decision_confidence`,
`thermal_state` (for glyph), open/closed at current timestamp.
Notes: point markers only — no continuous raster/heatmap layer (Information
Architecture §2 non-precision guard).

**`AssetMarker`**
Purpose: single asset's spatial representation.
Fields: `decision_state` (fill color), `decision_confidence` (ring style),
`thermal_state` (interior glyph), `is_open` (dim if closed).
States: default / hover(popover) / selected(focus outline) / closed(dimmed).

**`MarkerHoverPopover`**
Purpose: lightweight preview on hover.
Fields: name, `decision_state`, `decision_confidence` gloss.

**`MapLegend`**
Purpose: always-visible key for color/shape/glyph channels.
Fields: static — enumerates the palette from Visual Semantics §2–3.
Notes: not collapsible by default given 3 simultaneous map channels.

## Asset Decision panel (View 2)

**`AssetIdentityHeader`**
Fields: name, `tourism_category`, indoor/outdoor.

**`ThermalStateRow`**
Fields: `thermal_state`, UTCI value where applicable, "modelled" label.

**`DecisionStateBadge`**
Fields: `decision_state`.

**`ConfidenceIndicator`**
Fields: `decision_confidence` + plain-language gloss (Visual Semantics §6).
States: `ROBUST` / `BOUNDARY` / `UNSTABLE` / `INDOOR_BYPASS`, each with
distinct ring style and gloss text — `UNSTABLE` additionally supports an
"irreducible boundary case" annotation for the A24@18:00 worked example.

**`EvidenceConfidenceIndicator`**
Fields: `evidence_confidence`.
Notes: rendered with its own opacity/border-weight channel, never merged
visually with `ConfidenceIndicator`.

**`ExclusionReasonRow`**
Fields: `exclusion_reason` (if this asset is itself excluded in some
context).
Notes: uses `ExclusionExplainer` component (below).

**`RelevantLimitationsList`**
Fields: filtered subset of permanent limitations relevant to this asset's
indoor/outdoor status and hours-dependency.

**`ViewAlternativesButton`**
Fields: candidate count, or `NO_DEFENSIBLE_ALTERNATIVE` summary.
States: enabled(N>0) / zero-result summary / disabled(not a scenario
source).

## Alternative / Trade-off view (View 3)

**`AlternativeCard`**
Purpose: one surviving candidate, full trade-off dimensions.
Fields: name, `tourism_category`/experience type, indoor/outdoor, distance
(labelled straight-line), `thermal_state`/UTCI, `decision_confidence`,
`evidence_confidence`, `is_open`.
Notes: no score, no rank number, no "recommended" flag.

**`TradeoffSortControl`**
Fields: sort key (distance / indoor-outdoor / experience type).
Notes: reorders only; never filters or hides.

**`ExcludedCandidatesList`**
Purpose: on-demand disclosure of everything that didn't survive.
Fields: per item, same identity fields as `AlternativeCard` +
`exclusion_reason`.
States: collapsed(default, except inside `NoDefensibleAlternativePanel`) /
expanded.

**`ExclusionExplainer`**
Purpose: shared component — machine token + plain translation + expand-for-
detail, used in both View 2 and View 3.
Fields: `exclusion_reason` token, translation lookup (Interaction Spec §4),
source-row values (e.g. UTCI vs. limit, distance vs. radius) for the
expanded state.

**`NoDefensibleAlternativePanel`**
Purpose: S8's dedicated first-class empty-result state.
Fields: evaluated count, survivor count (0), full excluded list (expanded
by default), fixed methodological summary line.
Notes: visually distinct "verdict" treatment, not the generic empty state —
see Interaction Spec §6 for full copy/layout requirements.

**`BaselineComparisonToggle`**
Fields: on/off, scoped to current scenario.

**`BaselineComparisonPanel`**
Purpose: analysis-mode overlay showing the Phase 3 nearest-open baseline
pick against the HATI survivor set.
Fields: `baseline_pick_name`, `baseline_pick_distance_m`,
`baseline_pick_indoor_outdoor`, `baseline_pick_survives_hati`,
`baseline_pick_hati_exclusion`, `n_open_in_radius_baseline`,
`n_removed_by_hati_thermal_or_evidence`.
Notes: reads pre-computed `phase3_hati_vs_baseline.csv` rows; never
recomputes a baseline live.

## Shared primitives

**`ConfidenceRingGlyph`** — the shape/ring-style primitive shared by
`AssetMarker` and `ConfidenceIndicator`, so map and panel use one visual
vocabulary for confidence.

**`ExclusionTokenPill`** — monospace machine-token rendering, shared
wherever a raw `exclusion_reason` string appears.

**`CaveatFootnote`** — small inline link from a data point to its governing
limitation (e.g. a UTCI value links to "no field validation exists").
