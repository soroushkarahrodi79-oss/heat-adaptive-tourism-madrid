"""App shell.

Phase 4.1 kept the header, timestamp control, scenario chips and both
limitation tiers here. In 4.2 those moved to focused modules
(``command_bar``, ``scenario_selector``, ``limitations``, ``legend``); this
module now assembles them into the page frame and owns the contextual panel
container.
"""
from __future__ import annotations

import dash_mantine_components as dmc
from dash import html

from .. import constants as C
from .. import theme as T
from .command_bar import command_bar
from .legend import compact_legend, symbols_body
from .limitations import limitations_drawer
from .map_view import map_canvas


def symbols_modal():
    """The same symbol explanation the legend popover shows, reachable from
    the command bar. Needed below 700 px, where the compact legend collapses
    to an icon, and useful as a keyboard-first path at any width."""
    return dmc.Modal(
        symbols_body(),
        id="symbols-modal",
        opened=False,
        title=C.LEGEND_TITLE,
        size="lg",
        centered=True,
        closeOnEscape=True,
        className="symbols-modal",
    )


def panel_shell():
    """The contextual panel container.

    Mounted once and never unmounted, so opening and closing it cannot
    disturb the map. Only its children and width class change.
    """
    return html.Aside(
        dmc.ScrollArea(
            html.Div([], id="side-panel-body", className="panel-body"),
            type="hover", scrollbarSize=8, className="panel-scroll",
        ),
        id="side-panel",
        className="cockpit-panel cockpit-panel--closed",
        role="region",
        **{"aria-label": C.ARIA_PANEL_REGION},
    )


def workspace(timestamp: str, selected_asset: str | None = None):
    return html.Main(
        [
            html.Div(
                [map_canvas(timestamp, selected_asset), compact_legend()],
                className="map-wrap",
            ),
            panel_shell(),
        ],
        className="cockpit-main",
        **{"aria-label": C.ARIA_WORKSPACE},
    )


def page(timestamp: str, selected_asset: str | None = None,
         active_scenario: str | None = None):
    return html.Div(
        [
            command_bar(timestamp, selected_asset, active_scenario),
            workspace(timestamp, selected_asset),
            limitations_drawer(),
            symbols_modal(),
        ],
        className="cockpit",
    )
