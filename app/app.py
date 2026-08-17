"""HATI-Madrid — Phase 4.1 Visual Decision-Support MVP (Dash entrypoint).

A read-only presentation layer over the locked Phase 3 outputs. State is
interface-only (selected timestamp / asset / scenario / view / sort /
baseline). No scientific result table is ever recomputed or stored.

Run:  .venv_app/Scripts/python -m app.app     (from repo root)
"""
from __future__ import annotations

import dash
from dash import ALL, Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate

from . import constants as C
from . import data_loader as dl
from .components import asset_panel as ap
from .components import map_view as mv
from .components import shell
from .components import tradeoff as tv

app = dash.Dash(
    __name__,
    title="HATI-Madrid — Heat-Adaptive Tourism screening (Madrid pilot)",
    suppress_callback_exceptions=True,
    update_title=None,
)
server = app.server

DEFAULT_TIMESTAMP = "12:00"


def _layout():
    return html.Div(
        [
            # ── interface-only state (never scientific result tables) ──
            dcc.Store(id="store-timestamp", data=DEFAULT_TIMESTAMP),
            dcc.Store(id="store-selected-asset", data=None),
            dcc.Store(id="store-view", data=C.VIEW_MAP),
            dcc.Store(id="store-scenario", data=None),
            dcc.Store(id="store-sort", data="distance"),
            dcc.Store(id="store-baseline", data=False),

            # ── header ──
            html.Header(
                [
                    html.Div(
                        [
                            html.H1("HATI-Madrid", className="brand__title"),
                            html.Span("Heat-Adaptive Tourism screening · "
                                      "Prado–Retiro–Atocha pilot",
                                      className="brand__subtitle"),
                        ],
                        className="brand",
                    ),
                    shell.scenario_time_selector(DEFAULT_TIMESTAMP),
                ],
                className="app-header",
            ),
            shell.scenario_jump_chips(),
            shell.limitations_strip("map"),

            # ── main: map (View 1) + side panel (View 2/3) ──
            html.Main(
                [
                    html.Div(
                        [mv.map_canvas(DEFAULT_TIMESTAMP), shell.map_legend()],
                        className="map-wrap",
                    ),
                    html.Aside([], id="side-panel", className="side-panel side-panel--empty"),
                ],
                className="app-main",
            ),

            # ── Tier-2 limitations drawer (always available) ──
            html.Footer(shell.limitations_drawer(), className="app-footer"),
        ],
        className="app-root",
    )


app.layout = _layout


