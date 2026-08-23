"""Compact scenario access (S1–S8).

Phase 4.1 rendered eight permanent chips across the full width above the
map. They are shortcuts into worked examples — a secondary affordance — and
they were consuming 96 px of prime vertical space at every viewport width.
This replaces them with one keyboard-navigable menu that shows more
information per option than the chips did.

Choosing a scenario sets its pre-computed source asset and timestamp.
Nothing is recalculated, and no scenario is ever synthesised for an
(asset, timestamp) pair the pipeline did not run.
"""
from __future__ import annotations

import dash_mantine_components as dmc
from dash import html

from .. import constants as C
from .. import data_loader as dl
from .icons import icon


def _option(opt: dict, active: bool):
    rec = opt["recommendation"]
    if rec == "NO_DEFENSIBLE_ALTERNATIVE":
        outcome = C.RECOMMENDATION_MENU_GLOSS[rec]
        outcome_cls = "scn-item__outcome scn-item__outcome--nodef"
    else:
        n = opt["n_alternatives"]
        outcome = f"{n} {C.RECOMMENDATION_MENU_GLOSS.get(rec, rec.lower())}"
        outcome_cls = "scn-item__outcome"
    return dmc.MenuItem(
        html.Div(
            [
                html.Div(
                    [html.Span(opt["scenario"], className="scn-item__code"),
                     html.Span(opt["source_name"], className="scn-item__name"),
                     html.Span(opt["timestamp"], className="scn-item__ts tabular")],
                    className="scn-item__head",
                ),
                html.Div(
                    [html.Span(outcome, className=outcome_cls),
                     html.Span(f"within {opt['radius_m']} m",
                               className="scn-item__radius tabular")],
                    className="scn-item__meta",
                ),
            ],
            className="scn-item" + (" scn-item--active" if active else ""),
        ),
        id={"type": "scenario-item", "index": opt["scenario"]},
        n_clicks=0,
        className="scn-menuitem",
    )


def scenario_menu(active_scenario: str | None = None):
    opts = dl.scenario_options()
    label = active_scenario or C.SCENARIO_MENU_LABEL
    return dmc.Menu(
        [
            dmc.MenuTarget(
                dmc.Button(
                    [icon("layers", 15),
                     html.Span(label, id="scenario-btn-label",
                               className="bar-btn__text bar-btn__text--scenario"),
                     icon("chevron-down", 14)],
                    id="scenario-menu-btn",
                    variant="default",
                    className="bar-btn bar-btn--menu",
                    **{"aria-label": C.SCENARIO_MENU_TITLE},
                )
            ),
            dmc.MenuDropdown(
                [
                    dmc.MenuLabel(C.SCENARIO_MENU_TITLE),
                    html.P(C.SCENARIO_MENU_NOTE, className="scn-menu__note"),
                    dmc.MenuDivider(),
                    *[_option(o, o["scenario"] == active_scenario) for o in opts],
                ],
                className="scn-menu",
            ),
        ],
        id="scenario-menu",
        position="bottom-end",
        shadow="lg",
        width=320,
        trigger="click",
        closeOnItemClick=True,
    )
