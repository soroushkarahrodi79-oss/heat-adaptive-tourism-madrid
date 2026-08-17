"""
Phase 1.1 Audit 3: does the adaptation-resource gate (water/transit walkable
access) add meaningful discrimination?

Phase 1 finding: adaptation_state was GOOD or LIMITED for all 27 pilot assets;
POOR never occurred, so the gate never independently excluded a site
(docs/PHASE1_VALIDATION_REPORT.md S3).

This script runs two real-data tests, per the Phase 1.1 task spec:

  A) THRESHOLD SENSITIVITY on the existing 27 assets: grid-search the water/
     transit distance thresholds and find where (if anywhere) a defensible
     tightening starts producing POOR.

  B) SMALL BOUNDED RING EXTENSION: 6 additional real, named, OSM-sourced
     tourism-relevant assets just beyond the current study-area box, still
     within/adjacent to Retiro and the Atocha fringe (NOT city-wide expansion),
     evaluated against a correspondingly widened real water/transit point set.
     These are kept OUT of data/processed/pilot_assets.csv - they are a
     discrimination-test sample, not an adopted expansion of the Phase 1 pilot.

Both real-data test results are combined into a single recommendation: keep,
demote, or remove the gate.
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thresholds as th
from build_classifications import load_hazard_readings, TIMESTAMPS, EPISODE_DATE

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "osm"
PROCESSED = ROOT / "data" / "processed"
WGS84 = "EPSG:4326"
UTM30N = "EPSG:25830"

# 6 real OSM assets just outside the current study-area box, within a bounded
# ring around it (thematically Retiro/Atocha-adjacent) - see osm_ring_raw.json.
RING_ASSETS = [
    # (osm_type, osm_id, name, category, indoor_outdoor)
    ("relation", 2468711, "Plaza Niño Jesús", "park_general", "outdoor"),
    ("way", 15245169, "Jardines Doce de Octubre", "garden_outdoor", "outdoor"),
    ("way", 472650975, "Parque Daoíz y Velarde", "park_general", "outdoor"),
    ("way", 48761444, "La Casa Encendida", "museum_indoor", "indoor"),
    ("way", 239434996, "Jardín de Palestina", "garden_outdoor", "outdoor"),
    ("node", 5774110605, "Casa de Cervantes", "museum_indoor", "indoor"),
]


def load_ring_index():
    with open(RAW / "osm_ring_raw.json", "r", encoding="utf-8") as f:
        els = json.load(f)["elements"]
    return {(e["type"], e["id"]): e for e in els}


def latlon(e):
    if "lat" in e:
        return e["lat"], e["lon"]
    c = e.get("center")
    return (c["lat"], c["lon"]) if c else (None, None)


def build_ring_asset_gdf():
    idx = load_ring_index()
    rows = []
    for etype, eid, name, cat, io in RING_ASSETS:
        e = idx[(etype, eid)]
        lat, lon = latlon(e)
        rows.append({"asset_id": f"R{len(rows)+1:02d}", "name": name, "category": cat,
                      "indoor_outdoor": io, "latitude": lat, "longitude": lon,
                      "source": f"OpenStreetMap {etype}/{eid} (ring extension, ODbL)"})
    df = pd.DataFrame(rows)
    return gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs=WGS84)


def load_ring_points(fname, tag_filter):
    with open(RAW / fname, "r", encoding="utf-8") as f:
        els = json.load(f)["elements"]
    recs = []
    for e in els:
        t = e.get("tags", {})
        if not tag_filter(t):
            continue
        lat, lon = latlon(e)
        if lat is None:
            continue
        recs.append({"lat": lat, "lon": lon})
    geoms = [Point(r["lon"], r["lat"]) for r in recs]
    return gpd.GeoDataFrame(recs, geometry=geoms, crs=WGS84)


def nearest_m(gdf_utm, pts_utm):
    out = []
    pts = pts_utm.geometry.values
    for geom in gdf_utm.geometry.values:
        out.append(round(min(geom.distance(p) for p in pts), 1))
    return out


def part_a_threshold_sensitivity():
    print("=" * 70)
    print("PART A: threshold sensitivity on the existing 27 pilot assets")
    print("=" * 70)
    cls = pd.read_csv(PROCESSED / "pilot_classifications.csv")
    df = cls[cls["timestamp"].str.contains("12:00")][["asset_id", "name", "water_dist_m", "transit_dist_m"]]
    grid = []
    for w in (250, 200, 150, 100, 75, 50):
        for t in (400, 300, 200, 150, 100):
            good = ((df.water_dist_m <= w) & (df.transit_dist_m <= t)).sum()
            poor = ((df.water_dist_m > w) & (df.transit_dist_m > t)).sum()
            grid.append((w, t, good, len(df) - good - poor, poor))
    grid_df = pd.DataFrame(grid, columns=["water_thr_m", "transit_thr_m", "GOOD", "LIMITED", "POOR"])
    print(grid_df.to_string(index=False))
    first_poor = grid_df[grid_df["POOR"] > 0].sort_values(["water_thr_m", "transit_thr_m"], ascending=False)
    print("\nLoosest threshold pair that produces >=1 POOR case:")
    print(first_poor.tail(1).to_string(index=False) if len(first_poor) else "NONE found in grid")
    return grid_df


def part_b_ring_extension():
    print("\n" + "=" * 70)
    print("PART B: small bounded ring extension (6 real assets)")
    print("=" * 70)
    ring = build_ring_asset_gdf()
    water = load_ring_points("osm_ring_water_raw.json", lambda t: t.get("amenity") in ("drinking_water", "fountain"))
    transit = load_ring_points(
        "osm_ring_transit_raw.json",
        lambda t: (t.get("railway") in ("station", "halt") or t.get("public_transport") == "station"
                   or t.get("station") == "subway" or t.get("highway") == "bus_stop"),
    )
    print(f"Ring water points: {len(water)}, ring transit points: {len(transit)}")

    ring_utm = ring.to_crs(UTM30N)
    water_utm = water.to_crs(UTM30N)
    transit_utm = transit.to_crs(UTM30N)
    ring["water_dist_m"] = nearest_m(ring_utm, water_utm)
    ring["transit_dist_m"] = nearest_m(ring_utm, transit_utm)
    ring["adaptation_state"] = ring.apply(
        lambda r: th.adaptation_state(r["water_dist_m"], r["transit_dist_m"]), axis=1
    )
    print(ring[["asset_id", "name", "indoor_outdoor", "water_dist_m", "transit_dist_m", "adaptation_state"]]
          .to_string(index=False))

    # Also recompute the core 27's adaptation_state against this WIDER (superset)
    # water/transit set, as a consistency check that widening the search set
    # doesn't change the core pilot's own GOOD/LIMITED/POOR mix.
    core = pd.read_csv(PROCESSED / "pilot_assets.csv")
    core_gdf = gpd.GeoDataFrame(core, geometry=gpd.points_from_xy(core.longitude, core.latitude), crs=WGS84)
    core_utm = core_gdf.to_crs(UTM30N)
    core["water_dist_m_wide"] = nearest_m(core_utm, water_utm)
    core["transit_dist_m_wide"] = nearest_m(core_utm, transit_utm)
    core["adaptation_state_wide"] = core.apply(
        lambda r: th.adaptation_state(r["water_dist_m_wide"], r["transit_dist_m_wide"]), axis=1
    )
    cls = pd.read_csv(PROCESSED / "pilot_classifications.csv")
    orig = cls[cls["timestamp"].str.contains("12:00")][["asset_id", "adaptation_state"]].rename(
        columns={"adaptation_state": "adaptation_state_orig"})
    merged = core.merge(orig, on="asset_id")
    changed = merged[merged["adaptation_state_orig"] != merged["adaptation_state_wide"]]
    print(f"\nCore-27 adaptation_state changed when using the wider ring water/transit set: "
          f"{len(changed)} / {len(merged)}")
    if len(changed):
        print(changed[["asset_id", "name", "adaptation_state_orig", "adaptation_state_wide"]].to_string(index=False))

    # Feasibility impact: run the ring assets through the real 2023-08-21 hazard
    # timestamps and check whether adaptation_state ever changes the outcome
    # (i.e. whether removing the adaptation gate would change any ring result).
    hazard_by_time = load_hazard_readings()
    from build_classifications import feasibility_decision
    rows = []
    for _, a in ring.iterrows():
        for local_time, _ in TIMESTAMPS:
            temp_c = hazard_by_time[local_time]
            hz = th.meteorological_hazard_state(temp_c)
            # exposure_state is forced to MODERATE (not HIGH) for outdoor ring
            # assets. Rule 2 (SEVERE + exposure==HIGH -> NOT RECOMMENDED) is
            # checked BEFORE rule 3 (SEVERE + adaptation==POOR -> NOT
            # RECOMMENDED) in feasibility_decision()'s first-match-wins order;
            # forcing HIGH would make rule 2 fire first and short-circuit
            # before rule 3 (the adaptation rule) is ever reached, which would
            # silently defeat the point of this isolation test. MODERATE lets
            # execution reach rule 3, so adaptation_state's real marginal
            # effect (if any) is actually observable here.
            row = {
                "indoor_outdoor": a["indoor_outdoor"],
                "meteorological_hazard_state": hz,
                "exposure_state": "MODERATE" if a["indoor_outdoor"] == "outdoor" else None,
                "adaptation_state": a["adaptation_state"],
            }
            feas, reason, _ = feasibility_decision(row)
            rows.append({"asset_id": a["asset_id"], "name": a["name"], "timestamp": local_time,
                         "hazard": hz, "adaptation_state": a["adaptation_state"], "feasibility_with_gate": feas})
    feas_df = pd.DataFrame(rows)
    print("\nRing-asset feasibility at real 2023-08-21 timestamps "
          "(exposure_state forced to MODERATE for outdoor ring assets so rule 3, "
          "the adaptation-based exclusion, is actually reachable - see comment above):")
    print(feas_df.to_string(index=False))
    print("\nWould any row change if the adaptation gate (rule 3) were deleted "
          "outright? Compare feasibility_with_gate above against a version with "
          "rule 3 removed:")
    from thresholds import AEMET_MADRID_METRO_ORANGE_C, AEMET_MADRID_METRO_RED_C
    no_gate_rows = []
    for _, r in feas_df.iterrows():
        if r["hazard"] == "SEVERE" and r["adaptation_state"] == "POOR":
            no_gate_rows.append("FEASIBLE WITH CONDITIONS")  # what rule 4 would give instead
        else:
            no_gate_rows.append(r["feasibility_with_gate"])
    feas_df["feasibility_without_adaptation_gate"] = no_gate_rows
    diff = feas_df[feas_df["feasibility_with_gate"] != feas_df["feasibility_without_adaptation_gate"]]
    print(f"Rows that would change if rule 3 were deleted: {len(diff)} / {len(feas_df)}")

    out_path = PROCESSED / "audit3_ring_extension.csv"
    ring.drop(columns=["latitude", "longitude"]).to_csv(out_path, index=False, encoding="utf-8")
    print(f"\nWrote {out_path}")
    return ring, feas_df


if __name__ == "__main__":
    part_a_threshold_sensitivity()
    part_b_ring_extension()
