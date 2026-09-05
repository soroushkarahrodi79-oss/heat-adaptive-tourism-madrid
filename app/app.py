"""HATI-Madrid — Spatial Decision Cockpit (Dash entrypoint).

A read-only presentation layer over the locked Phase 3 outputs. State is
interface-only (selected timestamp / asset / scenario / view / sort /
baseline). No scientific result table is ever recomputed or stored, and no
callback in this module performs arithmetic on a scientific value.

Run:  .venv_app/bin/python -m app.app          (from the repo root)
"""
from __future__ import annotations

import dash
import dash_mantine_components as dmc
from dash import ALL, Input, Output, State, clientside_callback, dcc, html
from dash.exceptions import PreventUpdate

from . import constants as C
from . import data_loader as dl
from . import theme as T
from .components import asset_panel as ap
from .components import map_view as mv
from .components import shell
from .components import tradeoff as tv
from .components import replay
from .replay_contract import IntegrityError
from .replay_state import normalize, transition

app = dash.Dash(
    __name__,
    title="HATI-Madrid — Heat-Adaptive Tourism screening (Madrid pilot)",
    suppress_callback_exceptions=True,
    update_title=None,
)
server = app.server

# The token layer is injected here rather than duplicated in the stylesheet:
# `theme.py` is the single definition of every colour, space, radius, shadow
# and duration, and both the CSS and the Python components read it.
app.index_string = """<!DOCTYPE html>
<html lang="en">
  <head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <style>__HATI_TOKENS__</style>
  </head>
  <body>
    <a class="skip-link" href="#map-surface">Skip to the map</a>
    {%app_entry%}
    <footer>{%config%}{%scripts%}{%renderer%}</footer>
  </body>
</html>""".replace("__HATI_TOKENS__", T.css_variables())

DEFAULT_TIMESTAMP = "12:00"
DEFAULT_SORT = "name"


def _layout():
    try:
        dl._load_all()
    except IntegrityError as exc:
        return html.Div([
            html.H1("Replay integrity error"), html.P(str(exc)),
            html.P("Scientific display is blocked. Restore the pinned artifacts and restart the server."),
        ], id="replay-integrity-error", role="alert", className="replay-integrity-error")
    return html.Div(
        [
            # ── interface-only state (never scientific result tables) ──
            dcc.Store(id="store-timestamp", data=DEFAULT_TIMESTAMP),
            dcc.Store(id="store-selected-asset", data=None),
            dcc.Store(id="store-view", data=C.VIEW_MAP),
            dcc.Store(id="store-scenario", data=None),
            dcc.Store(id="store-sort", data=DEFAULT_SORT),
            dcc.Store(id="store-baseline", data=False),

            dmc.MantineProvider(
                shell.page(DEFAULT_TIMESTAMP),
                theme=T.mantine_theme(),
                forceColorScheme="light",
            ),
        ],
        className="app-root",
    )


app.layout = _layout


# ═══════════════════════════════════════════════════════════════════════════
# Router — interface state only.
# Every branch either copies a locked value into a store or flips a view
# flag. Nothing here derives a scientific value.
# ═══════════════════════════════════════════════════════════════════════════
def _any_click(values) -> bool:
    """Pattern-matching inputs fire once at registration with n_clicks=0."""
    return any(v for v in (values or []) if v)


