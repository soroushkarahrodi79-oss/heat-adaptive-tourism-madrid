# PHASE4_2_IMPLEMENTATION_REPORT.md — HATI-Madrid

Version 1.0 · Phase 4.2 · Spatial Decision Cockpit.
Branch `claude/phase-4-2-ui-ux-redesign-swywzi`, from `c317d80`.

**Verdict: PASS.**

The Phase 4.1 Dash MVP has been rebuilt as a map-centric scientific decision
cockpit. The locked scientific architecture is untouched: the seven Phase 3
files are byte-identical, all 14 Phase 4.1 contract tests still pass
unmodified, and no scientific value is computed anywhere in the interface.

---

## 1. What changed

### 1.1 The fold belongs to the map again

Phase 4.1 spent **265 px of permanent chrome** at every desktop width
(header 87 + eight scenario chips 96 + limitation strip 32 + footer 50). One
**command bar** replaces all four.

| Viewport | 4.1 chrome | 4.2 chrome | 4.1 map height | 4.2 map height |
|---|---|---|---|---|
| 1440×900 | 265 px | **80 px** | 636 px (70.7%) | **820 px (91%)** |
| 1280×800 | 265 px | **89 px** | 560 px (70.0%) | **711 px (89%)** |
| 900×800 | 265 px | 136 px | 440 px (55.0%) | **664 px (83%)** |
| 390×844 | 541 px | 169 px | 440 px, page scrolls | **464 px (55%), no page scroll** |

With the panel open the spatial canvas holds **72% of width** at 1440 and
1280, and **60%** at 900 — inside the 65–75% target at the two desktop sizes
and at the floor at the narrowest rail width.

### 1.2 Selection is now visible on the map

The single largest usability defect in 4.1: clicking a marker changed only
the side panel, so the user could not tell which of 27 dots produced it.
`build_markers()` now takes the selected asset and gives exactly one marker a
**neutral charcoal halo** (2 px ring at 4 px offset), a size step 28→34 px and
a z-index lift. The halo is deliberately outside the rust/teal pair and is
declared in the symbols panel as *"an interface state, not a fifth piece of
data."* Selection stays visible on a dimmed (closed) marker.

The marker LayerGroup is still the only thing that changes, so the map
container, its centre and its zoom survive selection exactly as they survive
a timestamp change.

### 1.3 The panel answers the decision question first

4.1 order: identity → thermal → decision → confidence → evidence, all at the
same weight. 4.2 order, in three explicit tiers:

- **Tier A** identity → **DECISION** (serif 20 px, the largest non-title
  element) → decision confidence, with its gloss.
- **Tier B** thermal condition (state, UTCI, tested envelope, provenance) →
  evidence confidence.
- **Tier A** the alternatives call to action.
- **Tier C** full decision trace and relevant limitations, in closed
  accordions.

Tiers A and B remain static rows. Nothing that Phase 4.0 required to be
always-visible was moved into a disclosure — a test enforces this by walking
the tree and failing if any `block--*` appears inside an accordion.

### 1.4 Eight permanent chips → one scenario menu

S1–S8 now live in a keyboard-navigable menu that shows more per option than
the chips did (source, timestamp, reach constraint, and the outcome —
`9 defensible alternatives` or `no defensible alternative`), in 96 px less
vertical space.

### 1.5 The legend shrank 3× and lost nothing

240×352 px → **236×111 px** (2% of the map at 1440, 3% at 390). The compact
form keeps the two decision colours and the statement that ring and glyph are
separate channels permanently on screen. "Explain map symbols" opens the
complete four-channel encoding, the dimming rule, the confidence-is-not-danger
caveat and the selection-halo note.

### 1.6 S8 is a designed result page

Verdict → tally → **why candidates were excluded** (counts of the locked
`exclusion_reason` column, as labelled bars: 15 out of reach, 6 another hot
outdoor location, 5 closed) → **reach sensitivity** (500 m → 0, 800 m → 2,
1200 m → 7, read-only, with "not adjustable in this interface") → the 26
excluded candidates, collapsed. The headline appears once. No error
iconography, no red, no retry, and — verified by a test that walks every
rendered view — no `Slider`, `NumberInput` or any other control that could
widen the constraint.

### 1.7 A24 @ 18:00 stays uncertain without becoming alarming

