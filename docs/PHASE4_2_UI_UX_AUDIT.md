# PHASE4_2_UI_UX_AUDIT.md — HATI-Madrid

Version 1.0 · Phase 4.2 · Audit of the running Phase 4.1 Dash MVP.

Audit basis: source review of `app/` (1,992 lines incl. CSS), the seven
locked Phase 3 CSVs, the Phase 4.0 specification set, and a live browser
inspection of `http://127.0.0.1:8050/` at 1440×900, 1280×800, 900×800 and
390×844 (Chromium 141, Playwright).

Pre-change baseline: `git HEAD c317d80`, `pytest tests/phase4_1` →
**14 passed**. Protected Phase 3 hashes verified intact.

---

## 1. What Phase 4.1 got right (must be preserved)

| Strength | Why it matters | Preservation rule for 4.2 |
|---|---|---|
| **Four independent map channels** (fill=`decision_state`, ring=`decision_confidence`, glyph=`thermal_state`, dim=`is_open`) | This is the single most valuable property of the interface: no visual variable is doing two jobs, so "hot" never reads as "uncertain". | Channel assignment is frozen. 4.2 may only improve legibility, never merge channels. |
| **Map container mounted once; only `LayerGroup.children` swap** | Pan/zoom survives every timestamp change. Rebuilding `MapContainer` would reset the user's spatial frame on every interaction. | Keep. Extend the same pattern to selection. |
| **Interface-only `dcc.Store` state** | No scientific table is ever held in browser state, so the UI cannot drift from the locked outputs. | Keep exactly. |
| **`data_loader` has no write path by construction** | Enforced by test 3. | Keep; no new I/O. |
| **S8 has a dedicated verdict component, not an empty grid** | `NO_DEFENSIBLE_ALTERNATIVE` is already treated as a result. | Keep the concept; upgrade the execution (§4.7). |
| **A24 @ 18:00 carries a distinct irreducible-boundary flag** | The one canonical UNSTABLE case is not softened into BOUNDARY. | Keep the distinction; restrain the styling (§4.8). |
| **Machine token always paired with a plain translation** | Auditability without engineering jargon as the primary voice. | Keep, but invert the emphasis (§4.9). |
| **Baseline comparison off by default, precomputed only** | No leaderboard, no recomputation. | Keep. |
| **Restrained palette already avoids traffic-light** | Rust/teal, no red/green, no gauge, no KPI wall. | Evolve into tokens; do not discard. |

---

## 2. Hierarchy problems

### 2.1 The map is not dominant — chrome eats the fold
Measured in Chromium (bounding boxes, default landing view):

| Viewport | header | chips | strip | footer | **chrome** | map height | map share |
|---|---|---|---|---|---|---|---|
| 1440×900 | 87 | 96 | 32 | 50 | **265 px** | 636 px | 70.7% |
| 1280×800 | 87 | 96 | 32 | 50 | **265 px** | 560 px | 70.0% |
| 900×800 | 87 | 96 | 32 | 50 | **265 px** | 440 px (fixed) | 55.0% |
| 390×844 | 202 | 241 | 48 | 50 | **541 px** | 440 px (fixed) | 52% of a page that now scrolls |

With the trade-off panel open at 1280 px the 560 px panel leaves the spatial
canvas **56% of width**, below the 65–75% target.

*User impact:* the first thing a destination manager sees is a wall of eight
long scenario chips and two advisory strips, not Madrid. The product reads as
a document with a map in it rather than a spatial tool.

### 2.2 Eight permanent scenario chips are the single largest offender
`S1 · Fuente de Neptuno · 15:00` ×8 wraps to two rows at every width below
~1500 px. They are navigation shortcuts — a secondary affordance — occupying
prime horizontal real estate above the primary working surface, permanently.

*User impact:* the chips are visually louder than the timestamp control,
which is the more frequently used control; and they imply eight equal-weight
"modes" when they are in fact eight worked examples.

### 2.3 The asset panel opens with metadata, not with the decision
Current order: identity → **thermal state** → decision → confidence →
evidence. The user's question ("what does HATI say about this place?") is
answered third, ~180 px down, in the same type size as the supporting facts.
`Very strong heat stress (modelled)` at 15 px sits above
`Avoid prolonged outdoor exposure` at 15 px — equal weight for a physical
observation and a decision.

