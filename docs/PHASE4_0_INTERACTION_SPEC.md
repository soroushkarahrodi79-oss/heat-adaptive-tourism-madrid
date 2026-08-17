# PHASE4_0_INTERACTION_SPEC.md — HATI-Madrid

Version 1.0 · 2026-08-17. Specification artifact only.

## 1. Temporal control

**Component:** a 3-position segmented control labelled
`Scenario timestamp: 12:00 · 15:00 · 18:00`, with the fixed date
`2023-08-21` shown adjacent and un-editable. Not a slider, not a play/loop
button, not a clock icon. Hovering or focusing the control shows
"3 modelled timestamps for one historical heat episode — not live or
forecast data" in a caption beneath it, always visible beneath the control
(not tooltip-only), consistent with the "do not call the prototype live"
requirement.

Switching timestamp: re-renders map marker states (decision state,
confidence), keeps map pan/zoom, keeps any open Asset Decision panel open
and updates its content in place if the same asset is still selected
(clearly re-labelled — never silently swaps content under an unchanged
panel without indicating the timestamp changed).

## 2. Map interaction (View 1)

- **Hover** a marker: lightweight popover with name, `decision_state`, and
  `decision_confidence` gloss only — a preview, not the full panel.
- **Click** a marker: opens the Asset Decision View as a right-hand side
  panel (~380–420px), map remains visible and interactive at reduced width,
  selected marker gets a focus outline. Clicking a different marker swaps
  panel content; clicking the same marker again, or a dedicated close
  control, closes the panel.
- **Scenario chips** (S1–S8, optional): clicking one sets the timestamp,
  pans/zooms to the source asset's neighborhood, opens that asset's Asset
  Decision panel, and — if it has alternatives — offers a one-click "view
  alternatives" straight into View 3. This is a shortcut through the normal
  drill-down, not a separate path with different content.
- **Zoom/pan** never changes what data is shown, only what's visible —
  no level-of-detail thermal reinterpolation, since there's no continuous
  surface to interpolate (see Information Architecture §2 non-precision
  guard).

## 3. Asset Decision View (View 2) interactions

