"""
Parse the real, official Ayuntamiento de Madrid tree records (fetched by
src/fetch_madrid_arbolado.py from the live ARBOLADO ArcGIS MapServer) into a
single clean point GeoDataFrame for the Phase 1.2 P1 proxy.

Input: data/raw/madrid_arbolado/arbolado_street_greenzone_full.geojson (6,089
real records, layer 11 "Arbolado de alineación y Zonas Verdes"),
arbolado_parques_historicos_full.geojson (34,751 real records, layer 8
"Arbolado Parques Históricos" - covers Retiro/Real Jardín Botánico area).
Output: data/interim/madrid_arbolado_points.geojson
"""
import json
from pathlib import Path

import geopandas as gpd
from shapely.geometry import shape

RAW = Path(__file__).resolve().parents[1] / "data" / "raw" / "madrid_arbolado"
OUT = Path(__file__).resolve().parents[1] / "data" / "interim" / "madrid_arbolado_points.geojson"
WGS84 = "EPSG:4326"


def load_layer(fname, source_layer):
    with open(RAW / fname, "r", encoding="utf-8") as f:
        fc = json.load(f)
    records = []
    for feat in fc["features"]:
        geom = feat.get("geometry")
        if geom is None:
            continue
        props = feat.get("properties", {})
        records.append({
            "source_layer": source_layer,
            "objectid": props.get("OBJECTID"),
            "especie": props.get("NOMBRE_ESPECIE") or "",
            "nombre_comun": props.get("NOMBRE_COMUN") or "",
            "altura_m": props.get("ALTURA"),
            "distrito": props.get("NOMBRE_DISTRITO") or "",
            "barrio": props.get("NOMBRE_BARRIO") or "",
            "geometry": shape(geom),
        })
    return records


def build():
    recs = load_layer("arbolado_street_greenzone_full.geojson", "street_greenzone")
    recs += load_layer("arbolado_parques_historicos_full.geojson", "parques_historicos")
    gdf = gpd.GeoDataFrame(recs, geometry="geometry", crs=WGS84)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(OUT, driver="GeoJSON")
    print(f"Wrote {OUT} with {len(gdf)} real official tree points")
    print(gdf["source_layer"].value_counts())
    return gdf


if __name__ == "__main__":
    build()
