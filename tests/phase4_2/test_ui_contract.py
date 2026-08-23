"""Phase 4.2 UI/UX contract tests.

These assert the redesign's *interface* guarantees. They never re-test
Phase 0-3 science, and they never relax a Phase 4.1 assertion — the 4.1
suite still runs unchanged alongside this one.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pandas as pd
import pytest
from dash import html

from app import constants as C
from app import data_loader as dl
from app import theme as T
from app.components import (asset_panel, command_bar, empty_states, icons,
                            legend, limitations, map_view, primitives,
                            scenario_selector, shell, tradeoff)

REPO_ROOT = Path(dl.REPO_ROOT)
APP_DIR = REPO_ROOT / "app"
CSS = (APP_DIR / "assets" / "style.css").read_text(encoding="utf-8")


# ── helpers ────────────────────────────────────────────────────────────────
def flatten(component) -> str:
    """Visible text of a Dash/DMC component tree (best effort)."""
    out: list[str] = []

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
        walk(getattr(node, "children", None))
        for prop in ("title", "label", "placeholder", "nothingFoundMessage"):
            v = getattr(node, prop, None)
            if isinstance(v, str):
                out.append(v)
        data = getattr(node, "data", None)
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    out.extend(str(v) for v in item.values())
    walk(component)
    return " ".join(out)


def class_sequence(component) -> list[str]:
    """className values in DOM order."""
    seq: list[str] = []

    def walk(node):
        if node is None or isinstance(node, (str, int, float)):
            return
        if isinstance(node, (list, tuple)):
            for n in node:
                walk(n)
            return
        cls = getattr(node, "className", None)
        if isinstance(cls, str):
            seq.append(cls)
        walk(getattr(node, "children", None))
    walk(component)
    return seq


def every_view():
    """One rendered instance of every view state the interface can reach."""
    yield "layout", shell.page("12:00")
    for ts in C.TIMESTAMPS:
        yield f"asset-A01-{ts}", asset_panel.asset_panel("A01", ts)
        yield f"asset-A24-{ts}", asset_panel.asset_panel("A24", ts)
        yield f"asset-A20-{ts}", asset_panel.asset_panel("A20", ts)
    for s in [f"S{i}" for i in range(1, 9)]:
        for sort_key in C.SORT_KEYS:
            yield f"alt-{s}-{sort_key}", tradeoff.tradeoff_view(s, sort_key)
        yield f"alt-{s}-baseline", tradeoff.tradeoff_view(s, "distance", True)


# ═══ 1. Design tokens ══════════════════════════════════════════════════════
def test_theme_is_the_single_token_source():
    css_vars = T.css_variables()
    for name in ["--bg", "--surface", "--text-primary", "--decision-rust",
                 "--decision-teal", "--focus", "--selection", "--space-md",
                 "--radius-md", "--shadow-s2", "--motion-base"]:
        assert f"{name}:" in css_vars, f"{name} missing from the token layer"
    # The stylesheet must consume tokens, not redeclare them.
    assert not re.search(r"^\s*:root\s*\{", CSS, re.M), \
        "style.css must not redeclare :root tokens"
    assert "var(--surface)" in CSS and "var(--decision-rust)" in CSS


def test_no_literal_colours_in_component_modules():
    """A hex literal in a component is how a palette starts drifting."""
    offenders = {}
    for path in sorted(APP_DIR.glob("components/*.py")):
        hexes = re.findall(r"#[0-9A-Fa-f]{6}\b", path.read_text(encoding="utf-8"))
        if hexes:
            offenders[path.name] = hexes
    assert offenders == {}, offenders


def test_decision_hues_come_from_the_locked_palette():
    assert T.DECISION_RUST == C.DECISION_STATE_COLOR[
        "AVOID_PROLONGED_OUTDOOR_EXPOSURE"]
    assert T.DECISION_TEAL == C.DECISION_STATE_COLOR["INDOOR_REFUGE"]


def test_type_scale_is_small_and_has_no_1px_steps():
    scale = sorted(T.TYPE_SCALE)
    assert len(scale) <= 6
    steps = [round(b - a, 2) for a, b in zip(scale, scale[1:])]
    assert all(s >= 1.5 for s in steps), f"near-duplicate type sizes: {scale}"


# ═══ 2. Contrast floor ═════════════════════════════════════════════════════
def _luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    channels = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
           for c in channels]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def _contrast(a: str, b: str) -> float:
    la, lb = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


@pytest.mark.parametrize("fg,bg,name", [
    (T.TEXT_PRIMARY, T.SURFACE, "primary/surface"),
    (T.TEXT_PRIMARY, T.BG, "primary/bg"),
    (T.TEXT_SECONDARY, T.SURFACE, "secondary/surface"),
    (T.TEXT_SECONDARY, T.SURFACE_MUTED, "secondary/muted"),
    (T.TEXT_TERTIARY, T.SURFACE, "tertiary/surface"),
    (T.TEXT_TERTIARY, T.SURFACE_MUTED, "tertiary/muted"),
    (T.EXCLUDED_INK, T.SURFACE, "excluded/surface"),
    (T.EXCLUDED_INK, T.SURFACE_MUTED, "excluded/muted"),
    (T.UNCERTAINTY_ACCENT, T.SURFACE_MUTED, "uncertainty/muted"),
    (T.TEXT_INVERSE, T.SURFACE_INVERSE, "inverse/inverse"),
    (T.FOCUS, T.SURFACE, "focus/surface"),
])
def test_text_tokens_meet_aa(fg, bg, name):
    ratio = _contrast(fg, bg)
    assert ratio >= 4.5, f"{name} is {ratio:.2f}:1"


def test_excluded_ink_fixed_the_phase41_failure():
    """Phase 4.1 rendered excluded candidate names at 2.55:1."""
    assert _contrast("#9A948C", "#F0ECE2") < 4.5          # the old value
    assert _contrast(T.EXCLUDED_INK, T.SURFACE_MUTED) >= 4.5


# ═══ 3. Marker states ══════════════════════════════════════════════════════
BASE_REC = {
    "asset_id": "A16", "name": "Fuente de Neptuno",
    "decision_state": "AVOID_PROLONGED_OUTDOOR_EXPOSURE",
    "decision_confidence": "ROBUST",
    "thermal_state": "VERY_STRONG_HEAT_STRESS", "is_open": True,
}


def test_selected_marker_is_visually_distinct():
    plain = primitives.marker_html(BASE_REC)
    chosen = primitives.marker_html(BASE_REC, selected=True)
    assert plain != chosen
    assert "asset-marker--selected" in chosen
    assert "asset-marker--selected" not in plain
    # ...and the halo is styled, not merely class-named.
    assert ".asset-marker--selected" in CSS


def test_selection_uses_a_neutral_channel_not_a_data_hue():
    """The halo must never borrow the decision palette."""
    rule = CSS.split(".asset-marker--selected {")[1].split("}")[0]
    assert "--selection" in rule
    assert "--decision-rust" not in rule and "--decision-teal" not in rule
    assert T.SELECTION not in (T.DECISION_RUST, T.DECISION_TEAL)


def test_selection_survives_the_closed_dimming():
    assert ".asset-marker--selected.asset-marker--closed" in CSS


def test_exactly_one_marker_is_selected():
    for ts in C.TIMESTAMPS:
        markers = map_view.build_markers(ts, "A16")
        htmls = [m.iconOptions["html"] for m in markers]
        assert len(markers) == 27
        assert sum("asset-marker--selected" in h for h in htmls) == 1
    # ...and none when nothing is selected.
    assert all("asset-marker--selected" not in m.iconOptions["html"]
               for m in map_view.build_markers("12:00"))


def test_four_data_channels_stay_independent():
    a = primitives.marker_html(BASE_REC)
    b = primitives.marker_html(dict(BASE_REC, decision_confidence="UNSTABLE"))
    c = primitives.marker_html(dict(BASE_REC, thermal_state="INDOOR_NOT_MODELLED"))
    d = primitives.marker_html(dict(BASE_REC, is_open=False))
    assert f"--fill:{T.DECISION_RUST}" in a and f"--fill:{T.DECISION_RUST}" in b
    assert "ring-solid" in a and "ring-dotted" in b        # confidence only
    assert "ring-solid" in c                               # thermal ≠ ring
    assert "asset-marker--closed" in d and "ring-solid" in d
    # a selection halo changes none of the four
    s = primitives.marker_html(BASE_REC, selected=True)
    assert f"--fill:{T.DECISION_RUST}" in s and "ring-solid" in s


# ═══ 4. Marker accessibility ═══════════════════════════════════════════════
def test_every_marker_has_an_accessible_identity():
    for ts in C.TIMESTAMPS:
        for m in map_view.build_markers(ts):
            html_str = m.iconOptions["html"]
            assert 'role="img"' in html_str
            assert 'aria-label="' in html_str
            assert m.title and m.alt
            assert m.keyboard is True          # tab-focusable


def test_marker_label_carries_all_four_channels_in_words():
    for ts in C.TIMESTAMPS:
        df = dl.assets_at_timestamp(ts)
        for _, row in df.iterrows():
            label = primitives.marker_aria_label(row.to_dict())
            assert str(row["asset_id"]) in label
            assert str(row["name"]) in label
            assert "Decision:" in label and "Decision confidence:" in label
            assert "Thermal condition:" in label
            assert ("Open at this timestamp" in label
                    or "Closed at this timestamp" in label)


def test_keyboard_activation_is_implemented_not_assumed():
    """Leaflet's own keypress→click path does not fire for these markers."""
    js = (APP_DIR / "assets" / "keyboard.js").read_text(encoding="utf-8")
    assert "leaflet-marker-icon" in js
    assert '"Enter"' in js and '" "' in js
    assert "mousedown" in js       # a bare click() is swallowed after a drag


