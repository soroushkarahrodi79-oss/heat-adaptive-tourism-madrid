"""Shared visual primitives.

The confidence ring glyph is the single shape vocabulary shared by the map
marker and every panel, so map and panel speak one confidence language
(PHASE4_0_COMPONENT_INVENTORY.md → shared primitives).

Channel discipline (PHASE4_0_VISUAL_SEMANTICS.md §2), unchanged in 4.2:

    fill colour    <- decision_state
    ring style     <- decision_confidence
    inner glyph    <- thermal_state
    dimming        <- is_open

Phase 4.2 adds one channel that carries no data at all — the selection halo —
drawn outside the marker body in neutral charcoal so it can never be read as
a fifth scientific fact.
"""
from __future__ import annotations

import dash_mantine_components as dmc
import pandas as pd
from dash import html

from .. import constants as C
from .. import theme as T
from .icons import icon


def is_blank(v) -> bool:
    return (v is None
            or (isinstance(v, float) and pd.isna(v))
            or str(v).strip() == "")


# ── Text helpers ───────────────────────────────────────────────────────────
def decision_label(state) -> str:
    return C.DECISION_STATE_LABEL.get(str(state), str(state))


def confidence_label(conf) -> str:
    return C.CONFIDENCE_SHORT.get(str(conf), str(conf))


def thermal_label(state) -> str:
    return C.THERMAL_STATE_LABEL.get(str(state), str(state))


def marker_aria_label(record: dict) -> str:
    """Every marker's accessible name carries all four data channels in
    words, so nothing on the map is available to sighted pointer users only.
    """
    open_txt = (C.ARIA_OPEN_AT if bool(record.get("is_open", True))
                else C.ARIA_CLOSED_AT)
    conf = str(record.get("decision_confidence", ""))
    parts = [
        f"{record.get('asset_id', '')} {record.get('name', '')}.",
        f"Decision: {decision_label(record.get('decision_state'))}.",
        f"Decision confidence: {confidence_label(conf)}.",
        f"Thermal condition: {thermal_label(record.get('thermal_state'))}.",
        f"{open_txt}.",
    ]
    return " ".join(p for p in parts if p.strip())


# ── Marker HTML (for dash-leaflet DivMarker iconOptions.html) ──────────────
def marker_html(record: dict, *, selected: bool = False) -> str:
    """Inner HTML for one asset marker.

    ``selected`` adds a neutral halo and a size step. It is deliberately the
    only visual difference the interface introduces on top of the four locked
    data channels, and it is documented as an interface state in the legend.
    """
    decision = str(record.get("decision_state", ""))
    confidence = str(record.get("decision_confidence", ""))
    thermal = str(record.get("thermal_state", ""))
    is_open = bool(record.get("is_open", True))

    fill = C.DECISION_STATE_COLOR.get(decision, T.DECISION_UNKNOWN)
    ring = C.CONFIDENCE_RING.get(confidence, "none")
    glyph = C.THERMAL_STATE_GLYPH.get(thermal, "·")

    cls = f"asset-marker asset-marker--ring-{ring}"
    if not is_open:
        cls += " asset-marker--closed"
    if selected:
        cls += " asset-marker--selected"

    label = marker_aria_label(record).replace('"', "&quot;")
    return (
        f'<div class="asset-marker-shell{" asset-marker-shell--selected" if selected else ""}" '
        f'role="img" aria-label="{label}">'
        f'<div class="{cls}" style="--fill:{fill};">'
        f'<span class="asset-marker__glyph" aria-hidden="true">{glyph}</span>'
        f'</div></div>'
    )


