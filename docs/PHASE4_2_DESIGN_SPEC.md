# PHASE4_2_DESIGN_SPEC.md — HATI-Madrid

> **Historical document.** This specification records the Phase 4.2 cockpit
> state before the HATI Spatial Decision Replay. The current authoritative
> replay implementation and verification are documented in
> [`docs/replay/README.md`](replay/README.md) and
> [`docs/replay/VALIDATION.md`](replay/VALIDATION.md).

Version 1.0 · Phase 4.2 · Spatial Decision Cockpit.
Binding design specification for the Phase 4.2 implementation. Everything
here is a *presentation* decision. No value in this document is a scientific
threshold, score, weight, ranking or result.

---

## 1. Visual thesis

> **A map-centric scientific decision cockpit where every visual element
> earns its place.**

- **Purpose** — scientific decision support for heat-adaptive urban tourism.
- **User** — urban-climate researchers, destination managers, reviewers.
- **Tone** — editorial, spatial, analytical, restrained, calm.
- **Differentiator** — the interface refuses to give a single recommendation
  score. It exposes **decision + decision confidence + thermal condition +
  evidence confidence + constraints**, as five separate, separately-encoded
  facts.

Design consequences:

1. The map is the ground plane; every other surface is a thin, quiet layer
   floating over it with a hairline border and a 1-step shadow.
2. Colour is scarce. Rust and teal are **reserved exclusively** for
   `decision_state`. Nothing else in the interface may use them as a fill.
   Every other surface is paper, panel, or ink.
3. Type does the hierarchy work that colour is not allowed to do.
4. Motion is confirmatory, never expressive: 120–180 ms, opacity and 1–2 px
   transforms only.

---

## 2. Information architecture

Three views, unchanged from Phase 4.0. No fourth primary view.

```
        ┌──────────── COMMAND BAR (56 px, always) ────────────┐
        │ identity · timestamp · scenario · symbols · limits  │
        └──────────────────────────────────────────────────────┘
 VIEW 1  ████████████ MAP (ground plane, always mounted) ████████████
         │  compact legend ↙                    contextual panel ↘  │
         │                                    ┌──────────────────┐  │
         │                            VIEW 2  │ asset decision   │  │
         │                            VIEW 3  │ alternatives     │  │
         │                                    └──────────────────┘  │
         └──────────────────────────────────────────────────────────┘
              overlays: [symbols popover]  [limitations drawer]
```

Navigation is drill-down, never a tab switch. The map never unmounts. S1–S8
are entry points inside the command bar, not a view.

### 2.1 The 5-second contract

| # | Question | Answered by | Latency |
|---|---|---|---|
| 1 | Where am I? | Map + `Madrid pilot · Prado–Retiro–Atocha` in the command bar | 0 s |
| 2 | Which timestamp? | Segmented control, active segment inverted | 0 s |
| 3 | What do the symbols mean? | Compact legend (3 lines) + `Explain map symbols` | 0 s / 1 click |
| 4 | Which asset is selected? | Selected marker halo + panel header carrying the same asset code | 0 s |
| 5 | What decision? | Panel Tier A — largest non-title type on the page | 0 s |
| 6 | How confident? | Panel Tier A, directly beneath, own ring glyph + word | 0 s |
| 7 | Why? | Panel Tier B — thermal condition, UTCI, evidence | 0 s |
| 8 | Which alternatives? | Tier A CTA → View 3 | 1 click |
| 9 | When is there no defensible alternative? | S8 verdict panel | 1 click |

---

## 3. Layout and responsive rules

### 3.1 Desktop ≥ 1200 px

```
┌────────────────────────────────────────────────────────────────────────────┐
│ ▮ HATI-Madrid  Heat-Adaptive Tourism Decision Support                      │ 56
│   Madrid pilot · 21 Aug 2023        [12:00│15:00│18:00]  [S1 ▾] [?] [Limits]│
├────────────────────────────────────────────────────────────────────────────┤
│                                                        ╎                    │
│                                                        ╎  ASSET  A16        │
│                MAP  (100% of remaining height)         ╎  Fuente de Neptuno │
│                                                        ╎  ─────────────     │
│                                                        ╎  DECISION          │
│                                                        ╎  ● Avoid prolonged │
│    ┌─────────────────────────┐                         ╎    outdoor exposure│
│    │ ● avoid  ● indoor       │                         ╎  ◌ Boundary        │
│    │ ○◌⋯ ring = confidence   │                         ╎  ─────────────     │
│    │ Explain map symbols  →  │                         ╎  …                 │
│    └─────────────────────────┘                         ╎                    │
└────────────────────────────────────────────────────────┴────────────────────┘
                                                          clamp(360,28vw,440)
```