def test_a_pointer_free_path_to_every_asset_exists():
    for ts in C.TIMESTAMPS:
        options = dl.asset_options(ts)
        assert len(options) == 27
        assert {o["value"] for o in options} == set(dl.all_asset_ids())
    picker = command_bar.asset_picker("12:00")
    assert picker.searchable is True


# ═══ 5. Panel hierarchy — decision before metadata ═════════════════════════
def test_decision_precedes_the_supporting_facts():
    for ts in C.TIMESTAMPS:
        seq = class_sequence(asset_panel.asset_panel("A16", ts))
        idx = {k: next((i for i, c in enumerate(seq) if k in c), -1)
               for k in ["panel__header", "block--decision", "block--confidence",
                         "block--thermal", "block--evidence", "alt-cta",
                         "hati-disclosure"]}
        assert -1 not in idx.values(), idx
        assert (idx["panel__header"] < idx["block--decision"]
                < idx["block--confidence"] < idx["block--thermal"]
                < idx["block--evidence"] < idx["hati-disclosure"]), idx


def test_five_concepts_keep_five_separate_blocks():
    seq = class_sequence(asset_panel.asset_panel("A16", "15:00"))
    for block in ["block--decision", "block--confidence", "block--thermal",
                  "block--evidence"]:
        assert sum(block in c for c in seq) == 1, block
    # the fifth concept (exclusion) appears in the trace when the row has one
    closed = dl.asset_record("A03", "18:00")
    if str(closed.get("context_free_exclusion_reason", "")).strip():
        assert "exclusion" in " ".join(
            class_sequence(asset_panel.asset_panel("A03", "18:00")))


