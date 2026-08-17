"""
Fetch the REAL, complete set of official Ayuntamiento de Madrid tree records
within the study area from the live ARBOLADO ArcGIS MapServer
(sigma.madrid.es), paginating past the server's maxRecordCount=2000 limit.

Source: https://sigma.madrid.es/hosted/rest/services/MEDIO_AMBIENTE/ARBOLADO/MapServer
Layers used:
  8  - "Arbolado Parques Históricos (PV24)"  (point geometry, historic/singular parks - covers Retiro)
  11 - "Arbolado de alineación y Zonas Verdes (ZV21)" (point geometry, street/alignment + green-zone trees)
Both are official, live-maintained municipal layers (Dirección General de
Gestión del Agua y Zonas Verdes), CC BY 4.0 (same licence as the dataset's
CKAN listing on datos.madrid.es, "Arbolado en parques y zonas verdes de
Madrid (detalle)", id 300761).

TEMPORAL NOTE: this is the CURRENT live service, not an archived 2023
snapshot - see docs/PHASE1_2_TEMPORAL_ALIGNMENT.md for why no 2023 geospatial
archive exists and how this mismatch is handled.
"""
import json
import time
from pathlib import Path

import requests

OUT_DIR = Path(__file__).resolve().parents[1] / "data" / "raw" / "madrid_arbolado"
BASE = "https://sigma.madrid.es/hosted/rest/services/MEDIO_AMBIENTE/ARBOLADO/MapServer"
BBOX = "-3.6960,40.4040,-3.6775,40.4210"  # matches data/processed/study_area.geojson
PAGE_SIZE = 1000


def fetch_layer(layer_id, out_name):
    all_features = []
    offset = 0
    while True:
        params = {
            "geometry": BBOX,
            "geometryType": "esriGeometryEnvelope",
            "inSR": 4326,
            "outSR": 4326,
            "spatialRel": "esriSpatialRelIntersects",
            "outFields": "*",
            "returnGeometry": "true",
            "f": "geojson",
            "resultOffset": offset,
            "resultRecordCount": PAGE_SIZE,
        }
        r = requests.get(f"{BASE}/{layer_id}/query", params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        feats = data.get("features", [])
        all_features.extend(feats)
        print(f"  layer {layer_id}: offset={offset} got={len(feats)} total_so_far={len(all_features)}")
        if len(feats) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
        time.sleep(0.3)

    fc = {"type": "FeatureCollection", "features": all_features}
    out_path = OUT_DIR / out_name
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(fc, f, ensure_ascii=False)
    print(f"Wrote {out_path} with {len(all_features)} features")
    return all_features


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Fetching layer 11 (street/alignment + green-zone trees)...")
    fetch_layer(11, "arbolado_street_greenzone_full.geojson")
    print("Fetching layer 8 (historic parks trees)...")
    fetch_layer(8, "arbolado_parques_historicos_full.geojson")
