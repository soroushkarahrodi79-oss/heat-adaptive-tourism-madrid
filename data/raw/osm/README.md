# data/raw/osm/ — OpenStreetMap extracts (immutable)

All files fetched via the public Overpass API, `https://overpass-api.de/api/interpreter`,
on 2026-08-17, bounding box `(40.4040,-3.6960,40.4210,-3.6775)` matching
`data/processed/study_area.geojson`. Licence: ODbL (OpenStreetMap contributors) —
attribution required in any derived output.

**Note on two fetches:** these queries were originally run against a tighter box
`(40.4055,-3.6960,40.4210,-3.6790)`. That box was widened (south edge -0.0015 lat,
east edge +0.0015 lon) after `tests/test_outputs.py` caught three real, curated
pilot assets whose OSM centroids fell just outside it, and all four files below
were re-fetched against the wider box. See `docs/PHASE1_METHOD.md` §2 and
`docs/PHASE1_VALIDATION_REPORT.md` §5 for the full story — widening the box also
recovered real tree data for two gardens that the original tighter tree query had
clipped out. The `.overpassql` query files reflect the final, wider box.

| File | Query | Content | Count |
|---|---|---|---|
| `osm_pois_raw.json` | `query.overpassql` | tourism, historic, leisure=park/garden, drinking_water/fountain, rail/metro stations | 523 elements |
| `osm_trees_raw.json` | `query_trees.overpassql` | `natural=tree` point nodes | 1,353 |
| `osm_buildings_bus_raw.json` | `query_buildings_transit.overpassql` | building footprints + `highway=bus_stop` | 1,099 buildings, 95 bus stops |
| `osm_green_polygons_raw.json` | `query_green_polygons.overpassql` | full real polygon geometry (not just centroid) for the 8 pilot assets whose OSM footprint is an area (parks/gardens), fetched by explicit OSM id, unaffected by the bbox change | 8 polygons |

## Known limitation (documented, not silently ignored)

OSM tree coverage is crowdsourced and known to be spatially uneven — Retiro Park and
the Real Jardín Botánico are well-mapped (likely benefiting from a past import of
Ayuntamiento de Madrid arbolado data), but street-tree coverage along ordinary
sidewalks elsewhere in the study area may be incomplete. Tree-count-based canopy
proxies computed from this file should therefore be read as a lower bound / relative
indicator, not an absolute canopy census — this is carried into the evidence-confidence
grading in `docs/PHASE1_METHOD.md`. Building height is not available for most footprints
(OSM height/levels tags sparse in this area, consistent with `docs/DATA_SOURCE_INVENTORY.csv`),
so building-footprint proximity is used only as a coarse street-canyon/enclosure proxy,
never as a computed shadow.
