# data/raw/madrid_meteo_municipal/ — municipal hourly meteorology (immutable)

Independent **urban** hourly meteorological check for **Gate 2** of the pedestrian-heat
research extension. This is the corridor-adjacent Ta/RH record used to bound forcing
representativeness (Escuelas Aguirre) — **not** the model forcing (which is Barajas).

- Source: Ayuntamiento de Madrid open data, dataset **300352** *Datos meteorológicos.
  Datos horarios desde 2019*.
- File: `meteo_municipal_202308.csv` — August 2023 monthly hourly file.
  - URL: `https://datos.madrid.es/dataset/300352-0-meteorologicos-horarios/resource/300352-46-meteorologicos-horarios-csv/download/300352-46-meteorologicos-horarios-csv.csv`
  - Acquired 2026-09-15; SHA-256 in `acquisition_provenance.json`.
- Format: `PROVINCIA;MUNICIPIO;ESTACION;MAGNITUD;PUNTO_MUESTREO;ANO;MES;DIA;H01;V01;…;H24;V24`.
  - `ESTACION = 8` → **Escuelas Aguirre** (air-quality code 28079008, Calle de Alcalá/O'Donnell, ~0.5 km ENE of Puerta de Alcalá).
  - `MAGNITUD 83` = air temperature (°C); `MAGNITUD 86` = relative humidity (%). Escuelas Aguirre does **not** report wind or radiation.
  - `Hnn` = hourly value, local official time (CEST = UTC+2 in August); `Vnn` = validity flag (`V` = valid).
- Licence: Madrid open data (free reuse with attribution).

Verified 24 Aug 2023 (study day) target hours 14:00/17:00: all values present and
flagged `V`. See `docs/research/pedestrian-heat/gate2/GATE2_METEOROLOGY_LEDGER.csv`.
