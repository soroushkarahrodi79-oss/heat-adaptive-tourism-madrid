"""Shared visual primitives.

ConfidenceRingGlyph is the single shape/ring vocabulary shared by the map
marker and the asset panel, so map and panel speak one confidence language
(PHASE4_0_COMPONENT_INVENTORY.md → shared primitives).
"""
from __future__ import annotations

import pandas as pd
from dash import html

from .. import constants as C


def _is_blank(v) -> bool:
    return v is None or (isinstance(v, float) and pd.isna(v)) or str(v).strip() == ""


# ── Marker HTML (for dash-leaflet DivMarker iconOptions.html) ──────────────
def marker_html(record: dict) -> str:
    """Build the inner HTML for one asset marker.

    Combines four independent channels:
      fill colour      <- decision_state
      ring style       <- decision_confidence
      interior glyph   <- thermal_state
      dim (opacity)    <- is_open (closed => dimmed)
    """
    decision = str(record.get("decision_state", ""))
    confidence = str(record.get("decision_confidence", ""))
    thermal = str(record.get("thermal_state", ""))
    is_open = bool(record.get("is_open", True))

    fill = C.DECISION_STATE_COLOR.get(decision, "#8A8A8A")
    ring = C.CONFIDENCE_RING.get(confidence, "none")
    glyph = C.THERMAL_STATE_GLYPH.get(thermal, "·")
    dim_cls = "" if is_open else " asset-marker--closed"

    # Ring style is expressed with the same CSS the panel glyph uses.
    return (
        f'<div class="asset-marker asset-marker--ring-{ring}{dim_cls}" '
        f'style="--fill:{fill};">'
        f'<span class="asset-marker__glyph">{glyph}</span>'
        f'</div>'
    )


# ── Confidence ring glyph as a Dash component (panel / legend) ─────────────
def confidence_ring_glyph(decision_state: str, decision_confidence: str,
                          thermal_state: str, is_open: bool = True,
                          size: int = 34):
    fill = C.DECISION_STATE_COLOR.get(str(decision_state), "#8A8A8A")
    ring = C.CONFIDENCE_RING.get(str(decision_confidence), "none")
    glyph = C.THERMAL_STATE_GLYPH.get(str(thermal_state), "·")
    cls = f"asset-marker asset-marker--ring-{ring}"
    if not is_open:
        cls += " asset-marker--closed"
    return html.Div(
        html.Span(glyph, className="asset-marker__glyph"),
        className=cls,
        style={"--fill": fill, "width": f"{size}px", "height": f"{size}px"},
    )


# ── Machine-token pill (monospace, always shown next to any raw token) ──────
def exclusion_token_pill(token: str):
    return html.Code(token, className="token-pill")


# ── Small label/value row primitive ────────────────────────────────────────
def field_row(label: str, value, *, mono: bool = False, className: str = ""):
    value_cls = "field-row__value" + (" mono" if mono else "")
    return html.Div(
        [
            html.Span(label, className="field-row__label"),
            html.Span(value, className=value_cls),
        ],
        className=f"field-row {className}".strip(),
    )


# ── Exclusion explainer (token + always-visible translation + expand) ──────
def exclusion_explainer(token: str, detail_lines: list[str] | None = None,
                        expanded: bool = False):
    """Collapsed: monospace pill + one-line plain translation (always shown).
    Expanded (``details`` open): the same translation plus source-row values.
    """
    if _is_blank(token):
        return None
    translation = C.EXCLUSION_TRANSLATIONS.get(str(token), str(token))
    summary = html.Summary(
        [
            exclusion_token_pill(str(token)),
            html.Span(translation, className="exclusion__translation"),
        ],
        className="exclusion__summary",
    )
    children = [summary]
    if detail_lines:
        children.append(
            html.Div(
                [html.Div(line, className="exclusion__detail-line")
                 for line in detail_lines],
                className="exclusion__detail",
            )
        )
    return html.Details(children, open=expanded, className="exclusion")
