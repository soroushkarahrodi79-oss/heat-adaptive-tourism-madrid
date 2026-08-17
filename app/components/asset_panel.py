"""View 2 — Asset Decision View (right-hand side panel).

Full audit trail for one asset's decision at one timestamp. Headline facts
(thermal_state, decision_state, decision_confidence, evidence_confidence) are
static rows, never accordions and never tooltip-only.
"""
from __future__ import annotations

import pandas as pd
from dash import html

from .. import constants as C
from .. import data_loader as dl
from .primitives import (confidence_ring_glyph, exclusion_explainer,
                         field_row)


def _blank(v) -> bool:
    return v is None or (isinstance(v, float) and pd.isna(v)) or str(v).strip() == ""


def _fmt_utci(v) -> str | None:
    if _blank(v):
        return None
    return f"{float(v):.1f} °C"


# ── Sub-blocks ──────────────────────────────────────────────────────────────
def _identity_header(rec: dict, timestamp: str):
    io = str(rec.get("indoor_outdoor", ""))
    return html.Div(
        [
            html.Div(rec.get("name", ""), className="panel__title"),
            html.Div(
                [
                    html.Span(str(rec.get("tourism_category", "")),
                              className="panel__category mono"),
                    html.Span(io.capitalize(), className="panel__io"),
                ],
                className="panel__subtitle",
            ),
            html.Div(
                [html.Span("Timestamp ", className="panel__ts-label"),
                 html.Span(f"{timestamp} · {C.STUDY_DATE}",
                           className="panel__ts-value")],
                className="panel__ts",
            ),
        ],
        className="panel__header",
    )


def _thermal_row(rec: dict):
    thermal = str(rec.get("thermal_state", ""))
    label = C.THERMAL_STATE_LABEL.get(thermal, thermal)
    utci = _fmt_utci(rec.get("utci_baseline"))
    lo = _fmt_utci(rec.get("utci_envelope_low"))
    hi = _fmt_utci(rec.get("utci_envelope_high"))
    children = [
        html.Div("Thermal state", className="block__label"),
        html.Div(label, className="block__value"),
    ]
    if utci:
        env = f"  (tested envelope {lo} – {hi})" if lo and hi else ""
        children.append(
            html.Div([html.Span("UTCI ", className="mono"),
                      html.Span(f"{utci}{env}", className="tabular"),
                      html.Span(" — model-derived (SOLWEIG/UTCI), not "
                                "field-measured", className="block__note")],
                     className="block__utci"))
    else:
        children.append(html.Div("UTCI not physically modelled for indoor "
                                 "assets.", className="block__note"))
    return html.Div(children, className="block block--thermal")


def _decision_row(rec: dict):
    decision = str(rec.get("decision_state", ""))
    label = C.DECISION_STATE_LABEL.get(decision, decision)
    color = C.DECISION_STATE_COLOR.get(decision, "#8A8A8A")
    return html.Div(
        [
            html.Div("Decision", className="block__label"),
            html.Div(
                [html.Span(className="decision-badge__chip",
                           style={"background": color}),
                 html.Span(label, className="decision-badge__text")],
                className="decision-badge",
            ),
        ],
        className="block block--decision",
    )


def _confidence_row(rec: dict, asset_id: str, timestamp: str):
    conf = str(rec.get("decision_confidence", ""))
    gloss = C.CONFIDENCE_GLOSS.get(conf, "")
    is_a24 = (asset_id == C.A24_UNSTABLE_ASSET
              and timestamp == C.A24_UNSTABLE_TIMESTAMP
              and conf == "UNSTABLE")
    block_cls = "block block--confidence"
    if conf == "UNSTABLE":
        block_cls += " block--unstable"
    children = [
        html.Div("Decision confidence", className="block__label"),
        html.Div(
            [
                confidence_ring_glyph(rec.get("decision_state", ""),
                                      conf, rec.get("thermal_state", ""),
                                      bool(rec.get("is_open", True)), size=30),
                html.Span(C.CONFIDENCE_SHORT.get(conf, conf),
                          className="confidence__name"),
            ],
            className="confidence__head",
        ),
        html.Div(gloss, className="confidence__gloss"),
    ]
    if is_a24:
        children.append(
            html.Div(
                [html.Span("Irreducible boundary case",
                           className="unstable-flag__tag"),
                 html.Span(C.A24_UNSTABLE_ANNOTATION,
                           className="unstable-flag__text")],
                className="unstable-flag",
            )
        )
    return html.Div(children, className=block_cls)


