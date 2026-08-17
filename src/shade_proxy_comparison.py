"""
Phase 1.2 principal shade/exposure-proxy comparison.

Compares four proxy families (P0 baseline OSM tree count, P1 Madrid official
tree inventory, P2 Copernicus Tree Cover Density, P3 green-polygon coverage)
on the SAME 14 outdoor pilot assets and the SAME three real 2023-08-21
timestamps, per the pre-registered spatial unit and classification method in
src/shade_proxy_prereg.py (written and committed BEFORE this script was run).

Outputs:
  data/processed/shade_proxy_comparison.csv
  outputs/tables/shade_proxy_agreement.csv
  outputs/maps/shade_proxy_instability.png
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
import rasterio
from rasterstats import zonal_stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thresholds as th
from shade_proxy_prereg import PRIMARY_BUFFER_M, SENSITIVITY_BUFFERS_M
from build_classifications import (
    load_assets, load_hazard_readings, feasibility_decision, TIMESTAMPS, UTM30N, WGS84,
)
from audit4_shade_proxy_test import compute_proxy2_green_coverage  # P3, retained verbatim

ROOT = Path(__file__).resolve().parents[1]
INTERIM = ROOT / "data" / "interim"
PROCESSED = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"
TABLES = ROOT / "outputs" / "tables"
MAPS = ROOT / "outputs" / "maps"

# Morphology classification (documented rule, decided from real OSM category /
# land-use context already recorded in pilot_assets.csv - NOT re-derived from
# proxy results). See docs/PHASE1_2_SHADE_EVIDENCE_GATE.md for the rationale
# per asset.
MORPHOLOGY = {
    "A14": "plaza_hardscape", "A15": "plaza_hardscape", "A16": "plaza_hardscape",
    "A18": "plaza_hardscape",
    "A17": "street_corridor",
    "A20": "park_garden", "A21": "park_garden", "A23": "park_garden",
    "A24": "park_garden", "A25": "park_garden", "A27": "park_garden",
    "A19": "attraction_exterior", "A22": "attraction_exterior", "A26": "attraction_exterior",
}


def tercile_state(series_outdoor, value):
    q1, q2 = series_outdoor.quantile([1 / 3, 2 / 3])
    if value <= q1:
        return "HIGH", (float(q1), float(q2))
    elif value <= q2:
        return "MODERATE", (float(q1), float(q2))
    else:
        return "LOW", (float(q1), float(q2))


def count_within_buffer(asset_gdf_utm, pts_utm, radius_m):
    pts = pts_utm.geometry.values
    return [sum(1 for p in pts if geom.buffer(radius_m).contains(p)) for geom in asset_gdf_utm.geometry]


def tcd_mean_within_buffer(assets_wgs84, radius_m, tif_path):
    # zonal_stats works in the raster's own CRS; buffer in metres requires a
    # projected CRS, so buffer in UTM then reproject the buffer polygons back
    # to the raster's CRS (WGS84, as exported) for zonal_stats.
    assets_utm = assets_wgs84.to_crs(UTM30N)
    buffers_utm = assets_utm.geometry.buffer(radius_m)
    buffers_wgs84 = gpd.GeoSeries(buffers_utm, crs=UTM30N).to_crs(WGS84)
    stats = zonal_stats(buffers_wgs84, str(tif_path), stats=["mean"], nodata=None)
    return [s["mean"] if s["mean"] is not None else 0.0 for s in stats]


def cohens_kappa(a, b, labels):
    """Manual Cohen's kappa (no sklearn in this environment)."""
    n = len(a)
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pa = {l: sum(1 for x in a if x == l) / n for l in labels}
    pb = {l: sum(1 for x in b if x == l) / n for l in labels}
    pe = sum(pa[l] * pb[l] for l in labels)
    if pe == 1.0:
        return 1.0 if po == 1.0 else 0.0
    return (po - pe) / (1 - pe)


