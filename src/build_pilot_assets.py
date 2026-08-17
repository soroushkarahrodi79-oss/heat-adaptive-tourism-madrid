"""
Curate the Phase 1 pilot tourism-asset list from real OSM data.

Source: data/raw/osm/osm_pois_raw.json (Overpass API extract, ODbL, fetched 2026-08-17,
see data/raw/osm/README.md for the exact query and licence terms).

This script does NOT invent, relocate, or synthesise any point. Every asset below is
selected by its real OSM type/id from the raw extract; the script fails loudly if an
id is missing from the source file, so the list cannot silently drift from real data.

Selection principle: hand-curate ~25-30 assets that (a) are real, named, verifiable
places within the study area, and (b) collectively span the adaptation-condition
categories the brief requires (outdoor attractions, shaded outdoor spaces, green
areas, museums/indoor attractions, transport-accessible alternatives). Whether a
given site *actually* has poor shade or strong vegetation is NOT decided here by
hand-label — it is computed later in src/build_classifications.py from real buffer
statistics against the OSM tree/building/park layers, so the exposure state is
data-derived, not asserted.
"""
import json
from pathlib import Path

import pandas as pd

RAW = Path(__file__).resolve().parents[1] / "data" / "raw" / "osm" / "osm_pois_raw.json"
OUT = Path(__file__).resolve().parents[1] / "data" / "processed" / "pilot_assets.csv"

# (osm_type, osm_id, category, indoor_outdoor, evidence_notes)
CURATED = [
    # --- Museums / indoor attractions ---
    ("relation", 7726080, "museum_indoor", "indoor",
     "Museo Nacional del Prado, main building (Edificio Villanueva). Air-conditioned gallery space; principal indoor cool-alternative anchor of the study area."),
    ("way", 991444051, "museum_indoor", "indoor",
     "Museo Nacional Centro de Arte Reina Sofía. Major indoor museum, south end of Paseo del Arte."),
    ("relation", 1869336, "museum_indoor", "indoor",
     "Museo Thyssen-Bornemisza. Indoor museum, north end of Paseo del Arte."),
    ("way", 286816147, "museum_indoor", "indoor",
     "CaixaForum Madrid. Indoor cultural centre; building also has an external vegetated wall (Jardín Vertical), noted for context but classified by its indoor visitor function."),
    ("way", 292649859, "museum_indoor", "indoor",
     "Museo Naval de Madrid. Indoor museum."),
    ("relation", 4525000, "museum_indoor", "indoor",
     "Museo Nacional de Antropología. Indoor museum."),
    ("relation", 8278843, "museum_indoor", "indoor",
     "Museo Nacional de Artes Decorativas. Indoor museum."),
    ("way", 30759780, "museum_indoor", "indoor",
     "Real Fábrica de Tapices. Working tapestry workshop and museum, indoor visit."),

    # --- Transport-accessible alternatives ---
    ("way", 733993037, "transit_hub", "indoor",
     "Estación de Madrid-Puerta de Atocha-Almudena Grandes: main-line rail terminus, air-conditioned concourse; principal transit-accessible indoor refuge at the south end of the study area."),
    ("node", 5299314577, "transit_hub", "indoor",
     "Estación del Arte (Metro Línea 1, formerly 'Atocha'). Underground metro station, indoor/underground refuge and rapid-transit anchor."),
    ("node", 25903356, "transit_hub", "indoor",
     "Retiro (Metro Línea 2). Underground metro station at the NE study-area boundary, adjacent to Puerta de Alcalá / Retiro."),
    ("node", 5303271999, "transit_hub", "indoor",
     "Banco de España (Metro Línea 2). Underground metro station near Cibeles / Paseo del Prado."),
    ("way", 554720472, "transit_hub_green", "indoor",
     "Jardín Tropical, historic Atocha station hall (Estación de Atocha antigua). A glazed indoor tropical garden inside the former station's train shed — unusual dual-role site: transit-adjacent AND indoor vegetated cool refuge; kept as its own asset because it is not a typical museum or ordinary station concourse."),

    # --- Outdoor monuments / attractions, largely open and hard-surfaced ---
    ("way", 174805987, "monument_outdoor", "outdoor",
     "Puerta de Alcalá. Free-standing neoclassical gate on a large open traffic roundabout/plaza; minimal overhead shade at the monument itself."),
    ("relation", 6345116, "monument_outdoor", "outdoor",
     "Fuente de Cibeles, Plaza de Cibeles. Open monumental roundabout plaza, hard-paved, minimal tree cover immediately at the fountain."),
    ("way", 553098274, "monument_outdoor", "outdoor",
     "Fuente de Neptuno, Plaza de Cánovas del Castillo. Open traffic-circle plaza between the Prado and Thyssen; minimal shade at the fountain itself."),
    ("node", 2045974223, "monument_outdoor", "outdoor",
     "Estatua de Goya, Prado forecourt (Puerta de Goya entrance area). High-footfall queueing area on the Paseo del Prado sidewalk; sparse street-tree shade."),
    ("node", 8928518873, "monument_outdoor", "outdoor",
     "Palacio de Cibeles (Ayuntamiento de Madrid). Landmark building with public viewpoint (mirador); surrounding plaza is open and hard-paved."),
    ("way", 29471311, "monument_outdoor", "outdoor",
     "Real Observatorio de Madrid. Historic hilltop observatory building at the south edge of the study area; elevated, exposed site with limited surrounding canopy."),

    # --- Green areas / shaded outdoor spaces ---
    ("relation", 13616929, "park_general", "outdoor",
     "Parque del Retiro. The study area's largest green space; asset point placed at the Estanque Grande (central lake) as the park's best-known tourist anchor."),
    ("way", 15244804, "garden_outdoor", "outdoor",
     "Real Jardín Botánico de Madrid. Densely planted, ticketed botanical garden immediately south of the Prado."),
    ("way", 23596451, "outdoor_pavilion_shaded", "outdoor",
     "Palacio de Cristal, Parque del Retiro. Glass exhibition pavilion beside a small lake, set within mature tree cover."),
    ("relation", 10005473, "garden_outdoor", "outdoor",
     "Jardines de Cecilio Rodríguez, Parque del Retiro. Formal, densely-planted, well-shaded garden (cedars, fountains, peacocks), a well-documented cool micro-site within the park."),
    ("way", 29471363, "garden_outdoor", "outdoor",
     "La Rosaleda, Parque del Retiro. Rose garden; planted but lower-canopy than Cecilio Rodríguez (shrub-height roses rather than closed tree canopy)."),
    ("relation", 20827650, "garden_outdoor", "outdoor",
     "Jardín del Parterre, Parque del Retiro. Formal historic garden near the Casón del Buen Retiro, mixed open lawn and mature trees."),
    ("way", 722360391, "outdoor_attraction_mixed_shade", "outdoor",
     "Monumento a Alfonso XII / Estanque Grande colonnade. Iconic lake-front monument; monument steps are open and sun-exposed, lake-path edges have tree shade nearby."),
    ("relation", 10005474, "garden_outdoor", "outdoor",
     "Jardines del Arquitecto Herrero Palacios, Parque del Retiro. Planted garden area near Puerta de Alcalá / Casa de Fieras, mature tree cover."),
]


