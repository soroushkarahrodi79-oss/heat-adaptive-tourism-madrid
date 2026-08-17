# data/raw/pnoa_lidar/ — IGN/CNIG WCS geometry extracts (immutable)

All files fetched via public, no-login OGC WCS 2.0.1 services, clipped
directly to the study-area bounding box (EPSG:25830: 440941,4472831,
442525,4474706 — matches `data/processed/study_area.geojson`). Fetched
2026-08-17. Full provenance narrative: `docs/PHASE2_INPUT_FEASIBILITY.md`.

| File | Service | Coverage ID | Content | Native resolution |
|---|---|---|---|---|
| `dem_wcs_5m.tif` | `https://servicios.idee.es/wcs-inspire/mdt` | `Elevacion25830_5` | Bare-earth terrain (DEM), PNOA-LiDAR-derived | 5 m |
| `mds_5m.tif` | `https://wcs-mds.idee.es/mds` | `mds05` | Raw surface model (ground+buildings+vegetation), not used directly in the final geometry (superseded by the composed DSM — see `src/build_solweig_geometry.py`) | 5 m |
| `building_ndsm_025.tif` | `https://wcs-mds.idee.es/mds` | `mdsn_e025` | Normalized building height (height above ground), PNOA-LiDAR 1ª cobertura | 2.5 m |
| `veg_ndsm_025.tif` | `https://wcs-mds.idee.es/mds` | `mdsn_v025` | Normalized vegetation/canopy height (height above ground), PNOA-LiDAR 1ª cobertura | 2.5 m |

Owner: Instituto Geográfico Nacional (IGN) / Centro Nacional de Información
Geográfica (CNIG), Spain. Licence: IGN/CNIG open data (free reuse,
attribution). Both nDSM layers derive from PNOA-LiDAR's **first coverage**
(nominally 2008–2015) — the newest vintage reachable via a bbox-queryable,
no-login service; a 2015–2021 vintage exists but only via an interactive
per-tile catalogue with no coordinate API (checked, not used — see
`docs/PHASE2_INPUT_FEASIBILITY.md` for the full reasoning). This is the
single largest temporal-vintage gap in Phase 2.

## Known issue (documented, fixed, not silent)

All four GeoTIFFs are served with a malformed `LOCAL_CS["ETRS89 / UTM zone
30N"]` CRS tag rather than a proper EPSG:25830 `PROJCS` definition — the
coordinate values themselves are correct (verified: they exactly match the
requested bbox), but SOLWEIG's CRS validator rejects the tag as
"not projected." Fixed by explicit re-tagging (a metadata correction, not a
reprojection) in `src/build_solweig_geometry.py:CRS_FIX` before any further
processing. The same malformed tag reappears on SOLWEIG's own output
rasters and is fixed again at that point — see
`docs/PHASE2_SOLWEIG_METHOD.md`.
