# PHASE1_DATA_PROVENANCE.md — HATI-Madrid Phase 1

Version 1.0 · 2026-08-17. Full provenance for every data source actually used in
the Phase 1 spike. Raw data is kept immutable in `data/raw/` (see the README.md
file in that directory and in `data/raw/osm/`); this document is the narrative
companion.

> **Phase 2 note:** provenance for the real PNOA-LiDAR/IGN geometry inputs and
> the SOLWEIG meteorological forcing acquired for the physical-model spike is
> in `docs/PHASE2_INPUT_FEASIBILITY.md` and `docs/PHASE2_SOLWEIG_METHOD.md`
> (kept separate rather than merged here, since Phase 2's inputs are a
> distinct acquisition with their own Step-0 feasibility audit).

---

## 1. Meteorological data

| Field | Value |
|---|---|
| Source | Meteostat bulk hourly archive, `https://bulk.meteostat.net/v2/hourly/08221.csv.gz` |
| Underlying data owner | AEMET (Agencia Estatal de Meteorología), relayed via NOAA's Integrated Surface Database / GTS SYNOP feed, aggregated by Meteostat |
| Station | Madrid/Barajas, WMO 08221, ICAO LEMD, lat 40.45, lon -3.55, elev 609 m |
| Access date | 2026-08-17 |
| Licence | Meteostat bulk data: free for non-commercial and attributed use; underlying AEMET data: Spanish open-data terms |
| Spatial resolution | Point station, ~9 km NE of the study area centroid |
| Temporal resolution | Hourly (UTC) |
| File used | `data/raw/episode_aug2023_barajas_raw.csv` (2023-08-19 to 2023-08-25 extract), `data/raw/aemet_barajas_08221_hourly_202308.csv` (full August 2023, for context) |
| Preprocessing | Filtered to episode window; UTC→Europe/Madrid (CEST, UTC+2) conversion applied only at the point of use in `src/build_classifications.py`, never applied in place to the raw file |
| Limitations | Station is ~9 km from the study area and sits on an airport apron (extensive paved/tarmac surface), so absolute values likely run warmer than a shaded urban park like Retiro on the same afternoon — evidenced by Barajas's hourly max that day (40.5 °C) slightly exceeding Retiro's officially reported daily max (40.0 °C). Used here as the best available REAL, DIRECT, sub-daily anchor for the regional hazard signal, not as a claim about exact on-site air temperature at each of the 27 pilot assets — see the exposure/hazard separation in `docs/PHASE1_METHOD.md` §5. |
| Cross-validation | Retiro station's officially published daily maximum (40.0 °C, 21 Aug 2023) corroborates the episode's severity independently of the Barajas series. |

**Rejected alternative (documented, not silently substituted):** Meteostat also
serves an "hourly" file for station id `08222` ("Madrid" — co-located with Retiro
park). This was downloaded and inspected, then discarded: the station's own
Meteostat inventory metadata shows `hourly: {start: null, end: null}` while
`model: {start: "2021-01-01"}` exactly matches the served file's start date,
indicating the values are model/reanalysis-interpolated rather than raw
observations. Using them would have misrepresented modelled data as observed, so
they were not used anywhere in this project. Full detail in `data/raw/README.md`.

## 2. Official AEMET threshold and episode-designation documents

| Document | Use in this project |
|---|---|
| `data/raw/aemet_official_pdfs/AEMET_ACM_MAD_202308_avance_climatologico.pdf` — AEMET Delegación Territorial en Madrid, "Avance climatológico mensual, agosto 2023 en la Comunidad de Madrid", published 2023-09-11 | Source of the episode designation (20–25 Aug 2023 "episodio de calor extremo") and Retiro's official daily-max figure (40.0 °C, 21 Aug) |
| `data/raw/aemet_official_pdfs/AEMET_METEOALERTA_ANX1_Umbrales_y_niveles_de_aviso.pdf` — AEMET Plan Meteoalerta threshold annex, v1, 2022-05-31 | Source of the hazard-gate thresholds (36/39/42 °C for Madrid zone 722802) |

