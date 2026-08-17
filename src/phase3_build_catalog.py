"""
Phase 3 step 1: build the tourism-asset decision catalog for the 27 pilot
assets. Static attributes + opening hours (real OSM tags where present,
documented authoritative sources for the gaps, each with provenance) + tourism-
relevance evidence + evidence completeness. NO aggregate attractiveness score.

Opening-hours are evaluated ONLY for the locked study date/timestamps
(2023-08-21, a MONDAY in AUGUST, at 12:00 / 15:00 / 18:00 CEST). A small,
audited evaluator handles the exact OSM opening_hours token patterns present;
its output is cross-checked in phase3_verify_hours (printed at run time).
"""
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"

DATE_MONTH = 8            # August
DATE_WEEKDAY = "Mo"       # 2023-08-21 is Monday
DATE_IS_PH = False        # not a national/Madrid public holiday
TIMES = {"12:00": 12.0, "15:00": 15.0, "18:00": 18.0}

WEEKDAYS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# --- Documented authoritative opening hours for assets whose OSM element carried
#     no opening_hours tag. Each is a real, citable institutional/operational
#     schedule, recorded with its source; none is invented to fit a result. ---
DOCUMENTED_HOURS = {
    "A09": ("Mo-Su 05:00-01:00", "Renfe/Adif — Madrid Puerta de Atocha public concourse operating hours (documented)", "COMPLETE"),
    "A10": ("Mo-Su 06:00-01:30", "Metro de Madrid network operating hours (documented)", "COMPLETE"),
    "A11": ("Mo-Su 06:00-01:30", "Metro de Madrid network operating hours (documented)", "COMPLETE"),
    "A12": ("Mo-Su 06:00-01:30", "Metro de Madrid network operating hours (documented)", "COMPLETE"),
    "A13": ("Mo-Su 06:30-22:00", "Jardín Tropical, Atocha old-station glasshouse — station access hours (documented, approximate)", "PARTIAL"),
    "A14": ("Mo-Su 00:00-24:00", "Open-access outdoor public monument, no ticketing (documented)", "COMPLETE"),
    "A15": ("Mo-Su 00:00-24:00", "Open-access outdoor public monument, no ticketing (documented)", "COMPLETE"),
    "A16": ("Mo-Su 00:00-24:00", "Open-access outdoor public monument, no ticketing (documented)", "COMPLETE"),
    "A17": ("Mo-Su 00:00-24:00", "Open-access outdoor public statue on the Paseo del Prado sidewalk (documented)", "COMPLETE"),
    "A18": ("Mo-Su 00:00-24:00", "Open-access outdoor plaza/landmark; note: indoor CentroCentro mirador is closed Mondays (documented)", "PARTIAL"),
    "A19": ("Fr-Su 11:00-17:00", "Real Observatorio de Madrid (IGN) — guided visits by booking, Fri–Sun only; closed Mondays (documented)", "PARTIAL"),
    "A22": ("Apr-Sep 10:00-22:00; Oct-Mar 10:00-18:00", "Museo Reina Sofía — Palacio de Cristal (Retiro), documented summer opening", "PARTIAL"),
    "A23": ("Apr-Sep 10:00-21:00; Oct-Mar 10:00-18:00", "Ayuntamiento de Madrid — Retiro enclosed historic gardens, documented summer opening", "PARTIAL"),
    "A25": ("Apr-Sep 10:00-21:00; Oct-Mar 10:00-18:00", "Ayuntamiento de Madrid — Retiro enclosed historic gardens, documented summer opening", "PARTIAL"),
    "A26": ("Apr-Sep 06:00-24:00; Oct-Mar 06:00-22:00", "Parque del Retiro open-access lakeside monument — park hours (documented)", "COMPLETE"),
    "A27": ("Apr-Sep 10:00-21:00; Oct-Mar 10:00-18:00", "Ayuntamiento de Madrid — Retiro enclosed historic gardens, documented summer opening", "PARTIAL"),
}


def _token_kind(tok):
    tok = tok.strip().strip(":")
    if tok == "PH":
        return ("ph", None)
    parts = tok.split("-")
    if all(p in WEEKDAYS for p in parts):
        return ("wd", parts)
    if all(p in MONTHS for p in parts):
        return ("mo", parts)
    return ("other", None)  # day numbers etc.


def _range(seq, a, b):
    i, j = seq.index(a), seq.index(b)
    return seq[i:j + 1] if i <= j else seq[i:] + seq[:j + 1]


def _selector_matches(selector, month, weekday, is_ph):
    """selector = text with time-ranges and 'off' already removed."""
    toks = re.split(r"[ ,]+", selector.strip())
    wd_tokens, mo_tokens, ph = [], [], False
    for t in toks:
        if not t:
            continue
        kind, parts = _token_kind(t)
        if kind == "wd":
            wd_tokens.append(parts)
        elif kind == "mo":
            mo_tokens.append(parts)
        elif kind == "ph":
            ph = True
    # month match: if any month token given, month must fall in one
    if mo_tokens:
        month_ok = any((month in [MONTHS.index(x) + 1 for x in _range(MONTHS, p[0], p[-1])]) for p in mo_tokens)
        if not month_ok:
            return False
    # weekday match: if weekday tokens or PH given, day must match one
    if wd_tokens or ph:
        wd_ok = any(weekday in _range(WEEKDAYS, p[0], p[-1]) for p in wd_tokens) or (ph and is_ph)
        if not wd_ok:
            return False
    return True


