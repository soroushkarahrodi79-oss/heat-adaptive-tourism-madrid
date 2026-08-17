"""
Define the Phase 1 pilot study-area geometry: Prado - Retiro - Atocha, Madrid.

The boundary is a rectangle in WGS84 whose four edges are each pinned to a named,
verifiable landmark rather than drawn freehand, so the geometry is reproducible and
auditable. See docs/PHASE1_METHOD.md, section "Study area", for the full rationale.

Corner logic (each edge justified by what it must include / exclude):
  - North edge  (lat_max = 40.4210): just north of Puerta de Alcalá / Plaza de la
    Independencia (40.4201 N), the traditional gateway between the Paseo del Prado
    axis and Retiro Park.
  - South edge  (lat_min = 40.4040): just south of Estación de Madrid-Puerta de
    Atocha's full building extent (its OSM building-relation centroid falls at
    40.40456 N; a plain point at the forecourt is at 40.4063 N), so the whole real
    station footprint - not just its forecourt point - falls inside the box.
  - West edge   (lon_min = -3.6960): west of the Paseo del Prado sidewalk / CaixaForum
    Madrid (-3.6936 W), so the full width of the Prado-Thyssen-Reina Sofía corridor
    ("Paseo del Arte") is included.
  - East edge   (lon_max = -3.6775): east into Retiro park's interior past the
    Estanque Grande (-3.6844 W) and Palacio de Cristal (-3.6823 W), far enough to
    contain the real full-polygon centroids of two named shaded gardens used as
    pilot assets (Jardines de Cecilio Rodríguez, -3.67797 W; Jardines del
    Arquitecto Herrero Palacios, -3.67863 W), so a genuine cross-section of
    shaded/vegetated park interior is represented, not just the park's western
    fringe.

These last two edges were widened by ~150 m and ~150 m respectively from an
initial landmark-only draft, after a reproducibility test (tests/test_outputs.py)
caught that three real, legitimately-curated pilot assets (the Atocha station
building, and the two named gardens above) had OSM centroids just outside the
draft box - because Overpass returns a way/relation's full-geometry centroid
even when only part of the feature intersects the query bounding box. Rather
than discard those real assets or silently leave the study-area polygon not
actually containing the pilot set it was drawn to represent, the box was
widened to honestly contain them. See docs/PHASE1_METHOD.md for the final
figures.

This yields an approx. 1.9 km (N-S) x 2.1 km (E-W) bounding box, ~3.5 sq km:
still small enough to be a defensible, walkable "pilot", per FEASIBILITY_GATE.md's
explicit instruction not to expand city-wide.
"""
import json
from pathlib import Path

from shapely.geometry import box, mapping

OUT_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

LAT_MIN, LAT_MAX = 40.4040, 40.4210
LON_MIN, LON_MAX = -3.6960, -3.6775

LANDMARKS = {
    "Puerta de Alcalá (N reference)": (40.4201, -3.6883),
    "Estación de Madrid-Puerta de Atocha (S reference, full building centroid)": (40.40456, -3.68868),
    "CaixaForum Madrid / Paseo del Prado west edge (W reference)": (40.4113, -3.6936),
    "Jardines de Cecilio Rodríguez (E interior reference, real polygon centroid)": (40.41335, -3.67797),
}


def build_study_area():
    geom = box(LON_MIN, LAT_MIN, LON_MAX, LAT_MAX)
    feature = {
        "type": "Feature",
        "properties": {
            "name": "HATI-Madrid Phase 1 pilot study area",
            "description": "Prado - Retiro - Atocha bounded pilot",
            "lat_min": LAT_MIN,
            "lat_max": LAT_MAX,
            "lon_min": LON_MIN,
            "lon_max": LON_MAX,
            "area_km2": round(geom_area_km2(geom), 3),
            "crs": "EPSG:4326",
            "landmarks_used_for_boundary": LANDMARKS,
        },
        "geometry": mapping(geom),
    }
    fc = {"type": "FeatureCollection", "features": [feature]}
    out_path = OUT_DIR / "study_area.geojson"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(fc, f, indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")
    return geom


def geom_area_km2(geom):
    # Equirectangular approximation at study-area latitude, adequate for a
    # ~1.5 km pilot box (no projected CRS dependency needed for this sanity figure).
    import math

    lat0 = (LAT_MIN + LAT_MAX) / 2
    km_per_deg_lat = 111.32
    km_per_deg_lon = 111.32 * math.cos(math.radians(lat0))
    width_km = (LON_MAX - LON_MIN) * km_per_deg_lon
    height_km = (LAT_MAX - LAT_MIN) * km_per_deg_lat
    return width_km * height_km


if __name__ == "__main__":
    build_study_area()