Four simultaneous differences from ordinary BOUNDARY (dotted vs dashed ring,
the word *Unstable*, the UNSTABLE-specific gloss, and a bordered
`IRREDUCIBLE BOUNDARY CASE` note carrying the locked annotation verbatim),
using a dark ochre 1 px rule on a muted surface — never a fill, never red,
never a warning icon. The note closes with a fixed line: *"Decision confidence
describes how stable the decision is under tested variation. It is not a
statement about physical danger."* A test asserts the whole danger register
("danger", "warning", "alert", "hazard", "critical", "severe", "unsafe") is
absent, and that `.block--unstable` declares no background.

### 1.8 Copy

| Before | After |
|---|---|
| `Sort (organisation, not ranking):` | `Sort by` + a framing note retaining the phrase "not ranking" |
| `Why this asset can be excluded elsewhere` | `Where this asset is excluded as an alternative` |
| `✓ Comparing to conventional baseline (click to hide)` | a `Switch` labelled `Compare with conventional baseline` |
| `View 9 alternatives — trade-offs` | `Explore defensible alternatives · 9` |
| `This is the correct result of the screening, not a missing feature.` | `This is the screening result, not a failed search.` |
| token then translation | translation then token (a test asserts the order) |

### 1.9 Accessibility, from near-zero to enforced

4.1 had no `:focus-visible` rule anywhere, no accessible name on any marker,
no keyboard path to 19 of 27 assets, and one text style failing AA. 4.2 adds
a skip link, labelled landmarks, a 2 px focus ring on every control, an
`aria-label` on every marker carrying all four data channels in words,
working Enter/Space activation on markers, a searchable asset picker as a
conventional keyboard path, `aria-live` on the decision block, Escape on
every overlay, a 24 px interactive-target floor, and reduced-motion support.

---

## 2. Files changed

### Modified (11)

| File | 4.1 | 4.2 | Change |
|---|---|---|---|
| `app/app.py` | 228 | 357 | Command-bar layout, router refactor, marker render takes selection, drawer/modal/picker callbacks, two clientside hooks, token injection |
| `app/constants.py` | 154 | 349 | Additive 4.2 copy; `SORT_KEYS` gains `name`; `TOURISM_CATEGORY_LABEL` added. No scientific value changed |
| `app/data_loader.py` | 158 | 217 | Additive read-only accessors (`asset_options`, `scenario_options`, `exclusion_breakdown`, `asset_name`, `scenario_source_name`). Same seven files, still no write path |
| `app/components/asset_panel.py` | 239 | 334 | Rebuilt to three tiers; public API unchanged |
| `app/components/tradeoff.py` | 328 | 388 | Rebuilt cards, grouped exclusions, reach block, baseline switch; public API unchanged |
| `app/components/primitives.py` | 107 | 229 | Marker selection state, accessible names, evidence chip, disclosure, count bar |
| `app/components/map_view.py` | 74 | 118 | Selection-aware markers, accessible names, keyboard, tooltip rebuild |
| `app/components/shell.py` | 142 | 80 | Reduced to page assembly + panel container |
| `app/assets/style.css` | 286 | 776 | Rewritten on the token layer; interaction, focus, stacking and responsive layers added |
| `app/requirements.txt` | — | — | `dash-mantine-components`, `dash-svg` added; `dash-iconify` documented as rejected |
| `app/requirements.lock.txt` | — | — | One line added |

### New (12)

`app/theme.py` (145) · `app/components/command_bar.py` (124) ·
`app/components/legend.py` (177) · `app/components/scenario_selector.py` (89) ·
`app/components/limitations.py` (77) · `app/components/empty_states.py` (84) ·
`app/components/icons.py` (69) · `app/assets/keyboard.js` (43) ·
`tests/phase4_2/test_ui_contract.py` (727) + `conftest.py` + `__init__.py` ·
`docs/PHASE4_2_UI_UX_AUDIT.md` · `docs/PHASE4_2_DESIGN_SPEC.md` ·
`docs/phase4_2_ui_qa/` (10 screenshots + README)

### Untouched

`data/**`, `outputs/**`, `src/**`, `manuscript/**`, `supplementary/**`,
`docs/PHASE0_*`–`docs/PHASE4_1_*`, `tests/phase4_1/**`,
`tests/test_outputs.py`, `README.md`, `REPRODUCIBILITY.md`.

---

## 3. Dependencies

**Added:** `dash-mantine-components==2.8.0`, `dash-svg==0.0.12` (already a
transitive dependency of dash-leaflet; promoted to direct because the icon
set uses it). DMC's only Python requirement is `dash`, already pinned, so the
lock file grew by exactly one line.

