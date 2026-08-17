# PHASE4_1_IMPLEMENTATION_REPORT.md — HATI-Madrid

Version 1.0 · 2026-08-18. Phase 4.1 — Visual Decision-Support MVP
Implementation. Records what was built, how it honours the Phase 4.0
contract, and the environment needed to run it.

## 1. Scope delivered

A Dash application under `app/` that presents the locked Phase 3 outputs as
the three approved views (Territorial/Time, Asset Decision, Alternative/
Trade-off) with the S8 first-class empty-result state, the A24 @ 18:00
UNSTABLE worked example, the off-by-default baseline comparison, and the
two-tier limitations disclosure. The app is a **read-only presentation
layer**: it never recomputes UTCI/feasibility/screening/baseline and never
writes to protected directories.

## 2. Pre-implementation baseline

Frozen in `docs/PHASE4_1_IMPLEMENTATION_BASELINE.md`. Baseline commit
`901954e1dc8a07970715ff5be82634a9abcc270f`.

## 3. Python environment

- Dedicated virtualenv `.venv_app`, **Python 3.12.10**, created separately
  from the SOLWEIG env (`.venv_solweig`) and from the main 3.14 geo-stack
  interpreter. `.venv_app` is git-ignored.
- Pinned direct dependencies (`app/requirements.txt`); full transitive lock
  in `app/requirements.lock.txt`:
  - `dash==4.4.1`
  - `dash-leaflet==1.1.3`
  - `pandas==2.3.3`
  - `pytest==8.4.2` (dev/test)
- **No** AG Grid, Bootstrap component library, React build tooling, MapLibre,
  ML/AI packages, or database infrastructure were added.
- **No** coordinate-transform library (e.g. pyproj) was needed:
  `phase3_asset_catalog.csv` already carries WGS84 `latitude`/`longitude`,
  handed directly to Leaflet. No reprojection is performed; the "one
  deterministic presentation-only conversion" the charter allowed for was
  found to be unnecessary.

## 4. Application structure

```
app/
  __init__.py
  constants.py            # palette, timestamps, glosses, token translations, limitations copy
  data_loader.py          # read-only load/filter/join/translate of the 7 CSVs (no write path)
  app.py                  # Dash app, layout shell, dcc.Stores (interface state only), callbacks
  components/
    __init__.py
    primitives.py         # ConfidenceRingGlyph, ExclusionTokenPill, ExclusionExplainer, field rows
    shell.py              # ScenarioTimeSelector, jump chips, LimitationsStrip, LimitationsDrawer, MapLegend
    map_view.py           # View 1: MapCanvas + AssetMarker (DivMarker html) + hover tooltip
    asset_panel.py        # View 2: identity, thermal, decision, confidence (+A24), evidence, exclusion, limitations
    tradeoff.py           # View 3: AlternativeCard grid, sort, ExcludedCandidatesList, radius sensitivity,
                          #          BaselineComparisonPanel, NoDefensibleAlternativePanel (S8)
  assets/style.css        # rust/teal/charcoal editorial styling; marker ring/glyph channels
  requirements.txt
  requirements.lock.txt
tests/phase4_1/
  conftest.py             # puts repo root on sys.path
  test_contract.py        # 11 implementation-contract tests
  test_smoke.py           # deterministic import/layout/build smoke tests
```

Run (from repo root):

```bash
.venv_app/Scripts/python -m app.app
```

then open `http://127.0.0.1:8050/`.

## 5. Data contract adherence

- Reads exactly the seven approved files (`app/data_loader.DATA_FILES`);
  nothing else is opened.
- Operations used: filter, join on existing identifiers (`asset_id`,
  `timestamp`, `scenario`, `source_id`), display sort, count of filtered
  rows, and fixed token→copy translation. No new column, score, ranking, or
  re-aggregation is produced.
- All display values trace to a CSV cell. Counts shown ("9 alternatives",
  "26 candidates evaluated · 0 survived") are `len()` of a filtered frame,
  not synthesized metrics.
- A "View alternatives" affordance appears **only** when a scenario was
  pre-computed for that exact (source asset, timestamp); otherwise it is a
  disabled explanatory line — the UI never invents a scenario the pipeline
  did not run, so it can never imply a live recomputation.

## 6. Visual channel mapping (each concept its own channel)

| Concept | Channel | Implementation |
|---|---|---|
| `decision_state` | fill colour | rust `#B5502E` / teal `#2E6B6B` marker + badge fill |
| `decision_confidence` | ring style | solid/dashed/dotted/none border on the marker + panel glyph, drawn at default zoom (not tooltip-only) |
| `evidence_confidence` | opacity/border weight | `evidence-chip` high/moderate/low, panel only |
| `thermal_state` | glyph + text | ☀ / ⌂ inside marker, always with an explicit text label in panels |
| `exclusion_reason` | desaturation + neutral badge | gray `excl-item` styling + monospace token pill + plain translation |

No channel is reused; no red/yellow/green ramp, gauge, KPI wall, star, or
score exists anywhere.

## 7. State management

Six `dcc.Store`s hold **interface state only**: `store-timestamp`,
`store-selected-asset`, `store-view`, `store-scenario`, `store-sort`,
`store-baseline`. No scientific result table is stored. All display content
is re-derived from these keys by filtering the loaded frames inside render
callbacks, so the UI cannot hold a stale or diverged copy of a CSV row. A
central router callback (pattern-matching inputs only) mutates the stores;
four render callbacks project them onto the markers, panel, timestamp
buttons, and limitations strip. The `MapContainer` is created once and never
rebuilt — only the marker `LayerGroup`'s children are swapped on a timestamp
change — so map pan/zoom stays stable.

## 8. Notable implementation decisions

- **Pattern-matching IDs for all interactive triggers.** Singleton buttons
  that live inside dynamically-rendered panels (open-alternatives, close,
  back, baseline-toggle) use `{"type": ..., "index": "x"}` IDs so the router
  callback's inputs never reference an object absent from the initial layout
  (a plain-ID version raised a Dash "nonexistent object" error that silently
  disabled the whole callback graph; caught and fixed during visual QA).
- **A24 @ 18:00** is detected structurally (`asset_id == A24 and timestamp
  == 18:00 and decision_confidence == UNSTABLE`) and rendered with a distinct
  `block--unstable` treatment plus an "Irreducible boundary case" flag — never
  collapsed into the ordinary BOUNDARY styling.
- **Radius sensitivity** (`phase3_accessibility_sensitivity.csv`) is surfaced
  as an explicitly-labelled read-only disclosure in View 3, never as a "try a
  bigger radius" retry action.

## 9. Basemap note

The map uses CartoDB Positron tiles (muted, editorial). Tiles require network
access at runtime; if offline, markers and all decision content still render
(the science is local), only the basemap imagery is absent.
