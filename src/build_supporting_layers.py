"""
Parse the raw OSM Overpass extracts into clean point-layer GeoJSONs for the
exposure / adaptation-resource proxy computation.

Inputs (data/raw/osm/, see README.md there for query + licence provenance):
  - osm_trees_raw.json          natural=tree nodes (real coordinates, point-precise)
  - osm_pois_raw.json           leisure=park/garden, amenity=drinking_water/fountain,
                                 rail/metro stations (way/relation geometry reduced to
                                 Overpass "center" centroid — see limitation note below)
  - osm_buildings_bus_raw.json  building footprints (centroid) + bus stops (point)

Outputs (data/interim/):
  - trees.geojson              point layer, real tree locations
  - green_spaces.geojson       point layer (centroids), parks/gardens
  - water_points.geojson       point layer, drinking water + fountains
  - transit_points.geojson     point layer, rail/metro stations + bus stops
  - buildings_centroids.geojson point layer, building centroids

LIMITATION (documented, not hidden): the POI and building queries used Overpass's
"out center" mode, which returns a single representative centroid for way/relation
geometries rather than the full polygon ring. This is sufficient for proximity /
density proxies (distance-to-nearest, point-count-within-buffer) but NOT sufficient
for area-coverage-fraction analysis (e.g. "% of a 100 m buffer covered by park
polygon"). The Phase 1 exposure/adaptation proxies below are therefore built only
from distance- and count-based statistics, which this data fully supports; polygon
coverage-fraction analysis is left for a future phase if justified. See
docs/PHASE1_METHOD.md and docs/PHASE1_DATA_PROVENANCE.md.
"""
import json
from pathlib import Path

import geopandas as gpd
from shapely.geometry import Point

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw" / "osm"
OUT_DIR = Path(__file__).resolve().parents[1] / "data" / "interim"
OUT_DIR.mkdir(parents=True, exist_ok=True)

WGS84 = "EPSG:4326"


def _load(fname):
    with open(RAW_DIR / fname, "r", encoding="utf-8") as f:
        return json.load(f)["elements"]


def _latlon(e):
    if "lat" in e:
        return e["lat"], e["lon"]
    c = e.get("center")
    if c:
        return c["lat"], c["lon"]
    return None, None


def _to_gdf(records):
    geoms = [Point(r["lon"], r["lat"]) for r in records]
    gdf = gpd.GeoDataFrame(records, geometry=geoms, crs=WGS84)
    return gdf.drop(columns=["lat", "lon"])


def build_trees():
    els = _load("osm_trees_raw.json")
    records = []
    for e in els:
        lat, lon = _latlon(e)
        if lat is None:
            continue
        t = e.get("tags", {})
        records.append({
            "osm_id": f"{e['type']}/{e['id']}",
            "genus": t.get("genus") or t.get("species") or "",
            "lat": lat, "lon": lon,
        })
    gdf = _to_gdf(records)
    gdf.to_file(OUT_DIR / "trees.geojson", driver="GeoJSON")
    print(f"trees: {len(gdf)} -> {OUT_DIR / 'trees.geojson'}")


def build_green_spaces():
    els = _load("osm_pois_raw.json")
    records = []
    for e in els:
        t = e.get("tags", {})
        if t.get("leisure") in ("park", "garden"):
            lat, lon = _latlon(e)
            if lat is None:
                continue
            records.append({
                "osm_id": f"{e['type']}/{e['id']}",
                "name": t.get("name:es") or t.get("name") or "",
                "leisure": t.get("leisure"),
                "lat": lat, "lon": lon,
            })
    gdf = _to_gdf(records)
    gdf.to_file(OUT_DIR / "green_spaces.geojson", driver="GeoJSON")
    print(f"green_spaces: {len(gdf)} -> {OUT_DIR / 'green_spaces.geojson'}")


def build_water_points():
    els = _load("osm_pois_raw.json")
    records = []
    for e in els:
        t = e.get("tags", {})
        if t.get("amenity") in ("drinking_water", "fountain"):
            lat, lon = _latlon(e)
            if lat is None:
                continue
            records.append({
                "osm_id": f"{e['type']}/{e['id']}",
                "amenity": t.get("amenity"),
                "lat": lat, "lon": lon,
            })
    gdf = _to_gdf(records)
    gdf.to_file(OUT_DIR / "water_points.geojson", driver="GeoJSON")
    print(f"water_points: {len(gdf)} -> {OUT_DIR / 'water_points.geojson'}")


def build_transit_points():
    poi_els = _load("osm_pois_raw.json")
    bus_els = _load("osm_buildings_bus_raw.json")
    records = []
    for e in poi_els:
        t = e.get("tags", {})
        if (t.get("railway") in ("station", "halt")
                or t.get("public_transport") == "station"
                or t.get("station") == "subway"):
            lat, lon = _latlon(e)
            if lat is None:
                continue
            records.append({
                "osm_id": f"{e['type']}/{e['id']}",
                "name": t.get("name:es") or t.get("name") or "",
                "mode": "rail_metro",
                "lat": lat, "lon": lon,
            })
    for e in bus_els:
        t = e.get("tags", {})
        if t.get("highway") == "bus_stop":
            lat, lon = _latlon(e)
            if lat is None:
                continue
            records.append({
                "osm_id": f"{e['type']}/{e['id']}",
                "name": t.get("name") or "",
                "mode": "bus",
                "lat": lat, "lon": lon,
            })
    gdf = _to_gdf(records)
    gdf.to_file(OUT_DIR / "transit_points.geojson", driver="GeoJSON")
    print(f"transit_points: {len(gdf)} -> {OUT_DIR / 'transit_points.geojson'}")


def build_building_centroids():
    els = _load("osm_buildings_bus_raw.json")
    records = []
    for e in els:
        t = e.get("tags", {})
        if t.get("building"):
            lat, lon = _latlon(e)
            if lat is None:
                continue
            records.append({
                "osm_id": f"{e['type']}/{e['id']}",
                "building": t.get("building"),
                "lat": lat, "lon": lon,
            })
    gdf = _to_gdf(records)
    gdf.to_file(OUT_DIR / "buildings_centroids.geojson", driver="GeoJSON")
    print(f"buildings_centroids: {len(gdf)} -> {OUT_DIR / 'buildings_centroids.geojson'}")


if __name__ == "__main__":
    build_trees()
    build_green_spaces()
    build_water_points()
    build_transit_points()
    build_building_centroids()
