"""Deterministic smoke test: the Dash app imports and constructs its layout,
and each of the three views builds without error.
"""
from __future__ import annotations

from dash import html

from app import constants as C


def test_app_imports_and_builds_layout():
    from app.app import app
    layout = app.layout() if callable(app.layout) else app.layout
    assert isinstance(layout, html.Div)


def test_three_views_build():
    from app.components import asset_panel, map_view, tradeoff
    # View 1
    for ts in C.TIMESTAMPS:
        assert len(map_view.build_markers(ts)) == 27
    # View 2
    assert isinstance(asset_panel.asset_panel("A01", "12:00"), html.Div)
    assert isinstance(asset_panel.asset_panel("A24", "18:00"), html.Div)
    # View 3 (normal + S8 + baseline on)
    assert isinstance(tradeoff.tradeoff_view("S1"), html.Div)
    assert isinstance(tradeoff.tradeoff_view("S8"), html.Div)
    assert isinstance(tradeoff.tradeoff_view("S1", "indoor_outdoor", True), html.Div)


def test_callbacks_registered():
    """The router + render callbacks are wired (interface-state only)."""
    from app.app import app
    # at least the router and the 4 render callbacks
    assert len(app.callback_map) >= 5
