"""Read-only data access for the seven locked Phase 3 files.

CONTRACT (PHASE4_0_TO_PHASE4_1_HANDOFF.md §12, Phase 4.1 charter):
  * Reads ONLY the seven approved CSVs listed in ``DATA_FILES``.
  * May filter, join on existing identifiers, sort for display, count
    filtered rows, and translate locked tokens into fixed copy.
  * NEVER recomputes UTCI / feasibility / screening / baseline, NEVER
    creates a score or ranking, and NEVER writes to any file. There is no
    write path anywhere in this module by construction.

The asset catalog already carries WGS84 ``latitude`` / ``longitude``; those
are handed straight to Leaflet. No coordinate reprojection is performed.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd

from . import constants as C

# Repo root = parent of the ``app`` package directory.
REPO_ROOT = Path(__file__).resolve().parent.parent

# The entire permitted data surface. Read-only.
DATA_FILES = {
    "catalog": REPO_ROOT / "data/processed/phase3_asset_catalog.csv",
    "screening": REPO_ROOT / "data/processed/phase3_candidate_screening.csv",
    "scenarios": REPO_ROOT / "data/processed/phase3_scenarios.csv",
    "summary": REPO_ROOT / "data/processed/phase3_scenarios_summary.csv",
    "exclusion_reasons": REPO_ROOT / "outputs/tables/phase3_exclusion_reasons.csv",
    "baseline": REPO_ROOT / "outputs/tables/phase3_hati_vs_baseline.csv",
    "accessibility": REPO_ROOT / "outputs/tables/phase3_accessibility_sensitivity.csv",
}


@lru_cache(maxsize=1)
def _load_all() -> dict[str, pd.DataFrame]:
    """Load the seven CSVs once. UTF-8, string timestamps preserved."""
    frames: dict[str, pd.DataFrame] = {}
    for key, path in DATA_FILES.items():
        if not path.exists():
            raise FileNotFoundError(f"Required Phase 3 file missing: {path}")
        df = pd.read_csv(path, encoding="utf-8", dtype={"timestamp": str})
        frames[key] = df
    return frames


def frame(key: str) -> pd.DataFrame:
    """Return a defensive copy of a loaded frame (callers never mutate cache)."""
    return _load_all()[key].copy()


# ── View 1: assets at a timestamp ──────────────────────────────────────────
def assets_at_timestamp(timestamp: str) -> pd.DataFrame:
    """The 27 assets with their per-timestamp screening state + coordinates.

    A left-join of the static catalog (identity, lat/lon) onto the
    per-timestamp screening rows. No value is computed; every column comes
    from one of the two CSVs.
    """
    if timestamp not in C.TIMESTAMPS:
        raise ValueError(f"Invalid timestamp {timestamp!r}")
    scr = frame("screening")
    scr = scr[scr["timestamp"] == timestamp].copy()
    cat = frame("catalog")[["asset_id", "latitude", "longitude",
                            "opening_hours", "opening_hours_source"]]
    merged = scr.merge(cat, on="asset_id", how="left")
    return merged


def asset_record(asset_id: str, timestamp: str) -> dict | None:
    """One asset's full screening record at a timestamp (View 2)."""
    merged = assets_at_timestamp(timestamp)
    row = merged[merged["asset_id"] == asset_id]
    if row.empty:
        return None
    return row.iloc[0].to_dict()


def all_asset_ids() -> list[str]:
    return sorted(frame("catalog")["asset_id"].unique().tolist())


# ── Scenario resolution (source asset + timestamp -> pre-computed scenario) ─
def scenario_for_source(asset_id: str, timestamp: str) -> dict | None:
    """Return the summary row for the scenario whose source is this asset at
    this timestamp, or ``None`` if no scenario was pre-computed. The UI never
    invents a scenario for an (asset, timestamp) the pipeline did not run.
    """
    summ = frame("summary")
    hit = summ[(summ["source_id"] == asset_id) &
               (summ["timestamp"] == timestamp)]
    if hit.empty:
        return None
    return hit.iloc[0].to_dict()


def summary_row(scenario: str) -> dict | None:
    summ = frame("summary")
    hit = summ[summ["scenario"] == scenario]
    return None if hit.empty else hit.iloc[0].to_dict()


