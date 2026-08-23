"""Limitations disclosure.

Phase 4.1 carried two permanent limitation surfaces: an amber Tier-1 strip
(32–48 px on every view) and a footer disclosure (50 px). Together they took
~80 px of permanent vertical space for text that never changes, and the amber
palette gave scope statements the visual register of a caution banner.

Phase 4.2 keeps both tiers but relocates them:

  Tier 1  — the context-sensitive one-liner is rendered *where it applies*
            (map legend footer, panel thermal block, alternatives note),
            not as a strip.
  Tier 2  — the full permanent list moves into a Drawer reachable in one
            click from the command bar, with Escape to close.

No limitation text was removed, softened or reworded.
"""
from __future__ import annotations

import dash_mantine_components as dmc
from dash import html

from .. import constants as C
from .icons import icon


def limitations_button():
    return dmc.Button(
        [icon("document", 15),
         html.Span(C.LIMITATIONS_LABEL, className="bar-btn__text")],
        id="limitations-open",
        n_clicks=0,
        variant="default",
        className="bar-btn",
        # Kept for the narrow breakpoint, where the text label is hidden.
        **{"aria-label": C.LIMITATIONS_LABEL},
    )


def limitations_drawer():
    items = [
        dmc.ListItem(text, className="limdrawer__item")
        for text in C.TIER2_LIMITATIONS
    ]
    return dmc.Drawer(
        [
            html.P(
                "These constraints are permanent properties of the method. "
                "They hold for every view, every asset and every timestamp.",
                className="limdrawer__intro",
            ),
            dmc.List(items, type="ordered", spacing="sm",
                     className="limdrawer__list"),
            dmc.Divider(className="limdrawer__divider"),
            html.P(C.TIER2_SOURCE_NOTE, className="limdrawer__source"),
        ],
        id="limitations-drawer",
        title="Permanent limitations",
        opened=False,
        position="right",
        size="min(520px, 92vw)",
        padding="lg",
        withCloseButton=True,
        closeOnEscape=True,
        closeOnClickOutside=True,
        lockScroll=False,
        className="limdrawer",
    )


def tier1(context: str, *, className: str = ""):
    """The context-sensitive Tier-1 line, rendered inline where it applies."""
    text = C.TIER1_LIMITATIONS.get(context, C.TIER1_LIMITATIONS["map"])
    return html.Div(
        [icon("info", 13, className="note__icon"), html.Span(text)],
        className=f"note note--tier1 {className}".strip(),
    )
