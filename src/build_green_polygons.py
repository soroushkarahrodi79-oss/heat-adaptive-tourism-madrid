"""
Build real polygon geometry for the pilot assets whose OSM footprint is an area
(park/garden/plaza), not a single point - so on-site tree exposure is measured
against the asset's actual extent rather than a single Overpass "center" centroid.

Why this exists: the first classification pass (build_classifications.py) buffered
each asset's centroid by 50 m and counted trees inside. For large or irregularly
shaped polygons (Parque del Retiro; the shaded gardens Jardines de Cecilio
Rodríguez, La Rosaleda, Jardín del Parterre), the Overpass-reported centroid can
land on an open lawn, path, or pond well away from the tree canopy that makes the
site notable in the first place, understating exposure for exactly the
"strong-vegetation" category the brief asks the pilot set to represent. That is a
geometry artefact, not a real finding, and reporting it uncorrected would be a
methodological error - so it is fixed here using each site's real OSM polygon.

Input: data/raw/osm/osm_green_polygons_raw.json (Overpass "out geom", fetched
2026-08-17, ODbL - see data/raw/osm/README.md).
Output: data/interim/green_polygons.geojson
"""
import json
from pathlib import Path

import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union

RAW = Path(__file__).resolve().parents[1] / "data" / "raw" / "osm" / "osm_green_polygons_raw.json"
OUT = Path(__file__).resolve().parents[1] / "data" / "interim" / "green_polygons.geojson"

WGS84 = "EPSG:4326"

# asset_id in pilot_assets.csv <- (osm_type, osm_id)
ASSET_MAP = {
    ("relation", 13616929): "A20",
    ("way", 15244804): "A21",
    ("way", 23596451): "A22",
    ("relation", 10005473): "A23",
    ("way", 29471363): "A24",
    ("relation", 20827650): "A25",
    ("way", 722360391): "A26",
    ("relation", 10005474): "A27",
}


def way_to_polygon(way):
    coords = [(pt["lon"], pt["lat"]) for pt in way["geometry"]]
    if len(coords) < 3:
        return None
    return Polygon(coords)


def relation_to_polygon(rel):
    outer_rings = []
    for m in rel.get("members", []):
        if m.get("type") == "way" and m.get("role") in ("outer", ""):
            geom = m.get("geometry")
            if not geom or len(geom) < 3:
                continue
            coords = [(pt["lon"], pt["lat"]) for pt in geom]
            outer_rings.append(coords)
    polys = []
    for ring in outer_rings:
        try:
            p = Polygon(ring)
            if p.is_valid and p.area > 0:
                polys.append(p)
        except Exception:
            continue
    if not polys:
        return None
    return unary_union(polys)


def build():
    with open(RAW, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = []
    for e in data["elements"]:
        key = (e["type"], e["id"])
        if key not in ASSET_MAP:
            continue
        if e["type"] == "way":
            geom = way_to_polygon(e)
        else:
            geom = relation_to_polygon(e)
        if geom is None or geom.is_empty:
            print(f"WARNING: no usable polygon for {key}")
            continue
        t = e.get("tags", {})
        records.append({
            "asset_id": ASSET_MAP[key],
            "osm_id": f"{e['type']}/{e['id']}",
            "name": t.get("name:es") or t.get("name") or "",
            "area_m2_wgs84_approx": None,  # computed after reprojection below
            "geometry": geom,
        })

    gdf = gpd.GeoDataFrame(records, geometry="geometry", crs=WGS84)
    gdf_utm = gdf.to_crs("EPSG:25830")
    gdf["area_m2"] = gdf_utm.geometry.area.round(0)
    gdf = gdf.drop(columns=["area_m2_wgs84_approx"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(OUT, driver="GeoJSON")
    print(f"Wrote {OUT} with {len(gdf)} polygons")
    for _, r in gdf.iterrows():
        print(f"  {r['asset_id']} {r['name']}: {r['area_m2']:.0f} m2")
    return gdf


if __name__ == "__main__":
    build()
