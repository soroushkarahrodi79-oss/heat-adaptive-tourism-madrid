"""The command bar — the single piece of permanent chrome.

Replaces the Phase 4.1 header + scenario-chip row + Tier-1 strip + footer
(265 px of permanent chrome at every desktop width) with one bar, so the
spatial canvas keeps the fold.

Contents, left to right:
  identity  ·  timestamp segmented control  ·  asset picker  ·
  scenario menu  ·  symbols  ·  limitations

The "not live or forecast" caption sits directly under the timestamp control
and is permanent: it is the single most important framing claim in the
interface and may never move into a disclosure.
"""
from __future__ import annotations

import dash_mantine_components as dmc
from dash import html

from .. import constants as C
from .. import data_loader as dl
from .icons import icon
from .limitations import limitations_button
from .scenario_selector import scenario_menu


def _identity():
    return html.Div(
        [
            html.Div(
                [html.Span(className="brand__mark", **{"aria-hidden": "true"}),
                 html.Span(C.PRODUCT_NAME, className="brand__title")],
                className="brand__line",
            ),
            html.Span(C.PRODUCT_TAGLINE, className="brand__tagline"),
            html.Span(f"{C.PILOT_LABEL} · {C.STUDY_DATE_HUMAN}",
                      className="brand__pilot"),
        ],
        className="brand",
    )


def timestamp_control(selected: str):
    return html.Div(
        [
            dmc.SegmentedControl(
                id="timestamp-control",
                value=selected,
                data=[{"value": ts, "label": ts} for ts in C.TIMESTAMPS],
                radius="md",
                size="sm",
                className="ts-segmented",
            ),
            html.Span(C.NOT_LIVE_CAPTION, className="ts-caption"),
        ],
        className="ts-block",
        role="group",
        **{"aria-label": C.ARIA_TIMESTAMP_GROUP},
    )


def asset_picker(timestamp: str, selected: str | None = None):
    """A searchable list of all 27 assets.

    This is the conventional keyboard path to selection. Map markers are
    focusable too, but a combobox is what a keyboard or screen-reader user
    will reach for, and it covers every asset at every timestamp.
    """
    return dmc.Select(
        id="asset-picker",
        data=dl.asset_options(timestamp),
        value=selected,
        placeholder=C.ASSET_PICKER_PLACEHOLDER,
        searchable=True,
        clearable=True,
        nothingFoundMessage="No asset matches that name.",
        leftSection=icon("search", 15),
        comboboxProps={"withinPortal": True, "shadow": "md"},
        size="sm",
        className="asset-picker",
        **{"aria-label": C.ASSET_PICKER_LABEL},
    )


def symbols_button():
    """Secondary entry point to the same symbol explanation the legend opens.

    Kept for narrow viewports, where the compact legend collapses.
    """
    return dmc.Button(
        [icon("help", 15), html.Span("Symbols", className="bar-btn__text")],
        id="symbols-open",
        n_clicks=0,
        variant="default",
        className="bar-btn bar-btn--symbols",
        **{"aria-label": C.LEGEND_TITLE},
    )


def command_bar(timestamp: str, selected_asset: str | None,
                active_scenario: str | None):
    return html.Header(
        [
            _identity(),
            html.Div(
                [
                    timestamp_control(timestamp),
                    html.Div(
                        [
                            asset_picker(timestamp, selected_asset),
                            scenario_menu(active_scenario),
                            symbols_button(),
                            limitations_button(),
                        ],
                        className="bar-actions",
                    ),
                ],
                className="bar-controls",
            ),
        ],
        className="command-bar",
        role="banner",
        **{"aria-label": C.ARIA_COMMAND_BAR},
    )
