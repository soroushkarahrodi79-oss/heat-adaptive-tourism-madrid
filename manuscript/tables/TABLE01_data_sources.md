# Table 1. Data sources and provenance

Open-data layers used in the analytical chain. Sources: `docs/DATA_SOURCE_INVENTORY.csv`,
`docs/PHASE5_0_PROXY_DEFINITION.md`, `docs/PHASE2_SOLWEIG_METHOD.md` (locked). Observed,
modelled/derived, and contextual inputs are distinguished as in Section 2.2.

| Layer | Provider | Variable(s) used | Support (spatial / temporal) | Licence | What it does **not** measure |
|---|---|---|---|---|---|
| Meteorological observations (observed) | AEMET — Madrid/Barajas station (WMO 08221, LEMD) | Air temperature, relative humidity, wind speed, pressure | Point station; hourly; 21 Aug 2023 (12:00/15:00/18:00) | Spanish open-data terms (attribution) | On-site air temperature at each asset; intra-urban variation |
| Meteorological warning thresholds (observed/official) | AEMET Meteoalerta (zone 722802) | Civil-protection max-temperature thresholds (36 / 39 / 42 °C) | Zone; static | AEMET open publications | Human thermal comfort; radiant load |
| Global horizontal irradiance (modelled/derived) | Ineichen–Perez clear-sky model | GHI forcing for the physical model | Study-area centroid; the three timestamps | Model output (open method) | Observed irradiance (Barajas has no pyranometer column) |
| Urban geometry — DEM (modelled input) | IGN/CNIG national LiDAR (PNOA) | 5 m digital elevation model | 5 m → resampled to 2.5 m grid | CC-BY 4.0 / IGN terms | Building/vegetation heights (separate layers) |
| Building & vegetation heights (modelled input) | IGN/CNIG national LiDAR (PNOA) | 2.5 m building nDSM; 2.5 m vegetation nDSM | 2.5 m; per LiDAR campaign | CC-BY 4.0 / IGN terms | Canopy season currency for every part of the domain (see Section 5.3) |
| Tourism assets (contextual) | OpenStreetMap | 27 curated assets: id, name, category, indoor/outdoor, coordinates | Vector; crowdsourced snapshot (retrieved 2026) | ODbL | A representative sample of Madrid tourism sites (purposive pilot) |
| Tree points (contextual) | OpenStreetMap `natural=tree` | Tree-presence count within asset extent | Vector points (n = 1,353 in area) | ODbL | Canopy cover, shadow geometry, or sun position |
| Park/garden polygons (contextual) | OpenStreetMap | Real footprints for area-type assets | Vector polygons | ODbL | Interior microclimate heterogeneity |
| Opening hours (contextual) | OpenStreetMap tags (11/27) + documented institutional schedules (16/27) | Open/closed at each timestamp | Per asset; documented 2026, applied to 2023 (see Section 5.5) | ODbL / cited institutional sources | Verified same-day schedule for 21 Aug 2023 |

*Abbreviations:* AEMET, Spanish State Meteorological Agency; DEM, digital elevation model;
nDSM, normalized digital surface model; GHI, global horizontal irradiance; ODbL, Open
Database Licence. Land-surface temperature (LST) and satellite thermal imagery were **not**
used anywhere in this study.
