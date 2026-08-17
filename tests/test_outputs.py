"""
Lightweight sanity checks on the Phase 1 processed outputs. Not a substitute for
the narrative validation in docs/PHASE1_VALIDATION_REPORT.md - these are structural
invariants (row counts, allowed category values, no missing required fields) that
should hold after any reproduction run of the src/ pipeline.

Run with: pytest tests/test_outputs.py   (or: python -m pytest tests/)
"""
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"

VALID_HAZARD = {"LOW", "ELEVATED", "SEVERE", "EXTREME"}
VALID_EXPOSURE = {"LOW", "MODERATE", "HIGH"}
VALID_ADAPTATION = {"GOOD", "LIMITED", "POOR"}
VALID_FEASIBILITY = {"FEASIBLE", "FEASIBLE WITH CONDITIONS", "NOT RECOMMENDED", "INSUFFICIENT EVIDENCE"}
VALID_CONFIDENCE = {"HIGH", "MEDIUM", "LOW"}


@pytest.fixture(scope="module")
def assets():
    return pd.read_csv(PROCESSED / "pilot_assets.csv")


@pytest.fixture(scope="module")
def classifications():
    return pd.read_csv(PROCESSED / "pilot_classifications.csv")


def test_asset_count_in_pilot_range(assets):
    assert 20 <= len(assets) <= 30, "pilot_assets.csv should have 20-30 rows per brief"


def test_asset_ids_unique(assets):
    assert assets["asset_id"].is_unique


def test_asset_coords_within_study_area(assets):
    # Bounds must match src/define_study_area.py LAT_MIN/LAT_MAX/LON_MIN/LON_MAX.
    # Kept as literals (not imported) so this test independently catches drift
    # between the two rather than trivially passing by construction.
    assert assets["latitude"].between(40.4040, 40.4210).all()
    assert assets["longitude"].between(-3.6960, -3.6775).all()


def test_indoor_outdoor_values(assets):
    assert set(assets["indoor_outdoor"].unique()) <= {"indoor", "outdoor"}


def test_classification_row_count(assets, classifications):
    assert len(classifications) == len(assets) * 3, "expected assets x 3 timestamps"


def test_classification_categoricals_valid(classifications):
    assert set(classifications["meteorological_hazard_state"].dropna().unique()) <= VALID_HAZARD
    assert set(classifications["exposure_state"].dropna().unique()) <= VALID_EXPOSURE
    assert set(classifications["adaptation_state"].dropna().unique()) <= VALID_ADAPTATION
    assert set(classifications["feasibility_state"].unique()) <= VALID_FEASIBILITY
    assert set(classifications["evidence_confidence"].unique()) <= VALID_CONFIDENCE


def test_indoor_assets_have_no_exposure_state(classifications):
    # classifications already carries its own indoor_outdoor column
    indoor_rows = classifications[classifications["indoor_outdoor"] == "indoor"]
    assert indoor_rows["exposure_state"].isna().all()


def test_not_recommended_rows_have_exclusion_reason(classifications):
    nr = classifications[classifications["feasibility_state"].isin(
        ["NOT RECOMMENDED", "INSUFFICIENT EVIDENCE"])]
    assert (nr["exclusion_reason"].astype(str).str.len() > 0).all()


def test_adaptation_gate_stays_demoted(classifications):
    # Phase 1.1 Audit 3: the adaptation-resource exclusion rule was removed
    # (never discriminated at any defensible threshold). This pins that no
    # exclusion_reason cites water/transit distance as the reason for exclusion,
    # so a future edit can't silently reintroduce the same decorative rule.
    reasons = classifications["exclusion_reason"].dropna().astype(str)
    assert not reasons.str.contains("drinking-water point", case=False).any()


def test_feasible_rows_have_no_exclusion_reason(classifications):
    ok = classifications[classifications["feasibility_state"] == "FEASIBLE"]
    assert ok["exclusion_reason"].isna().all() or (ok["exclusion_reason"].astype(str) == "").all()


def test_shade_proxy_comparison_has_required_columns():
    path = PROCESSED / "shade_proxy_comparison.csv"
    if not path.exists():
        pytest.skip("run src/shade_proxy_comparison.py first")
    df = pd.read_csv(path)
    required = {
        "asset_id", "timestamp", "OSM_tree_proxy", "Madrid_tree_proxy",
        "Copernicus_TCD_proxy", "green_polygon_proxy", "exposure_state_OSM",
        "exposure_state_Madrid", "exposure_state_TCD", "exposure_state_green",
        "feasibility_OSM", "feasibility_Madrid", "feasibility_TCD", "feasibility_green",
        "proxy_sensitive", "disagreement_direction", "evidence_notes",
    }
    assert required.issubset(set(df.columns))
    assert len(df) == 81  # 27 assets x 3 timestamps, same pilot as Phase 1


def test_shade_proxy_p0_matches_frozen_phase1_baseline(classifications):
    # P0 in the Phase 1.2 comparison must be byte-identical to the Phase 1
    # baseline it is frozen from - Phase 1.2 explicitly must not "improve it
    # retrospectively".
    path = PROCESSED / "shade_proxy_comparison.csv"
    if not path.exists():
        pytest.skip("run src/shade_proxy_comparison.py first")
    comp = pd.read_csv(path)
    comp["local_time"] = comp["timestamp"].str.extract(r"T(\d{2}:\d{2})")
    base = classifications.copy()
    base["local_time"] = base["timestamp"].str.extract(r"T(\d{2}:\d{2})")
    merged = comp.merge(base[["asset_id", "local_time", "feasibility_state"]],
                         on=["asset_id", "local_time"], how="left")
    mismatched = merged[merged["feasibility_OSM"] != merged["feasibility_state"]]
    assert len(mismatched) == 0


def test_no_row_reaches_extreme_hazard_in_this_pilot(classifications):
    # Documented finding in PHASE1_VALIDATION_REPORT.md - the 3 fixed timestamps
    # did not reach AEMET's red/EXTREME band. This test pins that documented fact
    # so a future data refresh that changes it is noticed, not silently ignored.
    # The EXTREME branch itself IS validated, separately, in
    # data/processed/extreme_branch_stress_test_2021-08-14.csv (Phase 1.1 Audit 2)
    # using a real historical reading - see test below.
    assert "EXTREME" not in classifications["meteorological_hazard_state"].unique()


def test_extreme_branch_validated_by_stress_test():
    # Phase 1.1 Audit 2: confirms the EXTREME branch has been exercised at least
    # once against a real, AEMET-confirmed reading, and behaves as designed
    # (unconditional NOT RECOMMENDED for every outdoor asset, FEASIBLE WITH
    # CONDITIONS for every indoor asset).
    path = PROCESSED / "extreme_branch_stress_test_2021-08-14.csv"
    assert path.exists(), "Audit 2 stress test output missing - run src/audit2_extreme_stress_test.py"
    df = pd.read_csv(path)
    extreme = df[df["meteorological_hazard_state"] == "EXTREME"]
    assert len(extreme) > 0, "stress test file exists but contains no EXTREME rows"
    outdoor = extreme[extreme["indoor_outdoor"] == "outdoor"]
    indoor = extreme[extreme["indoor_outdoor"] == "indoor"]
    assert (outdoor["feasibility_state"] == "NOT RECOMMENDED").all()
    assert (indoor["feasibility_state"] == "FEASIBLE WITH CONDITIONS").all()