**Evaluated and rejected: `dash-iconify`.** It resolves every icon from
`api.iconify.design` at render time. That host is unreachable from an
offline or network-restricted environment (verified here: the sandbox proxy
refuses it), which would leave the interface icon-less exactly where icons
carry meaning, and it adds a third-party runtime dependency to a
reproducibility-focused research artefact. Twelve equivalent icons ship
in-repo as inline SVG (`app/components/icons.py`, ~2 KB). Every icon in the
interface is paired with text, so no meaning is icon-only either way.

**DMC adopted selectively**, per the brief: `MantineProvider`,
`SegmentedControl`, `Select`, `Menu`, `Popover`, `Drawer`, `Modal`,
`Accordion`, `Switch`, `Tooltip`, `ScrollArea`, `Paper`, `Badge`, `Divider`,
`ActionIcon`. **Not** adopted: `AppShell` (its padding model fights a
full-bleed map canvas), `Card` (Paper plus local CSS keeps card internals
under our own tokens), `Alert` (its register is caution — wrong for scope
statements), `Skeleton` (the seven CSVs load in ~40 ms from `lru_cache`; a
skeleton would be theatre).

Mapping stack unchanged: `dash-leaflet` 1.1.3, CartoDB Positron, no WebGL,
no satellite basemap. No React rewrite, no Tailwind/Bootstrap, no database,
no API backend, no ML, no telemetry.

**Environment note.** The committed lock file's pre-existing pins were
resolved on Python 3.12 (as `app/requirements.txt` documents) and are left
untouched. This session ran on Python **3.11**, where `numpy==2.5.2` is
unavailable, so a handful of transitive packages resolved slightly lower
locally (numpy 2.4.6, protobuf 7.36.0, cachelib 0.16.1). That affects only
this QA run, not the committed pins — and none of those packages touches the
presentation layer.

---

## 4. Scientific contract status

| Check | Result |
|---|---|
| Phase 3 outputs unchanged | **YES** — `git diff` against the Phase 4.0 lock commit `901954e` over `data/processed outputs/tables outputs/maps docs/PHASE0-3 src/phase3_*.py` is **empty** |
| Protected SHA-256 hashes intact | **YES** — all seven verified by two independent tests |
| 3 timestamps | preserved (12:00 / 15:00 / 18:00, no slider, no interpolation, no animation between them) |
| 27 assets | preserved at every timestamp |
| S8 `NO_DEFENSIBLE_ALTERNATIVE` at 500 m | preserved, upgraded to a first-class result page |
| A24 @ 18:00 UNSTABLE | preserved and still visually distinct from BOUNDARY |
| Baseline | still precomputed-only, still off by default |
| No ranking, no score, no weights, no "best option" | enforced by tests across every reachable view |
| No new science, no recomputation | the app has no write path and performs no scientific arithmetic |
| No live / forecast claim | enforced; the "not live or forecast data" caption is permanent chrome |
| Five concepts, five channels | unchanged channel assignment; enforced by tests |

Nothing in §29 of the brief was triggered. No scientific threshold, scenario
definition, gate order or output was touched.

Two deliberate, presentation-only additions worth naming:

1. **`SORT_KEYS` gained `name` (A–Z).** Alphabetical order is the least
   evaluative order available. It reorders display only; a test asserts every
   sort key preserves the survivor set exactly.
2. **`exclusion_breakdown()`** is a `value_counts()` of the locked
   `exclusion_reason` column. It invents no category and renames nothing; a
   test compares its output against the CSV directly.

---

## 5. Tests

```
tests/phase4_1   14 passed      (unmodified — not one assertion weakened)
tests/phase4_2   67 passed      (new)
tests/test_outputs.py  14 passed
                 ────────────
                 95 passed
```

The Phase 4.2 suite covers: the token layer and the absence of colour
literals in components; AA contrast on every text token (including the
`#9A948C` → `#6B665E` fix for the one 4.1 failure at 2.55:1); marker
selection, channel independence and accessible identity; panel tier order
and the ban on hiding headline facts; the scenario menu against the
precomputed eight; sort-as-organisation; the S8 result page and its counts
against the locked CSV; A24 vs BOUNDARY and the absence of the danger
register; baseline default-off and neutrality; a copy audit over **every**
reachable view (3 timestamps × 3 assets, 8 scenarios × 4 sorts + baseline);
token→label coverage; disclosure defaults; the responsive contract;
reduced motion; focus preservation; the app-wide read-only guarantee; and the
protected hashes.