Map share of width: **100%** with no selection, **69–75%** with the asset
panel open at 1280–1600 px, **62–70%** with the alternatives panel open.
Map share of height below the bar: **93%** at 900 px tall.

### 3.2 Breakpoints

| Range | Panel | Legend | Command bar |
|---|---|---|---|
| ≥ 1200 px | right rail, `clamp(360px, 28vw, 440px)`; alternatives `clamp(420px, 34vw, 560px)` | compact, bottom-left | single row |
| 1000–1199 px | right rail, `clamp(340px, 32vw, 400px)` | compact, bottom-left | single row, identity subtitle hidden |
| 700–999 px | right rail `min(48vw, 380px)` | compact, bottom-left, symbols text hidden | two rows |
| < 700 px | **bottom sheet**: map keeps `55vh`, panel is a full-width sheet over the lower 45vh with its own scroll and a grab handle | icon-only chip, opens the symbols popover | two rows, scenario/limits collapse into an overflow menu |

The map is never given a fixed pixel height; it always takes remaining space
(`flex: 1 1 auto` / `55vh` in sheet mode).

### 3.3 Spatial persistence contract

`MapContainer` is created exactly once and never re-created. Only
`LayerGroup#asset-markers.children` is replaced. Consequences:

- changing timestamp → markers swap, centre/zoom **unchanged**
- selecting/deselecting an asset → markers swap, centre/zoom **unchanged**
- opening/closing the panel → the map element resizes; a `Leaflet
  invalidateSize()` is triggered by a clientside resize hook, centre
  preserved
- jumping to a scenario → timestamp + asset change, centre/zoom **unchanged**
  (the pilot area is 1.4 km across and always fully in frame at z15)

---

## 4. Design tokens

Single source of truth: `app/theme.py` (Python) → mirrored into CSS custom
properties on `:root` in `app/assets/style.css`, and into the Mantine theme
object. No literal colour, radius or spacing value may appear in a component
module.

### 4.1 Foundation

| Token | Value | Use |
|---|---|---|
| `--bg` | `#EFEBE2` | app background behind everything |
| `--surface` | `#FBFAF6` | panels, popovers, cards |
| `--surface-raised` | `#FFFFFF` | selected card, drawer body |
| `--surface-muted` | `#F2EEE5` | inset rows, excluded items, table stripes |
| `--surface-inverse` | `#2B2B31` | active segment, primary action |
| `--border-subtle` | `#E4DED2` | hairlines inside a surface |
| `--border-strong` | `#CBC3B4` | surface outlines, control borders |
| `--text-primary` | `#23232A` | 13.9:1 on surface |
| `--text-secondary` | `#5E594F` | 6.6:1 on surface |
| `--text-tertiary` | `#6F6A61` | 5.1:1 on surface, 4.5:1 on bg — smallest label colour |
| `--text-inverse` | `#F7F5EF` | on `--surface-inverse` |

### 4.2 Semantic (scarce by rule)

| Token | Value | Bound to | May be used for |
|---|---|---|---|
| `--decision-rust` | `#B5502E` | `AVOID_PROLONGED_OUTDOOR_EXPOSURE` | marker fill, decision chip, legend swatch — **nothing else** |
| `--decision-teal` | `#2E6B6B` | `INDOOR_REFUGE` | as above |
| `--confidence-ink` | `#3A3A42` | ring stroke for all confidence levels | ring only |
| `--evidence-ink` | `#5E594F` | evidence chip stroke/fill | evidence chip only |
| `--uncertainty-accent` | `#795C26` | UNSTABLE emphasis rule + A24 note border | 1 px rules and 10 px labels only, never a fill |
| `--verdict-ink` | `#2B2B31` | `NO_DEFENSIBLE_ALTERNATIVE` | S8 panel rule and label |
| `--excluded-ink` | `#6B665E` | excluded candidate text (5.4:1 on surface, replaces the failing `#9A948C`) | excluded rows |
| `--selection` | `#23232A` | selected-marker halo, selected card outline | interface state only |
| `--focus` | `#1F5F7A` | `:focus-visible` ring, 2 px + 2 px offset | focus only |
| `--disabled-fg` | `#8B857A` | disabled control text | |