def test_headline_facts_are_static_rows_not_disclosures():
    """Tiers A and B must never be hidden behind an accordion."""
    panel = asset_panel.asset_panel("A16", "15:00")
    tier_c = []

    def collect(node, inside=False):
        if node is None or isinstance(node, (str, int, float)):
            return
        if isinstance(node, (list, tuple)):
            for n in node:
                collect(n, inside)
            return
        cls = getattr(node, "className", "") or ""
        here = inside or "hati-disclosure" in cls
        if here and isinstance(cls, str) and cls.startswith("block--"):
            tier_c.append(cls)
        collect(getattr(node, "children", None), here)

    collect(panel)
    assert not tier_c, f"headline blocks hidden in a disclosure: {tier_c}"


def test_the_decision_is_the_largest_element_in_the_panel():
    decision = re.search(r"\.decision__text \{[^}]*font-size:\s*([\d.]+)px", CSS)
    confidence = re.search(r"\.confidence__name \{[^}]*font-size:\s*([\d.]+)px", CSS)
    thermal = re.search(r"\.thermal__state \{[^}]*font-size:\s*([\d.]+)px", CSS)
    assert decision and confidence and thermal
    assert float(decision.group(1)) > float(confidence.group(1))
    assert float(decision.group(1)) > float(thermal.group(1))