---

## 6. Browser QA

Playwright + Chromium 141, driven against the running app. **160 assertions
across four suites, all passing.**

| Suite | Checks | Covers |
|---|---|---|
| Interaction | 87 | 12:00→15:00→18:00 with pan/zoom persistence; marker selection ×3; close; **all eight scenarios** end-to-end (source, timestamp, marker halo, survivor count, anti-ranking framing); S8; sorting; baseline; excluded groups; A24 vs BOUNDARY; limitations; symbols |
| Accessibility | 29 | tab order, focus indicators, Enter on markers, the 27-asset picker, Escape, landmark names, marker `aria-label`s, computed contrast of every rendered string, colour-independence, touch targets, reduced motion, **overlay paint order** |
| Responsive | 32 | 1440×900, 1280×800, 900×800, 390×844 — chrome height, map share, legend footprint, overflow, panel behaviour, decision legibility |
| State | 12 | tile failure, no selection, no precomputed scenario, indoor UTCI, closed asset selection |

### Defects found in the browser and fixed

1. **The router callback was dead.** `sort-select` was a plain string ID
   absent from the initial layout, so Dash rejected the whole callback and
   nothing was interactive — the same class of failure Phase 4.1 hit. Fixed
   with a pattern-matching ID.
2. **The timestamp control contradicted the panel.** A scenario jump changed
   the timestamp in the store but the SegmentedControl kept its old value.
   Fixed with a sync callback.
3. **The limitations drawer and symbols modal painted *behind* the map.**
   Mantine's `*-root` elements are `position: static`, so a z-index on them
   is inert; the element that actually stacks is the fixed inner, shipped at
   z-index 200 — inside Leaflet's 400–1000 pane range. Found only by looking
   at screenshots: `elementFromPoint` reported the overlay as topmost because
   hit-testing is not painting. Fixed by lifting the inner and overlay
   layers, and covered by a new check that photographs the region with the
   overlay open and closed and requires the two to differ. That check was
   verified against the bug: reverting the CSS makes it fail.
4. **Icon-only buttons rendered empty below 700 px.** `.bar-btn span
   { display: none }` also hid the span DMC wraps the icons in. Fixed with a
   dedicated text class plus `aria-label` on each button.
5. **The map lost 42% of its width at 900 px** with the panel open (58%).
   Panel capped at `min(40vw, 360px)`.
6. **The command bar wrapped to two rows at 1280 px** (132 px tall). The
   permanent caption now wraps instead of the bar; 89 px.
7. **The S8 headline appeared twice** (view title and verdict panel), which
   read as an error notice. The header no longer carries a headline in that
   case.
8. **Two-up alternative cards at 490 px** wrapped names and stacked the
   confidence row. Switched to one full-width column.

### One QA-harness artefact, not an app defect

A synthetic `el.click()` on a marker stops working after any map drag:
Leaflet's `Map._draggableMoved` stays true until the next mousedown, so it
suppresses clicks that arrive without one. Real pointer input is unaffected.
The harness was changed to issue real mouse events. The same mechanism is why
`app/assets/keyboard.js` dispatches a full mousedown/mouseup/click sequence
rather than a bare `click()`.

---

## 7. Accessibility QA