`--decision-rust` at 4.8:1 on surface is used as a **fill** (marker, chip,
swatch) and never as body text; the decision sentence itself is
`--text-primary`, so no reading depends on the rust value.

Rust and teal never appear as a background wash, a gradient, a border of a
non-decision element, or a hover colour. `--uncertainty-accent` is deliberately
a dark desaturated ochre (6.0:1), not amber: it must not read as a caution banner.

### 4.3 Spacing / radius / elevation / motion

```
space:   2 4 6 8 12 16 20 24 32 40        (px, 4-based with 2 and 6 for hairline work)
radius:  sm 4 · md 6 · lg 10 · pill 999
shadow:  s1  0 1px 2px rgba(35,35,42,.06)
         s2  0 2px 8px rgba(35,35,42,.10)
         s3  0 8px 28px rgba(35,35,42,.14)   (drawer / popover only)
motion:  fast 120ms · base 160ms · slow 200ms   easing cubic-bezier(.2,0,.2,1)
         @media (prefers-reduced-motion: reduce) → all durations 1ms, no transform
control-height:  sm 28 · md 34 · lg 40      (touch target ≥ 34 px everywhere)
```

### 4.4 Typography

Three families, one role each, five sizes. No two sizes differ by 1 px.

| Role | Family | Size / weight / tracking |
|---|---|---|
| Product identity | serif | 17 / 600 / +.2 |
| View title (asset name, scenario title) | serif | 22 / 600 / -.1 |
| **Decision statement** | serif | 20 / 600 / -.1 — the largest non-title element in the panel |
| Body | sans | 14 / 400 / 0, line-height 1.5 |
| Supporting / caption | sans | 12.5 / 400 / 0, `--text-secondary` |
| Section label | sans | 11 / 600 / +.8, uppercase, `--text-tertiary` |
| Machine token | mono | 11.5 / 400, in a `--surface-muted` pill |
| Numeric | sans, `font-variant-numeric: tabular-nums` | always with a unit |

Scale = `11 · 12.5 · 14 · 17 · 20 · 22`. Nothing else.

---

## 5. Marker states

Base geometry: 28 px circle, 3 px ring, glyph centred, `iconAnchor` centre.

| State | Encoding | Notes |
|---|---|---|
| **data: decision** | fill = rust \| teal | categorical, 2 values in current data |
| **data: confidence** | ring style = solid \| dashed \| dotted \| none | `ROBUST` \| `BOUNDARY` \| `UNSTABLE` \| `INDOOR_BYPASS` |
| **data: thermal** | inner glyph ☀ \| ⌂ | independent of fill |
| **data: availability** | `opacity .42` + `grayscale(.6)` | closed at this timestamp |
| **hover** | `scale(1.10)`, shadow s1→s2, 120 ms | pointer only |
| **focus-visible** | 2 px `--focus` ring at 3 px offset | keyboard |
| **selected** | 28→34 px, plus a **2 px `--selection` halo at 4 px offset**, `z-index +1000`, shadow s2 | exactly one at a time; neutral charcoal so it cannot be confused with a data channel |
| **selected + closed** | halo at full opacity, marker body still dimmed | selection must remain visible on a dimmed marker |

Accessibility: every marker carries `role="img"` and an `aria-label` of the
form
`"A16 Fuente de Neptuno. Avoid prolonged outdoor exposure. Confidence: boundary. Very strong heat stress (modelled). Open at 15:00."`
The Leaflet marker keeps `keyboard=True`, so markers are tab-reachable and
Enter/Space activate them. A searchable **asset picker** in the command bar
provides a second, fully conventional keyboard path to all 27 assets.

**The halo is an interface state, not a data channel** — stated explicitly in
the symbols popover.

---

## 6. Panel states (View 2 — asset decision)