# ═══ 6. Scenario access ════════════════════════════════════════════════════
def test_scenario_menu_replaces_the_permanent_chip_row():
    page = shell.page("12:00")
    seq = " ".join(class_sequence(page))
    assert "jump-chip" not in seq and "chips-row" not in seq
    assert "limstrip" not in seq          # the permanent Tier-1 strip is gone
    menu = scenario_selector.scenario_menu()
    assert flatten(menu).count("S1") >= 1


def test_scenario_options_are_exactly_the_precomputed_eight():
    opts = dl.scenario_options()
    summary = pd.read_csv(REPO_ROOT / "data/processed/phase3_scenarios_summary.csv")
    assert len(opts) == len(summary) == 8
    for o in opts:
        row = summary[summary["scenario"] == o["scenario"]].iloc[0]
        assert o["source_id"] == row["source_id"]
        assert o["timestamp"] == row["timestamp"]
        assert o["n_alternatives"] == int(row["n_candidate_alternatives"])
        assert o["recommendation"] == row["recommendation"]


def test_menu_states_the_outcome_without_ranking_the_scenarios():
    text = flatten(scenario_selector.scenario_menu("S1")).lower()
    assert "no defensible alternative" in text
    for bad in ["best", "top ", "recommended", "worst", "#1"]:
        assert bad not in text


# ═══ 7. Sorting is organisation, never ranking ═════════════════════════════
def test_sort_keys_are_all_visible_row_attributes():
    assert set(C.SORT_KEYS) == {"distance", "name", "indoor_outdoor",
                                "experience_type"}
    forbidden = re.compile(r"score|rank|rating|best|weight|priority", re.I)
    assert not any(forbidden.search(k) or forbidden.search(v)
                   for k, v in C.SORT_KEYS.items())


def test_sorting_only_reorders_and_never_drops_a_survivor():
    for s in [f"S{i}" for i in range(1, 8)]:
        survivors, _ = dl.scenario_candidates(s)
        ids = set(survivors["candidate_id"])
        for key in C.SORT_KEYS:
            got = tradeoff._sort_survivors(survivors, key)
            assert set(got["candidate_id"]) == ids
            assert len(got) == len(survivors)


def test_cards_carry_no_ordinal_or_superlative():
    for s in [f"S{i}" for i in range(1, 8)]:
        text = flatten(tradeoff.tradeoff_view(s)).lower()
        assert "not ranking" in text
        for bad in ["1st", "2nd", "best", "top pick", "recommended",
                    "runner-up", "★", "highest", "optimal", "winner"]:
            assert bad not in text, (s, bad)


