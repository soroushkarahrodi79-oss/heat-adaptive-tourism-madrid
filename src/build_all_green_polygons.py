"""
Parse ALL real green-space polygons in the study area (not just the 8 pilot
assets that are themselves parks/gardens - see build_green_polygons.py) into a
single GeoDataFrame, for use as the Audit 4 green-coverage exposure proxy.

Input: data/raw/osm/osm_all_green_polygons_raw.json (Overpass "out geom",
leisure=park/garden + natural=wood + landuse=forest, study-area bbox, fetched
2026-08-17, ODbL).
Output: data/interim/all_green_polygons.geojson
"""
import json
from pathlib import Path

import geopandas as gpd
from shapely.geometry import Polygon
from shapely.ops import unary_union

RAW = Path(__file__).resolve().parents[1] / "data" / "raw" / "osm" / "osm_all_green_polygons_raw.json"
OUT = Path(__file__).resolve().parents[1] / "data" / "interim" / "all_green_polygons.geojson"
WGS84 = "EPSG:4326"


def way_to_polygon(way):
    coords = [(pt["lon"], pt["lat"]) for pt in way.get("geometry", []) if pt]
    if len(coords) < 3:
        return None
    try:
        p = Polygon(coords)
        return p if p.is_valid and p.area > 0 else None
    except Exception:
        return None


def relation_to_polygon(rel):
    polys = []
    for m in rel.get("members", []):
        if m.get("type") == "way" and m.get("role") in ("outer", ""):
            geom = m.get("geometry")
            if not geom or len(geom) < 3:
                continue
            try:
                p = Polygon([(pt["lon"], pt["lat"]) for pt in geom])
                if p.is_valid and p.area > 0:
                    polys.append(p)
            except Exception:
                continue
    return unary_union(polys) if polys else None


def build():
    with open(RAW, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = []
    for e in data["elements"]:
        geom = way_to_polygon(e) if e["type"] == "way" else relation_to_polygon(e)
        if geom is None or geom.is_empty:
            continue
        t = e.get("tags", {})
        records.append({
            "osm_id": f"{e['type']}/{e['id']}",
            "name": t.get("name:es") or t.get("name") or "",
            "kind": t.get("leisure") or t.get("natural") or t.get("landuse") or "",
            "geometry": geom,
        })

    gdf = gpd.GeoDataFrame(records, geometry="geometry", crs=WGS84)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(OUT, driver="GeoJSON")
    print(f"Wrote {OUT} with {len(gdf)} polygons")
    return gdf


if __name__ == "__main__":
    build()