def load_osm_index():
    with open(RAW, "r", encoding="utf-8") as f:
        data = json.load(f)
    idx = {}
    for e in data["elements"]:
        idx[(e["type"], e["id"])] = e
    return idx


def latlon(e):
    if "lat" in e:
        return e["lat"], e["lon"]
    c = e.get("center")
    if c:
        return c["lat"], c["lon"]
    raise ValueError(f"No coordinates for element {e.get('type')}/{e.get('id')}")


def build():
    idx = load_osm_index()
    rows = []
    for i, (etype, eid, category, indoor_outdoor, notes) in enumerate(CURATED, start=1):
        key = (etype, eid)
        if key not in idx:
            raise KeyError(f"OSM element {etype}/{eid} not found in {RAW} - re-check curation list")
        e = idx[key]
        tags = e.get("tags", {})
        name = tags.get("name:es") or tags.get("name") or "(unnamed)"
        lat, lon = latlon(e)
        rows.append({
            "asset_id": f"A{i:02d}",
            "name": name,
            "category": category,
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "indoor_outdoor": indoor_outdoor,
            "source": f"OpenStreetMap {etype}/{eid} (ODbL, fetched 2026-08-17 via Overpass API)",
            "evidence_notes": notes,
        })
    df = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False, encoding="utf-8")
    print(f"Wrote {OUT} with {len(df)} assets")
    print(df["category"].value_counts())
    print(df["indoor_outdoor"].value_counts())
    return df


if __name__ == "__main__":
    build()
