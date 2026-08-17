# PHASE4_0_INFORMATION_ARCHITECTURE.md — HATI-Madrid

Version 1.0 · 2026-08-17. Specification artifact only.

## 1. View count and rationale

**Three primary views.** A fourth candidate ("scenario library," i.e. a
browsable list of S1–S8) was considered and rejected as a primary view: it is
fully subsumed by the Territorial/Time View (pick a source asset + timestamp)
plus the Alternative/Trade-off View (see the result) — promoting it to a
fourth top-level nav item would duplicate navigation paths to the same
content. Instead, S1–S8 are entry points (a "jump to scenario" affordance)
into the same three views, not a separate view.

```
┌─────────────────────────────────────────────────────────────┐
│  TERRITORIAL / TIME VIEW  (map, default landing view)        │
│  select an asset ──────────────────────────────┐             │
└──────────────────────────────────────────────┬─┘             │
                                                 ▼               │
┌─────────────────────────────────────────────────────────────┐
│  ASSET DECISION VIEW  (side panel, map stays visible)         │
│  "view alternatives" ───────────────────────────┐             │
└──────────────────────────────────────────────┬─┘             │
                                                 ▼               │
┌─────────────────────────────────────────────────────────────┐
│  ALTERNATIVE / TRADE-OFF VIEW  (panel or focused screen)      │
└─────────────────────────────────────────────────────────────┘
```

Navigation is a drill-down, not a tab switch: the Territorial/Time View stays
the spatial anchor. Selecting an asset opens the Asset Decision View as a
panel *alongside* the map (not a full-screen replacement) so the user never
loses the "where am I" context. The Alternative/Trade-off View is reached
only from an asset that has candidate alternatives, and can return to the
map with the alternative set highlighted spatially.

## 2. View 1 — Territorial / Time View

**Purpose:** orient the user in space and time before any single asset is
inspected. Answers product questions 1–3 (thermal situation, feasibility,
confidence) at a glance, for the whole pilot area at once.

**Contents:**
- Map of Prado–Retiro–Atocha (EPSG:25830 data, web-projected for display)
  with all 27 assets as markers.
- A **scenario/timestamp selector** with exactly three states: `12:00`,
  `15:00`, `18:00`, all pinned to `2023-08-21`. This is not a time slider
  implying continuum — see Interaction Spec §Temporal control.
- Each marker encodes, at a glance: indoor/outdoor, decision state,
  decision confidence (see Visual Semantics doc for the channel mapping).
- A legend that is always visible (not a collapsed drawer) — given four
  distinct concepts are on the map, an undiscoverable legend would defeat
  the point.
- A persistent, compact caveat strip (see §5).
- Optional: "jump to scenario" chips (S1–S8) that pan/zoom the map and
  preselect the scenario's source asset and timestamp.

**Explicit non-precision guard:** the map renders asset-level points, not a
continuous thermal surface (no heatmap raster, no isolines). Phase 2.2 model
output exists at asset locations for the pilot's 27 assets, not as a
validated continuous field — rendering a smooth raster would visually assert
spatial precision the model does not have. If a future phase produces a
validated continuous surface, it can be added as an explicit, separately-
captioned layer; Phase 4.0 does not design for it.

**What changes when the timestamp changes:** marker decision state, decision
confidence, and (indirectly) which markers currently have surviving
alternatives. Static content (asset identity, location, category) never
changes with timestamp.

## 3. View 2 — Asset Decision View

**Purpose:** answer "why did the system reach this decision for this asset,
right now" — product questions 1–4. This is the auditability core of the
product.

**Contents, top to bottom:**
1. Asset identity: name, category (e.g. `museum_indoor`, `outdoor_monument`),
   indoor/outdoor.
2. `thermal_state` (e.g. `VERY_STRONG_HEAT_STRESS`, `INDOOR_NOT_MODELLED`) —
   modelled physiological stress band, labelled as modelled.
3. `decision_state` (e.g. `AVOID_PROLONGED_OUTDOOR_EXPOSURE`,
   `INDOOR_REFUGE`) — the tourism action implied.