```
┌──────────────────────────────────────────────┐
│ ⟵                                        ✕  │  ← back (View 3 only) / close
│ A16 · MONUMENT · OUTDOOR                     │  11/600/uppercase  tertiary
│ Fuente de Neptuno                            │  serif 22
│ 15:00 · 21 Aug 2023 (modelled)               │  12.5 secondary
├──────────────────────────────────────────────┤  ── TIER A ──
│ DECISION                                     │
│ ● Avoid prolonged outdoor exposure           │  serif 20/600  ← dominant
│                                              │
│ DECISION CONFIDENCE                          │
│ ◌ Boundary                                   │  sans 14/600 + ring glyph
│ This decision is close to a threshold; some  │  12.5 secondary
│ tested variations would flip it.             │
├──────────────────────────────────────────────┤  ── TIER B ──
│ THERMAL CONDITION                            │
│ Very strong heat stress (modelled)           │  14
│ UTCI 45.0 °C   envelope 43.7 – 45.1 °C       │  tabular
│ ⓘ Model-derived (SOLWEIG/UTCI). Not field-   │  11 tertiary
│   measured; no field validation exists.      │
│                                              │
│ EVIDENCE CONFIDENCE                          │
│ ▣ Moderate    (chip: filled/half/outline)    │  distinct chip, not a ring
│ Weakest link of opening-hours evidence and   │
│ thermal evidence — a supporting fact,        │
│ separate from decision confidence.           │
├──────────────────────────────────────────────┤
│ [ Explore defensible alternatives      · 9 ] │  primary action, 40 px
├──────────────────────────────────────────────┤  ── TIER C ──
│ ▸ Why this decision — full trace             │  accordion, closed
│ ▸ Relevant limitations (3)                   │  accordion, closed
└──────────────────────────────────────────────┘
```

Rules:
- Tiers A and B are **static rows**, never accordions, never tooltip-only.
- Tier C accordions are closed on open and reset when the asset changes.
- The five concepts occupy five separate labelled blocks. No block merges two.
- `Explore defensible alternatives` is enabled only when
  `scenario_for_source(asset, timestamp)` returns a row **and**
  `n_candidate_alternatives > 0`. Otherwise:
  - scenario exists, 0 survivors → the button reads
    `Review the no-alternative finding` (still enabled — it leads to the S8
    verdict, which is a result).
  - no scenario precomputed → a **disabled** state reading
    `No candidate screening was precomputed for this asset at this timestamp.`
    with `aria-disabled`. Never fabricate a scenario.

### 6.1 A24 @ 18:00 — the UNSTABLE state

Distinguished from ordinary `BOUNDARY` by **four** simultaneous differences,
none of which is an alarm:

