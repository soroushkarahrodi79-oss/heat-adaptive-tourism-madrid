"""Phase 4.1 implementation-contract tests.

These assert the app honours the locked data contract and the Phase 4.0
visual/decision guarantees. They do NOT re-test Phase 0-3 science.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pandas as pd
from dash import html

from app import constants as C
from app import data_loader as dl
from app.components import asset_panel, map_view, tradeoff

REPO_ROOT = Path(dl.REPO_ROOT)

# SHA-256 recorded in docs/PHASE4_1_IMPLEMENTATION_BASELINE.md §3.
BASELINE_HASHES = {
    "data/processed/phase3_asset_catalog.csv":
        "936d6dd51150e96d8c8445fec6910c40d273f005a99b5d945cff2f8b106b7b54",
    "data/processed/phase3_candidate_screening.csv":
        "deecfe44aa07f22cfc9d50718d090646943186befc246b5cc1a85be2f7fd28b2",
    "data/processed/phase3_scenarios.csv":
        "79ce49c174e9143cd937eaebb515be334efdf1e86989d65740e9d406200129cf",
    "data/processed/phase3_scenarios_summary.csv":
        "9b6c406d30d47308beeb824a6d27c71e7f3c7b60998beba7f05bff56845132be",
    "outputs/tables/phase3_exclusion_reasons.csv":
        "065babc59e0585c5f9693e4973ac213c3bfac92da68013858d98b4fa82b54f71",
    "outputs/tables/phase3_hati_vs_baseline.csv":
        "7ab737038c680144b472cabff2d4f6937d5bf2c6449cd3436f9ef5fc4dd28650",
    "outputs/tables/phase3_accessibility_sensitivity.csv":
        "2ded4494271d92aa2aefa63048b684cc1c05fc9ed79782d2adb8c062b0619ef0",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _text(component) -> str:
    """Flatten a Dash component tree to its visible text (best-effort)."""
    out = []

    def walk(node):
        if node is None:
            return
        if isinstance(node, (str, int, float)):
            out.append(str(node))
            return
        if isinstance(node, (list, tuple)):
            for n in node:
                walk(n)
            return
        # Dash component: recurse children + text-bearing props
        children = getattr(node, "children", None)
        walk(children)
        for prop in ("title",):
            v = getattr(node, prop, None)
            if isinstance(v, str):
                out.append(v)

    walk(component)
    return " ".join(out)


# ── 1. exactly the 3 valid timestamps ──────────────────────────────────────
def test_exactly_three_timestamps():
    assert C.TIMESTAMPS == ("12:00", "15:00", "18:00")
    scr = dl.frame("screening")
    assert sorted(scr["timestamp"].unique()) == ["12:00", "15:00", "18:00"]


# ── 2. 27 assets load ──────────────────────────────────────────────────────
def test_twenty_seven_assets():
    assert dl.frame("catalog")["asset_id"].nunique() == 27
    for ts in C.TIMESTAMPS:
        df = dl.assets_at_timestamp(ts)
        assert len(df) == 27
        assert len(map_view.build_markers(ts)) == 27


# ── 3. loader never writes to protected directories ────────────────────────
def test_loader_is_read_only():
    files = list(dl.DATA_FILES.values())
    before = {f: (f.stat().st_size, f.stat().st_mtime_ns, _sha256(f)) for f in files}
    # exercise a representative spread of loader operations
    for ts in C.TIMESTAMPS:
        dl.assets_at_timestamp(ts)
        dl.asset_record("A24", ts)
    for s in [f"S{i}" for i in range(1, 9)]:
        dl.scenario_candidates(s)
        dl.baseline_row(s)
        dl.accessibility_row(s)
        dl.summary_row(s)
    dl.known_exclusion_tokens()
    after = {f: (f.stat().st_size, f.stat().st_mtime_ns, _sha256(f)) for f in files}
    assert before == after
    # and there is no write path in the loader source itself
    src = (REPO_ROOT / "app" / "data_loader.py").read_text(encoding="utf-8")
    assert ".to_csv" not in src and ".to_parquet" not in src
    assert re.search(r"open\([^)]*['\"][wa]", src) is None


# ── 4. S8 -> NO_DEFENSIBLE_ALTERNATIVE, first-class panel ──────────────────
def test_s8_no_defensible():
    summ = dl.summary_row("S8")
    assert summ["source_id"] == "A20" and summ["timestamp"] == "15:00"
    assert int(summ["access_radius_m"]) == 500
    assert summ["recommendation"] == "NO_DEFENSIBLE_ALTERNATIVE"
    survivors, excluded = dl.scenario_candidates("S8")
    assert len(survivors) == 0 and len(excluded) > 0
    txt = _text(tradeoff.tradeoff_view("S8"))
    assert "No defensible alternative found." in txt
    assert "0 survived" in txt
    # must NOT be an error/retry/empty grid
    assert "try again" not in txt.lower() and "expand" not in txt.lower()


# ── 5. A24 @ 18:00 -> UNSTABLE treatment ───────────────────────────────────
def test_a24_1800_unstable():
    rec = dl.asset_record("A24", "18:00")
    assert rec["decision_confidence"] == "UNSTABLE"
    txt = _text(asset_panel.asset_panel("A24", "18:00"))
    assert "Genuine solar-boundary case" in txt
    # distinct from ordinary BOUNDARY: a BOUNDARY asset must not carry the flag
    boundary = dl.asset_record("A16", "15:00")
    assert boundary["decision_confidence"] == "BOUNDARY"
    btxt = _text(asset_panel.asset_panel("A16", "15:00"))
    assert "Genuine solar-boundary case" not in btxt


# ── 6. baseline mode reads the precomputed row ─────────────────────────────
def test_baseline_uses_precomputed_row():
    b = dl.baseline_row("S8")
    raw = pd.read_csv(REPO_ROOT / "outputs/tables/phase3_hati_vs_baseline.csv")
    raw_s8 = raw[raw["scenario"] == "S8"].iloc[0]
    assert b["baseline_pick_name"] == raw_s8["baseline_pick_name"]
    txt = _text(tradeoff.tradeoff_view("S8", baseline_on=True))
    assert str(raw_s8["baseline_pick_name"]) in txt
    assert "not recalculated" in txt.lower()


# ── 7. the five concepts remain separate fields + separate channels ────────
def test_concepts_stay_separate():
    scr = dl.frame("screening")
    for col in ["thermal_state", "decision_state", "decision_confidence",
                "evidence_confidence"]:
        assert col in scr.columns
    # channel maps are about different concepts and don't collapse:
    assert set(C.DECISION_STATE_COLOR) & set(C.CONFIDENCE_RING) == set()
    assert set(C.THERMAL_STATE_GLYPH) & set(C.DECISION_STATE_COLOR) == set()
    # same decision_state, different confidence => same fill, different ring.
    from app.components.primitives import marker_html
    a = {"decision_state": "AVOID_PROLONGED_OUTDOOR_EXPOSURE",
         "decision_confidence": "ROBUST", "thermal_state": "VERY_STRONG_HEAT_STRESS",
         "is_open": True}
    b = dict(a, decision_confidence="BOUNDARY")
    ha, hb = marker_html(a), marker_html(b)
    assert "--fill:#B5502E" in ha and "--fill:#B5502E" in hb  # same decision colour
    assert "ring-solid" in ha and "ring-dashed" in hb          # different confidence ring


# ── 8. no score / ranking / "best" anywhere ────────────────────────────────
def test_no_score_or_ranking_fields():
    forbidden_cols = re.compile(r"score|rank|rating|weight|\bbest\b", re.I)
    for key, path in dl.DATA_FILES.items():
        cols = pd.read_csv(path, nrows=0).columns
        bad = [c for c in cols if forbidden_cols.search(c)]
        assert not bad, f"{key}: forbidden-looking columns {bad}"
    # rendered View 3 must carry no ranking language / stars / "best option"
    txt = _text(tradeoff.tradeoff_view("S1")).lower()
    for bad in ["recommended", "best option", "★", "star rating", "top pick",
                "score:"]:
        assert bad not in txt
    assert "not ranking" in txt  # the explicit anti-ranking framing is present


# ── 9. no live / real-time / forecast wording in user-facing copy ──────────
def test_no_live_realtime_forecast_copy():
    # gather user-facing strings: constants + a rendered instance of each view
    strings = []
    for v in vars(C).values():
        if isinstance(v, str):
            strings.append(v)
        elif isinstance(v, dict):
            strings.extend(s for s in v.values() if isinstance(s, str))
        elif isinstance(v, (list, tuple)):
            strings.extend(s for s in v if isinstance(s, str))
    strings.append(_text(asset_panel.asset_panel("A01", "12:00")))
    strings.append(_text(tradeoff.tradeoff_view("S1")))
    blob = " ".join(strings).lower()
    # 'forecast'/'live' may appear ONLY inside the negated caption.
    allowed = "not live or forecast data"
    neutralised = blob.replace(allowed, " ")
    for word in ["real-time", "realtime", "forecast", "live data",
                 "current conditions", "up to the minute"]:
        assert word not in neutralised, f"forbidden liveness wording: {word!r}"


# ── 10. every exclusion token has a human-readable mapping ──────────────────
def test_every_exclusion_token_mapped():
    tokens = dl.known_exclusion_tokens()
    assert tokens, "expected at least one exclusion token in the data"
    missing = tokens - set(C.EXCLUSION_TRANSLATIONS)
    assert not missing, f"unmapped exclusion tokens: {missing}"
    for t in tokens:
        assert dl.translate_exclusion(t) != t or C.EXCLUSION_TRANSLATIONS[t] == t


# ── 11. protected-file hashes match the pre-implementation baseline ────────
def test_protected_file_hashes():
    for rel, expected in BASELINE_HASHES.items():
        got = _sha256(REPO_ROOT / rel)
        assert got == expected, f"{rel} changed since baseline (hash mismatch)"
