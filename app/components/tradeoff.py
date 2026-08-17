"""View 3 — Alternative / Trade-off View.

Surviving candidates side-by-side (no ranking), an on-demand excluded list,
the pre-registered radius-sensitivity table, the off-by-default baseline
comparison, and the dedicated S8 NoDefensibleAlternativePanel.
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


def _sort_survivors(df: pd.DataFrame, sort_key: str) -> pd.DataFrame:
    if sort_key == "indoor_outdoor":
        return df.sort_values(["indoor_outdoor", "distance_m"])
    if sort_key == "experience_type":
        return df.sort_values(["experience_type", "distance_m"])
    return df.sort_values("distance_m")            # default: distance


# ── One surviving-candidate card (no score, no rank, no "recommended") ──────
def _alternative_card(r: dict):
    exp = C.EXPERIENCE_TYPE_LABEL.get(str(r.get("experience_type", "")),
                                      str(r.get("experience_type", "")))
    conf = str(r.get("cand_decision_confidence", ""))
    ev = str(r.get("cand_evidence_confidence", ""))
    io = str(r.get("indoor_outdoor", "")).capitalize()
    dist = r.get("distance_m")
    walk = r.get("walk_min")
    dist_txt = (f"{float(dist):.0f} m straight-line"
                + (f" · ~{float(walk):.0f} min walk" if not _blank(walk) else "")
                ) if not _blank(dist) else "n/a"
    thermal_lbl = C.THERMAL_STATE_LABEL.get(str(r.get("cand_thermal_state", "")),
                                            str(r.get("cand_thermal_state", "")))
    cand_utci = r.get("cand_utci")
    thermal_bits = [thermal_lbl]
    if not _blank(cand_utci):
        thermal_bits.append(f"UTCI {float(cand_utci):.1f} °C (modelled)")
    note = r.get("improvement_note")

    body = [
        html.Div(
            [html.Span(r.get("candidate_name", ""), className="card__name"),
             html.Span(io, className="card__io")],
            className="card__title",
        ),
        html.Div(exp, className="card__exp"),
        field_row("Distance", dist_txt),
        field_row("Thermal", " · ".join(thermal_bits)),
    ]
    if not _blank(note):
        body.append(html.Div(
            [html.Span("vs source: ", className="card__note-label"),
             html.Span(str(note), className="card__note")],
            className="card__thermal-note"))
    body.append(html.Div(
        [
            html.Div(
                [confidence_ring_glyph(r.get("cand_decision_state", ""), conf,
                                       r.get("cand_thermal_state", ""), True, 24),
                 html.Span(C.CONFIDENCE_SHORT.get(conf, conf),
                           className="card__conf-name")],
                className="card__conf",
            ),
            html.Div(
                [html.Span(className=f"evidence-chip evidence-chip--{ev.lower()}"),
                 html.Span(f"Evidence: {ev.capitalize()}",
                           className="card__ev-name")],
                className="card__ev",
            ),
        ],
        className="card__confrow",
    ))
    body.append(html.Div("Open at this timestamp", className="card__open"))
    body.append(html.Button("Open this asset's record",
                            id={"type": "card-open-asset",
                                "index": r.get("candidate_id")},
                            n_clicks=0, className="card__open-btn"))
    return html.Div(body, className="alt-card")


# ── Excluded-candidates disclosure ──────────────────────────────────────────
def _excluded_detail_lines(r: dict, scenario: dict) -> list[str] | None:
    token = str(r.get("exclusion_reason", ""))
    if token == "ACCESSIBILITY_CONSTRAINT" and not _blank(r.get("distance_m")):
        return [f"Distance {float(r['distance_m']):.0f} m vs "
                f"search radius {int(scenario['access_radius_m'])} m."]
    if token == "OUTDOOR_EXPOSURE_TOO_HIGH":
        parts = []
        if not _blank(r.get("cand_utci")):
            parts.append(f"Candidate UTCI {float(r['cand_utci']):.1f} °C")
        if not _blank(r.get("source_utci")):
            parts.append(f"source UTCI {float(r['source_utci']):.1f} °C")
        return [" vs ".join(parts)] if parts else None
    if token == "NO_MEANINGFUL_THERMAL_IMPROVEMENT" and not _blank(r.get("improvement_note")):
        return [str(r["improvement_note"])]
    return None


def _excluded_item(r: dict, scenario: dict):
    return html.Div(
        [
            html.Div(
                [html.Span(r.get("candidate_name", ""), className="excl-item__name"),
                 html.Span(str(r.get("indoor_outdoor", "")).capitalize(),
                           className="excl-item__io")],
                className="excl-item__title",
            ),
            exclusion_explainer(str(r.get("exclusion_reason", "")),
                                detail_lines=_excluded_detail_lines(r, scenario)),
        ],
        className="excl-item",
    )


def _excluded_list(excluded: pd.DataFrame, scenario: dict, *, expanded: bool):
    n = len(excluded)
    items = [_excluded_item(r.to_dict(), scenario)
             for _, r in excluded.sort_values("distance_m").iterrows()]
    return html.Details(
        [
            html.Summary(
                f"{n} nearby option{'s' if n != 1 else ''} excluded — show why",
                className="excl-list__summary"),
            html.Div(items, className="excl-list__body"),
        ],
        open=expanded, className="excl-list",
    )


# ── Radius sensitivity disclosure (pre-registered, NOT a retry) ────────────
def _radius_sensitivity(scenario_id: str):
    acc = dl.accessibility_row(scenario_id)
    if acc is None:
        return None
    stable = bool(acc.get("recommendation_category_stable_500_1200"))
    return html.Details(
        [
            html.Summary("Radius sensitivity (pre-registered 500 / 800 / 1200 m)",
                         className="radius__summary"),
            html.Div(
                [
                    html.P("Pre-registered sensitivity parameter from Phase 3 — "
                           "shown for transparency, not an interactive 'try a "
                           "bigger circle' control.", className="radius__note"),
                    html.Table(
                        [
                            html.Tr([html.Th("Radius"), html.Th("Surviving alternatives")]),
                            html.Tr([html.Td("500 m"), html.Td(str(int(acc["n_alt_500m"])))]),
                            html.Tr([html.Td("800 m"), html.Td(str(int(acc["n_alt_800m"])))]),
                            html.Tr([html.Td("1200 m"), html.Td(str(int(acc["n_alt_1200m"])))]),
                        ],
                        className="radius__table",
                    ),
                    html.Div(
                        ("Recommendation category stable across 500–1200 m."
                         if stable else
                         "Recommendation category is NOT stable across "
                         "500–1200 m — the survivor set depends on radius here."),
                        className="radius__stability",
                    ),
                ],
                className="radius__body",
            ),
        ],
        className="radius-sensitivity",
    )


# ── Baseline comparison (pre-computed row only) ────────────────────────────
def _baseline_panel(scenario_id: str):
    b = dl.baseline_row(scenario_id)
    if b is None:
        return html.Div("No baseline comparison available for this scenario.",
                        className="baseline-panel")
    survives = bool(b.get("baseline_pick_survives_hati"))
    rows = [
        field_row("Baseline pick", f"{b.get('baseline_pick_name','')}"),
        field_row("Distance", f"{float(b['baseline_pick_distance_m']):.0f} m straight-line"
                  if not _blank(b.get("baseline_pick_distance_m")) else "n/a"),
        field_row("Indoor / outdoor",
                  str(b.get("baseline_pick_indoor_outdoor", "")).capitalize()),
        field_row("Survives HATI screening?", "Yes" if survives else "No"),
        field_row("Open in radius (baseline count)",
                  str(int(b["n_open_in_radius_baseline"]))
                  if not _blank(b.get("n_open_in_radius_baseline")) else "n/a"),
        field_row("Removed by HATI (thermal/evidence)",
                  str(int(b["n_removed_by_hati_thermal_or_evidence"]))
                  if not _blank(b.get("n_removed_by_hati_thermal_or_evidence")) else "n/a"),
    ]
    if not survives and not _blank(b.get("baseline_pick_hati_exclusion")):
        rows.append(html.Div(
            exclusion_explainer(str(b["baseline_pick_hati_exclusion"])),
            className="baseline-panel__excl"))
    return html.Div(
        [
            html.Div("Conventional baseline: nearest open option",
                     className="baseline-panel__title"),
            html.Div("Pre-computed in Phase 3 — not recalculated here.",
                     className="baseline-panel__note"),
            html.Div(rows, className="baseline-panel__rows"),
        ],
        className="baseline-panel",
    )


# ── S8: dedicated NoDefensibleAlternativePanel ─────────────────────────────
def _no_defensible_panel(scenario: dict, excluded: pd.DataFrame):
    n_eval = len(excluded)
    radius = int(scenario["access_radius_m"])
    return html.Div(
        [
            html.Div("No defensible alternative found.",
                     className="nodef__headline"),
            html.Div("This is the correct result of the screening, not a "
                     "missing feature.", className="nodef__subline"),
            html.Div(f"{n_eval} candidate{'s' if n_eval != 1 else ''} "
                     f"evaluated within {radius} m · 0 survived.",
                     className="nodef__tally"),
            html.Div(
                "Every open, in-range candidate was either another hot outdoor "
                "location or failed on evidence or thermal grounds — "
                "recommending one would mean sending a heat-stressed visitor to "
                "an equally hot location.",
                className="nodef__method",
            ),
            html.Div("Excluded candidates", className="nodef__excl-title"),
            html.Div(
                [_excluded_item(r.to_dict(), scenario)
                 for _, r in excluded.sort_values("distance_m").iterrows()],
                className="nodef__excl-list",
            ),
        ],
        className="nodef-panel",
    )


# ── Public builder ──────────────────────────────────────────────────────────
def tradeoff_view(scenario_id: str, sort_key: str = "distance",
                  baseline_on: bool = False):
    scenario = dl.summary_row(scenario_id)
    if scenario is None:
        return html.Div("Scenario not found.", className="tradeoff__empty")
    survivors, excluded = dl.scenario_candidates(scenario_id)

    header = html.Div(
        [
            html.Button("← Back to asset",
                        id={"type": "back-asset", "index": "x"}, n_clicks=0,
                        className="tradeoff__back"),
            html.Div(
                [html.Span(scenario["scenario"], className="tradeoff__scode"),
                 html.Span(f"From {scenario['source_name']} · "
                           f"{scenario['timestamp']} · {C.STUDY_DATE} · "
                           f"{int(scenario['access_radius_m'])} m radius",
                           className="tradeoff__source")],
                className="tradeoff__heading",
            ),
        ],
        className="tradeoff__header",
    )

    # S8 / zero-survivor -> dedicated verdict panel.
    if len(survivors) == 0:
        return html.Div(
            [header, _no_defensible_panel(scenario, excluded),
             _radius_sensitivity(scenario_id),
             _baseline_block(scenario_id, baseline_on)],
            className="tradeoff",
        )

    sorted_surv = _sort_survivors(survivors, sort_key)
    sort_control = html.Div(
        [
            html.Span("Sort (organisation, not ranking):",
                      className="sort__label"),
            html.Div(
                [html.Button(lbl, id={"type": "sort-btn", "index": key},
                             n_clicks=0,
                             className="sort-btn" + (" sort-btn--active"
                                                     if key == sort_key else ""))
                 for key, lbl in C.SORT_KEYS.items()],
                className="sort__group",
            ),
        ],
        className="sort-control",
    )
    cards = html.Div([_alternative_card(r.to_dict())
                      for _, r in sorted_surv.iterrows()],
                     className="alt-grid")

    return html.Div(
        [
            header,
            html.Div(f"{len(survivors)} surviving alternative"
                     f"{'s' if len(survivors) != 1 else ''} — no ranking; "
                     "each shown on its own terms.",
                     className="tradeoff__count"),
            sort_control,
            cards,
            _excluded_list(excluded, scenario, expanded=False),
            _radius_sensitivity(scenario_id),
            _baseline_block(scenario_id, baseline_on),
        ],
        className="tradeoff",
    )


def _baseline_block(scenario_id: str, baseline_on: bool):
    toggle = html.Button(
        ("✓ Comparing to conventional baseline (click to hide)" if baseline_on
         else "Compare to conventional baseline"),
        id={"type": "baseline-toggle", "index": "x"}, n_clicks=0,
        className="baseline-toggle" + (" baseline-toggle--on" if baseline_on else ""),
    )
    children = [toggle]
    if baseline_on:
        children.append(_baseline_panel(scenario_id))
    return html.Div(children, className="baseline-block")
