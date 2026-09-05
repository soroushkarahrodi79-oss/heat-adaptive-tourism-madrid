"""Deliberate empty / unavailable states.

`NO_DEFENSIBLE_ALTERNATIVE` is the important one: it is a legitimate
scientific result, not an error, not a failed search and not something to
retry. It gets a designed result page, in this order:

    verdict → tally → why candidates were excluded → reach sensitivity

No control in this module widens, relaxes or re-runs anything. The reach
sensitivity table is descriptive evidence recorded in Phase 3, presented as
read-only text.
"""
from __future__ import annotations

import pandas as pd
from dash import html

from .. import constants as C
from .. import data_loader as dl
from .icons import icon
from .primitives import count_bar, note, section_label


def no_defensible_panel(scenario: dict, excluded: pd.DataFrame):
    scenario_id = str(scenario["scenario"])
    n_eval = len(excluded)
    radius = int(scenario["access_radius_m"])
    breakdown = dl.exclusion_breakdown(scenario_id)

    bars = [
        count_bar(C.EXCLUSION_TRANSLATIONS.get(token, token), n, n_eval,
                  token=token)
        for token, n in breakdown
    ]

    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [icon("no-result", 17), html.Span(C.NODEF_KICKER)],
                        className="nodef__kicker",
                    ),
                    html.H2(C.NODEF_HEADLINE, className="nodef__headline"),
                    html.P(C.NODEF_SUBLINE, className="nodef__subline"),
                    html.Div(
                        [
                            html.Div(
                                [html.Span(str(n_eval), className="nodef__num tabular"),
                                 html.Span(f"candidates evaluated; {radius} m reach constraint",
                                           className="nodef__num-label")],
                                className="nodef__stat",
                            ),
                            html.Div(
                                [html.Span("0", className="nodef__num tabular"),
                                 html.Span("survived all gates",
                                           className="nodef__num-label")],
                                className="nodef__stat",
                            ),
                        ],
                        className="nodef__stats",
                    ),
                    html.P(C.NODEF_METHOD, className="nodef__method"),
                ],
                className="nodef__verdict",
            ),
            html.Div(
                [
                    section_label(C.NODEF_BREAKDOWN_TITLE),
                    html.Div(bars, className="nodef__bars"),
                    note(C.NODEF_BREAKDOWN_NOTE, className="note--quiet"),
                ],
                className="nodef__breakdown",
            ),
        ],
        className="nodef-panel",
    )


def unavailable(text: str, *, className: str = ""):
    return html.Div(
        [icon("info", 14, className="note__icon"), html.Span(text)],
        className=f"state-unavailable {className}".strip(),
    )
