"""
Phase 1.1 Audit 4: shade-proxy sensitivity audit.

The Phase 1 baseline's exposure gate uses PROXY 1 (tree_count within a 50 m
buffer, or the asset's own polygon+15m for the 8 pilot assets that are
themselves parks/gardens). This script builds two further, methodologically
distinct real-data proxies and compares all three - WITHOUT starting SOLWEIG
and without treating any of them as measured physical shade.

PROXY 1 - Tree-point density (Phase 1 baseline)
  Physical concept approximated: presence of individual shade-casting trees
  near the asset.
  Data: OSM natural=tree point nodes (n=1,353).
  Limitation: a point count says nothing about canopy diameter, height, or
  crown closure; a single old plane tree and a sapling count identically;
  known local coverage gaps exist (docs/PHASE1_DATA_PROVENANCE.md S3).

PROXY 2 - Green-polygon coverage fraction
  Physical concept approximated: presence of vegetated/permeable land cover
  in the immediate surroundings (a proxy for evapotranspirative cooling and
  lower surface heat storage, not overhead canopy specifically - a paved
  plaza inside a park polygon counts the same as dense tree cover).
  Data: OSM leisure=park/garden + natural=wood + landuse=forest polygons
  (n=161 polygons in the study area), real full geometry (not centroids).
  Metric: % of a uniform 50 m circular buffer around the asset's point that
  intersects any such polygon.
  Limitation: OSM land-use polygons do not distinguish lawn from woodland;
  digitised polygon boundaries do not always match true canopy edges;
  coverage-by-area does not equal coverage-by-shadow at any given sun angle.

PROXY 3 - Building density (built-shade / street-canyon proxy)
  Physical concept approximated: potential for shade cast by adjacent
  buildings (street-canyon enclosure), a completely different physical
  mechanism from vegetation.
  Data: OSM building footprint centroids (n=1,099).
  Metric: count of building centroids within the same uniform 50 m buffer.
  Limitation: building HEIGHT is not available for most footprints in this
  area (docs/DATA_SOURCE_INVENTORY.csv) so this cannot approximate actual cast
  shadow, only structural density/enclosure - deliberately NOT a shadow model
  (that would require height + sun-angle geometry, i.e. the SOLWEIG-class
  analysis this Phase 1.1 pass explicitly does not start).

All three proxies use the SAME tercile-split method as the Phase 1 baseline
(empirical tercile of the pilot's own outdoor-asset distribution, documented,
not a literature constant) and feed the SAME feasibility_decision() logic
unmodified, so any classification differences are attributable to the proxy
choice alone.
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thresholds as th
from build_classifications import (
    load_assets, load_hazard_readings, feasibility_decision, TIMESTAMPS, UTM30N, WGS84,
)

ROOT = Path(__file__).resolve().parents[1]
INTERIM = ROOT / "data" / "interim"
PROCESSED = ROOT / "data" / "processed"
BUFFER_M = 50  # uniform buffer for proxies 2 and 3, matching proxy 1's point-based radius


def compute_proxy2_green_coverage(assets_utm):
    polys = gpd.read_file(INTERIM / "all_green_polygons.geojson").to_crs(UTM30N)
    green_union = polys.geometry.union_all()
    pct = []
    for geom in assets_utm.geometry:
        buf = geom.buffer(BUFFER_M)
        inter = buf.intersection(green_union)
        pct.append(round(100 * inter.area / buf.area, 1))
    return pct


def compute_proxy3_building_density(assets_utm):
    buildings = gpd.read_file(INTERIM / "buildings_centroids.geojson").to_crs(UTM30N)
    pts = buildings.geometry.values
    counts = []
    for geom in assets_utm.geometry:
        buf = geom.buffer(BUFFER_M)
        counts.append(sum(1 for p in pts if buf.contains(p)))
    return counts


def tercile_exposure_state(df, value_col, indoor_col):
    outdoor = df[df[indoor_col] == "outdoor"]
    q1, q2 = outdoor[value_col].quantile([1 / 3, 2 / 3])

    def f(row):
        if row[indoor_col] == "indoor":
            return None
        v = row[value_col]
        if v <= q1:
            return "HIGH"
        elif v <= q2:
            return "MODERATE"
        else:
            return "LOW"

    return df.apply(f, axis=1), (float(q1), float(q2))


def run_feasibility_for_proxy(assets, exposure_col, hazard_by_time):
    rows = []
    for _, a in assets.iterrows():
        for local_time, _ in TIMESTAMPS:
            temp_c = hazard_by_time[local_time]
            hz = th.meteorological_hazard_state(temp_c)
            row = {
                "indoor_outdoor": a["indoor_outdoor"],
                "meteorological_hazard_state": hz,
                "exposure_state": a[exposure_col],
                "adaptation_state": "GOOD",  # demoted gate, value irrelevant to feasibility_decision
            }
            feas, reason, _ = feasibility_decision(row)
            rows.append({"asset_id": a["asset_id"], "name": a["name"],
                         "indoor_outdoor": a["indoor_outdoor"], "timestamp": local_time,
                         "hazard": hz, "exposure_state": a[exposure_col], "feasibility_state": feas})
    return pd.DataFrame(rows)


def run():
    assets = load_assets()
    assets_utm = assets.to_crs(UTM30N)
    hazard_by_time = load_hazard_readings()

    # Proxy 1: reuse the already-computed baseline exposure_state directly from
    # the pipeline's own output, so proxy 1 here is IDENTICAL to the Phase 1
    # baseline (no re-derivation drift).
    baseline_cls = pd.read_csv(PROCESSED / "pilot_classifications.csv")
    p1_exposure = baseline_cls[baseline_cls["timestamp"].str.contains("12:00")][
        ["asset_id", "exposure_state"]].rename(columns={"exposure_state": "exposure_state_p1"})
    assets = assets.merge(p1_exposure, on="asset_id")

    # Proxy 2
    assets["green_coverage_pct"] = compute_proxy2_green_coverage(assets_utm)
    assets["exposure_state_p2"], p2_cuts = tercile_exposure_state(assets, "green_coverage_pct", "indoor_outdoor")

    # Proxy 3
    assets["building_count_50m"] = compute_proxy3_building_density(assets_utm)
    # NOTE: building density is a NEGATIVE indicator of exposure risk under this
    # framework's convention only if we assume more buildings -> more potential
    # shade. This is a deliberately weak, explicitly-flagged assumption (no
    # height data - see module docstring) - HIGH building density is mapped to
    # LOW exposure (more potential street-canyon shade), mirroring how MORE
    # trees -> LOW exposure in proxies 1/2, for direct comparability. This
    # mapping choice itself is a limitation, stated here rather than buried.
    assets["exposure_state_p3"], p3_cuts = tercile_exposure_state(assets, "building_count_50m", "indoor_outdoor")

    print("Proxy 2 (green coverage %) tercile cuts:", p2_cuts)
    print("Proxy 3 (building count 50m) tercile cuts:", p3_cuts)
    outdoor = assets[assets["indoor_outdoor"] == "outdoor"]
    print("\nPer-asset proxy values (outdoor only):")
    print(outdoor[["asset_id", "name", "exposure_state_p1", "green_coverage_pct", "exposure_state_p2",
                    "building_count_50m", "exposure_state_p3"]].sort_values("asset_id").to_string(index=False))

    # Feasibility under each proxy
    feas1 = run_feasibility_for_proxy(assets, "exposure_state_p1", hazard_by_time)
    feas2 = run_feasibility_for_proxy(assets, "exposure_state_p2", hazard_by_time)
    feas3 = run_feasibility_for_proxy(assets, "exposure_state_p3", hazard_by_time)

    merged = feas1.merge(feas2, on=["asset_id", "name", "indoor_outdoor", "timestamp", "hazard"],
                          suffixes=("_p1", "_p2"))
    merged = merged.merge(
        feas3[["asset_id", "timestamp", "feasibility_state"]].rename(columns={"feasibility_state": "feasibility_state_p3"}),
        on=["asset_id", "timestamp"])

    out_path = PROCESSED / "audit4_proxy_comparison.csv"
    merged.to_csv(out_path, index=False, encoding="utf-8")
    print(f"\nWrote {out_path} with {len(merged)} rows")

    # Agreement / confusion tables (outdoor rows only - indoor bypasses exposure
    # entirely, so proxy choice cannot affect them; confirm that explicitly).
    outdoor_rows = merged[merged["indoor_outdoor"] == "outdoor"]
    indoor_rows = merged[merged["indoor_outdoor"] == "indoor"]
    indoor_identical = (
        (indoor_rows["feasibility_state_p1"] == indoor_rows["feasibility_state_p2"]).all()
        and (indoor_rows["feasibility_state_p1"] == indoor_rows["feasibility_state_p3"]).all()
    )
    print(f"\nIndoor rows identical across all 3 proxies (expected True, exposure bypassed): {indoor_identical}")

    print(f"\n=== Outdoor rows: proxy 1 vs proxy 2 agreement ===")
    print(f"n={len(outdoor_rows)}, agree={sum(outdoor_rows.feasibility_state_p1 == outdoor_rows.feasibility_state_p2)}"
          f" ({100*sum(outdoor_rows.feasibility_state_p1 == outdoor_rows.feasibility_state_p2)/len(outdoor_rows):.1f}%)")
    print(pd.crosstab(outdoor_rows["feasibility_state_p1"], outdoor_rows["feasibility_state_p2"],
                       rownames=["Proxy1 (tree count)"], colnames=["Proxy2 (green coverage)"]))

    print(f"\n=== Outdoor rows: proxy 1 vs proxy 3 agreement ===")
    print(f"n={len(outdoor_rows)}, agree={sum(outdoor_rows.feasibility_state_p1 == outdoor_rows.feasibility_state_p3)}"
          f" ({100*sum(outdoor_rows.feasibility_state_p1 == outdoor_rows.feasibility_state_p3)/len(outdoor_rows):.1f}%)")
    print(pd.crosstab(outdoor_rows["feasibility_state_p1"], outdoor_rows["feasibility_state_p3"],
                       rownames=["Proxy1 (tree count)"], colnames=["Proxy3 (building density)"]))

    # Unstable assets: any outdoor asset whose feasibility_state differs
    # between ANY pair of proxies at ANY timestamp.
    def is_unstable(g):
        return not (g["feasibility_state_p1"].eq(g["feasibility_state_p1"].iloc[0]).all()
                    and g["feasibility_state_p2"].eq(g["feasibility_state_p1"].iloc[0]).all()
                    and g["feasibility_state_p3"].eq(g["feasibility_state_p1"].iloc[0]).all())

    unstable_ids = []
    for aid, g in outdoor_rows.groupby("asset_id"):
        row_unstable = (g["feasibility_state_p1"] != g["feasibility_state_p2"]) | \
                        (g["feasibility_state_p1"] != g["feasibility_state_p3"]) | \
                        (g["feasibility_state_p2"] != g["feasibility_state_p3"])
        if row_unstable.any():
            unstable_ids.append(aid)

    print(f"\nUnstable outdoor assets (feasibility differs between >=2 proxies at >=1 timestamp): "
          f"{len(unstable_ids)} / {outdoor_rows['asset_id'].nunique()}")
    unstable_detail = outdoor_rows[outdoor_rows["asset_id"].isin(unstable_ids)][
        ["asset_id", "name", "timestamp", "feasibility_state_p1", "feasibility_state_p2", "feasibility_state_p3"]
    ].sort_values(["asset_id", "timestamp"])
    print(unstable_detail.to_string(index=False))

    unstable_path = PROCESSED / "audit4_unstable_assets.csv"
    unstable_detail.to_csv(unstable_path, index=False, encoding="utf-8")
    print(f"\nWrote {unstable_path}")

    return assets, merged, unstable_ids


if __name__ == "__main__":
    run()