def _evidence_row(rec: dict):
    ev = str(rec.get("evidence_confidence", ""))
    return html.Div(
        [
            html.Div("Evidence confidence", className="block__label"),
            html.Div(
                [html.Span(className=f"evidence-chip evidence-chip--{ev.lower()}"),
                 html.Span(ev.capitalize(), className="evidence__name")],
                className="evidence__head",
            ),
            html.Div(C.EVIDENCE_NOTE, className="block__note"),
        ],
        className="block block--evidence",
    )


def _exclusion_row(rec: dict):
    token = rec.get("context_free_exclusion_reason")
    if _blank(token):
        return None
    detail = None
    if str(token) == "INSUFFICIENT_EVIDENCE":
        detail = [f"Thermal evidence: {rec.get('thermal_evidence', 'n/a')} · "
                  f"opening-hours evidence: {rec.get('opening_hours_evidence', 'n/a')}"]
    elif str(token) == "CLOSED_AT_TIMESTAMP":
        detail = [f"Documented hours: {rec.get('opening_hours', 'n/a')}"]
    return html.Div(
        [
            html.Div("Why this asset can be excluded elsewhere",
                     className="block__label"),
            exclusion_explainer(str(token), detail_lines=detail),
        ],
        className="block block--exclusion",
    )


def _relevant_limitations(rec: dict):
    io = str(rec.get("indoor_outdoor", ""))
    items = []
    if io == "outdoor":
        items.append("Accessibility from here is straight-line only; "
                     "walking-route heat exposure is not modelled.")
        items.append("Thermal values are model-derived (SOLWEIG/UTCI), "
                     "never field-measured.")
    else:
        items.append("Indoor refuge assumes thermal buffering without "
                     "verified A/C or queue-exposure modelling.")
    items.append("Opening hours are 2026-documented values applied to the "
                 "2023 study date, not verified for 2023.")
    return html.Div(
        [html.Div("Relevant limitations", className="block__label"),
         html.Ul([html.Li(t) for t in items], className="relevant-lims")],
        className="block block--limitations",
    )


def _alternatives_entry(asset_id: str, timestamp: str):
    scenario = dl.scenario_for_source(asset_id, timestamp)
    if scenario is None:
        return html.Div(
            "No candidate screening was pre-computed for this asset at this "
            "timestamp — it is not a scenario source.",
            className="alt-entry alt-entry--disabled",
        )
    n = int(scenario.get("n_candidate_alternatives", 0))
    survivors, excluded = dl.scenario_candidates(scenario["scenario"])
    n_eval = len(survivors) + len(excluded)
    if n > 0:
        return html.Button(
            f"View {n} alternative{'s' if n != 1 else ''} — trade-offs",
            id={"type": "open-alt", "index": "x"}, n_clicks=0,
            className="alt-entry alt-entry--btn",
        )
    # Zero survivors -> inline NO_DEFENSIBLE summary + link into View 3.
    return html.Div(
        [
            html.Div("No defensible alternative", className="alt-entry__verdict"),
            html.Div(f"{n_eval} candidate{'s' if n_eval != 1 else ''} "
                     f"evaluated within {int(scenario['access_radius_m'])} m · "
                     f"0 survived.", className="alt-entry__tally"),
            html.Button("View full reasoning",
                        id={"type": "open-alt", "index": "x"},
                        n_clicks=0, className="alt-entry--link"),
        ],
        className="alt-entry alt-entry--nodef",
    )


# ── Public builder ──────────────────────────────────────────────────────────
def asset_panel(asset_id: str, timestamp: str):
    rec = dl.asset_record(asset_id, timestamp)
    if rec is None:
        return html.Div("Asset not found.", className="panel__empty")
    hours_dependent = not _blank(rec.get("opening_hours"))
    blocks = [
        html.Button("✕ Close", id={"type": "close-panel", "index": "x"},
                    n_clicks=0, className="panel__close"),
        _identity_header(rec, timestamp),
        _thermal_row(rec),
        _decision_row(rec),
        _confidence_row(rec, asset_id, timestamp),
        _evidence_row(rec),
    ]
    excl = _exclusion_row(rec)
    if excl is not None:
        blocks.append(excl)
    blocks.append(_relevant_limitations(rec))
    blocks.append(_alternatives_entry(asset_id, timestamp))
    return html.Div(blocks, className="asset-panel")