# ═══ 8. S8 — NO_DEFENSIBLE_ALTERNATIVE ═════════════════════════════════════
def test_s8_is_a_designed_result_not_an_error():
    text = flatten(tradeoff.tradeoff_view("S8"))
    low = text.lower()
    assert C.NODEF_HEADLINE in text
    assert "0" in text and "survived all gates" in low
    assert "not a failed search" in low
    # never an error, never a retry, never a radius control
    for bad in ["try again", "expand", "widen", "increase the radius", "oops",
                "something went wrong", "no results found", "error", "retry"]:
        assert bad not in low, bad


def test_s8_headline_appears_once():
    assert flatten(tradeoff.tradeoff_view("S8")).count(C.NODEF_HEADLINE) == 1


def test_s8_breakdown_counts_match_the_locked_column():
    raw = pd.read_csv(REPO_ROOT / "data/processed/phase3_scenarios.csv")
    s8 = raw[(raw["scenario"] == "S8") & (raw["status"] == "EXCLUDED")]
    expected = s8["exclusion_reason"].value_counts().to_dict()
    assert dict(dl.exclusion_breakdown("S8")) == expected
    assert sum(expected.values()) == 26
    text = flatten(tradeoff.tradeoff_view("S8"))
    for token, n in expected.items():
        assert C.EXCLUSION_TRANSLATIONS[token] in text
        assert str(n) in text


def test_s8_shows_the_precomputed_reach_sensitivity_only():
    acc = pd.read_csv(REPO_ROOT / "outputs/tables/phase3_accessibility_sensitivity.csv")
    row = acc[acc["scenario"] == "S8"].iloc[0]
    text = flatten(tradeoff.tradeoff_view("S8"))
    for col, label in [("n_alt_500m", "500 m"), ("n_alt_800m", "800 m"),
                       ("n_alt_1200m", "1200 m")]:
        assert label in text and str(int(row[col])) in text
    assert "not adjustable" in text.lower()


def test_no_radius_or_threshold_input_exists_anywhere():
    """A control here would turn read-only evidence into a recomputation."""
    for name, view in every_view():
        def walk(node):
            if node is None or isinstance(node, (str, int, float)):
                return
            if isinstance(node, (list, tuple)):
                for n in node:
                    walk(n)
                return
            t = type(node).__name__
            assert t not in ("Slider", "RangeSlider", "NumberInput",
                             "Input", "Textarea"), f"{name}: {t}"
            walk(getattr(node, "children", None))
        walk(view)


# ═══ 9. A24 @ 18:00 — uncertainty, not alarm ═══════════════════════════════
def test_a24_1800_is_distinct_from_ordinary_boundary():
    a24 = flatten(asset_panel.asset_panel("A24", "18:00"))
    assert "Genuine solar-boundary case" in a24
    assert "Unstable" in a24 and "UNSTABLE" in a24
    boundary = flatten(asset_panel.asset_panel("A16", "15:00"))
    assert "Genuine solar-boundary case" not in boundary
    assert "Boundary" in boundary
    # ring style differs on the map too
    rec24 = dl.asset_record("A24", "18:00")
    rec16 = dl.asset_record("A16", "15:00")
    assert "ring-dotted" in primitives.marker_html(rec24)
    assert "ring-dashed" in primitives.marker_html(rec16)


def test_unstable_is_not_dramatised_as_danger():
    text = flatten(asset_panel.asset_panel("A24", "18:00")).lower()
    assert "not a statement about physical danger" in text
    for bad in ["danger", "warning", "alert", "hazard", "critical", "severe",
                "unsafe", "risk of"]:
        assert bad not in text.replace("not a statement about physical danger",
                                       " "), bad
    # ...and the styling uses the ochre accent, never red
    assert "--uncertainty-accent" in CSS
    rule = CSS.split(".block--unstable {")[1].split("}")[0]
    assert "background" not in rule, "UNSTABLE must not get an alarm fill"


