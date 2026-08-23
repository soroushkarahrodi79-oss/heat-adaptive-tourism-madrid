"""Map legend: a compact always-visible core plus a full symbol explanation.

Phase 4.0 IA §2 requires the legend to be visible rather than hidden in a
drawer, because four concepts are simultaneously encoded on the map. Phase
4.2 keeps that requirement and shrinks the footprint: the two decision
colours and the fact that ring and glyph are *separate* channels stay on
screen at all times; the complete encoding is one click away.
"""
from __future__ import annotations

import dash_mantine_components as dmc
from dash import html

from .. import constants as C
from .icons import icon


def _swatch(color: str, label: str):
    return html.Div(
        [html.Span(className="legend__swatch", style={"background": color},
                   **{"aria-hidden": "true"}),
         html.Span(label, className="legend__label")],
        className="legend__row",
    )


def _ring(style: str, label: str):
    return html.Div(
        [html.Span(className=f"legend__ring legend__ring--{style}",
                   **{"aria-hidden": "true"}),
         html.Span(label, className="legend__label")],
        className="legend__row",
    )


def _glyph(glyph: str, label: str):
    return html.Div(
        [html.Span(glyph, className="legend__glyph", **{"aria-hidden": "true"}),
         html.Span(label, className="legend__label")],
        className="legend__row",
    )


# ── Full explanation (popover body) ────────────────────────────────────────
def symbols_body():
    channel_rows = [
        html.Div(
            [html.Span(name, className="legend__chan-name"),
             html.Span(meaning, className="legend__chan-meaning"),
             html.Code(field, className="token-pill")],
            className="legend__chan",
        )
        for name, meaning, field in C.LEGEND_CHANNELS
    ]
    return html.Div(
        [
            html.Div(C.LEGEND_TITLE, className="legend__title"),
            html.P(C.LEGEND_INTRO, className="legend__intro"),
            html.Div(channel_rows, className="legend__chans"),
            dmc.Divider(className="legend__divider"),

            html.Div("Fill colour · decision", className="legend__group"),
            _swatch(C.DECISION_STATE_COLOR["AVOID_PROLONGED_OUTDOOR_EXPOSURE"],
                    C.DECISION_STATE_LABEL["AVOID_PROLONGED_OUTDOOR_EXPOSURE"]),
            _swatch(C.DECISION_STATE_COLOR["INDOOR_REFUGE"],
                    C.DECISION_STATE_LABEL["INDOOR_REFUGE"]),

            html.Div("Ring style · decision confidence", className="legend__group"),
            _ring("solid", "Robust — held under every tested variation"),
            _ring("dashed", "Boundary — close to a threshold"),
            _ring("dotted", "Unstable — changed under tested variation"),
            _ring("none", "Indoor bypass — confidence does not apply"),
            html.P(C.CONFIDENCE_NOT_SEVERITY_NOTE, className="legend__caveat"),

            html.Div("Inner glyph · thermal condition", className="legend__group"),
            _glyph(C.THERMAL_STATE_GLYPH["VERY_STRONG_HEAT_STRESS"],
                   C.THERMAL_STATE_LABEL["VERY_STRONG_HEAT_STRESS"]),
            _glyph(C.THERMAL_STATE_GLYPH["INDOOR_NOT_MODELLED"],
                   C.THERMAL_STATE_LABEL["INDOOR_NOT_MODELLED"]),

            html.Div("Dimming · availability", className="legend__group"),
            html.Div(
                [html.Span(className="legend__dim-example",
                           **{"aria-hidden": "true"}),
                 html.Span("Dimmed — closed at this timestamp",
                           className="legend__label")],
                className="legend__row",
            ),

            html.Div("Interface state", className="legend__group"),
            html.Div(
                [html.Span(className="legend__halo-example",
                           **{"aria-hidden": "true"}),
                 html.Span(C.LEGEND_SELECTION_NOTE, className="legend__label")],
                className="legend__row",
            ),

            dmc.Divider(className="legend__divider"),
            html.P(C.LEGEND_TIER1, className="legend__tier1"),
        ],
        className="legend-full",
    )


# ── Compact legend + its disclosure trigger ────────────────────────────────
def compact_legend():
    """The always-visible core, plus one control that opens the full encoding.

    The trigger opens the same modal the command bar's Symbols button opens.
    A Popover was tried first and rejected: Mantine sets its dropdown's
    z-index inline at 300, which is inside Leaflet's own 400-1000 pane range,
    so the panel rendered underneath the map. One disclosure surface also
    means one focus-and-Escape behaviour to get right instead of two.
    """
    trigger = dmc.UnstyledButton(
        [html.Span(C.LEGEND_OPEN_LABEL, className="legend__more-text"),
         icon("chevron-right", 14)],
        id="legend-open",
        n_clicks=0,
        className="legend__more",
        **{"aria-label": C.LEGEND_TITLE},
    )
    body = html.Div(
        [
            html.Div(
                [_swatch(C.DECISION_STATE_COLOR["AVOID_PROLONGED_OUTDOOR_EXPOSURE"],
                         "Avoid outdoor"),
                 _swatch(C.DECISION_STATE_COLOR["INDOOR_REFUGE"],
                         "Indoor refuge")],
                className="legend__compact-row",
            ),
            html.Div(
                [html.Span(className="legend__ring legend__ring--solid",
                           **{"aria-hidden": "true"}),
                 html.Span(className="legend__ring legend__ring--dashed",
                           **{"aria-hidden": "true"}),
                 html.Span(className="legend__ring legend__ring--dotted",
                           **{"aria-hidden": "true"}),
                 html.Span("ring = decision confidence",
                           className="legend__label")],
                className="legend__compact-row",
            ),
            html.Div(
                [html.Span(C.THERMAL_STATE_GLYPH["VERY_STRONG_HEAT_STRESS"],
                           className="legend__glyph", **{"aria-hidden": "true"}),
                 html.Span(C.THERMAL_STATE_GLYPH["INDOOR_NOT_MODELLED"],
                           className="legend__glyph", **{"aria-hidden": "true"}),
                 html.Span("glyph = thermal condition",
                           className="legend__label")],
                className="legend__compact-row",
            ),
        ],
        className="legend__compact-body",
    )
    return html.Div([body, trigger], className="legend legend--compact")


def map_hint():
    """Shown only while no asset is selected (visibility is CSS-driven)."""
    return html.Div(
        [icon("map-pin", 14), html.Span(C.MAP_HINT_NO_SELECTION)],
        id="map-hint", className="map-hint",
    )


def tile_fallback_notice():
    """Degradation notice for an unreachable basemap.

    Hidden unless the clientside tile watcher sets ``data-tiles="failed"`` on
    the map surface. The screening results are computed locally and stay
    correct whether or not tiles load, and the copy says exactly that.
    """
    return html.Div(
        [icon("layers", 14), html.Span(C.MAP_TILE_FALLBACK)],
        id="tile-fallback", className="tile-fallback",
        role="status",
    )
