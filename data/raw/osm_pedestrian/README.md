# data/raw/osm_pedestrian/ — OD1 pedestrian-network extract (immutable)

Bounded Overpass acquisition for **Gate 2** of the pedestrian-heat research extension
(`docs/research/pedestrian-heat/gate2/`). **Not** a city-wide network.

- Endpoint: `https://overpass-api.de/api/interpreter`
- Corridor bbox (S,W,N,E): `40.4035,-3.6950,40.4210,-3.6820` (OD1: Atocha → Puerta de Alcalá).
- Acquired: 2026-09-14T19:46:20Z; OSM base: 2026-09-14T19:45:03Z.
- Licence: **ODbL** — © OpenStreetMap contributors; attribution + share-alike on derived network products.

| File | Content |
|---|---|
| `query_od1_pedestrian.overpassql` | The exact query (walkable ways + crossings + barriers + access). |
| `osm_od1_pedestrian_raw.json` | Raw Overpass response (2979 elements: 2262 ways, 717 nodes). SHA-256 in `acquisition_provenance.json`. |
| `acquisition_provenance.json` | Timestamp, endpoint, hash, element counts, attribution. |

Derived frozen routes (EPSG:25830, hashed) live in
`data/processed/pedestrian-heat/OD1_Route_{A,B}_epsg25830.geojson`. No thermal
information was used in route construction.