Both are official Spanish government (AEMET) publications, fetched 2026-08-17, and
retained in full in `data/raw/aemet_official_pdfs/` for audit.

## 3. Tourism assets, trees, buildings, water, transit

| Field | Value |
|---|---|
| Source | OpenStreetMap, via the public Overpass API (`https://overpass-api.de/api/interpreter`) |
| Owner | OpenStreetMap contributors |
| Access date | 2026-08-17 |
| Licence | Open Database Licence (ODbL) — attribution required on any derived output |
| Spatial resolution | Point/way/relation, native OSM precision (sub-metre digitisation, though positional accuracy varies by contributor) |
| Temporal resolution | Current snapshot as of the query date (2026-08-17), applied retrospectively to a 2023-08-21 episode — see limitation below |
| Files used | `data/raw/osm/osm_pois_raw.json` (POIs, 523 elements), `osm_trees_raw.json` (1,353 tree points), `osm_buildings_bus_raw.json` (1,099 building centroids, 95 bus stops), `osm_green_polygons_raw.json` (8 full park/garden polygons for the pilot assets that are areas, not points) |
| Preprocessing | Parsed into clean point/polygon GeoJSON layers by `src/build_supporting_layers.py` and `src/build_green_polygons.py`; the 27-asset pilot list hand-curated from the POI extract by `src/build_pilot_assets.py`, which resolves each curated asset by its exact OSM type/id and fails if not found (no silent drift possible) |
| Licence compliance | Every output CSV/map that uses this data credits "OpenStreetMap contributors (ODbL)" |

**Limitations, stated explicitly (not hidden):**

1. **Temporal mismatch.** The OSM snapshot is from 2026, applied to a 2023 heat
   episode. This assumes the pilot area's urban form (trees, buildings, transit
   stops, museum locations) did not change materially between August 2023 and
   the query date — reasonable for a stable, protected, monumental city core over
   a ~3-year window, but not verified. A tree removed or planted in that window,
   a temporarily-closed metro entrance, or a relocated fountain would not be
   reflected correctly.
2. **Crowdsourced completeness is uneven.** The `natural=tree` layer is well
   populated inside Retiro Park and the Real Jardín Botánico (likely benefiting
   from a past bulk import of Ayuntamiento de Madrid arbolado data) but has a
   confirmed gap for at least two real, named, densely-planted gardens within
   Retiro (Jardines de Cecilio Rodríguez, Jardines del Arquitecto Herrero
   Palacios — both returned zero mapped trees despite being well-documented
   shaded gardens). This was caught and corrected with a documented override
   rule rather than left to silently misclassify those sites — see
   `docs/PHASE1_METHOD.md` §5.2 and `docs/PHASE1_VALIDATION_REPORT.md`.
3. **Building height is not used.** Consistent with `docs/DATA_SOURCE_INVENTORY.csv`'s
   note that OSM building-height tags are sparse in this area, no shadow or
   street-canyon model was attempted; building centroids were downloaded but are
   not used in the final feasibility computation in this baseline (kept in
   `data/interim/buildings_centroids.geojson` for potential Phase 2 use).
4. **Water-point and transit-point "availability" is structural, not operational.**
   A drinking-water point being mapped in OSM does not confirm it was flowing on
   21 August 2023; this mirrors the exact caveat already flagged in
   `docs/DATA_SOURCE_INVENTORY.csv` for the Madrid Open Data fountains layer.
5. **Polygon vs. centroid geometry.** The Overpass POI query used `out center`,
   returning a single centroid for way/relation features rather than full
   geometry. This is adequate for the distance- and count-based proxies actually
   used (see `docs/PHASE1_METHOD.md` §5) but would NOT be adequate for an
   area-coverage-fraction analysis (e.g. "% of a buffer covered by park
   polygon") — that analysis was not attempted for this reason. Full polygon
   geometry was fetched separately, and only, for the 8 pilot assets whose OSM
   footprint is itself a park/garden area (see `src/build_green_polygons.py`).

## 4. Sources evaluated in Phase 0 but NOT used in Phase 1

Per `docs/DATA_SOURCE_INVENTORY.csv`, several sources rated "USE" for the eventual
full HATI system were not pulled for this bounded Phase 1 baseline, because the
baseline's simpler proxy variables did not require them: PNOA LiDAR (building/tree
heights, needed for SOLWEIG/Tmrt, explicitly deferred — see
`docs/PHASE1_GATE.md`), Spanish Cadastre building geometry, Copernicus Urban Atlas
Street Tree Layer / HRL Tree Cover Density, Sentinel-2, and Landsat LST. This is a
deliberate scope decision, not a failed acquisition — each remains available and
rated "USE" for a future SOLWEIG-based phase, should `docs/PHASE1_GATE.md` justify
it.

