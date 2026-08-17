# PHASE4_0_IMPLEMENTATION_RECOMMENDATION.md — HATI-Madrid

Version 1.0 · 2026-08-17. Specification artifact only. No framework is
installed or coded in this phase.

## 1. Options compared

Three approaches, chosen as the realistic span for a Python-data-backed,
map-centered, panel-heavy research prototype:

1. **Streamlit**
2. **Dash** (Plotly)
3. **Lightweight custom React + MapLibre GL JS** (or equivalent — e.g.
   Svelte + MapLibre; the substance is "custom SPA + dedicated map library")

## 2. Evaluation

| Criterion | Streamlit | Dash | Custom React/MapLibre |
|---|---|---|---|
| Scientific traceability (reads Phase 3 CSVs directly, same stack as `src/phase3_*.py`) | High — pure Python | High — pure Python | Medium — needs a thin data-serving layer (static JSON export or small API) between the Python pipeline and the JS app |
| Map capability | Weak-to-medium (via `st.map`/pydeck; multi-layer categorical styling is awkward) | Medium-good (Plotly mapbox/scattermapbox, or `dash-leaflet`) | Best — MapLibre gives full control over marker styling per Visual Semantics doc (custom rings, glyphs, desaturation) |
| Interaction quality (persistent side panel + map selection state without losing context, per Interaction Spec) | Weak — Streamlit's rerun-on-interaction model makes a stable "map stays open, panel updates in place" pattern awkward, though `st.session_state` can approximate it | Good — callback model supports panel updates without full-page rerender | Best — native SPA state management, exactly matches the drill-down spec |
| Implementation complexity for this scope | Lowest | Medium | Highest |
| Reproducibility (single environment, few moving parts) | Highest — one `streamlit run` | High — one `python app.py` | Lower — needs a build step, bundler, possibly a separate data-export script |
| Portability (share as a link/demo) | Easy (Streamlit Cloud / simple host) | Easy (any WSGI/ASGI host) | Easy once built, but more deployment surface (static hosting + build pipeline) |
| Visual polish achievable (editorial, restrained, non-generic-dashboard per style constraint) | Low-medium — fighting Streamlit's default widget chrome to avoid a "generic dashboard" look takes real effort | Medium — full CSS control via Dash HTML/CSS, achievable with discipline | Highest — no default framework chrome to fight |
| Fit for research/demo audience at this stage (not yet a scaled product) | Good fit if polish requirement were lower | **Best overall fit** given all constraints together | Would be the right choice for a later, scaled-up phase |

## 3. Recommendation

**Dash.** It is the only option that scores acceptably on every hard
constraint simultaneously: it stays in the same Python/CSV stack as the
locked Phase 0–3 pipeline (no data-export or API layer to keep in sync, so
there is zero risk of the visual layer silently drifting from the immutable
CSVs); its callback model supports the map-stays-open, panel-updates-in-
place interaction pattern the spec requires, which Streamlit's rerun model
does not do cleanly; and it gives enough CSS control to avoid a stock
"Power BI" look with disciplined component styling, which Streamlit's
default widget chrome resists.

Map layer: `dash-leaflet` or Plotly's `scattermapbox`/`scattermap`, either
sufficient for point markers with custom styling (color/ring/glyph) — full
MapLibre-level polish is not required for a research/demo prototype at this
scope, and Dash does not block adopting MapLibre later if the map layer
turns out to be the limiting factor.

**When to revisit this recommendation:** if Phase 5+ turns this into a
public-facing, high-traffic, or tourist-facing product, re-run this
comparison — the custom React/MapLibre column wins decisively once visual
polish and interaction fidelity outweigh reproducibility/simplicity, which
is not yet the case for a professional research/demo prototype per the
Phase 4.0 brief's audience definition.

**Streamlit is not recommended** for this specific design, not in general —
its weakness is specifically the persistent-panel-plus-map interaction
pattern this spec requires, not Streamlit as a tool.

## 4. What this recommendation does not authorize

No Dash installation, scaffolding, or code in Phase 4.0. This document
exists so that when implementation is chartered, the framework decision is
already made and justified against this project's actual constraints rather
than decided ad hoc at build time.
