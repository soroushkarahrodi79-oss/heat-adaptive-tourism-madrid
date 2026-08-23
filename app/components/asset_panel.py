"""View 2 — Asset Decision panel.

Phase 4.2 hierarchy (decision before metadata):

    Tier A  identity → DECISION → decision confidence
    Tier B  thermal condition → evidence confidence
    Tier A  the alternatives call to action
    Tier C  full decision trace · relevant limitations   (disclosure)

The five locked concepts keep five separate labelled blocks. Tiers A and B
are static rows — never accordions, never tooltip-only — as required by the
Phase 4.0 interaction spec. Only provenance-depth material is progressively
disclosed.

Public API (`asset_panel`) is unchanged from Phase 4.1.
"""
from __future__ import annotations

import dash_mantine_components as dmc
from dash import html

from .. import constants as C
from .. import data_loader as dl
from .. import theme as T
from .icons import icon
from .primitives import (confidence_ring_glyph, decision_label, disclosure,
                         evidence_chip, exclusion_explainer, field_row,
                         is_blank, note, section_label, thermal_label,
                         token_pill)


def _fmt_utci(v) -> str | None:
    if is_blank(v):
        return None
    return f"{float(v):.1f} °C"


# ── Header ─────────────────────────────────────────────────────────────────
def _identity(rec: dict, timestamp: str, *, on_back: str | None):
    io = str(rec.get("indoor_outdoor", "")).capitalize()
    category = C.TOURISM_CATEGORY_LABEL.get(
        str(rec.get("tourism_category", "")),
        str(rec.get("tourism_category", "")).replace("_", " ").capitalize())
    open_txt = ("Open at this time" if bool(rec.get("is_open", True))
                else "Closed at this time")
    nav = []
    if on_back:
        nav.append(
            dmc.UnstyledButton(
                [icon("arrow-left", 14), html.Span(f"Back to {on_back}")],
                id={"type": "back-asset", "index": "x"}, n_clicks=0,
                className="panel__back",
            )
        )
    nav.append(
        dmc.ActionIcon(
            icon("close", 16),
            id={"type": "close-panel", "index": "x"}, n_clicks=0,
            variant="subtle", className="panel__close",
            **{"aria-label": "Close the asset panel"},
        )
    )
    return html.Div(
        [
            html.Div(nav, className="panel__nav"),
            html.Div(
                [html.Span(str(rec.get("asset_id", "")), className="panel__code"),
                 html.Span(category, className="panel__category"),
                 html.Span(io, className="panel__io")],
                className="panel__kicker",
            ),
            html.H2(str(rec.get("name", "")), className="panel__title"),
            html.Div(
                [html.Span(f"{timestamp} · {C.STUDY_DATE_HUMAN}",
                           className="panel__ts tabular"),
                 html.Span("·", className="panel__dot"),
                 html.Span(open_txt, className="panel__open")],
                className="panel__meta",
            ),
        ],
        className="panel__header",
    )


# ── Tier A: the decision ───────────────────────────────────────────────────
def _decision_block(rec: dict):
    state = str(rec.get("decision_state", ""))
    color = C.DECISION_STATE_COLOR.get(state, T.DECISION_UNKNOWN)
    return html.Div(
        [
            section_label(C.PANEL_DECISION_LABEL),
            html.Div(
                [html.Span(className="decision__chip",
                           style={"background": color},
                           **{"aria-hidden": "true"}),
                 html.Span(decision_label(state), className="decision__text")],
                className="decision",
            ),
        ],
        className="block block--decision",
        **{"aria-live": "polite"},
    )


def _confidence_block(rec: dict, asset_id: str, timestamp: str):
    conf = str(rec.get("decision_confidence", ""))
    gloss = C.CONFIDENCE_GLOSS.get(conf, "")
    is_a24 = (asset_id == C.A24_UNSTABLE_ASSET
              and timestamp == C.A24_UNSTABLE_TIMESTAMP
              and conf == "UNSTABLE")
    cls = "block block--confidence"
    if conf == "UNSTABLE":
        cls += " block--unstable"
    children = [
        section_label(C.PANEL_CONFIDENCE_LABEL),
        html.Div(
            [confidence_ring_glyph(rec.get("decision_state", ""), conf,
                                   rec.get("thermal_state", ""),
                                   bool(rec.get("is_open", True)), size=26),
             html.Span(C.CONFIDENCE_SHORT.get(conf, conf),
                       className="confidence__name"),
             token_pill(conf)],
            className="confidence__head",
        ),
        html.P(gloss, className="confidence__gloss"),
    ]
    if is_a24:
        children.append(
            html.Div(
                [
                    html.Div("Irreducible boundary case",
                             className="unstable-flag__tag"),
                    html.P(C.A24_UNSTABLE_ANNOTATION,
                           className="unstable-flag__text"),
                    html.P(C.CONFIDENCE_NOT_SEVERITY_NOTE,
                           className="unstable-flag__caveat"),
                ],
                className="unstable-flag",
            )
        )
    return html.Div(children, className=cls)