@app.callback(
    Output("store-timestamp", "data"),
    Output("store-selected-asset", "data"),
    Output("store-view", "data"),
    Output("store-scenario", "data"),
    Output("store-sort", "data"),
    Output("store-baseline", "data"),
    Input("timestamp-control", "value"),
    Input("asset-picker", "value"),
    Input({"type": "asset-marker", "index": ALL}, "n_clicks"),
    Input({"type": "scenario-item", "index": ALL}, "n_clicks"),
    Input({"type": "sort-select", "index": ALL}, "value"),
    Input({"type": "card-open-asset", "index": ALL}, "n_clicks"),
    Input({"type": "open-alt", "index": ALL}, "n_clicks"),
    Input({"type": "close-panel", "index": ALL}, "n_clicks"),
    Input({"type": "back-asset", "index": ALL}, "n_clicks"),
    Input({"type": "baseline-toggle", "index": ALL}, "checked"),
    State("store-timestamp", "data"),
    State("store-selected-asset", "data"),
    State("store-view", "data"),
    State("store-scenario", "data"),
    State("store-sort", "data"),
    State("store-baseline", "data"),
    prevent_initial_call=True,
)
def _router(ts_value, picker_value, marker_clicks, scenario_clicks, sort_values,
            card_clicks, alt_clicks, close_clicks, back_clicks, baseline_checked,
            timestamp, asset, view, scenario, sort, baseline):
    trig = dash.callback_context.triggered_id
    if trig is None:
        raise PreventUpdate

    kind = trig.get("type") if isinstance(trig, dict) else trig
    current = (timestamp, asset, view, scenario, sort, baseline)
    if kind == "timestamp-control":
        if ts_value == timestamp or ts_value not in C.TIMESTAMPS:
            raise PreventUpdate
        return transition(current, "timestamp", ts_value)
    if kind == "asset-picker":
        if picker_value == asset:
            raise PreventUpdate
        return transition(current, "asset", picker_value)
    if kind in ("asset-marker", "card-open-asset", "scenario-item", "back-asset", "close-panel", "open-alt"):
        clicks = {"asset-marker": marker_clicks, "card-open-asset": card_clicks,
                  "scenario-item": scenario_clicks, "back-asset": back_clicks,
                  "close-panel": close_clicks, "open-alt": alt_clicks}[kind]
        if not _any_click(clicks):
            raise PreventUpdate
        if kind == "open-alt":
            row = dl.scenario_for_source(asset, timestamp)
            if row is None:
                raise PreventUpdate
            return transition(current, "scenario", row["scenario"])
        event = {"asset-marker": "asset", "card-open-asset": "asset",
                 "scenario-item": "scenario", "back-asset": "back", "close-panel": "close"}[kind]
        return transition(current, event, trig.get("index"))
    if kind == "sort-select":
        return transition(current, "sort", next((v for v in sort_values if v), None))
    if kind == "baseline-toggle":
        return transition(current, "baseline", next((v for v in baseline_checked if v is not None), False))
    raise PreventUpdate

# ═══════════════════════════════════════════════════════════════════════════
# Render callbacks
# ═══════════════════════════════════════════════════════════════════════════
@app.callback(
    Output("asset-markers", "children"),
    Input("store-timestamp", "data"),
    Input("store-selected-asset", "data"),
    Input("store-scenario", "data"),
)
def _render_markers(timestamp, selected, scenario):
    """Only the LayerGroup children are replaced — the MapContainer, its
    centre and its zoom are never touched, so the spatial frame persists
    across every timestamp change and every selection."""
    return mv.build_markers(timestamp or DEFAULT_TIMESTAMP, selected, scenario)


@app.callback(
    Output("side-panel-body", "children"),
    Output("side-panel", "className"),
    Input("store-view", "data"),
    Input("store-selected-asset", "data"),
    Input("store-timestamp", "data"),
    Input("store-scenario", "data"),
    Input("store-sort", "data"),
    Input("store-baseline", "data"),
)
def _render_side_panel(view, asset, timestamp, scenario, sort, baseline):
    timestamp, asset, view, scenario, sort, baseline = normalize(timestamp, asset, view, scenario, sort, baseline)
    base = "cockpit-panel"
    if scenario:
        return replay.panel(scenario, asset), f"{base} {base}--open {T.PANEL_CLASS_ALTERNATIVES}"
    if view == C.VIEW_ASSET and asset:
        return (html.Div([ap.asset_panel(asset, timestamp), replay.asset_provenance(asset, timestamp)]),
                f"{base} {base}--open {T.PANEL_CLASS_ASSET}")
    return [], f"{base} {base}--closed"


@app.callback(
    Output("asset-picker", "value"),
    Output("asset-picker", "data"),
    Input("store-selected-asset", "data"),
    Input("store-timestamp", "data"),
)
def _sync_asset_picker(asset, timestamp):
    """Keep the keyboard picker in step with map selection, in both
    directions, so the two paths are one selection state."""
    return asset, dl.asset_options(timestamp or DEFAULT_TIMESTAMP)