# ── Central router: interface state only ───────────────────────────────────
@app.callback(
    Output("store-timestamp", "data"),
    Output("store-selected-asset", "data"),
    Output("store-view", "data"),
    Output("store-scenario", "data"),
    Output("store-sort", "data"),
    Output("store-baseline", "data"),
    Input({"type": "ts-btn", "index": ALL}, "n_clicks"),
    Input({"type": "asset-marker", "index": ALL}, "n_clicks"),
    Input({"type": "jump-chip", "index": ALL}, "n_clicks"),
    Input({"type": "sort-btn", "index": ALL}, "n_clicks"),
    Input({"type": "card-open-asset", "index": ALL}, "n_clicks"),
    Input({"type": "open-alt", "index": ALL}, "n_clicks"),
    Input({"type": "close-panel", "index": ALL}, "n_clicks"),
    Input({"type": "back-asset", "index": ALL}, "n_clicks"),
    Input({"type": "baseline-toggle", "index": ALL}, "n_clicks"),
    State("store-timestamp", "data"),
    State("store-selected-asset", "data"),
    State("store-view", "data"),
    State("store-scenario", "data"),
    State("store-sort", "data"),
    State("store-baseline", "data"),
    prevent_initial_call=True,
)
def _router(_ts, _mk, _chip, _sort, _card, _alt, _close, _back, _base,
            timestamp, asset, view, scenario, sort, baseline):
    trig = dash.callback_context.triggered_id
    if trig is None:
        raise PreventUpdate

    def _clicked(n):
        return n is not None and n > 0

    if not isinstance(trig, dict):
        raise PreventUpdate
    kind = trig.get("type")

    if kind == "ts-btn":
        timestamp = trig["index"]
        # keep panel open + update in place; a timestamp change invalidates a
        # pre-computed scenario, so step back from View 3 to View 2.
        if view == C.VIEW_ALTERNATIVES:
            view = C.VIEW_ASSET
    elif kind == "asset-marker":
        if not any(_clicked(n) for n in _mk):      # ignore initial n_clicks=0
            raise PreventUpdate
        asset = trig["index"]
        view = C.VIEW_ASSET
    elif kind == "jump-chip":
        if not any(_clicked(n) for n in _chip):
            raise PreventUpdate
        row = dl.summary_row(trig["index"])
        if row is None:
            raise PreventUpdate
        timestamp = row["timestamp"]
        asset = row["source_id"]
        scenario = trig["index"]
        view = C.VIEW_ASSET
        sort, baseline = "distance", False
    elif kind == "sort-btn":
        if not any(_clicked(n) for n in _sort):
            raise PreventUpdate
        sort = trig["index"]
    elif kind == "card-open-asset":
        if not any(_clicked(n) for n in _card):
            raise PreventUpdate
        asset = trig["index"]
        view = C.VIEW_ASSET
    elif kind == "open-alt":
        if not any(_clicked(n) for n in _alt):
            raise PreventUpdate
        scn = dl.scenario_for_source(asset, timestamp)
        if scn is None:
            raise PreventUpdate
        scenario = scn["scenario"]
        view = C.VIEW_ALTERNATIVES
        sort, baseline = "distance", False
    elif kind == "close-panel":
        if not any(_clicked(n) for n in _close):
            raise PreventUpdate
        view, asset = C.VIEW_MAP, None
    elif kind == "back-asset":
        if not any(_clicked(n) for n in _back):
            raise PreventUpdate
        view = C.VIEW_ASSET
    elif kind == "baseline-toggle":
        if not any(_clicked(n) for n in _base):
            raise PreventUpdate
        baseline = not bool(baseline)
    else:
        raise PreventUpdate

    return timestamp, asset, view, scenario, sort, baseline


# ── Render: markers (rebuild on timestamp; map container untouched) ────────
@app.callback(Output("asset-markers", "children"),
              Input("store-timestamp", "data"))
def _render_markers(timestamp):
    return mv.build_markers(timestamp or DEFAULT_TIMESTAMP)


# ── Render: timestamp button active state ──────────────────────────────────
@app.callback(Output({"type": "ts-btn", "index": ALL}, "className"),
              Input("store-timestamp", "data"))
def _render_ts_buttons(timestamp):
    return ["ts-btn ts-btn--active" if t == timestamp else "ts-btn"
            for t in C.TIMESTAMPS]


# ── Render: side panel (View 2 / View 3) + width class ─────────────────────
@app.callback(
    Output("side-panel", "children"),
    Output("side-panel", "className"),
    Input("store-view", "data"),
    Input("store-selected-asset", "data"),
    Input("store-timestamp", "data"),
    Input("store-scenario", "data"),
    Input("store-sort", "data"),
    Input("store-baseline", "data"),
)
def _render_side_panel(view, asset, timestamp, scenario, sort, baseline):
    if view == C.VIEW_ASSET and asset:
        return ap.asset_panel(asset, timestamp), "side-panel side-panel--open"
    if view == C.VIEW_ALTERNATIVES and scenario:
        return (tv.tradeoff_view(scenario, sort or "distance", bool(baseline)),
                "side-panel side-panel--open side-panel--wide")
    return [], "side-panel side-panel--empty"


# ── Render: Tier-1 limitations strip context ───────────────────────────────
@app.callback(Output("limitations-strip", "children"),
              Input("store-view", "data"))
def _render_limstrip(view):
    ctx = {C.VIEW_MAP: "map", C.VIEW_ASSET: "asset",
           C.VIEW_ALTERNATIVES: "alternatives"}.get(view, "map")
    text = C.TIER1_LIMITATIONS[ctx]
    return [html.Span("Limitation", className="limstrip__tag"),
            html.Span(text, className="limstrip__text")]


if __name__ == "__main__":
    app.run(debug=False, port=8050)