# ── Tier B: the physical facts behind it ───────────────────────────────────
def _thermal_block(rec: dict):
    thermal = str(rec.get("thermal_state", ""))
    utci = _fmt_utci(rec.get("utci_baseline"))
    lo = _fmt_utci(rec.get("utci_envelope_low"))
    hi = _fmt_utci(rec.get("utci_envelope_high"))
    children = [
        section_label(C.PANEL_THERMAL_LABEL),
        html.Div(thermal_label(thermal), className="thermal__state"),
    ]
    if utci:
        children.append(
            html.Div(
                [html.Span("UTCI", className="thermal__key"),
                 html.Span(utci, className="thermal__val tabular")]
                + ([html.Span(f"tested envelope {lo} – {hi}",
                              className="thermal__env tabular")]
                   if lo and hi else []),
                className="thermal__row",
            )
        )
        children.append(note(C.MODEL_PROVENANCE_NOTE, with_icon=True))
        if lo and hi:
            children.append(note(C.ENVELOPE_NOTE, className="note--quiet"))
    else:
        children.append(note(C.INDOOR_NOT_MODELLED_NOTE, with_icon=True))
    return html.Div(children, className="block block--thermal")


def _evidence_block(rec: dict):
    ev = str(rec.get("evidence_confidence", ""))
    return html.Div(
        [
            section_label(C.PANEL_EVIDENCE_LABEL),
            html.Div(
                [evidence_chip(ev, 13),
                 html.Span(ev.capitalize(), className="evidence__name"),
                 token_pill(ev)],
                className="evidence__head",
            ),
            html.P(C.EVIDENCE_NOTE, className="evidence__gloss"),
        ],
        className="block block--evidence",
    )


# ── Tier A: alternatives call to action ────────────────────────────────────
def _alternatives_cta(asset_id: str, timestamp: str):
    scenario = dl.scenario_for_source(asset_id, timestamp)
    if scenario is None:
        return html.Div(
            [icon("info", 14, className="note__icon"),
             html.Span(C.ALT_CTA_UNAVAILABLE)],
            className="alt-cta alt-cta--unavailable",
            **{"aria-disabled": "true"},
        )
    n = int(scenario.get("n_candidate_alternatives", 0))
    if n > 0:
        return dmc.Button(
            [html.Span(C.ALT_CTA),
             dmc.Badge(str(n), variant="filled", className="alt-cta__count"),
             icon("chevron-right", 15)],
            id={"type": "open-alt", "index": "x"}, n_clicks=0,
            fullWidth=True, size="md", className="alt-cta alt-cta--primary",
        )
    survivors, excluded = dl.scenario_candidates(scenario["scenario"])
    n_eval = len(survivors) + len(excluded)
    return html.Div(
        [
            html.Div(
                [icon("no-result", 15), html.Span(C.NODEF_HEADLINE)],
                className="alt-cta__verdict",
            ),
            html.Div(f"{n_eval} candidates evaluated within "
                     f"{int(scenario['access_radius_m'])} m · 0 survived.",
                     className="alt-cta__tally tabular"),
            dmc.Button(
                [html.Span(C.ALT_CTA_NODEF), icon("chevron-right", 15)],
                id={"type": "open-alt", "index": "x"}, n_clicks=0,
                fullWidth=True, size="md", variant="default",
                className="alt-cta alt-cta--nodef-btn",
            ),
        ],
        className="alt-cta alt-cta--nodef",
    )