4. `decision_confidence` (`ROBUST` / `BOUNDARY` / `UNSTABLE` /
   `INDOOR_BYPASS`) with a one-line plain-language gloss (see Visual
   Semantics doc §Uncertainty).
5. `evidence_confidence` (`HIGH` / `MODERATE` / `LOW`) — weakest-link of
   opening-hours evidence and thermal evidence, shown as a separate fact
   from decision confidence, not merged with it.
6. If excluded as a candidate elsewhere: `exclusion_reason`, translated to
   plain language with the raw machine-readable token retained (see
   Interaction Spec §Exclusion explainability).
7. Relevant limitations for *this* asset (e.g. an outdoor asset always shows
   the straight-line-accessibility and no-walking-exposure caveats; an
   indoor asset always shows the indoor-refuge-assumption caveat; every
   asset shows the opening-hours temporal-alignment caveat if its status
   depends on hours at this timestamp).
8. If this asset is a scenario source with surviving candidates: a count and
   an entry point into the Alternative/Trade-off View ("9 alternatives —
   view trade-offs"). If none survive: the `NO_DEFENSIBLE_ALTERNATIVE`
   summary inline (see §4 and Interaction Spec §S8).

**Does not contain:** a synthesized score, a single-word verdict badge that
merges confidence into decision state, or a ranked list.

## 4. View 3 — Alternative / Trade-off View

**Purpose:** let the user compare surviving candidates on their own terms —
product questions 5–7.

**Contents:**
- A card or row per surviving candidate (`status = CANDIDATE_ALTERNATIVE`),
  laid out side-by-side, showing: indoor/outdoor, approximate distance
  (labelled straight-line), experience type, candidate `thermal_state` /
  UTCI where applicable, `decision_confidence`, `evidence_confidence`, open
  status at this timestamp.
- No default sort implies quality. A user-controlled sort (e.g. by distance,
  by indoor/outdoor) is allowed — sorting by one visible attribute is not
  the same as scoring, provided the sort key is explicit and user-chosen,
  never a blended default.
- An "excluded candidates" disclosure (collapsed by default, one click to
  expand) listing everything in the 800 m radius that did *not* survive,
  each with its `exclusion_reason`. This is what makes the screening
  auditable rather than a black box — see handoff §10 ("Show exclusion
  reasons on demand").
- **`NO_DEFENSIBLE_ALTERNATIVE` state** (S8): when zero candidates survive,
  this view renders a dedicated, deliberate-looking state — not an empty
  grid — see Interaction Spec §S8 for full design.
- Optional baseline-comparison toggle (see Interaction Spec §Baseline
  comparison mode) scoped to this view only.

## 5. Cross-cutting: limitations disclosure layer

Not a fourth view — a persistent UI layer present on all three views.
Two-tier: (a) an always-visible compact strip naming the single most
relevant caveat for current context (e.g. "Modelled thermal data, not field-
measured" on the map; "Opening hours are 2026 records applied
retrospectively to 2023" on an asset whose state depends on hours), and (b)
an expandable panel with the full permanent-limitations list (handoff §7)
and the temporal-alignment caveat (handoff §8) in full. Detail in Interaction
Spec §Limitations disclosure.

## 6. Data field → view mapping

| Field | View 1 (map) | View 2 (asset) | View 3 (alternatives) |
|---|---|---|---|
| `thermal_state` | marker color channel | shown, labelled "modelled" | shown per candidate |
| `decision_state` | marker color channel | shown | shown per candidate |
| `decision_confidence` | marker badge/shape | shown with gloss | shown per candidate |
| `evidence_confidence` | not shown at map scale (too dense) | shown | shown per candidate |
| `exclusion_reason` | not applicable | shown if this asset is itself excluded somewhere | shown per excluded candidate (on demand) |
| trade-off dimensions (distance, indoor/outdoor, experience type) | not applicable | summarised as a count | shown per candidate, full |

`evidence_confidence` is deliberately withheld from the map's default view —
five simultaneous visual channels on ~27 markers would violate the "avoid
overloaded map layers" style constraint. It is one click away (asset panel),
not hidden behind a tooltip only.
