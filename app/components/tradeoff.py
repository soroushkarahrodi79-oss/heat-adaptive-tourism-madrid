"""View 3 — Alternative / Trade-off view.

Surviving candidates side by side, with no ranking anywhere: no ordinal, no
position badge, no superlative, no emphasis difference between cards. Sorting
changes reading order only.

Also hosts the on-demand excluded list (grouped by the locked exclusion
reason), the pre-registered reach-sensitivity evidence, the off-by-default
baseline comparison, and — via ``empty_states`` — the dedicated
``NO_DEFENSIBLE_ALTERNATIVE`` result page.

Public API (`tradeoff_view`) is unchanged from Phase 4.1.
"""
from __future__ import annotations

import dash_mantine_components as dmc
import pandas as pd
from dash import html

from .. import constants as C
from .. import data_loader as dl
from .empty_states import no_defensible_panel, unavailable
from .icons import icon
from .primitives import (confidence_ring_glyph, decision_label, disclosure,
                         evidence_chip, exclusion_explainer, field_row,
                         is_blank, note, section_label, thermal_label,
                         token_pill)


def _sort_survivors(df: pd.DataFrame, sort_key: str) -> pd.DataFrame:
    """Display order only. Every key is a plainly visible attribute of the
    row; none of them is an evaluation of the candidate."""
    if sort_key == "name":
        return df.sort_values("candidate_name")
    if sort_key == "indoor_outdoor":
        return df.sort_values(["indoor_outdoor", "candidate_name"])
    if sort_key == "experience_type":
        return df.sort_values(["experience_type", "candidate_name"])
    return df.sort_values("distance_m")


# ── One surviving-candidate card ───────────────────────────────────────────
def _alternative_card(r: dict):
    exp = C.EXPERIENCE_TYPE_LABEL.get(str(r.get("experience_type", "")),
                                      str(r.get("experience_type", "")))
    conf = str(r.get("cand_decision_confidence", ""))
    ev = str(r.get("cand_evidence_confidence", ""))
    io = str(r.get("indoor_outdoor", "")).capitalize()
    dist = r.get("distance_m")
    walk = r.get("walk_min")
    dist_bits = []
    if not is_blank(dist):
        dist_bits.append(f"{float(dist):.0f} m")
    if not is_blank(walk):
        dist_bits.append(f"~{float(walk):.0f} min walk")
    cand_utci = r.get("cand_utci")
    note_txt = r.get("improvement_note")

    return html.Div(
        [
            html.Div(
                [html.Span(str(r.get("candidate_name", "")),
                           className="card__name"),
                 html.Span(io, className="card__io")],
                className="card__title",
            ),
            html.Div(exp, className="card__exp"),
            html.Div(
                [icon("map-pin", 13),
                 html.Span(" · ".join(dist_bits) or "distance unavailable",
                           className="tabular")],
                className="card__dist",
            ),
            html.Div(
                [html.Span(thermal_label(r.get("cand_thermal_state", "")),
                           className="card__thermal-state")]
                + ([html.Span(f"UTCI {float(cand_utci):.1f} °C (modelled)",
                              className="card__thermal-utci tabular")]
                   if not is_blank(cand_utci) else []),
                className="card__thermal",
            ),
            html.Div(
                [html.Span("vs source: ", className="card__note-label"),
                 html.Span(str(note_txt))],
                className="card__note",
            ) if not is_blank(note_txt) else None,
            dmc.Divider(className="card__divider"),
            html.Div(
                [
                    html.Div(
                        [confidence_ring_glyph(r.get("cand_decision_state", ""),
                                               conf,
                                               r.get("cand_thermal_state", ""),
                                               True, 20),
                         html.Span(C.CONFIDENCE_SHORT.get(conf, conf),
                                   className="card__meta-val")],
                        className="card__meta",
                        title="Decision confidence",
                    ),
                    html.Div(
                        [evidence_chip(ev, 11),
                         html.Span(f"Evidence {ev.capitalize()}",
                                   className="card__meta-val")],
                        className="card__meta",
                        title="Evidence confidence",
                    ),
                    html.Div(
                        [icon("clock", 12), html.Span("Open at this timestamp")],
                        className="card__open",
                    ),
                ],
                className="card__metarow",
            ),
            dmc.Button(
                [html.Span("Open this record"), icon("chevron-right", 14)],
                id={"type": "card-open-asset", "index": r.get("candidate_id")},
                n_clicks=0, variant="default", size="xs", fullWidth=True,
                className="card__open-btn",
            ),
        ],
        className="alt-card",
    )