# ── Tier C: disclosures ────────────────────────────────────────────────────
def _trace_body(rec: dict, timestamp: str):
    rows = [
        field_row("Screening status",
                  str(rec.get("screening_status", "")), mono=True),
        field_row("Thermal state", str(rec.get("thermal_state", "")), mono=True),
        field_row("Decision state", str(rec.get("decision_state", "")), mono=True),
        field_row("Decision confidence",
                  str(rec.get("decision_confidence", "")), mono=True),
        field_row("Thermal evidence",
                  str(rec.get("thermal_evidence", "")), mono=True),
        field_row("Opening-hours evidence",
                  str(rec.get("opening_hours_evidence", "")), mono=True),
        field_row("Evidence confidence",
                  str(rec.get("evidence_confidence", "")), mono=True),
        field_row("Open at this timestamp",
                  "Yes" if bool(rec.get("is_open", True)) else "No"),
    ]
    if not is_blank(rec.get("opening_hours")):
        rows.append(field_row("Documented hours",
                              str(rec.get("opening_hours"))))
    if not is_blank(rec.get("opening_hours_source")):
        rows.append(field_row("Hours source",
                              str(rec.get("opening_hours_source"))))
    if not is_blank(rec.get("tourism_relevance_evidence")):
        rows.append(field_row("Relevance evidence",
                              str(rec.get("tourism_relevance_evidence"))))

    body = [
        html.P("Every value below is read unchanged from the locked Phase 3 "
               "screening output for this asset at this timestamp.",
               className="trace__intro"),
        html.Div(rows, className="trace__rows"),
    ]

    token = rec.get("context_free_exclusion_reason")
    if not is_blank(token):
        detail = None
        if str(token) == "INSUFFICIENT_EVIDENCE":
            detail = [f"Thermal evidence {rec.get('thermal_evidence', 'n/a')} · "
                      f"opening-hours evidence "
                      f"{rec.get('opening_hours_evidence', 'n/a')}"]
        elif str(token) == "CLOSED_AT_TIMESTAMP":
            detail = [f"Documented hours: {rec.get('opening_hours', 'n/a')}"]
        body.extend([
            dmc.Divider(className="trace__divider"),
            section_label(C.PANEL_EXCLUSION_LABEL),
            exclusion_explainer(str(token), detail_lines=detail),
            note(C.PANEL_EXCLUSION_NOTE, className="note--quiet"),
        ])
    return html.Div(body, className="trace")


def _relevant_limitations(rec: dict) -> list[str]:
    io = str(rec.get("indoor_outdoor", ""))
    items = []
    if io == "outdoor":
        items.append("Thermal values here are model-derived (SOLWEIG/UTCI) "
                     "and were never field-measured.")
        items.append("Accessibility from here is straight-line distance "
                     "only; walking-route heat exposure is not modelled.")
    else:
        items.append("Indoor refuge assumes thermal buffering, without "
                     "verified air-conditioning or queue-exposure modelling.")
        items.append("No indoor thermal value is modelled, so no UTCI is "
                     "shown for this asset.")
    items.append("Opening hours are 2026-documented values applied "
                 "retrospectively to the 2023 study date, and are not "
                 "verified as fact for 2023.")
    return items


# ── Public builder ─────────────────────────────────────────────────────────
def asset_panel(asset_id: str, timestamp: str, *, back_to: str | None = None):
    rec = dl.asset_record(asset_id, timestamp)
    if rec is None:
        return html.Div(
            html.P(C.EMPTY_ASSET_NOT_FOUND, className="panel__empty-text"),
            className="panel__empty",
        )

    lims = _relevant_limitations(rec)
    body = [
        _identity(rec, timestamp, on_back=back_to),
        html.Div(
            [_decision_block(rec),
             _confidence_block(rec, asset_id, timestamp)],
            className="tier tier--a",
        ),
        html.Div(
            [_thermal_block(rec), _evidence_block(rec)],
            className="tier tier--b",
        ),
        html.Div(_alternatives_cta(asset_id, timestamp), className="tier tier--cta"),
        html.Div(
            disclosure([
                (C.PANEL_TRACE_LABEL, _trace_body(rec, timestamp)),
                (f"{C.PANEL_LIMITATIONS_LABEL} ({len(lims)})",
                 html.Ul([html.Li(t) for t in lims], className="relevant-lims")),
            ]),
            className="tier tier--c",
        ),
    ]
    return html.Div(body, className="asset-panel")