# ═══ 10. Baseline ══════════════════════════════════════════════════════════
def test_baseline_is_off_by_default_and_precomputed():
    for s in [f"S{i}" for i in range(1, 9)]:
        off = flatten(tradeoff.tradeoff_view(s, "distance", False))
        on = flatten(tradeoff.tradeoff_view(s, "distance", True))
        assert C.BASELINE_LABEL in off
        assert "Baseline pick" not in off          # nothing rendered until asked
        assert "Baseline pick" in on
        assert "not recalculated" in on.lower()
        row = dl.baseline_row(s)
        assert str(row["baseline_pick_name"]) in on


def test_baseline_never_declares_a_winner():
    for s in [f"S{i}" for i in range(1, 9)]:
        text = flatten(tradeoff.tradeoff_view(s, "distance", True)).lower()
        assert "neither is labelled preferable" in text
        for bad in ["winner", "beats", "outperform", "better than", "superior",
                    "wins"]:
            assert bad not in text, (s, bad)


# ═══ 11. Copy audit across every reachable view ════════════════════════════
FORBIDDEN_COPY = [
    "oops", "something went wrong", "great choice", "recommended for you",
    "you might like", "we suggest", "our pick", "best option", "top pick",
    "overall risk", "risk score", "confidence score", "% confident",
]


def test_no_consumer_ux_or_score_language_anywhere():
    for name, view in every_view():
        low = flatten(view).lower()
        for bad in FORBIDDEN_COPY:
            assert bad not in low, f"{name}: {bad!r}"


def test_no_liveness_claim_anywhere():
    allowed = C.NOT_LIVE_CAPTION.lower()
    for name, view in every_view():
        low = flatten(view).lower().replace(allowed, " ")
        low = low.replace("not live or forecast data", " ")
        for bad in ["real-time", "realtime", "forecast", "live data",
                    "current conditions", "right now", "up to the minute",
                    "today's", "currently"]:
            assert bad not in low, f"{name}: {bad!r}"


def test_new_constants_carry_no_forbidden_wording():
    blob = " ".join(
        s for v in vars(C).values()
        for s in ([v] if isinstance(v, str)
                  else list(v.values()) if isinstance(v, dict)
                  else list(v) if isinstance(v, (list, tuple)) else [])
        if isinstance(s, str)
    ).lower().replace(C.NOT_LIVE_CAPTION.lower(), " ")
    for bad in FORBIDDEN_COPY + ["real-time", "forecast", "live data"]:
        assert bad not in blob, bad


def test_plain_language_leads_and_the_token_follows():
    explainer = primitives.exclusion_explainer("OUTDOOR_EXPOSURE_TOO_HIGH")
    text = flatten(explainer)
    plain = C.EXCLUSION_TRANSLATIONS["OUTDOOR_EXPOSURE_TOO_HIGH"]
    assert text.index(plain) < text.index("OUTDOOR_EXPOSURE_TOO_HIGH")


# ═══ 12. Token → copy coverage ═════════════════════════════════════════════
def test_every_category_and_experience_token_has_a_label():
    cat = set(dl.frame("catalog")["tourism_category"].dropna().astype(str))
    assert cat <= set(C.TOURISM_CATEGORY_LABEL), cat - set(C.TOURISM_CATEGORY_LABEL)
    exp = set(dl.frame("scenarios")["experience_type"].dropna().astype(str))
    exp = {e for e in exp if e.strip()}
    assert exp <= set(C.EXPERIENCE_TYPE_LABEL), exp - set(C.EXPERIENCE_TYPE_LABEL)


def test_every_confidence_and_thermal_token_has_a_label():
    scr = dl.frame("screening")
    assert set(scr["decision_confidence"].astype(str)) <= set(C.CONFIDENCE_SHORT)
    assert set(scr["decision_confidence"].astype(str)) <= set(C.CONFIDENCE_GLOSS)
    assert set(scr["thermal_state"].astype(str)) <= set(C.THERMAL_STATE_LABEL)
    assert set(scr["decision_state"].astype(str)) <= set(C.DECISION_STATE_LABEL)


