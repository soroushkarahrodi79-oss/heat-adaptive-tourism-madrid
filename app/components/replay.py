"""Linked scenario inspection. Every scientific field is a recorded lookup."""
from dash import html

from .. import data_loader as dl
from ..replay_contract import manifest
from .primitives import field_row, is_blank

ROLE_LABELS = {"SOURCE": "Source", "CANDIDATE_ALTERNATIVE": "Survivor", "EXCLUDED": "Excluded"}
ROLE_BADGES = {"SOURCE": "SRC", "CANDIDATE_ALTERNATIVE": "IN", "EXCLUDED": "OUT"}


def roles(scenario, timestamp):
    row = dl.summary_row(scenario) if scenario else None
    if row is None or row["timestamp"] != timestamp:
        return {}
    survivors, excluded = dl.scenario_candidates(scenario)
    result = {row["source_id"]: "SOURCE"}
    result.update({r.candidate_id: r.status for _, r in survivors.iterrows()})
    result.update({r.candidate_id: r.status for _, r in excluded.iterrows()})
    return result


def context(scenario, timestamp):
    row = dl.summary_row(scenario) if scenario else None
    if row is None or row["timestamp"] != timestamp:
        return "No precomputed scenario at this timestamp." if timestamp == "12:00" else "Asset-state inspection · select a recorded scenario to inspect eligibility."
    return (f"{scenario} · source {row['source_id']} · {timestamp} · fixed {int(row['access_radius_m'])} m reach. "
            "Scenario badges: SRC source · IN survivor · OUT excluded. Thermal glyph, decision colour and confidence ring are unchanged.")


def provenance(key, identity, fields=None):
    contract = manifest()
    spec = contract["artifacts"][key]
    commit = contract["scientific_commit"]
    url = f"https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/blob/{commit}/{spec['path']}"
    columns = fields or spec["columns"]
    return html.Details([
        html.Summary(f"Pinned source record · {identity}"),
        html.P(["Artifact: ", html.A(spec["path"], href=url, target="_blank", rel="noopener noreferrer")]),
        html.P(f"Row key: {identity}"),
        html.P(f"Scientific commit: {commit}"),
        html.P(f"SHA-256: {spec['sha256']}"),
        html.P("Columns read unchanged: " + ", ".join(columns)),
        html.P("Schema " + contract["schema_version"] + " · UI foundation " + contract["phase4_2_ui_commit"]),
    ], className="replay-provenance", **{"data-artifact": key})


def asset_provenance(asset, timestamp):
    return html.Div([
        provenance("screening", f"asset_id={asset}; timestamp={timestamp}"),
        provenance("catalog", f"asset_id={asset}"),
    ])


def _button(asset, name, role, selected):
    return html.Button([
        html.Span(ROLE_BADGES[role], className="replay-list-badge", **{"aria-hidden": "true"}),
        html.Span(f"{asset} · {name}"),
        html.Span(ROLE_LABELS[role], className="replay-list-role"),
    ], id={"type": "card-open-asset", "index": asset}, n_clicks=0,
        className="replay-candidate" + (" replay-candidate--selected" if selected else ""),
        **{"aria-label": f"Inspect {asset} {name}: {ROLE_LABELS[role]}",
           "aria-pressed": str(selected).lower(), "data-role": role, "data-asset": asset})