@app.callback(
    Output("timestamp-control", "value"),
    Input("store-timestamp", "data"),
)
def _sync_timestamp_control(timestamp):
    """A scenario jump sets the timestamp too, so the control has to follow
    the store or the bar would contradict the panel."""
    return timestamp or DEFAULT_TIMESTAMP


@app.callback(
    Output("scenario-btn-label", "children"),
    Input("store-scenario", "data"),
)
def _render_scenario_label(scenario):
    return scenario or C.SCENARIO_MENU_LABEL


@app.callback(
    Output("replay-context", "children"),
    Input("store-scenario", "data"), Input("store-timestamp", "data"),
)
def _render_replay_context(scenario, timestamp):
    return replay.context(scenario, timestamp)


@app.callback(
    Output("limitations-drawer", "opened"),
    Input("limitations-open", "n_clicks"),
    prevent_initial_call=True,
)
def _open_limitations(n):
    if not n:
        raise PreventUpdate
    return True


@app.callback(
    Output("symbols-modal", "opened"),
    Input("symbols-open", "n_clicks"),
    Input("legend-open", "n_clicks"),
    prevent_initial_call=True,
)
def _open_symbols(from_bar, from_legend):
    """Both the command-bar button and the legend's "Explain map symbols"
    open the one symbol-explanation surface."""
    if not (from_bar or from_legend):
        raise PreventUpdate
    return True


# ── Clientside: keep Leaflet's canvas correct when the panel resizes, and
#    surface a basemap failure without touching any scientific output. ──────
clientside_callback(
    """
    function(cls) {
        const el = document.getElementById('map-canvas');
        if (!el) { return window.dash_clientside.no_update; }
        // Let the CSS width transition finish, then tell Leaflet its
        // container changed. pan:true keeps the map CENTRE fixed (pan:false
        // would pin the top-left corner and shift the study area sideways).
        setTimeout(function () {
            const map = el._leaflet_map ||
                        (window.dash_leaflet && window.dash_leaflet.maps &&
                         window.dash_leaflet.maps['map-canvas']);
            if (map && map.invalidateSize) { map.invalidateSize({pan: true}); }
            else { window.dispatchEvent(new Event('resize')); }
        }, 220);
        return window.dash_clientside.no_update;
    }
    """,
    Output("map-surface", "data-resize"),
    Input("side-panel", "className"),
)

clientside_callback(
    """
    function(n) {
        const surface = document.getElementById('map-surface');
        if (!surface) { return window.dash_clientside.no_update; }
        // Mark the surface once a tile error is seen, so the fallback notice
        // can explain that the science is local and still correct.
        const mark = function () {
            surface.setAttribute('data-tiles', 'failed');
        };
        if (!surface.__hatiTileCapture) {
            surface.__hatiTileCapture = true;
            surface.addEventListener('error', function(e) {
                if (e.target.classList && e.target.classList.contains('leaflet-tile')) mark();
            }, true);
        }
        const attach = function () {
            const imgs = surface.querySelectorAll('.leaflet-tile');
            imgs.forEach(function (img) {
                if (img.complete && !img.naturalWidth) mark();
                if (!img.__hatiWatched) {
                    img.__hatiWatched = true;
                    img.addEventListener('error', mark, {once: true});
                }
            });
        };
        attach();
        setTimeout(attach, 1200);
        setTimeout(attach, 4000);
        return window.dash_clientside.no_update;
    }
    """,
    Output("map-surface", "data-tilewatch"),
    Input("asset-markers", "children"),
)

clientside_callback(
    """
    function(children) {
        const previousFocus = document.activeElement;
        requestAnimationFrame(function() {
            if (document.activeElement !== previousFocus && document.activeElement?.matches('.replay-candidate')) return;
            const heading = document.getElementById('replay-selected-title');
            if (heading) { heading.focus({preventScroll: true}); heading.scrollIntoView({block: 'nearest'}); }
        });
        return window.dash_clientside.no_update;
    }
    """,
    Output("side-panel", "data-selection-focus"),
    Input("side-panel-body", "children"),
    prevent_initial_call=True,
)


if __name__ == "__main__":
    app.run(debug=False, port=8050)