- Opens as a panel, not a modal — modal would block map reference, which
  the audit workflow needs (compare this asset's location to alternatives).
- Each data row (`thermal_state`, `decision_state`, `decision_confidence`,
  `evidence_confidence`) is static text/badges, not accordions — these are
  the headline facts and must not require a click to see.
- The exclusion-reason row (present only if this asset is itself excluded in
  some scenario context) is a single line with an inline "why" expand — see
  §4.
- "View N alternatives" is a button, not a link buried in prose; disabled
  with explanatory microcopy ("No candidates were evaluated for this
  asset — it is not a scenario source") when not applicable, rather than
  hidden, so its absence is legible rather than confusing.
- If the asset's alternatives resolve to zero survivors, this button is
  replaced by a compact inline summary of the `NO_DEFENSIBLE_ALTERNATIVE`
  result (count evaluated, count excluded) with a "view full reasoning"
  link into View 3's dedicated empty state — never just omitted.

## 4. Exclusion explainability

**Component:** an expandable row/chip per excluded item, wherever an
`exclusion_reason` exists (Asset Decision View, Alternative/Trade-off View's
excluded-candidates list).

**Collapsed state:** machine token as a small monospace pill (e.g.
`OUTDOOR_EXPOSURE_TOO_HIGH`) plus a **one-line plain-language translation**
always shown alongside it (not only on expand) — traceability and
readability both satisfied without a click:

| Token | Plain-language translation |
|---|---|
| `CLOSED_AT_TIMESTAMP` | Closed at this time, based on documented hours. |
| `ACCESSIBILITY_CONSTRAINT` | Outside the straight-line search radius from the source. |
| `THERMAL_LIMIT_EXCEEDED` | Modelled heat stress here exceeds the tolerable limit. |
| `INSUFFICIENT_EVIDENCE` | Not enough reliable data to support a decision. |
| `NO_MEANINGFUL_THERMAL_IMPROVEMENT` | Would not be meaningfully cooler than the source (below the 0.8 °C pre-registered margin). |
| `OUTDOOR_EXPOSURE_TOO_HIGH` | Another hot outdoor location — doesn't solve the heat problem. |

**Expanded state** (click "why," not hover-only): the same translation plus
the specific values that produced it where available (e.g. distance vs.
radius for `ACCESSIBILITY_CONSTRAINT`; UTCI value vs. limit for
`THERMAL_LIMIT_EXCEEDED`), sourced directly from the relevant CSV row —
never a re-derived or approximated number.

This satisfies "translate but retain traceability": the raw token is always
visible (monospace pill), never replaced by prose alone.

## 5. Alternative / Trade-off View (View 3) interactions

- Default layout: a card grid or table (implementation decides; spec
  requires side-by-side, simultaneous visibility of all survivors up to a
  reasonable count — no single-item carousel/swipe that hides peers).
- **Sort control**, explicit and user-initiated: by distance, by
  indoor/outdoor, by experience type. Changing sort never changes which
  items are shown, only order — reinforces that this is organization, not
  ranking.
- **No default "recommended" flag, star, or top-of-list emphasis** on any
  card.
- Excluded-candidates section: collapsed by default (label states the
  count, e.g. "14 nearby options excluded — show why"), expands in place
  below/beside the surviving set, each item using the exclusion
  explainability component from §4.
- Each card links back to the map (highlight this candidate's marker) and
  supports opening its own Asset Decision View (a candidate is itself an
  asset with its own record).

## 6. S8 — `NO_DEFENSIBLE_ALTERNATIVE` (dedicated design)

**Trigger:** View 3 reached with zero `CANDIDATE_ALTERNATIVE` rows for the
selected source+timestamp (canonical case: Parque del Retiro, A20, 15:00,
500 m radius).

**Design requirement:** this must not reuse the generic "no results" empty
state pattern (blank illustration + "nothing found"). It renders as a
**structured verdict**, matching the weight given to a successful result:

1. Headline, non-alarmed, non-apologetic: **"No defensible alternative
   found."** Subline: "This is the correct result of the screening, not a
   missing feature."
2. A visible tally: "N candidates evaluated within [radius] · 0 survived."
3. The full excluded-candidates list, **expanded by default** in this state
   only (elsewhere it's collapsed) — because in the zero-survivor case, the
   exclusion reasons *are* the content, not a secondary drill-down.
4. A short methodological line, sourced from the Phase 3 validation
   framing, not invented for the UI: e.g. "Every open, in-range candidate
   was either another hot outdoor location or failed on evidence/thermal
   grounds — recommending one would mean sending a heat-stressed visitor to
   an equally hot location."
5. No retry button, no "expand search radius" auto-action — accessibility
   radius is a pre-registered sensitivity parameter (500/800/1200 m tested
   in Phase 3), not a live user-adjustable escape hatch. If radius
   sensitivity is exposed at all, it is a separate, explicitly-labelled
   "sensitivity" toggle showing the pre-computed 500/800/1200 m table
   (`phase3_accessibility_sensitivity.csv`), never framed as "try again with
   a bigger circle to get an answer."

## 7. Baseline comparison mode

**Entry point:** a single explicit toggle/button in View 3, "Compare to
conventional baseline" — off by default, scoped to the currently-open
scenario, not a global app mode.

**Behavior when on:** shows the Phase 3 nearest-open baseline pick for this
source+timestamp alongside the HATI survivor set, with:
- the baseline pick's name, distance, indoor/outdoor;
- whether it survives HATI screening (`baseline_pick_survives_hati`);
- if not, its `exclusion_reason`, via the same explainability component;
- the two summary counts already computed in Phase 3
  (`n_open_in_radius_baseline`, `n_removed_by_hati_thermal_or_evidence`).

**Explicitly not:** a permanent split-screen default layout, a second nav
tab, or a live baseline recomputation — this mode surfaces the pre-computed
`phase3_hati_vs_baseline.csv` row for the current scenario, framed as an
analysis/demo mode a presenter would switch on deliberately.

## 8. Limitations disclosure (two-tier)

**Tier 1 — always visible:** a single-line, low-visual-weight strip present
on every view, context-sensitive:
- Map default: "Thermal values are modelled (SOLWEIG/UTCI), not field-
  measured."
- Any panel where opening hours drive the shown state: "Opening hours are
  2026-documented values applied to the 2023 study date."
- Alternative view: "Distances are straight-line; walking-route heat
  exposure is not modelled."

**Tier 2 — expandable drawer**, one click from Tier 1 (a "Limitations" link,
not an icon-only affordance): the full permanent-limitations list (handoff
§7, all 6 items) and the full opening-hours caveat (handoff §8), in plain
prose, each traceable to its source doc if the audience wants to go deeper
(e.g. a footnote pointing to `docs/PHASE2_2_DECISION_UNCERTAINTY.md`).

This satisfies "not a footer nobody reads": Tier 1 is unavoidable and
contextual (different fact depending on what's on screen), Tier 2 is
complete but opt-in.

## 9. Form factor

Primary target: desktop/laptop, minimum effective width ~1280px (three-panel
layout — map + side panel — needs room; no mobile breakpoint designed in
Phase 4.0). Secondary: tablet-readable, meaning the layout degrades to a
stacked map-then-panel single column above ~768px width, not a redesign —
this is a readability fallback, not a second design target. No phone
breakpoint is in scope.