def scenario_candidates(scenario: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(survivors, excluded) candidate rows for a scenario.

    survivors = rows with status == CANDIDATE_ALTERNATIVE.
    excluded  = rows with status == EXCLUDED.
    """
    scn = frame("scenarios")
    scn = scn[scn["scenario"] == scenario]
    survivors = scn[scn["status"] == "CANDIDATE_ALTERNATIVE"].copy()
    excluded = scn[scn["status"] == "EXCLUDED"].copy()
    return survivors, excluded


def all_scenarios() -> pd.DataFrame:
    """Summary rows for S1..S8 in scenario order (for the jump chips)."""
    summ = frame("summary")
    return summ.sort_values("scenario").reset_index(drop=True)


# ── Baseline comparison (pre-computed only) ────────────────────────────────
def baseline_row(scenario: str) -> dict | None:
    base = frame("baseline")
    hit = base[base["scenario"] == scenario]
    return None if hit.empty else hit.iloc[0].to_dict()


# ── Accessibility radius sensitivity (pre-computed only) ───────────────────
def accessibility_row(scenario: str) -> dict | None:
    acc = frame("accessibility")
    hit = acc[acc["scenario"] == scenario]
    return None if hit.empty else hit.iloc[0].to_dict()


# ── Token translation (lookup only) ────────────────────────────────────────
def translate_exclusion(token: str | float | None) -> str | None:
    """Locked exclusion token -> fixed human copy. Returns None for blanks."""
    if token is None or (isinstance(token, float)) or str(token).strip() == "":
        return None
    return C.EXCLUSION_TRANSLATIONS.get(str(token), str(token))


def known_exclusion_tokens() -> set[str]:
    """Every exclusion token actually present anywhere in the loaded data."""
    tokens: set[str] = set()
    scn = frame("scenarios")["exclusion_reason"].dropna()
    tokens.update(t for t in scn.astype(str) if t.strip())
    scr = frame("screening")["context_free_exclusion_reason"].dropna()
    tokens.update(t for t in scr.astype(str) if t.strip())
    base = frame("baseline")["baseline_pick_hati_exclusion"].dropna()
    tokens.update(t for t in base.astype(str) if t.strip())
    excl = frame("exclusion_reasons")["exclusion_reason"].dropna()
    tokens.update(t for t in excl.astype(str) if t.strip())
    return tokens


# ═══════════════════════════════════════════════════════════════════════════
# Phase 4.2 — additional read-only accessors.
# Filter / join / sort / count only. Nothing below computes a scientific
# value, and there is still no write path anywhere in this module.
# ═══════════════════════════════════════════════════════════════════════════
def asset_options(timestamp: str) -> list[dict]:
    """`{value, label}` for every asset, for the command-bar asset picker.

    Sorted by name — an alphabetical list is the least evaluative order
    available and is what a reader looking up a specific place expects.
    """
    df = assets_at_timestamp(timestamp)
    df = df.sort_values("name")
    return [{"value": r["asset_id"], "label": str(r["name"])}
            for _, r in df.iterrows()]


def scenario_options() -> list[dict]:
    """Summary rows S1..S8 flattened for the scenario menu (display only)."""
    out = []
    for _, r in all_scenarios().iterrows():
        out.append({
            "scenario": r["scenario"],
            "source_id": r["source_id"],
            "source_name": r["source_name"],
            "timestamp": r["timestamp"],
            "radius_m": int(r["access_radius_m"]),
            "n_alternatives": int(r["n_candidate_alternatives"]),
            "recommendation": str(r["recommendation"]),
            "description": str(r.get("scenario_desc", "")),
        })
    return out


def exclusion_breakdown(scenario: str) -> list[tuple[str, int]]:
    """`(exclusion_reason, count)` for one scenario's excluded candidates.

    A ``value_counts`` of the locked ``exclusion_reason`` column, descending.
    No category is invented, merged or renamed here; the plain-language
    rendering happens at display time via ``translate_exclusion``.
    """
    _, excluded = scenario_candidates(scenario)
    if excluded.empty:
        return []
    counts = excluded["exclusion_reason"].fillna("").astype(str).value_counts()
    return [(token, int(n)) for token, n in counts.items() if token.strip()]


def scenario_source_name(scenario: str) -> str | None:
    row = summary_row(scenario)
    return None if row is None else str(row["source_name"])


def asset_name(asset_id: str) -> str | None:
    cat = frame("catalog")
    hit = cat[cat["asset_id"] == asset_id]
    return None if hit.empty else str(hit.iloc[0]["name"])