| Requirement | Result |
|---|---|
| Skip link first in tab order | PASS |
| Every control reachable by Tab, DOM order matches visual order | PASS |
| Visible focus indicator on all 14 sampled stops | PASS (14/14) |
| Enter/Space activates a focused marker | PASS (implemented explicitly — Leaflet's own keypress→click never fires here; verified keydown/keypress/keyup all arrive and no click is produced) |
| All 27 assets selectable without a pointer | PASS (focusable markers + searchable picker, kept in sync both ways) |
| Escape closes drawer / modal / menu / picker | PASS |
| Landmarks labelled | PASS (`header`, `main`, `aside`, map region) |
| Marker `aria-label` carries all four channels | PASS (27/27) |
| Text contrast ≥ 4.5:1 | PASS — lowest rendered string 5.14:1; active timestamp label over its indicator 12.9:1 |
| No state encoded by colour alone | PASS (decision + text, confidence ring + word, evidence chip + word, dimming + words) |
| Tooltips never the sole source of meaning | PASS (marker tooltip content is duplicated in the `aria-label` and the panel; the tooltip also appears on keyboard focus) |
| Interactive targets ≥ 24 px | PASS (was failing on Mantine's 22 px clear button and Leaflet's 14 px attribution link) |
| `prefers-reduced-motion` respected | PASS (transitions → 1 ms, transforms removed) |
| Machine tokens announced as such | PASS |

---

## 8. Known limitations

1. **Basemap tiles could not be loaded in this environment.** The QA
   sandbox's network policy blocks `*.basemaps.cartocdn.com`. Nine of the ten
   committed screenshots therefore show a synthetic light-grid stand-in tile
   injected by the harness; the tenth shows the genuine failure path. Layout,
   contrast and overlay legibility were judged against the stand-in. **The
   app is unchanged and still points at CartoDB Positron; tile rendering
   itself has not been visually confirmed in this session.**
2. **Marker keyboard activation is ours, not Leaflet's.** 43 lines of JS. If
   a future dash-leaflet release wires `keyboard: true` through to a click,
   the file becomes redundant and can be deleted.
3. **27 map markers are 27 tab stops.** That is standard Leaflet behaviour
   and every marker is individually labelled, but a keyboard user crossing
   the map must pass through all of them. The skip link jumps to the map and
   the asset picker offers a one-stop alternative; a roving-tabindex marker
   group would be better and is listed under NOT NOW.
4. **The mobile bottom sheet is fixed-height, not draggable.** Usable at
   390×844 (map 55vh, sheet 45vh with its own scroll) but not a polished
   touch experience.
5. **No screen-reader was run.** Accessibility was verified by computed
   styles, ARIA attributes, tab traversal and contrast maths, not with
   NVDA/VoiceOver.
6. **No visual-regression baseline.** Screenshots are audit artefacts, not
   pixel-diff fixtures.
7. **Two-column alternative cards were dropped**, so nine survivors take
   ~1,800 px of panel scroll. One column made each card comparable
   line-for-line; the trade-off is scroll length.
8. **The `improvement_note` column is shown verbatim** (e.g. *"UTCI 42.6 <=
   source 45.0 - 0.8"*). It is locked Phase 3 text and paraphrasing it would
   be interpretation, so it is labelled *"vs source:"* and left alone.

---

## 9. Before / after, in one line each

| | Phase 4.1 | Phase 4.2 |
|---|---|---|
| First impression | a document with a map in it | a map with a thin control layer over it |
| Chrome at 1440×900 | 265 px | 80 px |
| Selected asset | invisible on the map | halo + size step + z-lift, one at a time |
| Decision in the panel | third block, same weight as the rest | first block, largest element on the page |
| Scenario access | 8 permanent chips, 2 rows, 96 px | one menu, richer options, 0 px |
| Legend | 240×352 px, always all of it | 236×111 px + full encoding one click away |
| Limitations | amber strip + footer, always | in context, plus a drawer one click away |
| S8 | a verdict box with 26 items expanded below it | a result page: verdict → why → sensitivity → detail |
| Keyboard | 8 of 27 assets reachable | all 27, two ways |
| Contrast | one style at 2.55:1 | lowest rendered string 5.14:1 |
| Mobile | page scrolls, legend covers ⅔ of the map | bottom sheet, no page scroll, legend 3% |
| Tokens | literals in 3 places | one definition in `theme.py` |

---

## 10. Recommended future work

### NOW (small, in the same spirit)

- Roving tabindex over the marker group, so the map is one tab stop with
  arrow-key traversal (limitation 3).
- Highlight the surviving alternatives spatially on the map while View 3 is
  open — Phase 4.0 IA §1 anticipated it and it is the clearest remaining gap
  between the panel and the canvas.
- A draggable bottom sheet with a snap point on touch (limitation 4).
- Deep-linkable URL state (`?ts=15:00&asset=A16`) so a reviewer can cite an
  exact view.

### NOT NOW (needs a decision beyond UI)

- Any continuous thermal surface. Blocked by the Information Architecture
  §2 non-precision guard until a validated continuous field exists.
- Walking-route exposure. Requires new science, not new UI.
- An interactive reach constraint. Would turn read-only sensitivity evidence
  into recomputation and break the read-only contract.
- Screen-reader certification and a pixel-diff regression baseline. Both
  worthwhile, both a separate work item.
- Multi-city support. The current shell assumes one pilot area and one date;
  generalising is a data-contract change, not a redesign.