# ═══ 13. Progressive disclosure ════════════════════════════════════════════
def test_limitations_are_one_interaction_away_and_complete():
    drawer = limitations.limitations_drawer()
    text = flatten(drawer)
    assert len(C.TIER2_LIMITATIONS) == 7
    for item in C.TIER2_LIMITATIONS:
        assert item in text
    assert C.TIER2_SOURCE_NOTE in text
    assert drawer.opened is False and drawer.closeOnEscape is True
    # reachable from the permanent chrome
    assert "limitations-open" in str(shell.page("12:00"))


def test_tier1_limitations_survive_the_strip_removal():
    """Each context line must still be rendered where it applies."""
    assert C.TIER1_LIMITATIONS["map"] in flatten(legend.symbols_body())
    alt = flatten(tradeoff.tradeoff_view("S1")).lower()
    assert "straight-line" in alt and "walking-route heat" in alt
    panel = flatten(asset_panel.asset_panel("A16", "15:00"))
    assert "2026-documented" in panel


def test_the_legend_never_hides_the_critical_encoding():
    compact = flatten(legend.compact_legend())
    assert "Avoid outdoor" in compact and "Indoor refuge" in compact
    assert "decision confidence" in compact and "thermal condition" in compact
    full = flatten(legend.symbols_body())
    for name, _, field in C.LEGEND_CHANNELS:
        assert name in full and field in full
    assert C.LEGEND_SELECTION_NOTE in full        # halo declared as interface


def test_disclosures_are_closed_by_default():
    for name, view in every_view():
        def walk(node):
            if node is None or isinstance(node, (str, int, float)):
                return
            if isinstance(node, (list, tuple)):
                for n in node:
                    walk(n)
                return
            if type(node).__name__ == "Accordion":
                assert getattr(node, "value", None) in (None, [], ""), name
            walk(getattr(node, "children", None))
        walk(view)


# ═══ 14. Responsive contract ═══════════════════════════════════════════════
def test_panel_widths_are_fluid_not_fixed():
    assert "clamp(360px, 28vw, 440px)" in CSS
    assert "clamp(420px, 34vw, 560px)" in CSS
    assert T.PANEL_CLASS_ASSET.split("--")[-1] in CSS


def test_a_bottom_sheet_replaces_the_rail_on_small_screens():
    assert "@media (max-width: 699px)" in CSS
    small = CSS.split("@media (max-width: 699px)")[1]
    assert "flex-direction: column" in small
    assert "55vh" in small           # the map keeps the top of the screen


def test_the_map_is_never_given_a_fixed_pixel_height():
    assert not re.search(r"\.map-wrap\s*\{[^}]*height:\s*\d+px", CSS)


def test_reduced_motion_is_respected():
    assert "prefers-reduced-motion: reduce" in CSS
    block = CSS.split("prefers-reduced-motion: reduce")[1].split("\n}")[0]
    assert "transition-duration: 1ms" in block


def test_focus_is_never_removed_without_a_replacement():
    assert ":focus-visible" in CSS
    assert "--focus" in CSS
    stripped = re.sub(r"/\*.*?\*/", "", CSS, flags=re.S)
    for selector, _body in re.findall(
            r"([^{}]+)\{([^}]*outline:\s*none[^}]*)\}", stripped):
        selector = selector.strip()
        # A round marker draws its ring on the marker body instead; every
        # other :focus rule must supply a visible replacement.
        assert (":focus" not in selector
                or "leaflet-marker-icon" in selector), selector
    assert ".leaflet-marker-icon:focus-visible .asset-marker" in CSS