def build_for_buffer(radius_m, assets, madrid_trees_utm, tif_path, label):
    """Compute P1/P2/P3 exposure_state + tercile cuts for a given buffer radius."""
    assets_utm = assets.to_crs(UTM30N)
    outdoor_mask = assets["indoor_outdoor"] == "outdoor"

    # P1 - Madrid official tree count
    p1_count = count_within_buffer(assets_utm, madrid_trees_utm, radius_m)
    assets[f"madrid_tree_count_{label}"] = p1_count

    # P2 - Copernicus TCD mean %
    p2_mean = tcd_mean_within_buffer(assets, radius_m, tif_path)
    assets[f"tcd_mean_pct_{label}"] = p2_mean

    # P3 - green-polygon coverage % (Audit 4 function, same radius applied)
    orig_buffer = None
    import audit4_shade_proxy_test as a4
    orig_buffer = a4.BUFFER_M
    a4.BUFFER_M = radius_m
    p3_pct = compute_proxy2_green_coverage(assets_utm)
    a4.BUFFER_M = orig_buffer
    assets[f"green_pct_{label}"] = p3_pct

    outdoor = assets[outdoor_mask]
    p1_states, p1_cuts = {}, tercile_state(outdoor[f"madrid_tree_count_{label}"], 0)[1]
    p2_states, p2_cuts = {}, tercile_state(outdoor[f"tcd_mean_pct_{label}"], 0)[1]
    p3_states, p3_cuts = {}, tercile_state(outdoor[f"green_pct_{label}"], 0)[1]

    def state_col(col, q1, q2):
        def f(row):
            if row["indoor_outdoor"] == "indoor":
                return None
            v = row[col]
            if v <= q1:
                return "HIGH"
            elif v <= q2:
                return "MODERATE"
            return "LOW"
        return f

    assets[f"exposure_state_madrid_{label}"] = assets.apply(state_col(f"madrid_tree_count_{label}", *p1_cuts), axis=1)
    assets[f"exposure_state_tcd_{label}"] = assets.apply(state_col(f"tcd_mean_pct_{label}", *p2_cuts), axis=1)
    assets[f"exposure_state_green_{label}"] = assets.apply(state_col(f"green_pct_{label}", *p3_cuts), axis=1)

    print(f"\n--- Buffer {radius_m}m ({label}) tercile cuts ---")
    print(f"  P1 Madrid tree count: q1={p1_cuts[0]:.2f}, q2={p1_cuts[1]:.2f}")
    print(f"  P2 TCD mean %:        q1={p2_cuts[0]:.2f}, q2={p2_cuts[1]:.2f}")
    print(f"  P3 green coverage %:  q1={p3_cuts[0]:.2f}, q2={p3_cuts[1]:.2f}")
    return assets, {"P1": p1_cuts, "P2": p2_cuts, "P3": p3_cuts}


def run_feasibility(assets, exposure_col, hazard_by_time):
    rows = []
    for _, a in assets.iterrows():
        for local_time, _ in TIMESTAMPS:
            temp_c = hazard_by_time[local_time]
            hz = th.meteorological_hazard_state(temp_c)
            row = {
                "indoor_outdoor": a["indoor_outdoor"],
                "meteorological_hazard_state": hz,
                "exposure_state": a[exposure_col] if pd.notna(a[exposure_col]) else None,
                "adaptation_state": "GOOD",  # demoted, value irrelevant
            }
            feas, reason, _ = feasibility_decision(row)
            rows.append({"asset_id": a["asset_id"], "timestamp": local_time, "hazard": hz, "feasibility": feas})
    return pd.DataFrame(rows)