*User impact:* fails the 5-second test. The decision does not win the page.

### 2.4 The legend out-weighs the map content it explains
The always-visible legend is 240 px wide × 352 px tall — roughly **9% of the
map viewport at 1440 px, and 61%×80% of it at 390 px** — and reproduces all four channels plus a dim example in full
prose at all times, including for a user who has already learned them.

*User impact:* on a 900-px-wide viewport the legend covers a meaningful part
of the study area; the user must mentally subtract it.

### 2.5 Two limitation surfaces compete
A permanent Tier-1 amber strip *plus* a permanent footer disclosure. The
amber strip reads as a warning banner (the amber `#EFE7D6`/`#7A5A22` pairing
is a conventional caution colour), which is the wrong register: these are
scope statements, not alerts.

*User impact:* alarm fatigue on a text that never changes urgency, and 74 px
of permanent vertical space for content the user reads once.

---

## 3. Usability weaknesses

### 3.1 No selected-marker state — the core interaction is invisible
`marker_html()` renders identically whether or not the asset is selected.
Selection changes only the side panel. `_render_markers` is keyed on
timestamp alone, so there is no mechanism to express selection on the map.

*User impact:* **the most important usability defect in the build.** After
clicking, the user cannot tell which of 27 dots produced the panel. The
map↔panel relationship, which is the whole premise of a spatial cockpit,
must be reconstructed by re-reading the asset name.

### 3.2 Selection cannot be reached by keyboard
Markers are `DivMarker`s with no accessible name and no keyboard path.
Everything downstream of asset selection (View 2, View 3, S8, A24) is
therefore keyboard-unreachable except via the eight scenario chips, which
cover only 8 of 27 assets and only 3 of 81 (asset × timestamp) states.

### 3.3 Tooltip is the only place several facts exist on the map
The marker tooltip carries the decision label, confidence name and the
confidence gloss. Hover is unavailable on touch, and tooltips are invisible
to a user reading with a screen reader.

### 3.4 Sort control is mislabelled as a caveat
`Sort (organisation, not ranking):` puts a disclaimer in the control's label.
The disclaimer is correct and necessary, but as the label it makes the
control read as something the designer is apologising for.

### 3.5 "Why this asset can be excluded elsewhere" is unanswerable copy
The heading names a hypothetical context the user is not in. It appears in
the asset panel whenever `context_free_exclusion_reason` is non-blank (16 of
81 rows, all `CLOSED_AT_TIMESTAMP` plus 1 `INSUFFICIENT_EVIDENCE`).

### 3.6 Excluded candidates are expanded by default in S8
All 26 excluded rows render open, producing a ~2,000 px scroll of near-
identical items and burying the radius-sensitivity evidence below them.

