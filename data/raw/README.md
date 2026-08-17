# data/raw/ — immutable source extracts

Files in this directory are unmodified (beyond adding a CSV header row) extracts from
their original sources. Do not edit in place; if a correction is needed, re-download
and add a new dated file.

## Meteorological data

- `episode_aug2023_barajas_raw.csv` — Hourly synoptic observations, Madrid/Barajas
  station (WMO 08221, ICAO LEMD, AEMET indicativo 3129), 2023-08-19 to 2023-08-25
  (heat episode window + 1-day buffer). Columns follow Meteostat's hourly parameter
  set: `date,hour_utc,temp_c,dwpt_c,rhum_pct,prcp_mm,snow_mm,wdir_deg,wspd_kmh,wpgt_kmh,pres_hpa,tsun_min,coco`.
  **`hour_utc` is UTC** (Meteostat hourly bulk data is documented as UTC throughout).
  Madrid local time in August is CEST = UTC+2.
  Source: Meteostat bulk hourly archive, `https://bulk.meteostat.net/v2/hourly/08221.csv.gz`,
  downloaded 2026-08-17. Meteostat's own station inventory confirms `hourly` coverage
  for 08221 spans 1931-01-02 to 2026-03-10, i.e. genuine long-run synoptic observations
  (not a reanalysis/model product) — verified against `stations/lite.json` metadata
  (`inventory.hourly.start = "1931-01-02"`, distinct from `inventory.model.start = "2018-01-28"`).
  Meteostat itself sources Spanish station data from NOAA's Integrated Surface Database /
  GTS SYNOP relay of AEMET observations.

- `aemet_barajas_08221_hourly_202308.csv` — Same station and columns, full month of
  August 2023, for episode-context and validation-report use (e.g. showing Aug 21 was
  not an isolated spike within the month).

- `aemet_official_pdfs/AEMET_ACM_MAD_202308_avance_climatologico.pdf` — Official AEMET
  Delegación Territorial en Madrid monthly climatological advance report, "AVANCE
  CLIMATOLÓGICO MENSUAL — AGOSTO 2023 en la COMUNIDAD DE MADRID", published 2023-09-11.
  Source: `https://repositorio.aemet.es/bitstream/20.500.11765/15165/1/ACM_MAD_202308.pdf`,
  fetched 2026-08-17. This is the primary citation for the episode designation
  ("Del día 20 al 25 de agosto hubo un episodio de calor extremo") and for the
  official Retiro station daily figures (max 40.0°C on 21 August 2023).

- `aemet_official_pdfs/AEMET_METEOALERTA_ANX1_Umbrales_y_niveles_de_aviso.pdf` —
  Official AEMET Plan Meteoalerta threshold annex (v1, 2022-05-31), giving the
  per-zone maximum-temperature warning thresholds used for the hazard gate.
  Source: `https://www.aemet.es/documentos/es/eltiempo/prediccion/avisos/plan_meteoalerta/METEOALERTA_ANX1_Umbrales_y_niveles_de_aviso.pdf`,
  fetched 2026-08-17. Madrid zone 722802 "Metropolitana y Henares" (covers the city
  of Madrid, including the study area): amarillo 36°C, naranja 39°C, rojo 42°C
  (daily maximum temperature).

## Rejected source (documented, not silently substituted)

Meteostat also serves an hourly file for station id `08222` ("Madrid", lat 40.4167,
lon -3.6833 — co-located with Retiro park, matching AEMET's Retiro station). This was
downloaded and inspected but **discarded**: the station's own Meteostat inventory
metadata shows `hourly: {start: null, end: null}` while `model: {start: "2021-01-01"}`
exactly matches the hourly file's start date — i.e. the "hourly" values served for
this id are model/reanalysis-interpolated, not raw observations, and using them would
misrepresent modelled data as observed. Retiro's genuine, officially published readings
for the episode (daily max only, not hourly) are taken instead from the AEMET PDF above.
This is why the project's sub-daily hazard signal is anchored to Barajas (regional
synoptic anchor, ~9 km NE of the study area, airport surface) rather than to Retiro
directly — see `docs/PHASE1_DATA_PROVENANCE.md` for the representativeness discussion
and its consequence for evidence-confidence grading.

## Phase 2 addition

- `phase2_met_forcing.csv` — real Ta/RH/wind/pressure (same Barajas source
  above) plus ESTIMATED clear-sky global/direct/diffuse irradiance (pvlib
  Ineichen model) for the SOLWEIG meteorological forcing. See
  `docs/PHASE2_SOLWEIG_METHOD.md` and `data/raw/pnoa_lidar/README.md` for
  the geometry inputs used alongside it.

