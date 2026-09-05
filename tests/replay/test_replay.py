import copy
import hashlib
import json
from pathlib import Path

import pytest

from app import constants as C, data_loader as dl
from app.components import replay, map_view
from app.replay_contract import IntegrityError, load_verified, manifest, validate_frames
from app.replay_state import normalize, transition

INITIAL = ("12:00", None, C.VIEW_MAP, None, "name", False)


def text(node):
    if isinstance(node, (str, int, float)):
        return str(node)
    if isinstance(node, (list, tuple)):
        return " ".join(text(n) for n in node)
    return text(getattr(node, "children", "")) if node is not None else ""


def test_snapshot_and_lineage():
    contract = manifest()
    frames = load_verified(dl.REPO_ROOT, dl.DATA_FILES)
    assert [len(frames[k]) for k in ("catalog", "screening", "scenarios")] == [27, 81, 208]
    for key, spec in contract["artifacts"].items():
        assert hashlib.sha256(dl.DATA_FILES[key].read_bytes()).hexdigest() == spec["sha256"]
        assert set(spec["source_column_lineage"]) == set(frames[key].columns)


@pytest.mark.parametrize("scenario,count", [(f"S{i}", n) for i, n in enumerate([9, 6, 4, 8, 7, 9, 6, 0], 1)])
def test_all_scenario_sets_map_and_list(scenario, count):
    row = dl.summary_row(scenario)
    survivors, excluded = dl.scenario_candidates(scenario)
    roles = replay.roles(scenario, row["timestamp"])
    assert {a for a, role in roles.items() if role == "CANDIDATE_ALTERNATIVE"} == set(survivors.candidate_id)
    assert {a for a, role in roles.items() if role == "EXCLUDED"} == set(excluded.candidate_id)
    assert list(roles.values()).count("SOURCE") == 1
    assert len(survivors) == count and len(excluded) == 26 - count
    markers = map_view.build_markers(row["timestamp"], row["source_id"], scenario)
    assert len(markers) == 27
    for m in markers:
        role = roles[m.id["index"]]
        assert f'data-role="{role}"' in m.iconOptions["html"]
        assert replay.ROLE_LABELS[role] in m.title
    rendered = text(replay.panel(scenario, row["source_id"]))
    for candidate in excluded.candidate_id:
        assert candidate in rendered


def test_a24_source_and_candidate_are_different():
    candidate = text(replay.panel("S4", "A24"))
    source = text(replay.panel("S7", "A24"))
    for rendered in (candidate, source):
        assert "UNSTABLE" in rendered and "LOW" in rendered
    assert "INSUFFICIENT_EVIDENCE" in candidate
    assert "Source — not evaluated as its own candidate" in source
    assert "scenario=S4; candidate_id=A24" in candidate
    assert "scenario=S7" in source


def test_s8_and_copy_ceiling():
    assert dict(dl.exclusion_breakdown("S8")) == {
        "ACCESSIBILITY_CONSTRAINT": 15, "OUTDOOR_EXPOSURE_TOO_HIGH": 6, "CLOSED_AT_TIMESTAMP": 5}
    rendered = text(replay.panel("S8", "A20"))
    assert "0 survivors" in rendered and "26 exclusions" in rendered
    assert "includes out-of-reach assets" in rendered
    for path in (dl.REPO_ROOT / "app").rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        for misleading in ("sending a heat-stressed visitor", "remain correct", "candidates evaluated within"):
            assert misleading not in source, path


@pytest.mark.parametrize("scenario", [f"S{i}" for i in range(1, 9)])
def test_state_invalidation_and_back(scenario):
    state = transition(INITIAL, "scenario", scenario)
    row = dl.summary_row(scenario)
    assert state[:4] == (row["timestamp"], row["source_id"], C.VIEW_ALTERNATIVES, scenario)
    candidate = next(a for a in dl.all_asset_ids() if a != row["source_id"])
    state = transition(state, "asset", candidate)
    assert state[3] == scenario
    assert transition(state, "back")[1] == row["source_id"]
    state = transition(state, "timestamp", "12:00")
    assert state[3] is None and transition(state, "back")[3] is None
    assert replay.roles(scenario, "12:00") == {}
    assert replay.context(None, "12:00") == "No precomputed scenario at this timestamp."


def test_invalid_state_and_close():
    assert normalize("bad", "A99", "bad", "S99", "score", True)[:4] == INITIAL[:4]
    state = transition(INITIAL, "scenario", "S1")
    assert transition(state, "close")[1:4] == (None, C.VIEW_MAP, None)
    assert normalize("12:00", "A16", C.VIEW_ALTERNATIVES, "S1", "name", False)[3] is None


def test_hash_failure_blocks_layout_without_touching_science(tmp_path, monkeypatch):
    files = {}
    for key, spec in manifest()["artifacts"].items():
        path = tmp_path / spec["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(dl.DATA_FILES[key].read_bytes())
        files[key] = path
    files["scenarios"].write_bytes(files["scenarios"].read_bytes() + b"\n")
    with pytest.raises(IntegrityError, match="SHA-256 mismatch"):
        load_verified(tmp_path, files)
    from app.app import _layout
    def fail():
        return load_verified(tmp_path, files)
    monkeypatch.setattr(dl, "_load_all", fail)
    layout = _layout()
    assert layout.id == "replay-integrity-error"
    assert "Scientific display is blocked" in text(layout)
    assert "A24" not in text(layout)


@pytest.mark.parametrize("fault", ["column", "duplicate", "binding", "enum"])
def test_schema_failures(fault):
    frames = {k: dl.frame(k) for k in dl.DATA_FILES}
    if fault == "column":
        frames["scenarios"] = frames["scenarios"].drop(columns=["status"])
    elif fault == "duplicate":
        frames["scenarios"].iloc[1] = frames["scenarios"].iloc[0]
    elif fault == "binding":
        frames["scenarios"].loc[0, "timestamp"] = "12:00"
    else:
        frames["screening"].loc[0, "decision_confidence"] = "SAFE"
    with pytest.raises(IntegrityError):
        validate_frames(frames, manifest())


def test_verified_snapshot_is_deterministic_and_defensive():
    first = {k: dl.frame(k).to_json() for k in dl.DATA_FILES}
    changed_copy = dl.frame("scenarios")
    changed_copy.loc[0, "status"] = "EXCLUDED"
    second = {k: dl.frame(k).to_json() for k in dl.DATA_FILES}
    assert first == second
    indoor = text(replay.panel("S1", "A01"))
    assert "Not physically modelled for indoor assets." in indoor


def test_no_new_scientific_runtime_dependencies():
    import ast
    for path in (dl.REPO_ROOT / "app").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        imports = [n.module or "" for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
        imports += [alias.name for n in ast.walk(tree) if isinstance(n, ast.Import) for alias in n.names]
        assert not any(x.startswith(("src", "requests", "httpx", "solweig")) for x in imports)