# ── Excluded candidates, grouped by the locked reason ──────────────────────
def _excluded_detail_lines(r: dict, scenario: dict) -> list[str] | None:
    token = str(r.get("exclusion_reason", ""))
    if token == "ACCESSIBILITY_CONSTRAINT" and not is_blank(r.get("distance_m")):
        return [f"{float(r['distance_m']):.0f} m from the source · reach "
                f"constraint {int(scenario['access_radius_m'])} m"]
    if token == "OUTDOOR_EXPOSURE_TOO_HIGH":
        parts = []
        if not is_blank(r.get("cand_utci")):
            parts.append(f"candidate UTCI {float(r['cand_utci']):.1f} °C")
        if not is_blank(r.get("source_utci")):
            parts.append(f"source UTCI {float(r['source_utci']):.1f} °C")
        return [" · ".join(parts)] if parts else None
    if (token == "NO_MEANINGFUL_THERMAL_IMPROVEMENT"
            and not is_blank(r.get("improvement_note"))):
        return [str(r["improvement_note"])]
    return None


def _excluded_item(r: dict, scenario: dict):
    dist = r.get("distance_m")
    lines = _excluded_detail_lines(r, scenario) or []
    return html.Div(
        [
            html.Div(
                [html.Span(str(r.get("candidate_name", "")),
                           className="excl-item__name"),
                 html.Span(f"{float(dist):.0f} m" if not is_blank(dist) else "",
                           className="excl-item__dist tabular")],
                className="excl-item__title",
            ),
            html.Div([html.Div(t, className="excl-item__detail") for t in lines],
                     className="excl-item__details") if lines else None,
        ],
        className="excl-item",
    )


def _excluded_groups(excluded: pd.DataFrame, scenario: dict):
    scenario_id = str(scenario["scenario"])
    groups = []
    for token, n in dl.exclusion_breakdown(scenario_id):
        rows = excluded[excluded["exclusion_reason"].astype(str) == token]
        rows = rows.sort_values("distance_m")
        groups.append(
            html.Div(
                [
                    html.Div(
                        [html.Span(C.EXCLUSION_TRANSLATIONS.get(token, token),
                                   className="excl-group__reason"),
                         html.Span(str(n), className="excl-group__count tabular")],
                        className="excl-group__head",
                    ),
                    token_pill(token),
                    html.Div([_excluded_item(r.to_dict(), scenario)
                              for _, r in rows.iterrows()],
                             className="excl-group__items"),
                ],
                className="excl-group",
            )
        )
    return html.Div(
        [note(C.ALT_EXCLUDED_NOTE, className="note--quiet"),
         html.Div(groups, className="excl-groups")],
        className="excl-list",
    )


# ── Reach (accessibility-radius) sensitivity — read-only evidence ──────────
def _radius_body(scenario_id: str):
    acc = dl.accessibility_row(scenario_id)
    if acc is None:
        return None
    stable = bool(acc.get("recommendation_category_stable_500_1200"))
    cells = [("500 m", int(acc["n_alt_500m"])),
             ("800 m", int(acc["n_alt_800m"])),
             ("1200 m", int(acc["n_alt_1200m"]))]
    return html.Div(
        [
            html.Div(
                [html.Div([html.Span(lbl, className="reach__radius"),
                           html.Span(str(v), className="reach__count tabular")],
                          className="reach__cell")
                 for lbl, v in cells],
                className="reach__grid",
            ),
            html.Div("surviving alternatives at each pre-registered reach",
                     className="reach__axis-note"),
            html.P(C.RADIUS_STABLE if stable else C.RADIUS_UNSTABLE,
                   className="reach__stability"),
            note(C.RADIUS_NOTE, className="note--quiet"),
        ],
        className="reach",
    )


# ── Baseline comparison (pre-computed row only, off by default) ────────────
def _baseline_body(scenario_id: str):
    b = dl.baseline_row(scenario_id)
    if b is None:
        return unavailable(C.EMPTY_NO_BASELINE)
    survives = bool(b.get("baseline_pick_survives_hati"))
    rows = [
        field_row("Baseline pick", str(b.get("baseline_pick_name", ""))),
        field_row("Distance",
                  f"{float(b['baseline_pick_distance_m']):.0f} m straight-line"
                  if not is_blank(b.get("baseline_pick_distance_m")) else "n/a"),
        field_row("Indoor / outdoor",
                  str(b.get("baseline_pick_indoor_outdoor", "")).capitalize()),
        field_row("Survives HATI screening", "Yes" if survives else "No"),
        field_row("Open within reach (baseline count)",
                  str(int(b["n_open_in_radius_baseline"]))
                  if not is_blank(b.get("n_open_in_radius_baseline")) else "n/a"),
        field_row("Removed by HATI (thermal or evidence)",
                  str(int(b["n_removed_by_hati_thermal_or_evidence"]))
                  if not is_blank(b.get("n_removed_by_hati_thermal_or_evidence"))
                  else "n/a"),
    ]
    children = [
        note(C.BASELINE_WHAT, with_icon=True),
        html.Div(rows, className="baseline__rows"),
    ]
    if not survives and not is_blank(b.get("baseline_pick_hati_exclusion")):
        children.append(
            html.Div(exclusion_explainer(str(b["baseline_pick_hati_exclusion"])),
                     className="baseline__excl"))
    children.append(note(C.BASELINE_PRECOMPUTED, className="note--quiet"))
    children.append(note(C.BASELINE_NEUTRALITY, className="note--quiet"))
    return html.Div(children, className="baseline")


