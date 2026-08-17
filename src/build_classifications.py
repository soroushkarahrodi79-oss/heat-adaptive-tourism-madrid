"""
Phase 1 baseline constraint-first classification pipeline.

Reproducible from source: run build_study_area.py, build_pilot_assets.py, and
build_supporting_layers.py first (or just run this file, which does not modify
them but does depend on their outputs existing).

Output: data/processed/pilot_classifications.csv, one row per (asset x timestamp).
"""
import math
from pathlib import Path

import geopandas as gpd
import pandas as pd

import thresholds as th

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
INTERIM = ROOT / "data" / "interim"
RAW = ROOT / "data" / "raw"

WGS84 = "EPSG:4326"
UTM30N = "EPSG:25830"  # ETRS89 / UTM zone 30N - correct projected CRS for Madrid, metres

# --- Episode + timestamps (see docs/PHASE1_METHOD.md "Heat episode" section) -----
EPISODE_DATE = "2023-08-21"
TIMEZONE = "Europe/Madrid"  # CEST = UTC+2 on this date
# (local_time, utc_hour) - utc_hour must match the 'hour_utc' column in the raw
# Barajas extract exactly (local = UTC+2 in August).
TIMESTAMPS = [
    ("12:00", "10"),
    ("15:00", "13"),
    ("18:00", "16"),
]

STATION_ID = "AEMET 08221 Madrid/Barajas (WMO) / AEMET indicativo 3129, ~9 km NE of study area"

# --- Phase 1.1 Audit 1: station representativeness note --------------------------
# Real, documented AEMET-derived hourly observations for Madrid/Retiro (AEMET
# indicativo 3195, inside/adjacent the study area) were sought and could not be
# obtained within this project's constraints:
#   - AEMET OpenData API requires a registered api_key (confirmed: anonymous
#     request to the daily-values endpoint returns HTTP 401 "JWT strings must
#     contain exactly 2 period characters. Found: 0"); registering an account is
#     outside what this project performs on the user's behalf without explicit
#     authorisation, and email-verified registration is not completable
#     synchronously in any case.
#   - datosclima.es (a third-party AEMET-data reseller) only offers Retiro hourly
#     data via a manual email request + EUR 2.50 payment per batch - not a
#     programmatic, immediately reproducible source, and a purchase this project
#     does not make unilaterally.
#   - x-y.es publishes a Retiro monthly page with a "Calendario" section, but the
#     day-level detail is rendered as a non-interactive chart image with no
#     underlying scrapable hourly table or per-day URL.
#   - Meteostat also serves an hourly file for a station co-located with Retiro
#     (id 08222), but this was already identified and rejected in Phase 1
#     (data/raw/README.md): its own inventory metadata shows the "hourly" values
#     start exactly where its "model" (reanalysis-interpolated) coverage starts,
#     i.e. they are not raw observations.
# Per the Phase 1.1 task specification, Retiro hourly values are therefore NOT
# fabricated or interpolated. Barajas remains the sole hourly hazard input, with
# this explicit spatial-representativeness limitation attached to every row.
# Retiro's OFFICIAL DAILY figures (from the AEMET monthly climatological advance
# report, not this project's own aggregation) are used as an independent
# cross-check instead:
#   - Retiro official daily max, 2023-08-21: 40.0 C. Barajas daily max the same
#     day (this project's own hourly extract): 40.5 C -> +0.5 C, Barajas warmer,
#     consistent with an open airport-apron site vs. a shaded urban park.
#   - Retiro official August-2023 monthly mean: 28.0 C. Barajas August-2023
#     monthly mean (this project's own hourly extract, n=744 hourly readings):
#     28.11 C -> +0.11 C, i.e. close agreement at monthly scale.
# See docs/PHASE1_1_BASELINE_HARDENING.md, Audit 1, for the full attempt log.
STATION_REPRESENTATIVENESS_NOTE = (
    "Hourly hazard input is Madrid/Barajas (~9 km NE of study area; open airport "
    "apron). Real Retiro (in/adjacent to study area) hourly data was sought and "
    "found unobtainable without account registration or payment - see "
    "docs/PHASE1_1_BASELINE_HARDENING.md Audit 1. Retiro's OFFICIAL daily max "
    "(40.0C, 21 Aug 2023) and monthly mean (28.0C, Aug 2023) are used as "
    "independent cross-checks: Barajas ran +0.5C warmer at daily-max and +0.11C "
    "warmer at monthly-mean for the same period, i.e. close regional agreement "
    "at daily/monthly scale, but hourly-scale agreement is NOT independently "
    "verified and must not be assumed at sub-daily resolution."
)