def panel(scenario, selected):
    row = dl.summary_row(scenario)
    timestamp, source = row["timestamp"], row["source_id"]
    survivors, excluded = dl.scenario_candidates(scenario)
    selected = selected or source
    rec = dl.asset_record(selected, timestamp)
    candidates = dl.frame("scenarios")
    hit = candidates[(candidates.scenario == scenario) & (candidates.candidate_id == selected)]
    candidate = None if hit.empty else hit.iloc[0].to_dict()
    role = "SOURCE" if selected == source else candidate["status"]
    facts = []
    if candidate is not None:
        facts += [field_row("Scenario status", candidate["status"], mono=True),
                  field_row("Recorded first failure", candidate["exclusion_reason"] if role == "EXCLUDED" else "None recorded — survived", mono=True),
                  field_row("Recorded straight-line distance", f"{candidate['distance_m']:g} m")]
        values = [("Thermal state", "cand_thermal_state"), ("Decision state", "cand_decision_state"),
                  ("Decision confidence", "cand_decision_confidence"), ("Evidence confidence", "cand_evidence_confidence")]
        facts += [field_row(label, candidate[column], mono=True) for label, column in values]
        if not is_blank(candidate["improvement_note"]):
            facts.append(field_row("Recorded improvement note", candidate["improvement_note"]))
        record_source = provenance("scenarios", f"scenario={scenario}; candidate_id={selected}")
    else:
        facts += [field_row("Scenario role", "Source — not evaluated as its own candidate")]
        facts += [field_row(label, rec[column], mono=True) for label, column in
                  [("Thermal state", "thermal_state"), ("Decision state", "decision_state"),
                   ("Decision confidence", "decision_confidence"), ("Evidence confidence", "evidence_confidence")]]
        record_source = provenance("summary", f"scenario={scenario}")
    facts += [field_row("UTCI (model-derived)", "Not physically modelled for indoor assets." if is_blank(rec["utci_baseline"]) else f"{rec['utci_baseline']:g} °C"),
              field_row("Thermal evidence", rec["thermal_evidence"]),
              field_row("Opening-hours evidence", rec["opening_hours_evidence"]),
              field_row("Documented hours source", rec["opening_hours_source"]),
              field_row("Context-free status (separate from scenario)", rec["screening_status"], mono=True)]
    if not is_blank(rec["utci_envelope_low"]):
        facts.append(field_row("Recorded tested envelope", f"{rec['utci_envelope_low']:g}–{rec['utci_envelope_high']:g} °C"))
    breakdown = html.Ul([html.Li(f"{token}: {count}") for token, count in dl.exclusion_breakdown(scenario)])
    buttons = []
    # ID order is stable display organization; never an evaluative ranking.
    for _, c in candidates[candidates.scenario == scenario].sort_values("candidate_id").iterrows():
        buttons.append(html.Li(_button(c.candidate_id, c.candidate_name, c.status, selected == c.candidate_id)))
    return html.Div([
        html.Div([
            html.Button("Back to scenario overview", id={"type": "back-asset", "index": "x"}, n_clicks=0, className="panel__back"),
            html.Button("Close inspection", id={"type": "close-panel", "index": "x"}, n_clicks=0, className="panel__back"),
        ], className="replay-nav"),
        html.H2(f"{scenario} · Recorded screening", id="replay-title"),
        html.P(f"Source: {source} · {row['source_name']} · {timestamp} Madrid local · 21 August 2023"),
        html.P(f"{len(survivors)} survivors · {len(excluded)} exclusions · 26 candidates evaluated", id="replay-tally", role="status"),
        html.P(f"Fixed {int(row['access_radius_m'])} m straight-line reach is one screening constraint; the 26-candidate universe includes out-of-reach assets."),
        html.P("NO_DEFENSIBLE_ALTERNATIVE · No defensible alternative found." if not len(survivors) else "ALTERNATIVES_FOUND", className="replay-outcome"),
        html.P("Historical screening only. Eligibility is distinct from thermal state. Confidence is tested stability, not safety or eligibility."),
        html.P([html.A("Jump to candidate list", href="#replay-candidates"), " · ",
                html.A("Jump to selected evidence", href="#replay-selected-title")]),
        html.Section([
            html.H3(f"{selected} · {rec['name']} · {ROLE_LABELS[role]}", id="replay-selected-title", tabIndex=-1),
            html.Div(facts, id="replay-facts", **{"aria-live": "polite"}),
            html.P("Recorded final status and first failure only; later gate outcomes are not reconstructed."),
            record_source, asset_provenance(selected, timestamp),
        ], id="replay-evidence", **{"aria-label": "Selected record evidence and provenance"}),
        html.Details([html.Summary("Recorded exclusion groups"), breakdown]),
        html.H3("Source"), _button(source, row["source_name"], "SOURCE", selected == source),
        html.H3("All 26 candidates"),
        html.P("Asset ID order, not ranking. IN = survivor; OUT = excluded. All remain on the map."),
        html.Ul(buttons, id="replay-candidates", className="replay-candidates"),
        html.Details([html.Summary("Replay limitations and methods"),
                      html.Ul([html.Li(x) for x in manifest()["limitations"]]),
                      html.P("Methods: " + "; ".join(manifest()["method_references"]))]),
    ], className="replay-panel", **{"data-scenario": scenario, "data-timestamp": timestamp})