## 4a. Phase 1.1 additional sources (2026-08-17)

Added during the baseline-hardening pass documented in
`docs/PHASE1_1_BASELINE_HARDENING.md`; the Phase 1 sources above are unchanged.

| Source | Use | File(s) |
|---|---|---|
| Meteostat bulk hourly archive, station 08221, 2021-08-11 to 2021-08-16 | Audit 2: real EXTREME-hazard stress test | `data/raw/extreme_aug2021_barajas_raw.csv` |
| AEMET Delegación Territorial en Madrid, "Avance climatológico mensual, agosto 2021 en Madrid" (official PDF) | Audit 2: confirms 2021-08-14 as part of an official "intensa ola de calor" (11–15 Aug 2021), Barajas daily max 42.7°C | `data/raw/aemet_official_pdfs/AEMET_avance_climat_MAD_202108.pdf` |
| AEMET OpenData API (anonymous request, no key) | Audit 1: documents the exact failure mode (HTTP 401, JWT required) supporting the Retiro-hourly-unobtainable determination | not a data file - see `docs/PHASE1_1_BASELINE_HARDENING.md` Audit 1 for the request and response |
| OpenStreetMap, Overpass API, widened ring bbox (40.4000,-3.7000,40.4250,-3.6700) | Audit 3: 6 real ring-extension assets + widened water/transit point set | `data/raw/osm/osm_ring_raw.json`, `osm_ring_water_raw.json`, `osm_ring_transit_raw.json` |
| OpenStreetMap, Overpass API, full geometry for all `leisure=park/garden` + `natural=wood` + `landuse=forest` in the study area | Audit 4: green-polygon coverage shade proxy (Proxy 2) | `data/raw/osm/osm_all_green_polygons_raw.json` → `data/interim/all_green_polygons.geojson` |

Licence for all OSM sources: ODbL, as in the Phase 1 sources above. Licence for
AEMET sources: Spanish open-data terms, attribution required, as in Phase 1.

## 4b. Phase 1.2 additional sources (2026-08-17)

Added for the shade/exposure-proxy robustness comparison
(`docs/PHASE1_2_SHADE_EVIDENCE_GATE.md`,
`docs/PHASE1_2_TEMPORAL_ALIGNMENT.md`). Full field-by-field provenance
(dataset date, licence, geometry, attributes, limitations) is in
`docs/PHASE1_2_SHADE_EVIDENCE_GATE.md` §1; summarised here for the
provenance index.

| Source | Owner | Access date | Licence | Use | File(s) |
|---|---|---|---|---|---|
| ARBOLADO ArcGIS MapServer (live), layers 8 + 11 | Ayuntamiento de Madrid | 2026-08-17 | CC BY 4.0 | P1: official per-tree inventory, 40,840 real records in study area | `data/raw/madrid_arbolado/arbolado_*_full.geojson` → `data/interim/madrid_arbolado_points.geojson` |
| "Arbolado en parques históricos..." 2023 + "Arbolado en zonas verdes, distritos y calles" 2023 (CSV) | Ayuntamiento de Madrid | 2026-08-17 | CC BY 4.0 | **Checked, not used**: genuinely 2023-dated but a species-count summary, not geolocated per-tree data — see temporal-alignment doc for the full reasoning | `data/raw/madrid_arbolado/arbolado_parques_historicos_2023.csv`, `arbolado_zonas_verdes_calles_2023.csv` |
| HRL Tree Cover Density 2018, EEA public ImageServer | Copernicus Land Monitoring Service / EEA | 2026-08-17 | Copernicus/EEA open licence (attribution required) | P2: canopy-density raster, 10 m, exported clip of the study area | `data/raw/copernicus_tcd/tcd_2018_study_area.tif` |
| OSM leisure=park/garden/wood/forest polygons (161, full geometry) | OpenStreetMap contributors | 2026-08-17 (reused from Phase 1.1) | ODbL | P3: green-polygon coverage, retained from Phase 1.1 unchanged | `data/interim/all_green_polygons.geojson` |

