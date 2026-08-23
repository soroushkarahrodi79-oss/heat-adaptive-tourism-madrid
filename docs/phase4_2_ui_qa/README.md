# Phase 4.2 — visual QA artifacts

Captured with Playwright (Chromium 141) against the running app at
`http://127.0.0.1:8050/`. Ten screenshots, one per state that carries a
distinct design decision. Working screenshots taken during iteration were
not committed.

| File | Viewport | State |
|---|---|---|
| `desktop_map.png` | 1440×900 | View 1, nothing selected — command bar, compact legend, selection hint |
| `desktop_asset.png` | 1440×900 | View 2, S1 source (A16 @ 15:00) — decision-first panel, selected-marker halo |
| `desktop_alternatives.png` | 1440×900 | View 3, S1 — nine surviving alternatives, anti-ranking framing, sort control |
| `s8_empty_state.png` | 1440×900 | S8 `NO_DEFENSIBLE_ALTERNATIVE` — verdict, exclusion breakdown, reach sensitivity |
| `a24_unstable.png` | 1440×900 | A24 @ 18:00 — the irreducible solar-boundary UNSTABLE case |
| `map_symbols.png` | 1440×900 | The complete four-channel encoding, including the selection-halo note |
| `limitations_drawer.png` | 1440×900 | All seven permanent limitations, one click from the command bar |
| `narrow_layout.png` | 900×800 | Map + narrower rail (map keeps 60% of width) |
| `mobile_layout.png` | 390×844 | Bottom-sheet panel, icon-only command bar, map keeps 55vh |
| `tiles_unavailable.png` | 1440×900 | Basemap unreachable — graceful degradation |

## Basemap in these captures

The QA sandbox's network policy blocks `*.basemaps.cartocdn.com`
(verified: the proxy answers 403 to CONNECT). Nine of the ten screenshots
therefore render a **synthetic stand-in tile** — a warm off-white raster with
a faint street grid, injected by the QA harness — so that overlay contrast
and legend legibility can be judged against a light basemap of the kind
CartoDB Positron produces. It is a test fixture only: the application itself
is unchanged and still points at CartoDB Positron.

`tiles_unavailable.png` is the exception. It is captured with tiles genuinely
failing, and shows the real degradation path: the map keeps its background,
a notice explains that asset positions and every screening result are
computed locally and remain correct, and all 27 markers plus the full
decision panel keep working.

## Reproducing

```bash
.venv_app/bin/python -m app.app          # then, in another shell:
.venv_app/bin/python -m pytest tests/phase4_1 tests/phase4_2 -q
```

The browser suites (interaction, accessibility, responsive, state) are
described in `docs/PHASE4_2_IMPLEMENTATION_REPORT.md` §Browser QA.
