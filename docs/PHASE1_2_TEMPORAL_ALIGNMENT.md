# PHASE1_2_TEMPORAL_ALIGNMENT.md — HATI-Madrid Phase 1.2

Version 1.0 · 2026-08-17. Required temporal-honesty assessment per the Phase
1.2 task specification. The heat episode under study is **August 2023**
(`docs/PHASE1_METHOD.md` §3). Every data layer feeding the shade/exposure
proxy comparison is checked against that date below.

---

## Temporal-alignment table

| Layer | Reference date used | Access/query date | Gap to episode (Aug 2023) | Status |
|---|---|---|---:|---|
| **Meteorology** (AEMET Barajas hourly, hazard gate) | 2023-08-21 (actual episode day) | 2026-08-17 (data pulled from historical archive) | 0 years | Exact match — the archive preserves the real historical observation, not a current snapshot |
| **P0 — OSM tree points** (Phase 1 baseline, frozen) | 2026-08-17 (OSM live snapshot at original Phase 1 fetch) | 2026-08-17 | ~3 years | Mismatch, already documented in Phase 1 (`docs/PHASE1_DATA_PROVENANCE.md` §3) |
| **P1 — Madrid official tree inventory** (this phase) | See "P1 currency" below — best evidence points to ~2025-2026 | 2026-08-17 (live ArcGIS MapServer query) | ~3 years (best estimate) | Mismatch — no 2023 geospatial archive exists (see below); explicitly documented, not implied to be 2023 |
| **P2 — Copernicus HRL Tree Cover Density** (this phase) | 2018 (confirmed reference year of the only reachable, non-authenticated raster service) | 2026-08-17 (service queried live, but the raster itself is the static 2018 product) | **5 years** | Largest mismatch of any layer in this project; 2023/2021 vintages exist at Copernicus but were not reachable — see below |
| **P3 — Green-polygon coverage** (retained from Phase 1.1) | 2026-08-17 (OSM live snapshot) | 2026-08-17 | ~3 years | Same OSM-snapshot mismatch as P0, already documented |

## P1 currency: what is actually known, and what is not

The CKAN listing for the source dataset ("Arbolado en parques y zonas verdes
de Madrid (detalle)", id 300761) states **Publication Date: 2025-07-09** and
**Last Update: 2026-07-27** for the full detailed inventory. The live
ArcGIS MapServer layers queried in this phase (`MEDIO_AMBIENTE/ARBOLADO`,
sub-layers 8 and 11) are the same municipally-maintained backing data source
and were queried on 2026-08-17 — i.e. **after** that last-update date, so the
records returned reflect the current, actively-maintained state of the
inventory, not a static file frozen at publication.

Two of the sub-layer names carry internal version-looking suffixes —
"Arbolado de alineación y Zonas Verdes (**ZV21**)" and "Arbolado Parques
Históricos (**PV24**)" — which *could* plausibly denote 2021/2024 data-vintage
codes, but no per-record date field exists in the schema to confirm this
(`ESA_ESPECIE, NOMBRE_COMUN, NOMBRE_ESPECIE, ALTURA, MINTDISTRITO,
NOMBRE_DISTRITO, MINTBARRIO, NOMBRE_BARRIO, OBJECTID, SHAPE` — no date/year
attribute). **This project does not claim to know P1's exact underlying
per-record vintage.** The honest, defensible bound is: not older than
2025-07-09 (the dataset's stated publication date) as an upper bound on
staleness, and current as of 2026-08-17 as the query date. Either way, it
postdates the August 2023 episode by roughly two to three years, and this
project does **not** imply the 2023 tree canopy was identical to what this
layer shows — trees are planted, removed, and grow measurably over a 2-3 year
window, particularly in an actively-managed municipal programme.

## Why no 2023 archive exists for P1 (attempt log)

A genuinely 2023-dated resource **does exist** on datos.madrid.es
(dataset id 300264, "Arbolado en parques históricos, singulares y forestales
2023" and "Arbolado en zonas verdes, distritos y calles 2023", both CSV) and
was downloaded (`data/raw/madrid_arbolado/arbolado_parques_historicos_2023.csv`,
`arbolado_zonas_verdes_calles_2023.csv`). On inspection, both are **species ×
park/district count summaries** (e.g. "JARDINES DEL BUEN RETIRO;
Aesculus hippocastanum; 5826" — a total count of horse-chestnuts in the whole
of Retiro, not individual tree locations) — real, official, and genuinely
2023-dated, but **not geolocated per-tree records**, and therefore unusable
for the buffer-based spatial analysis this comparison requires. The task
specification's preferred "authoritative geospatial representation... such as
the published Shape resource" only exists as a current (2025/2026-labelled)
resource on datos.madrid.es; no archived Shape/geometry file for 2023 was
found. This is reported as a real, checked negative result, not an
unexamined assumption.

## Why no 2023 (or 2021) Copernicus TCD layer was used

The task's stated preference — the 2023 status layer via the current VLCC
(Vegetated Land Cover Characteristics) infrastructure — was sought at
`https://geoserver.vlcc.geoville.com/geoserver/ows` (WMS GetCapabilities):
the connection **timed out** from this project's network environment (21 s
connect timeout, `Could not connect to server`), so no 2021+ vintage could be
retrieved through that route. The official CLMS product page
(`land.copernicus.eu`) returned HTTP 401 to automated fetch. The EEA's public,
authentication-free mirror (`image.discomap.eea.europa.eu/arcgis/rest/services/
GioLandPublic/`) was checked layer-by-layer and its newest Tree Cover Density
product is **`HRL_TreeCoverDensity_2018`** — later reference years (2021,
2022-2023) are not present in that public catalogue. This is the source
actually used, at its native 10 m resolution, over the study-area bounding
box (`data/raw/copernicus_tcd/tcd_2018_study_area.tif`).

**This is the single largest, and most consequential, temporal gap in this
comparison.** Five years is enough time for meaningful canopy change in an
actively-managed urban park system (planting programmes, storm losses, tree
maturation), and this gap is materially larger than the ~2-3 year gap
affecting every other layer. It is treated as a first-class limitation in
`docs/PHASE1_2_SHADE_EVIDENCE_GATE.md`, not a footnote.

## What this means for interpreting the comparison

No proxy in this comparison is contemporaneous with the August 2023 episode
except the meteorology itself. The comparison therefore answers "do
independent, real, current-best-available vegetation/shade data sources
agree with each other and with the frozen OSM-based Phase 1 baseline" — it
does **not** answer "what was the true canopy state in August 2023." Given
that even under this generous framing (every proxy given its best current
data, none artificially aged to match 2023) the proxies still disagree
substantially (see `docs/PHASE1_2_SHADE_EVIDENCE_GATE.md`), the temporal
mismatch is very unlikely to be masking an underlying agreement — if
anything, true 2023-dated layers might show even more divergence from the
2026-dated ones due to real intervening canopy change, not less.