**Attempted but not used (documented negative results, not silent
substitutions):** AEMET OpenData API for Retiro (Phase 1.1, still applicable);
`geoserver.vlcc.geoville.com` WMS for Copernicus TCD 2021+ (connection
timeout); `land.copernicus.eu` CLMS portal direct download (HTTP 401 to
automated access); Madrid's 660 MB current Shape/CSV full-city detail file
(not needed — the live queryable ArcGIS layer returned the same underlying
records for the study-area bbox only, at far lower transfer cost).

## 5. Full reproducibility chain

```
data/raw/episode_aug2023_barajas_raw.csv          (Meteostat, real hourly obs)
data/raw/aemet_official_pdfs/*.pdf                (AEMET, official)
data/raw/osm/osm_pois_raw.json                    (OSM Overpass)
data/raw/osm/osm_trees_raw.json                   (OSM Overpass)
data/raw/osm/osm_buildings_bus_raw.json           (OSM Overpass)
data/raw/osm/osm_green_polygons_raw.json          (OSM Overpass)
        |
        v  src/define_study_area.py
data/processed/study_area.geojson
        |
        v  src/build_pilot_assets.py
data/processed/pilot_assets.csv
        |
        v  src/build_supporting_layers.py, src/build_green_polygons.py
data/interim/{trees,green_spaces,water_points,transit_points,
              buildings_centroids,green_polygons}.geojson
        |
        v  src/build_classifications.py  (uses src/thresholds.py)
data/processed/pilot_classifications.csv
        |
        v  src/make_maps.py
outputs/maps/01-04*.png

Phase 1.1 (each independent of the others, all depend on the Phase 1 chain above):
data/raw/extreme_aug2021_barajas_raw.csv  --> src/audit2_extreme_stress_test.py
                                           --> data/processed/extreme_branch_stress_test_2021-08-14.csv
data/raw/osm/osm_ring_*.json              --> src/audit3_adaptation_gate_test.py
                                           --> data/processed/audit3_ring_extension.csv
data/raw/osm/osm_all_green_polygons_raw.json --> src/build_all_green_polygons.py
                                           --> data/interim/all_green_polygons.geojson
                                           --> src/audit4_shade_proxy_test.py
                                           --> data/processed/audit4_proxy_comparison.csv,
                                               data/processed/audit4_unstable_assets.csv
                                           --> src/make_maps.py --> outputs/maps/05*.png

Phase 1.2 (depends on the Phase 1 chain for pilot_assets.csv/pilot_classifications.csv):
data/raw/madrid_arbolado/arbolado_*_full.geojson --> src/build_madrid_arbolado_points.py
                                           --> data/interim/madrid_arbolado_points.geojson
data/raw/copernicus_tcd/tcd_2018_study_area.tif  (used directly, no build step)
src/shade_proxy_prereg.py (buffer/method decisions, committed before any run)
        |
        v  src/shade_proxy_comparison.py
data/processed/shade_proxy_comparison.csv
        |
        v  src/shade_proxy_agreement.py
outputs/tables/shade_proxy_agreement.csv
        |
        v  src/make_maps.py (map_shade_proxy_instability)
outputs/maps/shade_proxy_instability.png
src/shade_proxy_buffer_sensitivity.py  (25m/100m sensitivity check, independent script)
```

No step requires network access to reproduce from `data/raw/` onward; network
access is required only to re-fetch `data/raw/` itself from the original sources
listed above, should a user want to refresh rather than reuse the archived extract.