def main():
    print(f"PRE-REGISTERED primary buffer: {PRIMARY_BUFFER_M} m "
          f"(src/shade_proxy_prereg.py, committed before this run)")

    assets = load_assets()
    hazard_by_time = load_hazard_readings()

    madrid_trees = gpd.read_file(INTERIM / "madrid_arbolado_points.geojson")
    madrid_trees_utm = madrid_trees.to_crs(UTM30N)
    tif_path = RAW / "copernicus_tcd" / "tcd_2018_study_area.tif"

    # --- PRIMARY buffer (the one used for the gate decision) ---
    assets, cuts_primary = build_for_buffer(PRIMARY_BUFFER_M, assets, madrid_trees_utm, tif_path, "b50")

    # --- P0: reuse Phase 1 baseline verbatim, no changes ---
    baseline = pd.read_csv(PROCESSED / "pilot_classifications.csv")
    p0_by_time = {}
    for local_time, _ in TIMESTAMPS:
        sub = baseline[baseline["timestamp"].str.contains(local_time)][
            ["asset_id", "tree_count_50m", "exposure_state", "feasibility_state"]]
        p0_by_time[local_time] = sub.set_index("asset_id")

    # --- Feasibility per proxy, primary buffer ---
    feas_p0 = baseline[["asset_id", "timestamp", "meteorological_hazard_state", "exposure_state", "feasibility_state"]].copy()
    feas_p0["local_time"] = feas_p0["timestamp"].str.extract(r"T(\d{2}:\d{2})")
    feas_madrid = run_feasibility(assets, "exposure_state_madrid_b50", hazard_by_time)
    feas_tcd = run_feasibility(assets, "exposure_state_tcd_b50", hazard_by_time)
    feas_green = run_feasibility(assets, "exposure_state_green_b50", hazard_by_time)

    # --- Assemble the required comparison CSV ---
    rows = []
    asset_lookup = assets.set_index("asset_id")
    for _, a in assets.iterrows():
        aid = a["asset_id"]
        for local_time, _ in TIMESTAMPS:
            osm_p = p0_by_time[local_time].loc[aid] if aid in p0_by_time[local_time].index else None
            madrid_row = feas_madrid[(feas_madrid.asset_id == aid) & (feas_madrid.timestamp == local_time)].iloc[0]
            tcd_row = feas_tcd[(feas_tcd.asset_id == aid) & (feas_tcd.timestamp == local_time)].iloc[0]
            green_row = feas_green[(feas_green.asset_id == aid) & (feas_green.timestamp == local_time)].iloc[0]

            states = [osm_p["exposure_state"] if osm_p is not None else None,
                      a["exposure_state_madrid_b50"], a["exposure_state_tcd_b50"], a["exposure_state_green_b50"]]
            feass = [osm_p["feasibility_state"] if osm_p is not None else None,
                     madrid_row["feasibility"], tcd_row["feasibility"], green_row["feasibility"]]
            valid_feass = [f for f in feass if f is not None]
            sensitive = len(set(valid_feass)) > 1

            direction = ""
            if sensitive and a["indoor_outdoor"] == "outdoor":
                order = {"FEASIBLE": 0, "FEASIBLE WITH CONDITIONS": 1, "NOT RECOMMENDED": 2, "INSUFFICIENT EVIDENCE": -1}
                vals = [order.get(f, -1) for f in valid_feass]
                if max(vals) - min(vals) >= 2:
                    direction = "MAJOR (spans FEASIBLE<->NOT RECOMMENDED)"
                elif max(vals) > min(vals):
                    direction = "MINOR (adjacent levels only)"

            rows.append({
                "asset_id": aid, "name": a["name"], "indoor_outdoor": a["indoor_outdoor"],
                "morphology": MORPHOLOGY.get(aid, "indoor" if a["indoor_outdoor"] == "indoor" else "other"),
                "timestamp": f"2023-08-21T{local_time}:00+02:00",
                "OSM_tree_proxy": osm_p["tree_count_50m"] if osm_p is not None else None,
                "Madrid_tree_proxy": a["madrid_tree_count_b50"],
                "Copernicus_TCD_proxy": round(a["tcd_mean_pct_b50"], 1),
                "green_polygon_proxy": round(a["green_pct_b50"], 1),
                "exposure_state_OSM": osm_p["exposure_state"] if osm_p is not None else None,
                "exposure_state_Madrid": a["exposure_state_madrid_b50"],
                "exposure_state_TCD": a["exposure_state_tcd_b50"],
                "exposure_state_green": a["exposure_state_green_b50"],
                "feasibility_OSM": osm_p["feasibility_state"] if osm_p is not None else None,
                "feasibility_Madrid": madrid_row["feasibility"],
                "feasibility_TCD": tcd_row["feasibility"],
                "feasibility_green": green_row["feasibility"],
                "proxy_sensitive": sensitive,
                "disagreement_direction": direction,
                "evidence_notes": (
                    "indoor asset - exposure gate bypassed, proxy choice cannot affect outcome"
                    if a["indoor_outdoor"] == "indoor" else
                    f"buffer={PRIMARY_BUFFER_M}m; Madrid tree source=official ArcGIS live layer "
                    f"(2026 snapshot); TCD source=Copernicus HRL 2018 (10m); green source=OSM real polygons"
                ),
            })

    out = pd.DataFrame(rows)
    out_path = PROCESSED / "shade_proxy_comparison.csv"
    out.to_csv(out_path, index=False, encoding="utf-8")
    print(f"\nWrote {out_path} with {len(out)} rows")

    return out, assets, cuts_primary


if __name__ == "__main__":
    main()