### 3.7 Two different affordances look like one
`.alt-entry--btn` (a real `<button>`) and `.card__open` ("Open at this
timestamp", a plain `<div>` label immediately above a real button) sit
adjacent with no visual grammar distinguishing statement from action.

### 3.8 Baseline toggle is a button pretending to be a switch
`✓ Comparing to conventional baseline (click to hide)` — state, action and
instruction crammed into one label, with no `aria-pressed`.

---

## 4. Accessibility issues

| # | Issue | Impact |
|---|---|---|
| A1 | Map markers have no accessible name, no role, no keyboard path (§3.2) | Screen-reader and keyboard users cannot reach View 2/3 at all for 19 of 27 assets. |
| A2 | No visible focus styling anywhere — no `:focus-visible` rule exists in `style.css` | Keyboard users cannot see where they are. Chrome's default outline is suppressed on several controls by `border: none`. |
| A3 | Timestamp group is `role="group"` with no `aria-label`, buttons have no `aria-pressed` | The active timestamp is conveyed by colour only. |
| A4 | `evidence_confidence` is conveyed by an opacity-only chip plus a word; `decision_confidence` ring style is shape-only on the map | Fails "status not encoded by colour/one channel alone" on the map layer. |
| A5 | `<details>`/`<summary>` used for the excluded list, radius table and Tier-2 drawer with `list-style:none` and no marker replacement in some rules | Disclosure state is not always visible. |
| A6 | Computed contrast: ink `#26262B`/paper 13.4:1 ✓, charcoal 11.1:1 ✓, limstrip 6.9:1 ✓, muted `#6E685F` on panel 5.3:1 ✓, teal `#2E6B6B` on panel 5.9:1 ✓, rust `#B5502E` on panel 4.8:1 ✓ — but `.excl-item__name` `#9A948C` on `#F0ECE2` is **2.55:1, fails AA** | Excluded candidate names are the least readable text in the app, at 12.5 px. |
| A7 | Touch targets: `.jump-chip` measures 182×**22 px**; `.sort-btn` and `.card__open-btn` are specified at 23–25 px | All below the 24 px minimum; unusable on touch. |
| A8 | No reduced-motion handling (`transition: width .18s` on the panel) | Minor, but trivially fixable. |
| A9 | Tooltip is sole carrier of the confidence gloss on the map (§3.3) | Information loss for non-pointer users. |
| A10 | No skip link, no landmark labelling; a single unlabelled `<aside>` | Screen-reader navigation is guesswork. |

---

## 5. Responsive issues

| Width | Behaviour | Verdict |
|---|---|---|
| 1440×900 | Works. | OK |
| 1280×800 | Trade-off panel 560 px = 44% of width; alt-grid drops to 1–2 columns. | Tight |
| ~1000 px | Breakpoint switches to stacked column: map fixed **440 px**, panel full-width below. | The map stops being the working surface at exactly the width where a laptop user still expects it to be. |
| 900×800 | Stacked; 265 px chrome above a fixed 440 px map (55%). | Poor |
| 390×844 | Header 202 px + chips 241 px + strip 48 px = **491 px of chrome above the map**; the legend (240 px, absolutely positioned) covers 61% of the 390 px map width and 80% of its height. | **Collapses.** The map is effectively unusable. |

Root cause: a single 1000 px breakpoint and a fixed-pixel side panel
(`410px` / `560px`) with no fluid clamp.

---

## 6. Code issues that affect UX

1. **Selection cannot be expressed** — `_render_markers` takes only
   `store-timestamp` as input (`app/app.py:171`). Fixing §3.1 requires the
   selected asset as a second input; the LayerGroup-swap pattern already
   makes this cheap and map-state-preserving.
2. **Nine `Input` lists in one router callback** (`app/app.py:83–108`) — every
   pattern-matching group fires the router, and the router re-derives six
   store values on every click. Correct, but the `_clicked()` guard is
   duplicated nine times and the branch chain is 70 lines. Maintainability,
   not performance (27 assets).
3. **`{"index": "x"}` sentinel IDs** for close/back/open-alt/baseline —
   pattern-matching used purely to dodge the "ID not in initial layout"
   error. Works, but the sentinel is unexplained at three call sites.
4. **Literal values scattered across CSS and Python** — `#B5502E` appears in
   `constants.py` and twice in `style.css`; `34px` marker size in
   `primitives.py`, `map_view.py` and `style.css`; panel widths only in CSS.
   Any token change needs three edits, which is how palettes drift.
5. **`shell.py` mixes four unrelated concerns** (brand, temporal control,
   scenario chips, two limitation tiers) in 142 lines.
6. **Unused imports** — `confidence_ring_glyph` in `shell.py`, `field_row` in
   `asset_panel.py`, `html` in `test_smoke.py`'s unused import list.
7. **No focus/hover/selected CSS layer at all** — interaction states were
   simply never authored.

---

## 7. Copy audit

| Current | Problem | Direction |
|---|---|---|
| `Sort (organisation, not ranking):` | Disclaimer as label | Label = `Sort by`; disclaimer moves to a caption. Must retain the literal phrase "not ranking" (contract test 8). |
| `Why this asset can be excluded elsewhere` | Names a context the user isn't in | `Where this asset is excluded as an alternative` |
| `✓ Comparing to conventional baseline (click to hide)` | Three messages in one control | A switch labelled `Compare with conventional baseline`, off by default |
| `View 9 alternatives — trade-offs` | Two nouns, unclear verb | `Explore defensible alternatives · 9` |
| `26 nearby options excluded — show why` | Fine | Keep, group by reason with counts |
| `No defensible alternative found.` | Good | Keep verbatim (contract test 4) |
| `This is the correct result of the screening, not a missing feature.` | Slightly defensive | `This is the screening result, not a failed search.` |
| `OUTDOOR_EXPOSURE_TOO_HIGH` shown before its translation | Machine voice leads | Plain language leads; token becomes a secondary monospace pill |

No instance of "Oops", "Something went wrong", "Great choice", "Recommended
for you", "best", "score", "rank" exists in the current build. That
discipline is intact and must stay intact.

---

## 8. Opportunities (ranked by user impact)

1. **Selected-marker state + map↔panel binding** — fixes the single defect
   that most undermines the "spatial cockpit" claim.
2. **Reclaim the fold**: one 60 px command bar replaces header + chips +
   strip + footer → map gains ~150 px and the full width when no asset is
   selected.
3. **Compact legend + "Explain map symbols" disclosure** — 200×90 px instead
   of 240×340 px, with the complete scientific encoding one click away.
4. **Decision-first panel** with three explicit tiers.
5. **Scenario popover** replacing eight chips — S1–S8 with their source,
   timestamp and outcome in one compact, keyboard-navigable menu.
6. **Keyboard parity for asset selection** — a searchable asset picker plus
   focusable markers, so 27 assets × 3 timestamps are all reachable.
7. **S8 as a designed result page** — verdict, exclusion breakdown by
   reason, constraint-sensitivity evidence, in that order.
8. **A token system** (CSS variables + a Python mirror for the Mantine
   theme) so palette/spacing/typography have one definition.
9. **Fluid responsive panel** (`clamp()`), a second breakpoint, and a
   bottom-sheet panel below ~700 px.

---

## 9. Files expected to change

| File | Change |
|---|---|
| `app/app.py` | Layout → command bar + map + contextual panel; router refactor; marker render gains selection input; drawer/popover callbacks. |
| `app/theme.py` | **New.** Design tokens + Mantine theme (single source of truth). |
| `app/constants.py` | Additive presentation copy only (legend, panel, S8, scenario menu). No scientific value changes. |
| `app/data_loader.py` | Additive read-only helpers (`scenario_options`, `exclusion_breakdown`, `asset_options`). No new files read. |
| `app/components/primitives.py` | Marker states, confidence glyph, token pill, exclusion explainer rebuilt on DMC. |
| `app/components/map_view.py` | Selection-aware markers, accessible names, compact legend host. |
| `app/components/asset_panel.py` | Rebuilt to the three-tier hierarchy. Public API unchanged. |
| `app/components/tradeoff.py` | Rebuilt cards, accordion exclusions, S8 panel, baseline switch. Public API unchanged. |
| `app/components/shell.py` | Reduced to the limitations drawer + shared shell chrome. |
| `app/components/command_bar.py` | **New.** |
| `app/components/scenario_selector.py` | **New.** |
| `app/components/legend.py` | **New.** |
| `app/components/empty_states.py` | **New.** |
| `app/components/icons.py` | **New.** Local inline-SVG icon set. |
| `app/assets/style.css` | Rewritten around tokens; interaction-state layer added. |
| `app/requirements*.txt` | `dash-mantine-components` added. |
| `tests/phase4_2/` | **New** UI/accessibility contract tests. |

## 10. Files that must NOT change

`data/processed/**`, `outputs/**`, `src/**`, `manuscript/**`,
`supplementary/**`, `docs/PHASE0_*`–`docs/PHASE4_1_*`,
`tests/phase4_1/**` (assertions), `tests/test_outputs.py`, `REPRODUCIBILITY.md`.

The seven protected SHA-256 hashes in
`docs/PHASE4_1_IMPLEMENTATION_BASELINE.md` §3 must still verify.

---

## 11. Scientific-contract risks in this redesign, and their controls

| Risk | Control |
|---|---|
| A "cleaner" panel merges decision + confidence into one badge | Five concepts keep five separate blocks; enforced by contract test 7 and a new 4.2 test. |
| Sort-by-distance in a card grid reads as a ranking | Explicit "not ranking" caption retained; cards carry no position number, no ordinal, no emphasis difference. |
| Grouping exclusions by reason invents a taxonomy | Groups are `value_counts()` of the locked `exclusion_reason` column; no new categories. |
| A radius control appears next to the sensitivity table | Sensitivity stays a static read-only table; no radius input exists anywhere in the DOM. |
| Icon-only status | Every icon is paired with text; no state is icon-only or colour-only. |
| Marker "selected" halo mistaken for a fifth data channel | The halo is neutral charcoal, drawn outside the marker body, and appears on exactly one marker at a time; it is documented in the legend disclosure as an interface state, not data. |
