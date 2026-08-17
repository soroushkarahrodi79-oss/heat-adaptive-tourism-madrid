"""App shell: header, temporal selector, scenario jump chips, and the
two-tier limitations disclosure. These frame all three views.
"""
from __future__ import annotations

from dash import html

from .. import constants as C
from .. import data_loader as dl
from .primitives import confidence_ring_glyph


# ── Temporal control (3 fixed positions, never a slider) ───────────────────
def scenario_time_selector(selected: str):
    buttons = [
        html.Button(
            ts,
            id={"type": "ts-btn", "index": ts},
            n_clicks=0,
            className="ts-btn" + (" ts-btn--active" if ts == selected else ""),
        )
        for ts in C.TIMESTAMPS
    ]
    return html.Div(
        [
            html.Div(
                [
                    html.Span("Scenario timestamp", className="ts-label"),
                    html.Div(buttons, className="ts-group", role="group"),
                    html.Span(C.STUDY_DATE, className="ts-date"),
                ],
                className="ts-row",
            ),
            # "not live" caption — always visible beneath the control.
            html.Div(C.NOT_LIVE_CAPTION, className="ts-caption"),
        ],
        className="ts-selector",
    )


# ── Scenario jump chips S1..S8 (shortcuts, not a 4th view) ──────────────────
def scenario_jump_chips():
    chips = []
    for _, r in dl.all_scenarios().iterrows():
        label = f"{r['scenario']} · {r['source_name']} · {r['timestamp']}"
        chips.append(
            html.Button(
                label,
                id={"type": "jump-chip", "index": r["scenario"]},
                n_clicks=0,
                className="jump-chip",
                title=str(r.get("scenario_desc", "")),
            )
        )
    return html.Div(
        [html.Span("Jump to scenario", className="chips-label"),
         html.Div(chips, className="chips-row")],
        className="jump-chips",
    )


# ── Tier-1 limitations strip (always visible, context-sensitive) ───────────
def limitations_strip(context: str = "map"):
    text = C.TIER1_LIMITATIONS.get(context, C.TIER1_LIMITATIONS["map"])
    return html.Div(
        [html.Span("Limitation", className="limstrip__tag"),
         html.Span(text, className="limstrip__text")],
        id="limitations-strip",
        className="limstrip",
    )


# ── Tier-2 limitations drawer (one click, never leaves the interface) ──────
def limitations_drawer():
    items = [html.Li(t) for t in C.TIER2_LIMITATIONS]
    return html.Details(
        [
            html.Summary("Permanent limitations", className="limdrawer__summary"),
            html.Div(
                [
                    html.P("These constraints are permanent properties of the "
                           "method and hold for every view and every asset:",
                           className="limdrawer__intro"),
                    html.Ol(items, className="limdrawer__list"),
                    html.P(C.TIER2_SOURCE_NOTE, className="limdrawer__source"),
                ],
                className="limdrawer__body",
            ),
        ],
        className="limdrawer",
    )


# ── Always-visible map legend (3 simultaneous channels) ────────────────────
def map_legend():
    def swatch(color, label):
        return html.Div(
            [html.Span(className="legend__swatch",
                       style={"background": color}),
             html.Span(label, className="legend__label")],
            className="legend__row",
        )

    def ring_example(style, label):
        return html.Div(
            [html.Span(className=f"legend__ring legend__ring--{style}"),
             html.Span(label, className="legend__label")],
            className="legend__row",
        )

    def glyph_example(glyph, label):
        return html.Div(
            [html.Span(glyph, className="legend__glyph"),
             html.Span(label, className="legend__label")],
            className="legend__row",
        )

    return html.Div(
        [
            html.Div("Legend", className="legend__title"),
            html.Div("Decision", className="legend__group"),
            swatch(C.DECISION_STATE_COLOR["AVOID_PROLONGED_OUTDOOR_EXPOSURE"],
                   "Avoid prolonged outdoor exposure"),
            swatch(C.DECISION_STATE_COLOR["INDOOR_REFUGE"], "Indoor refuge"),
            html.Div("Decision confidence", className="legend__group"),
            ring_example("solid", "Robust"),
            ring_example("dashed", "Boundary"),
            ring_example("dotted", "Unstable"),
            ring_example("none", "Indoor bypass (n/a)"),
            html.Div("Thermal state", className="legend__group"),
            glyph_example(C.THERMAL_STATE_GLYPH["VERY_STRONG_HEAT_STRESS"],
                          "Very strong heat stress (modelled)"),
            glyph_example(C.THERMAL_STATE_GLYPH["INDOOR_NOT_MODELLED"],
                          "Indoor — not modelled"),
            html.Div("Availability", className="legend__group"),
            html.Div([html.Span(className="legend__dim-example"),
                      html.Span("Dimmed = closed at this timestamp",
                                className="legend__label")],
                     className="legend__row"),
        ],
        className="legend",
    )