def load_hazard_readings():
    df = pd.read_csv(RAW / "episode_aug2023_barajas_raw.csv", dtype={"hour_utc": str})
    df = df[df["date"] == EPISODE_DATE]
    out = {}
    for local_time, utc_hour in TIMESTAMPS:
        row = df[df["hour_utc"] == utc_hour.zfill(2)]
        if row.empty:
            out[local_time] = None
        else:
            out[local_time] = float(row.iloc[0]["temp_c"])
    return out


def load_assets():
    df = pd.read_csv(PROCESSED / "pilot_assets.csv")
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs=WGS84
    )
    return gdf


def nearest_distance_m(asset_gdf_utm, points_gdf_utm):
    """For each asset, distance in metres to the nearest point in points_gdf."""
    if len(points_gdf_utm) == 0:
        return [None] * len(asset_gdf_utm)
    dists = []
    pts = points_gdf_utm.geometry.values
    for geom in asset_gdf_utm.geometry.values:
        d = min(geom.distance(p) for p in pts)
        dists.append(round(d, 1))
    return dists


def count_within_m(asset_gdf_utm, points_gdf_utm, radius_m):
    counts = []
    pts = points_gdf_utm.geometry.values
    for geom in asset_gdf_utm.geometry.values:
        buf = geom.buffer(radius_m)
        c = sum(1 for p in pts if buf.contains(p))
        counts.append(c)
    return counts


POLYGON_EDGE_BUFFER_M = 15  # catches trees digitised just outside a polygon's edge


def count_trees_for_asset(asset_id, geom_point_utm, trees_utm, polygons_utm):
    """Tree count for one asset: if the asset has a real OSM polygon extent (a
    park/garden - see build_green_polygons.py), count trees within that polygon
    buffered by POLYGON_EDGE_BUFFER_M; otherwise fall back to a fixed-radius
    buffer around the asset's point/centroid (EXPOSURE_BUFFER_M)."""
    if asset_id in polygons_utm.index:
        poly = polygons_utm.loc[asset_id, "geometry"]
        area = poly.buffer(POLYGON_EDGE_BUFFER_M)
        method = f"polygon+{POLYGON_EDGE_BUFFER_M}m (real extent, {polygons_utm.loc[asset_id, 'area_m2']:.0f} m2)"
    else:
        area = geom_point_utm.buffer(th.EXPOSURE_BUFFER_M)
        method = f"point+{th.EXPOSURE_BUFFER_M}m radius (centroid)"
    pts = trees_utm.geometry.values
    count = sum(1 for p in pts if area.contains(p))
    return count, method


def compute_site_metrics(assets):
    trees = gpd.read_file(INTERIM / "trees.geojson").to_crs(UTM30N)
    water = gpd.read_file(INTERIM / "water_points.geojson").to_crs(UTM30N)
    transit = gpd.read_file(INTERIM / "transit_points.geojson").to_crs(UTM30N)
    green_poly = gpd.read_file(INTERIM / "green_polygons.geojson").to_crs(UTM30N).set_index("asset_id")

    assets_utm = assets.to_crs(UTM30N)

    assets = assets.copy()
    tree_counts, methods = [], []
    for aid, geom in zip(assets_utm["asset_id"], assets_utm.geometry):
        c, m = count_trees_for_asset(aid, geom, trees, green_poly)
        tree_counts.append(c)
        methods.append(m)
    assets["tree_count_50m"] = tree_counts
    assets["exposure_measurement_method"] = methods
    assets["water_dist_m"] = nearest_distance_m(assets_utm, water)
    assets["transit_dist_m"] = nearest_distance_m(assets_utm, transit)

    # Exposure state: empirical tercile split, computed ONLY over outdoor assets
    # (indoor assets don't have a meaningful outdoor-exposure reading; the gate is
    # bypassed for them regardless). Documented in thresholds.EXPOSURE_METHOD_NOTE.
    outdoor = assets[assets["indoor_outdoor"] == "outdoor"]
    q1, q2 = outdoor["tree_count_50m"].quantile([1 / 3, 2 / 3])
    print(f"Exposure tercile cutpoints (tree_count_50m, outdoor assets, n={len(outdoor)}): "
          f"q1={q1:.2f}, q2={q2:.2f}")
    print(outdoor[["asset_id", "name", "tree_count_50m", "exposure_measurement_method"]]
          .sort_values("tree_count_50m").to_string(index=False))

    def exposure_state_and_note(row):
        if row["indoor_outdoor"] == "indoor":
            return None, ""
        tc = row["tree_count_50m"]
        if tc <= q1:
            if row["category"] in th.GREEN_LAND_USE_CATEGORIES:
                return ("MODERATE",
                        "on-site OSM tree-point layer returned zero/near-zero trees despite "
                        "this being a real, officially-tagged leisure=garden/park polygon; "
                        "treated as a known local gap in OSM's crowdsourced tree layer, not "
                        "as evidence the site is unshaded - downgraded from HIGH to MODERATE "
                        "exposure with reduced confidence rather than left uncorrected")
            return "HIGH", ""   # poor shade: bottom tercile, genuinely no green land use either
        elif tc <= q2:
            return "MODERATE", ""
        else:
            return "LOW", ""    # well shaded: top tercile

    exp_results = assets.apply(exposure_state_and_note, axis=1)
    assets["exposure_state"] = exp_results.apply(lambda x: x[0])
    assets["exposure_override_note"] = exp_results.apply(lambda x: x[1])
    assets["adaptation_state"] = assets.apply(
        lambda r: th.adaptation_state(r["water_dist_m"], r["transit_dist_m"]), axis=1
    )
    return assets, (float(q1), float(q2))