def _baseline_block(scenario_id: str, baseline_on: bool):
    children = [
        dmc.Switch(
            id={"type": "baseline-toggle", "index": "x"},
            checked=bool(baseline_on),
            label=C.BASELINE_LABEL,
            size="sm",
            className="baseline__switch",
        )
    ]
    if baseline_on:
        children.append(_baseline_body(scenario_id))
    return html.Div(children, className="baseline-block")


# ── Header ─────────────────────────────────────────────────────────────────
def _header(scenario: dict, survivors_n: int, *, nodef: bool):
    """Header for View 3.

    In the zero-survivor case the verdict panel below *is* the title, so the
    header deliberately carries no headline of its own — repeating
    "No defensible alternative found." twice would read as an error notice
    rather than as one considered result.
    """
    src = str(scenario["source_name"])
    children = [
        dmc.UnstyledButton(
            [icon("arrow-left", 14), html.Span(f"Back to {src}")],
            id={"type": "back-asset", "index": "x"}, n_clicks=0,
            className="panel__back",
        ),
        html.Div(
            [html.Span(str(scenario["scenario"]), className="tradeoff__code"),
             html.Span("" if nodef else C.ALT_VIEW_KICKER,
                       className="tradeoff__kicker")],
            className="tradeoff__kickerrow",
        ),
    ]
    if not nodef:
        children.append(
            html.H2(f"{survivors_n} surviving alternative"
                    f"{'s' if survivors_n != 1 else ''}",
                    className="tradeoff__title"))
    return html.Div(
        children + [
            html.Div(
                [html.Span(f"From {src}"),
                 html.Span("·", className="panel__dot"),
                 html.Span(f"{scenario['timestamp']} · {C.STUDY_DATE_HUMAN}",
                           className="tabular"),
                 html.Span("·", className="panel__dot"),
                 html.Span(f"within {int(scenario['access_radius_m'])} m",
                           className="tabular")],
                className="tradeoff__meta",
            ),
        ],
        className="tradeoff__header" + (" tradeoff__header--nodef" if nodef else ""),
    )


# ── Public builder ─────────────────────────────────────────────────────────
def tradeoff_view(scenario_id: str, sort_key: str = "distance",
                  baseline_on: bool = False):
    scenario = dl.summary_row(scenario_id)
    if scenario is None:
        return html.Div(unavailable(C.EMPTY_SCENARIO_NOT_FOUND),
                        className="tradeoff tradeoff--empty")
    survivors, excluded = dl.scenario_candidates(scenario_id)

    # ── Zero survivors → the dedicated result page. ──
    if len(survivors) == 0:
        reach = _radius_body(scenario_id)
        blocks = [
            _header(scenario, 0, nodef=True),
            no_defensible_panel(scenario, excluded),
        ]
        if reach is not None:
            blocks.append(html.Div(
                [section_label(C.RADIUS_TITLE), reach],
                className="tradeoff__section"))
        blocks.append(disclosure([
            (f"{C.NODEF_FULL_LIST_TITLE} ({len(excluded)})",
             _excluded_groups(excluded, scenario)),
        ]))
        blocks.append(_baseline_block(scenario_id, baseline_on))
        return html.Div(blocks, className="tradeoff tradeoff--nodef")

    sorted_surv = _sort_survivors(survivors, sort_key)
    controls = html.Div(
        [
            # A plain span, not a <label for>: the control's DOM id is a
            # serialised pattern-matching dict. The accessible name is
            # carried by aria-label on the Select itself.
            html.Span(C.ALT_SORT_LABEL, className="sort__label",
                      **{"aria-hidden": "true"}),
            dmc.Select(
                # Pattern-matching id: this control only exists once a
                # scenario with survivors is open, and Dash rejects a plain
                # string Input that is absent from the initial layout.
                id={"type": "sort-select", "index": "x"},
                value=sort_key,
                data=[{"value": k, "label": v} for k, v in C.SORT_KEYS.items()],
                allowDeselect=False,
                size="xs",
                className="sort__select",
                comboboxProps={"withinPortal": True},
                **{"aria-label": C.ALT_SORT_LABEL},
            ),
        ],
        className="sort-control",
    )

    n_excl = len(excluded)
    return html.Div(
        [
            _header(scenario, len(survivors), nodef=False),
            html.Div(C.NOT_RANKING_NOTE, className="tradeoff__framing"),
            controls,
            html.Div([_alternative_card(r.to_dict())
                      for _, r in sorted_surv.iterrows()],
                     className="alt-grid"),
            note(C.ALT_DISTANCE_NOTE, className="note--quiet note--distance"),
            disclosure([
                (f"{n_excl} {C.ALT_EXCLUDED_TITLE}",
                 _excluded_groups(excluded, scenario)),
                (C.RADIUS_TITLE, _radius_body(scenario_id) or
                 unavailable("No pre-registered reach sensitivity was "
                             "recorded for this scenario.")),
            ]),
            _baseline_block(scenario_id, baseline_on),
        ],
        className="tradeoff",
    )