def evaluate_open(oh, month, weekday, is_ph, t):
    """Return True/False whether open at decimal-hour t, applying OSM rule
    override semantics (later matching rule wins; unlisted day => closed)."""
    if not isinstance(oh, str) or not oh.strip():
        return None
    state = False
    matched_any = False
    for rule in oh.split(";"):
        rule = rule.strip()
        if not rule:
            continue
        times = re.findall(r"(\d{1,2}):(\d{2})-(\d{1,2}):(\d{2})", rule)
        is_off = bool(re.search(r"\boff\b", rule))
        selector = re.sub(r"(\d{1,2}):(\d{2})-(\d{1,2}):(\d{2})", " ", rule)
        selector = re.sub(r"\boff\b", " ", selector)
        if not _selector_matches(selector, month, weekday, is_ph):
            continue
        matched_any = True
        if is_off or not times:
            state = False if is_off else state
            if is_off:
                state = False
            continue
        open_now = False
        for h1, m1, h2, m2 in times:
            start = int(h1) + int(m1) / 60.0
            end = int(h2) + int(m2) / 60.0
            if end <= start:  # crosses midnight
                if t >= start or t < end:
                    open_now = True
            elif start <= t < end:
                open_now = True
        state = open_now
    return state if matched_any else False


def main():
    assets = pd.read_csv(PROCESSED / "pilot_assets.csv")
    osm = pd.read_csv(PROCESSED / "phase3_osm_opening_hours_raw.csv").set_index("asset_id")

    rows = []
    for _, a in assets.iterrows():
        aid = a["asset_id"]
        oh_osm = str(osm.loc[aid, "opening_hours"]) if aid in osm.index else ""
        oh_osm = "" if oh_osm == "nan" else oh_osm
        if oh_osm:
            oh, oh_src, ev = oh_osm, f"OSM {osm.loc[aid,'osm_ref']} opening_hours tag (ODbL)", "COMPLETE"
        elif aid in DOCUMENTED_HOURS:
            oh, oh_src, ev = DOCUMENTED_HOURS[aid]
        else:
            oh, oh_src, ev = "", "NONE", "MISSING"

        wikidata = str(osm.loc[aid, "wikidata"]) if aid in osm.index else ""
        wikidata = "" if wikidata == "nan" else wikidata
        # tourism relevance evidence (observable, not a score)
        rel = []
        if wikidata:
            rel.append(f"Wikidata:{wikidata}")
        for k in ["tourism", "historic", "amenity", "leisure"]:
            v = str(osm.loc[aid, k]) if aid in osm.index else ""
            if v and v != "nan":
                rel.append(f"osm:{k}={v}")
        relevance = "; ".join(rel) if rel else "category-only"

        open_states = {ts: evaluate_open(oh, DATE_MONTH, DATE_WEEKDAY, DATE_IS_PH, t) for ts, t in TIMES.items()}
        rows.append({
            "asset_id": aid, "name": a["name"], "tourism_category": a["category"],
            "indoor_outdoor": a["indoor_outdoor"],
            "latitude": a["latitude"], "longitude": a["longitude"],
            "opening_hours": oh, "opening_hours_source": oh_src,
            "open_1200": open_states["12:00"], "open_1500": open_states["15:00"],
            "open_1800": open_states["18:00"],
            "tourism_relevance_evidence": relevance,
            "evidence_completeness": ev,
            "asset_source": a["source"],
        })

    out = pd.DataFrame(rows)
    out_path = PROCESSED / "phase3_asset_catalog.csv"
    out.to_csv(out_path, index=False, encoding="utf-8")
    pd.set_option("display.width", 260, "display.max_colwidth", 44)
    print(out[["asset_id", "name", "tourism_category", "indoor_outdoor",
               "open_1200", "open_1500", "open_1800", "evidence_completeness"]].to_string(index=False))
    print(f"\nWrote {out_path} ({len(out)} assets)")

    # ---- verification of the tricky Monday/August cases ----
    print("\n=== opening-hours evaluator verification (Mon 2023-08-21) ===")
    checks = {
        "A01": (True, True, True),    # Prado Mo-Sa 10-20
        "A03": (True, True, False),   # Thyssen Mo 12-16 -> closed by 18
        "A05": (False, False, False), # Naval Mo off
        "A06": (False, False, False), # Antropología no Mo
        "A07": (False, False, False), # Artes Decorativas no Mo
        "A08": (False, False, False), # Real Fábrica Aug off
        "A19": (False, False, False), # Observatorio Fr-Su only
        "A21": (True, True, True),    # Botánico May-Aug 10-21
    }
    ok = True
    for aid, exp in checks.items():
        r = out[out.asset_id == aid].iloc[0]
        got = (r.open_1200, r.open_1500, r.open_1800)
        flag = "OK " if got == exp else "MISMATCH"
        if got != exp:
            ok = False
        print(f"  {flag} {aid} {r['name'][:34]:34s} got {got} expected {exp}")
    print("ALL VERIFY PASS" if ok else "!!! VERIFICATION FAILED")
    return out


if __name__ == "__main__":
    main()