def feasibility_decision(row):
    """Returns (feasibility_state, exclusion_reason, missing_inputs)."""
    missing = []
    if row["meteorological_hazard_state"] is None:
        missing.append("temperature")
    if row["indoor_outdoor"] == "outdoor":
        if row["exposure_state"] is None:
            missing.append("tree_count_buffer")
        if row["adaptation_state"] is None:
            missing.append("water_or_transit_distance")

    if missing:
        return "INSUFFICIENT EVIDENCE", "required input missing: " + ", ".join(missing), missing

    hz = row["meteorological_hazard_state"]

    if row["indoor_outdoor"] == "indoor":
        if hz in ("SEVERE", "EXTREME"):
            return ("FEASIBLE WITH CONDITIONS",
                    "indoor visit assumed thermally buffered, but A/C operational status "
                    "is not verified in source data and outdoor approach/queueing exposure "
                    f"is a residual risk at {hz.lower()} regional hazard", [])
        return ("FEASIBLE",
                "indoor visit assumed thermally buffered; regional hazard not severe "
                "enough to flag residual approach-exposure risk", [])

    # Outdoor decision table (thresholds.FEASIBILITY_RULES_OUTDOOR)
    exp = row["exposure_state"]
    ada = row["adaptation_state"]

    if hz == "EXTREME":
        return ("NOT RECOMMENDED",
                f"regional air temperature at/above AEMET red-warning threshold "
                f"({th.AEMET_MADRID_METRO_RED_C:.0f}C) for the Madrid Metropolitana zone; "
                "no on-site shade or adaptation-resource combination is treated as "
                "sufficient at this baseline evidence level", [])

    if hz == "SEVERE" and exp == "HIGH":
        return ("NOT RECOMMENDED",
                f"orange-level regional heat warning ({th.AEMET_MADRID_METRO_ORANGE_C:.0f}-"
                f"{th.AEMET_MADRID_METRO_RED_C:.0f}C) combined with low measured tree density "
                "at this site (bottom tercile of pilot sample, i.e. poor on-site shade)", [])

    # NOTE (Phase 1.1 Audit 3): a rule excluding SEVERE-hazard + adaptation==POOR
    # sites was REMOVED here. It never fired across 81 Phase 1 rows or 18 Audit 3
    # ring-extension rows (adaptation_state was never POOR at any defensible
    # water/transit distance threshold for this pilot's geography) - see
    # docs/PHASE1_1_BASELINE_HARDENING.md Audit 3 and src/thresholds.py's
    # adaptation-resource INDICATOR comment. `ada` (adaptation_state) is still
    # computed and still returned as an output column for informational use;
    # it is intentionally unused in the branching below.
    if hz == "SEVERE":
        return ("FEASIBLE WITH CONDITIONS",
                "orange-level regional heat warning; on-site shade is adequate but a "
                "precautionary hydration/shade-break recommendation applies "
                "(nearest water/transit distance reported for context, not decisive)", [])

    if hz == "ELEVATED" and exp == "HIGH":
        return ("FEASIBLE WITH CONDITIONS",
                "yellow-level regional heat warning combined with low on-site tree "
                "density; hydration and shade-seeking recommended", [])

    if hz == "ELEVATED":
        return ("FEASIBLE WITH CONDITIONS",
                "yellow-level regional heat warning; standard heat-season precaution "
                "recommended", [])

    if hz == "LOW" and exp == "HIGH":
        return ("FEASIBLE WITH CONDITIONS",
                "regional hazard modest but on-site tree density is in the lowest "
                "tercile of the pilot sample (poor shade); precautionary flag only", [])

    return ("FEASIBLE",
            "regional hazard below yellow-warning threshold and on-site shade is "
            "average-to-good for the pilot sample", [])


