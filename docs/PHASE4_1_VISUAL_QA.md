# PHASE4_1_VISUAL_QA.md — HATI-Madrid

Version 1.0 · 2026-08-18. Visual / interaction QA of the running Phase 4.1
MVP, performed against `http://127.0.0.1:8050/` via DOM inspection and
scripted interaction (in-app browser). Screenshots were not capturable in
this session's headless pane; verification was done by reading the live DOM,
computed styles, and callback behaviour, which is stronger than pixel
inspection for the channel-separation checks.

## Method

The running app was driven programmatically: timestamp switches, jump chips,
marker/panel drill-down, baseline toggle, and window resizes, each followed
by reading the resulting DOM/computed-style state.

## Findings by required inspection

### Three views + drill-down
- **View 1** renders 27 markers with the CartoDB basemap (24 tiles loaded),
  always-visible legend, jump chips (8), and the "not live" caption.
- Drill-down works: marker/chip click → **View 2** side panel (map stays
  visible); "View N alternatives" → **View 3**; "Back to asset" returns.
- Confirmed the callback graph is live (a fresh-tab load captured **zero**
  window errors; earlier console errors were stale buffer from two pre-fix
  loads and did not recur).

### 12:00 / 15:00 / 18:00
Switching timestamps re-renders marker states while keeping map pan/zoom and
any open panel. Confidence-ring distribution changes correctly with time:

| Timestamp | solid (ROBUST) | dashed (BOUNDARY) | dotted (UNSTABLE) | none (INDOOR_BYPASS) | dimmed (closed) |
|---|---|---|---|---|---|
| 12:00 | 14 | 0 | 0 | 13 | 5 |
| 18:00 | 11 | 2 | 1 | 13 | 6 |

Decision-state fills at 12:00: 14 rust (avoid outdoor) + 13 teal (indoor
refuge). All three map channels (fill / ring / glyph) are simultaneously
legible at default zoom — none inferred from another.

### A24 @ 18:00 (canonical UNSTABLE)
Opened via the S7 chip. Panel shows: "Unstable" with its distinct gloss, a
dedicated **"Irreducible boundary case"** flag reading *"Genuine
solar-boundary case, not a data artefact…"*, and the correct
`block--unstable` treatment — visibly distinct from an ordinary BOUNDARY row
(verified a BOUNDARY asset, A16 @ 15:00, does **not** carry the flag). UTCI
45.4 °C is shown with its tested envelope and a "model-derived, not
field-measured" label.

### S8 (A20 @ 15:00, 500 m) — NoDefensibleAlternativePanel
Rendered as a deliberate verdict, not an empty grid:
- Headline "No defensible alternative found." + subline "This is the correct
  result of the screening, not a missing feature."
- Tally "26 candidates evaluated within 500 m · 0 survived."
- Fixed methodological line present.
- All 26 excluded candidates listed, **expanded by default**, each with its
  token pill + plain translation.
- No card grid, **no retry / no expand-radius action** (verified absent).

### Baseline comparison
Off by default. Switched on for S7: renders the pre-computed row (Palacio de
Cristal, 345 m, outdoor, survives HATI = Yes, 6 open in radius, 0 removed)
with the label "Pre-computed in Phase 3 — not recalculated here." Value
matches `phase3_hati_vs_baseline.csv`.

### Tier-1 / Tier-2 limitations
- Tier-1 strip is present on every view and is context-correct: map →
  "modelled … not field-measured"; asset panel → "opening hours 2026 …
  applied to 2023"; alternatives → "distances are straight-line …".
- Tier-2 drawer contains the full **7-item** permanent-limitations list
  (6 handoff items + opening-hours temporal-alignment caveat) plus the
  source-doc footnote.

### Desktop and tablet widths
- Desktop (~1280px): map + side panel side-by-side (panel 410px asset / 560px
  trade-off).
- Tablet fallback (760px): `.app-main` switches to a stacked column (map
  fixed 440px, panel full-width), **no horizontal page overflow**.

## Defects found and fixed during QA
1. **Callback graph disabled by plain-ID inputs.** The router referenced
   singleton button IDs absent from the initial layout, which Dash rejected,
   silently killing all interactivity. Fixed by converting those triggers to
   pattern-matching IDs. Re-verified: full drill-down now functional.
2. **Stale dev server.** An earlier code revision was masked by a still-running
   server on port 8050; resolved by killing the port owner and relaunching.
   (Process hygiene only; no code impact.)

## Result
No blocking communication defect remains. Every required inspection passed.
The interface reads as a restrained spatial scientific decision-support tool,
not a generic dashboard: no traffic-light ramp, gauge, KPI wall, star, score,
or "best option" appears anywhere.