# ── Confidence ring glyph as a Dash component (panel / legend / cards) ─────
def confidence_ring_glyph(decision_state: str, decision_confidence: str,
                          thermal_state: str, is_open: bool = True,
                          size: int = 28):
    fill = C.DECISION_STATE_COLOR.get(str(decision_state), T.DECISION_UNKNOWN)
    ring = C.CONFIDENCE_RING.get(str(decision_confidence), "none")
    glyph = C.THERMAL_STATE_GLYPH.get(str(thermal_state), "·")
    cls = f"asset-marker asset-marker--ring-{ring} asset-marker--static"
    if not is_open:
        cls += " asset-marker--closed"
    return html.Div(
        html.Span(glyph, className="asset-marker__glyph",
                  **{"aria-hidden": "true"}),
        className=cls,
        style={"--fill": fill, "width": f"{size}px", "height": f"{size}px"},
        **{"aria-hidden": "true"},
    )


# ── Evidence chip — a deliberately different shape from the ring ───────────
def evidence_chip(level: str, size: int = 14):
    """Square, stepped-fill chip. Square vs. circle keeps evidence confidence
    visually separate from decision confidence at a glance."""
    lvl = str(level).lower()
    return html.Span(
        className=f"evidence-chip evidence-chip--{lvl}",
        style={"width": f"{size}px", "height": f"{size}px"},
        **{"aria-hidden": "true"},
    )


# ── Machine-token pill (monospace, always secondary to plain language) ─────
def token_pill(token: str):
    return html.Code(
        str(token), className="token-pill",
        title="Machine-readable token from the locked Phase 3 output",
    )


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


def section_label(text: str, *, className: str = ""):
    return html.Div(text, className=f"section-label {className}".strip())


def note(text, *, className: str = "", with_icon: bool = False):
    children = [icon("info", 13, className="note__icon")] if with_icon else []
    children.append(html.Span(text))
    return html.Div(children, className=f"note {className}".strip())


# ── Exclusion explainer — plain language first, token second ───────────────
def exclusion_explainer(token: str, detail_lines: list[str] | None = None,
                        *, compact: bool = False):
    """Plain-language reason leads; the locked machine token follows as a
    monospace pill; row-level evidence follows that.

    Phase 4.1 put the token first. The reason a destination manager needs is
    the sentence, not the enum.
    """
    if is_blank(token):
        return None
    translation = C.EXCLUSION_TRANSLATIONS.get(str(token), str(token))
    children = [
        html.Div(
            [html.Span(translation, className="exclusion__translation"),
             token_pill(str(token))],
            className="exclusion__head",
        )
    ]
    if detail_lines:
        children.append(
            html.Div([html.Div(line, className="exclusion__detail-line")
                      for line in detail_lines],
                     className="exclusion__detail")
        )
    cls = "exclusion" + (" exclusion--compact" if compact else "")
    return html.Div(children, className=cls)


# ── Disclosure — one Accordion vocabulary for the whole app ────────────────
def disclosure(items: list[tuple[str, object]], *, value=None,
               className: str = "", multiple: bool = False):
    """``items`` = [(label, children), ...]. Closed by default."""
    return dmc.Accordion(
        [
            dmc.AccordionItem(
                [
                    dmc.AccordionControl(label),
                    dmc.AccordionPanel(children),
                ],
                value=f"item-{i}",
            )
            for i, (label, children) in enumerate(items)
        ],
        value=value,
        multiple=multiple,
        chevronPosition="right",
        variant="default",
        className=f"hati-disclosure {className}".strip(),
    )


# ── Count bar (a proportion of a locked count, never a score) ──────────────
def count_bar(label: str, count: int, total: int, *, token: str | None = None):
    pct = 0 if total <= 0 else round(100 * count / total)
    return html.Div(
        [
            html.Div(
                [html.Span(label, className="countbar__label"),
                 html.Span(str(count), className="countbar__value tabular")],
                className="countbar__head",
            ),
            html.Div(
                html.Div(className="countbar__fill", style={"width": f"{pct}%"}),
                className="countbar__track",
                **{"aria-hidden": "true"},
            ),
            token_pill(token) if token else None,
        ],
        className="countbar",
    )