def evidence_confidence(row):
    """Weakest-link categorical confidence. See docs/PHASE1_METHOD.md."""
    if row["feasibility_state"] == "INSUFFICIENT EVIDENCE":
        return "LOW"
    if row["indoor_outdoor"] == "indoor" and row["meteorological_hazard_state"] in ("SEVERE", "EXTREME"):
        # A/C-operational-status assumption becomes decision-relevant
        return "LOW"
    if row.get("exposure_override_note"):
        # Tree-point layer conflicted with real land-use tag at this site
        # (documented OSM tree-mapping coverage gap) - exposure input is genuinely
        # uncertain here, not just proxy-typical.
        return "LOW"
    # Every remaining row rests on: a real-but-regionally-displaced hazard reading
    # (~9 km from site), a real-but-proxy exposure measure (tree count, not
    # measured canopy/shadow), and a real-but-completeness-uncertain adaptation
    # network (OSM water/transit point coverage not independently audited).
    # No row in this Phase 1 baseline is rated HIGH - see PHASE1_VALIDATION_REPORT.md.
    return "MEDIUM"


def build():
    hazard_by_time = load_hazard_readings()
    print("Meteorological hazard readings (local Europe/Madrid time, 2023-08-21, Barajas 08221):")
    for t, v in hazard_by_time.items():
        print(f"  {t} -> {v} C -> {th.meteorological_hazard_state(v)}")

    assets = load_assets()
    assets, tercile_cuts = compute_site_metrics(assets)

    rows = []
    for _, a in assets.iterrows():
        for local_time, utc_hour in TIMESTAMPS:
            temp_c = hazard_by_time[local_time]
            hz = th.meteorological_hazard_state(temp_c)
            row = {
                "asset_id": a["asset_id"],
                "name": a["name"],
                "indoor_outdoor": a["indoor_outdoor"],
                "timestamp": f"{EPISODE_DATE}T{local_time}:00{'+02:00'}",
                "temp_c_barajas": temp_c,
                "meteorological_hazard_state": hz,
                "tree_count_50m": a["tree_count_50m"],
                "exposure_measurement_method": a["exposure_measurement_method"],
                "exposure_state": a["exposure_state"],
                "exposure_override_note": a["exposure_override_note"],
                "water_dist_m": a["water_dist_m"],
                "transit_dist_m": a["transit_dist_m"],
                "adaptation_state": a["adaptation_state"],
            }
            feas, reason, missing = feasibility_decision(row)
            row["feasibility_state"] = feas
            row["exclusion_reason"] = reason if feas in ("NOT RECOMMENDED", "INSUFFICIENT EVIDENCE") else ""
            row["missing_inputs"] = ";".join(missing)
            row["evidence_confidence"] = evidence_confidence(row)
            row["method_version"] = th.METHOD_VERSION
            row["station_used"] = STATION_ID
            row["station_representativeness_note"] = STATION_REPRESENTATIVENESS_NOTE
            rows.append(row)

    out = pd.DataFrame(rows)
    # Reorder / select final columns per spec (asset_id, timestamp,
    # meteorological_hazard_state, exposure_state, adaptation_state,
    # feasibility_state, exclusion_reason, evidence_confidence, missing_inputs,
    # method_version) + supporting evidence.
    cols = [
        "asset_id", "name", "indoor_outdoor", "timestamp",
        "temp_c_barajas", "meteorological_hazard_state",
        "tree_count_50m", "exposure_measurement_method", "exposure_state", "exposure_override_note",
        "water_dist_m", "transit_dist_m", "adaptation_state",
        "feasibility_state", "exclusion_reason",
        "evidence_confidence", "missing_inputs", "method_version", "station_used",
        "station_representativeness_note",
    ]
    out = out[cols]
    out_path = PROCESSED / "pilot_classifications.csv"
    out.to_csv(out_path, index=False, encoding="utf-8")
    print(f"\nWrote {out_path} with {len(out)} rows ({len(assets)} assets x {len(TIMESTAMPS)} timestamps)")
    print("\nFeasibility state counts:")
    print(out["feasibility_state"].value_counts())
    return out, tercile_cuts


if __name__ == "__main__":
    build()