1. ring style dotted (vs dashed) — already in the locked channel map;
2. the word `Unstable` (vs `Boundary`);
3. the `UNSTABLE`-specific gloss ("This decision changed under tested
   variations — treat as uncertain.");
4. an additional bordered note, `--uncertainty-accent` 1 px left rule on
   `--surface-muted`, labelled **`IRREDUCIBLE BOUNDARY CASE`**, carrying the
   locked A24 annotation verbatim.

Explicitly **not** used: red, an alert icon, a warning triangle, a banner
fill, bold body copy, or any word from the danger register. Uncertainty is
communicated as *epistemic*, never as *hazard*. The note ends with the fixed
line "Uncertainty about a decision is not a statement about physical danger."

---

## 7. View 3 — alternatives / trade-off

```
┌──────────────────────────────────────────────┐
│ ⟵ Back to Fuente de Neptuno                  │
│ S1 · DEFENSIBLE ALTERNATIVES                 │  11/600 uppercase
│ 9 surviving alternatives                     │  serif 22
│ From Fuente de Neptuno · 15:00 · within 800 m│  12.5 secondary
│ ┌──────────────────────────────────────────┐ │
│ │ Surviving alternatives, not ranked       │ │ inset note, --surface-muted
│ │ recommendations. Sorting is for reading  │ │
│ │ order only, not ranking.                 │ │
│ └──────────────────────────────────────────┘ │
│ Sort by [ Distance ▾ ]                       │  Select, 34 px
├──────────────────────────────────────────────┤
│ ┌────────────────────┐ ┌────────────────────┐│  2-up ≥ 520 px, else 1-up
│ │ Museo Thyssen…     │ │ CaixaForum Madrid  ││
│ │ Indoor cultural    │ │ Indoor cultural    ││
│ │ 134 m · ~2 min     │ │ 356 m · ~4 min     ││
│ │ ⌂ Indoor — not     │ │ ⌂ Indoor — not     ││
│ │   modelled         │ │   modelled         ││
│ │ ─ n/a  ▣ Moderate  │ │ ─ n/a  ▣ Moderate  ││
│ │ Open at 15:00      │ │ Open at 15:00      ││
│ └────────────────────┘ └────────────────────┘│
├──────────────────────────────────────────────┤
│ ▸ 17 nearby options were excluded — show why │  accordion, grouped by reason
│ ▸ Reach sensitivity (pre-registered)         │  accordion, static table
│ ⌁ Compare with conventional baseline   [ off]│  switch, off by default
└──────────────────────────────────────────────┘
```

Card rules: fixed internal order, identical for every card; no ordinal
number, no position badge, no "top"/"nearest" superlative, no emphasis
difference between cards. Clicking a card opens that asset's record while
the scenario stays in the back-stack (`⟵ Back to <source>` returns).

Sort options (display-only): `Distance` · `Name` · `Indoor / outdoor` ·
`Experience type`. The literal phrase **"not ranking"** is retained in the
inset note (contract test 8).

Excluded accordion: grouped by locked `exclusion_reason`, each group labelled
in plain language with a count and the machine token as a secondary pill,
each item showing name, distance and the row-level evidence that produced the
exclusion. Excluded text uses `--excluded-ink` (4.9:1) — receding, not
unreadable.

Baseline: a `Switch`, off by default, with a permanent one-line explanation
of what the conventional baseline is and the fixed statement that both
approaches are shown side by side without either being labelled preferable.

---

## 8. S8 — the `NO_DEFENSIBLE_ALTERNATIVE` state

A designed result page, in this order:

```
┌──────────────────────────────────────────────┐
│ ⟵ Back to Parque del Retiro                  │
│ S8 · SCREENING RESULT                        │
├──────────────────────────────────────────────┤
│ ▌ No defensible alternative found.           │  serif 22, --verdict-ink,
│ ▌                                            │  4 px charcoal left rule
│ ▌ This is the screening result, not a failed │
│ ▌ search. Under the specified source,        │
│ ▌ timestamp and reach constraint, no         │
│ ▌ candidate satisfies all gates.             │
│ ▌                                            │
│ ▌ 26 candidates evaluated                     │  tabular
│ ▌  0 survived all gates                      │
├──────────────────────────────────────────────┤
│ WHY CANDIDATES WERE EXCLUDED                 │
│ Outside the 500 m reach                  15  │  bar + count, neutral ink
│ Another hot outdoor location              6  │
│ Closed at this time                       5  │
│  (counts are of the locked exclusion_reason  │
│   column; first failure wins)                │
├──────────────────────────────────────────────┤
│ REACH SENSITIVITY (PRE-REGISTERED)           │
│   500 m → 0    800 m → 2    1200 m → 7       │  static table
│ Descriptive evidence recorded in Phase 3.    │
│ The reach constraint for this scenario is    │
│ fixed at 500 m and is not adjustable here.   │
├──────────────────────────────────────────────┤
│ ▸ All 26 excluded candidates                 │  accordion, closed
│ ⌁ Compare with conventional baseline   [ off]│
└──────────────────────────────────────────────┘
```

Hard rules:
- No error iconography, no red, no retry, no "no results found" phrasing.
- **No control anywhere widens the reach constraint.** The sensitivity table
  is read-only text; the words "expand", "try again", "increase radius" and
  "widen" appear nowhere in this view.
- The verdict uses `--verdict-ink` (neutral charcoal), deliberately outside
  the rust/teal pair, per Visual Semantics §3.
- The literal strings `No defensible alternative found.` and `0 survived`
  are retained (contract test 4).
- The 26 excluded candidates are available but **collapsed** by default so
  the sensitivity evidence stays above the fold.

---

## 9. Command bar

```
▮ HATI-Madrid · Heat-Adaptive Tourism Decision Support
  Madrid pilot · Prado–Retiro–Atocha · 21 Aug 2023
                    [ 12:00 │ 15:00 │ 18:00 ]  [ Find asset ▾ ]
                    [ Scenario ▾ ]  [ ? Symbols ]  [ Limitations ]
```

- **Timestamp** — `dmc.SegmentedControl`, 3 fixed positions, never a slider.
  Directly beneath, an always-visible 11 px caption: *"3 modelled timestamps
  for one historical heat episode — not live or forecast data."* This claim
  is permanent and may not be moved into a disclosure.
- **Scenario** — `dmc.Menu` popover listing S1–S8 as
  `S1 · Fuente de Neptuno · 15:00` with a secondary line
  `9 defensible alternatives` / `no defensible alternative`. Replaces eight
  permanent chips. Keyboard-navigable, Escape closes.
- **Find asset** — `dmc.Select` (searchable) over all 27 assets: the
  conventional keyboard path to selection.
- **Symbols** — `dmc.Popover` containing the complete four-channel encoding,
  the closed-asset dimming rule, and the note that the selection halo is an
  interface state.
- **Limitations** — `dmc.Drawer` (right, Escape to close) with the full
  7-item permanent list and the source-document reference.

The context-sensitive Tier-1 limitation is **not** a permanent strip. It is
placed where it applies: the map legend footer (modelled thermal values), the
panel thermal block (opening hours), and the alternatives inset note
(straight-line distance).

---

## 10. Legend

Compact, bottom-left, ~230 × 96 px:

```
┌─────────────────────────────────┐
│ ● Avoid outdoor  ● Indoor refuge│
│ ○ ◌ ⋯ ring = decision confidence│
│ ☀ ⌂ glyph = thermal state       │
│ Explain map symbols          →  │
└─────────────────────────────────┘
```

Never fully hidden: the two decision colours and the statement that the ring
and glyph are separate channels are always on screen. The popover carries the
complete encoding including exact ring↔confidence mapping, glyph↔thermal
mapping, the dimming rule and the selection-halo note. Below 700 px the
legend becomes a single `?` chip that opens the same popover.

---

## 11. Component library decisions

`dash-mantine-components` 2.8.0 is adopted **selectively**, for components
where hand-rolled equivalents were measurably worse on accessibility:

| Used | Replaces | Reason |
|---|---|---|
| `MantineProvider` | — | theme host; carries the token mirror |
| `SegmentedControl` | 3 hand-rolled buttons | roving focus, `aria-checked` |
| `Select` (searchable) | nothing | new keyboard path to 27 assets |
| `Menu` | 8 chips | keyboard menu semantics, Escape |
| `Popover` | nothing | symbols disclosure with focus return |
| `Drawer` | `<details>` footer | Escape, focus trap, `aria-modal` |
| `Accordion` | `<details>`/`<summary>` | `aria-expanded`, chevron affordance |
| `Switch` | toggle `<button>` | real `aria-checked` for baseline |
| `Tooltip` | Leaflet-only tooltips | still never the sole carrier of meaning |
| `ScrollArea` | raw `overflow-y` | consistent panel scrolling |
| `Paper`, `Badge`, `Divider`, `Group`, `Stack`, `ThemeIcon` | ad-hoc divs | layout consistency |

**Not adopted:** `AppShell` (the map must own the flex height; AppShell's
padding model fights a full-bleed canvas), `Card` (Paper + local CSS is
sufficient and keeps card internals under our own token control), `Alert`
(its visual register is caution — wrong for scope statements), `Skeleton`
(the seven CSVs load in ~40 ms from `lru_cache`; a skeleton would be theatre).

**`dash-iconify` is not adopted.** It fetches every icon from
`api.iconify.design` at render time. That host is unreachable from an
offline or network-restricted review environment (verified: blocked here),
which would leave the interface icon-less exactly where icons carry meaning,
and it adds a third-party runtime dependency to a reproducibility-focused
research artefact. Equivalent functional icons are shipped as **local inline
SVG** in `app/components/icons.py` (12 icons, ~2 KB, no network). Every icon
is paired with a text label, so no meaning is icon-only either way.

Mapping stack unchanged: `dash-leaflet` 1.1.3, CartoDB Positron.

---

## 12. Accessibility requirements (acceptance-level)

| # | Requirement |
|---|---|
| K1 | Every interactive element is reachable by Tab in DOM order; DOM order matches visual order. |
| K2 | `:focus-visible` renders a 2 px `--focus` ring at 2 px offset on every control, including map markers. No `outline: none` without a replacement. |
| K3 | Enter and Space activate every custom control. |
| K4 | Escape closes the drawer, the symbols popover, the scenario menu and the mobile sheet, returning focus to the trigger. |
| K5 | All 27 assets × 3 timestamps are selectable without a pointer (asset picker + focusable markers). |
| N1 | `<header>` / `<main>` / `<aside>` landmarks, each with an `aria-label`. |
| N2 | The panel is `role="region"` with `aria-live="polite"` on the decision block, so a screen reader announces the new decision on selection. |
| N3 | Every marker has an `aria-label` carrying identity + all four data channels in words. |
| C1 | Body text ≥ 4.5:1; text below 14 px ≥ 4.5:1 (no reliance on the large-text exemption). |
| C2 | No state is encoded by colour alone: decision = colour **+** text label; confidence = ring shape **+** word; evidence = chip **+** word; availability = dimming **+** the words "closed at this time". |
| C3 | Tooltips are never the sole source of any fact. |
| T1 | Interactive targets ≥ 34 × 34 px (markers 28 px visual with a 34 px hit area). |
| M1 | `prefers-reduced-motion: reduce` collapses all transitions to 1 ms and removes transforms. |
| S1 | Machine tokens are announced as such (`aria-label="machine token"` on the pill). |

---

## 13. Empty, loading, disabled and failure states

| State | Treatment |
|---|---|
| No asset selected | Panel absent; map full width. A one-line hint chip below the legend: *"Select an asset on the map to see its decision."* |
| Asset not found | `Asset record unavailable for this identifier.` — plain, no apology, no "oops". |
| No scenario precomputed for (asset, timestamp) | Disabled CTA with the exact reason (§6). Never a fabricated scenario. |
| 0 survivors | The S8 verdict panel (§8), never an empty grid. |
| No baseline row | `No precomputed baseline comparison exists for this scenario.` |
| No sensitivity row | The section is omitted entirely rather than showing zeros. |
| Absent UTCI (indoor) | `Not physically modelled for indoor assets.` — never `0.0 °C`, never `n/a` alone. |
| **Basemap tiles unavailable** | The map keeps `--bg`; a dismissible chip states *"Basemap tiles unavailable — asset positions and recorded screening results remain inspectable without the basemap."* Markers and panel continue to function. |
| Initial load | No skeleton; the layout is server-rendered and complete on first paint. |

---

## 14. Interaction model (state machine)

Interface-only state, all in `dcc.Store`, exactly as Phase 4.1:

```
timestamp ∈ {12:00, 15:00, 18:00}          default 12:00
asset     ∈ {A01..A27} ∪ {None}            default None
view      ∈ {map, asset, alternatives}     default map
scenario  ∈ {S1..S8} ∪ {None}              default None
sort      ∈ {distance, name, indoor_outdoor, experience_type}  default distance
baseline  ∈ {False, True}                  default False
```

Transitions:

| Event | Effect |
|---|---|
| timestamp change | `timestamp := t`; if `view = alternatives` → `view := asset` (the precomputed scenario is timestamp-bound) |
| marker / picker select | `asset := a`, `view := asset` |
| scenario menu pick | `timestamp, asset := row.timestamp, row.source_id`; `scenario := S`; `view := asset`; `sort := distance`; `baseline := False` |
| explore alternatives | `scenario := scenario_for_source(asset, timestamp)`; `view := alternatives` |
| card open | `asset := candidate`, `view := asset` (scenario retained for back) |
| back | `view := asset` |
| close | `view := map`, `asset := None` |
| sort | `sort := k` |
| baseline switch | `baseline := bool` |

No transition recomputes anything. Every displayed value is a lookup.

---

## 15. Non-goals for Phase 4.2

Continuous heat rasters · isolines · animation between timestamps · a fourth
primary view · a scenario builder · any radius/threshold input · overall risk
percentages · ranking or scoring of alternatives · ML/AI interpretation ·
live or forecast data · a satellite basemap · WebGL mapping · a React
rewrite · telemetry.
