"""UI state transitions only; no eligibility calculation."""
from . import constants as C
from . import data_loader as dl


def normalize(timestamp, asset, view, scenario, sort, baseline):
    timestamp = timestamp if timestamp in C.TIMESTAMPS else "12:00"
    asset = asset if asset in dl.all_asset_ids() else None
    row = dl.summary_row(scenario) if scenario else None
    if row is None or row["timestamp"] != timestamp:
        scenario = None
        if view == C.VIEW_ALTERNATIVES:
            view = C.VIEW_ASSET if asset else C.VIEW_MAP
    if view not in (C.VIEW_MAP, C.VIEW_ASSET, C.VIEW_ALTERNATIVES):
        view = C.VIEW_MAP
    if not asset:
        view, scenario = C.VIEW_MAP, None
    return timestamp, asset, view, scenario, sort if sort in C.SORT_KEYS else "name", bool(baseline)


def transition(state, kind, value=None):
    timestamp, asset, view, scenario, sort, baseline = normalize(*state)
    if kind == "timestamp":
        timestamp = value
        scenario, baseline = None, False
        view = C.VIEW_ASSET if asset else C.VIEW_MAP
    elif kind == "scenario":
        row = dl.summary_row(value)
        if row is not None:
            timestamp, asset, scenario = row["timestamp"], row["source_id"], value
            view, sort, baseline = C.VIEW_ALTERNATIVES, "name", False
    elif kind == "asset":
        asset, view = value, C.VIEW_ASSET
    elif kind == "back":
        row = dl.summary_row(scenario) if scenario else None
        if row is not None:
            asset, view = row["source_id"], C.VIEW_ALTERNATIVES
    elif kind == "close":
        asset, scenario, view, baseline = None, None, C.VIEW_MAP, False
    elif kind == "sort":
        sort = value
    elif kind == "baseline":
        baseline = value
    return normalize(timestamp, asset, view, scenario, sort, baseline)