# ═══ 15. Read-only guarantee, app-wide ═════════════════════════════════════
def test_no_module_in_the_app_can_write():
    for path in sorted(APP_DIR.rglob("*.py")):
        src = path.read_text(encoding="utf-8")
        assert ".to_csv" not in src, path
        assert ".to_parquet" not in src, path
        assert not re.search(r"\bopen\([^)]*['\"][wax]", src), path
        assert "shutil" not in src and "os.remove" not in src, path


def test_the_data_surface_is_still_exactly_seven_files():
    assert len(dl.DATA_FILES) == 7
    for path in dl.DATA_FILES.values():
        assert path.exists()


# ═══ 16. Protected artefacts ═══════════════════════════════════════════════
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


def test_phase3_hashes_unchanged_by_the_redesign():
    for rel, expected in BASELINE_HASHES.items():
        got = hashlib.sha256((REPO_ROOT / rel).read_bytes()).hexdigest()
        assert got == expected, rel


def test_rendering_every_view_does_not_touch_a_protected_file():
    before = {p: (p.stat().st_size, p.stat().st_mtime_ns)
              for p in dl.DATA_FILES.values()}
    for _ in every_view():
        pass
    for ts in C.TIMESTAMPS:
        map_view.build_markers(ts, "A16")
    after = {p: (p.stat().st_size, p.stat().st_mtime_ns)
             for p in dl.DATA_FILES.values()}
    assert before == after


# ═══ 17. Wiring ════════════════════════════════════════════════════════════
def test_layout_and_callbacks():
    from app.app import app
    layout = app.layout() if callable(app.layout) else app.layout
    assert isinstance(layout, html.Div)
    assert len(app.callback_map) >= 7
    # the marker renderer must see the selection, or selection cannot show
    marker_cb = next(v for k, v in app.callback_map.items()
                     if "asset-markers" in k)
    inputs = [i["id"] for i in marker_cb["inputs"]]
    assert "store-timestamp" in inputs and "store-selected-asset" in inputs


def test_map_container_is_built_once_and_only_children_swap():
    src = (APP_DIR / "app.py").read_text(encoding="utf-8")
    assert 'Output("asset-markers", "children")' in src
    assert 'Output("map-canvas"' not in src        # never rebuild the container
    assert 'Output("side-panel-body", "children")' in src


def test_icons_are_local_with_no_network_dependency():
    """dash-iconify resolves every icon over the network at render time."""
    for path in sorted(APP_DIR.rglob("*.py")):
        src = path.read_text(encoding="utf-8")
        assert not re.search(r"^\s*(import|from)\s+dash_iconify", src, re.M), path
    reqs = (REPO_ROOT / "app" / "requirements.txt").read_text(encoding="utf-8")
    assert not re.search(r"^dash-iconify", reqs, re.M)
    assert len(icons.available()) >= 10
    for name in icons.available():
        assert icons.icon(name) is not None
    # nothing in the served assets reaches for a remote host
    for asset in sorted((APP_DIR / "assets").iterdir()):
        text = asset.read_text(encoding="utf-8")
        assert "api.iconify.design" not in text, asset
        assert not re.search(r"@import\s+url\(https?:", text), asset


def test_empty_states_are_deliberate():
    assert C.EMPTY_ASSET_NOT_FOUND and "oops" not in C.EMPTY_ASSET_NOT_FOUND.lower()
    missing = asset_panel.asset_panel("A99", "12:00")
    assert C.EMPTY_ASSET_NOT_FOUND in flatten(missing)
    assert C.EMPTY_SCENARIO_NOT_FOUND in flatten(tradeoff.tradeoff_view("S99"))
    # an asset that is not a scenario source gets a reason, not a dead button
    text = flatten(asset_panel.asset_panel("A01", "12:00"))
    assert "not a scenario source" in text
    assert "0.0 °C" not in text                    # never an invented indoor UTCI
    assert C.MAP_TILE_FALLBACK in flatten(legend.tile_fallback_notice())
