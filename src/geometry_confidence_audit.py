"""
Phase 2.1 Audit 2: vegetation-geometry confidence audit.

Compares the Phase 2 LiDAR-derived CDSM (PNOA-LiDAR 1a cobertura, ~2008-2015
- see docs/PHASE2_INPUT_FEASIBILITY.md) against THREE independent, newer
sources already acquired in this project (Phase 1.2), for a targeted set of
8 decision-relevant outdoor assets. This is a CONFIDENCE AUDIT, not a
reconstruction - no attempt is made to infer exact 2023 canopy height, and
the Phase 2 baseline geometry is not modified.

Independent newer evidence (all real, all already acquired, none re-fetched
here):
  - Madrid official tree inventory (Phase 1.2 P1): live ArcGIS service,
    current as of 2026-08-17 - real per-tree point locations.
  - Green-polygon coverage (Phase 1.2 P3): OSM real park/garden polygons,
    2026-08-17 snapshot.
  - Copernicus HRL Tree Cover Density (Phase 1.2 P2): 2018 vintage - itself
    older than the 2023 episode, but NEWER than the LiDAR's 2008-2015
    vintage, so it serves as a useful intermediate cross-check.
"""
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterstats import zonal_stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phase2_prereg import PRIMARY_BUFFER_M

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
INTERIM = ROOT / "data" / "interim"
RAW = ROOT / "data" / "raw"
WGS84 = "EPSG:4326"
UTM30N = "EPSG:25830"

# Selected per the task's priority criteria: park/garden + strong vegetation-
# Tmrt sensitivity (A20,A21,A23,A24,A25,A27, all park_garden morphology) +
# 2 additional Phase 1.2 proxy-sensitive, non-park assets for contrast
# (A17 street_corridor, A19 attraction_exterior).
SELECTED_ASSETS = ["A20", "A21", "A23", "A24", "A25", "A27", "A17", "A19"]


def load_assets():
    df = pd.read_csv(PROCESSED / "pilot_assets.csv")
    df = df[df["asset_id"].isin(SELECTED_ASSETS)]
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs=WGS84)
    return gdf.to_crs(UTM30N)


def main():
    assets = load_assets()
    buffers = assets.geometry.buffer(PRIMARY_BUFFER_M)  # same 10 m, pre-registered in Phase 2

    # 1. LiDAR CDSM (Phase 2 geometry, LOCKED, not modified)
    cdsm_stats = zonal_stats(buffers, str(INTERIM / "solweig" / "cdsm_2m5.tif"), stats=["mean", "max"])

    # 2. Madrid official tree count (Phase 1.2 P1, live 2026 snapshot)
    madrid_trees = gpd.read_file(INTERIM / "madrid_arbolado_points.geojson").to_crs(UTM30N)
    madrid_pts = madrid_trees.geometry.values
    madrid_counts = [sum(1 for p in madrid_pts if buf.contains(p)) for buf in buffers]

    # 3. Green-polygon coverage % (Phase 1.2 P3, OSM 2026 snapshot)
    green_polys = gpd.read_file(INTERIM / "all_green_polygons.geojson").to_crs(UTM30N)
    green_union = green_polys.geometry.union_all()
    green_pct = [round(100 * buf.intersection(green_union).area / buf.area, 1) for buf in buffers]

    # 4. Copernicus TCD 2018 (Phase 1.2 P2 - intermediate vintage cross-check)
    tcd_stats = zonal_stats(buffers.to_crs(WGS84) if buffers.crs != WGS84 else buffers,
                             str(RAW / "copernicus_tcd" / "tcd_2018_study_area.tif"), stats=["mean"])

    rows = []
    for i, (_, a) in enumerate(assets.iterrows()):
        cdsm_mean = round(float(cdsm_stats[i]["mean"]), 2)
        cdsm_max = round(float(cdsm_stats[i]["max"]), 1)
        madrid_n = madrid_counts[i]
        green_p = green_pct[i]
        tcd_p = round(float(tcd_stats[i]["mean"]), 1)

        # Confidence classification: does independent newer evidence agree
        # the site is real, meaningfully vegetated, matching what the LiDAR
        # CDSM shows? Simple, documented, non-arbitrary rule (not tuned
        # after seeing results): LiDAR "sees vegetation" if cdsm_mean > 1 m
        # (a real canopy signal, not noise); newer evidence "confirms
        # vegetation" if AT LEAST TWO of the three independent newer sources
        # each independently indicate real vegetation presence (Madrid
        # trees > 5 within 10 m; green coverage > 30%; TCD > 20%).
        lidar_sees_veg = cdsm_mean > 1.0
        newer_signals = [madrid_n > 5, green_p > 30, tcd_p > 20]
        n_confirm = sum(newer_signals)

        if lidar_sees_veg and n_confirm >= 2:
            confidence = "REPRESENTATIVE"
            reason = (f"LiDAR CDSM shows real canopy (mean {cdsm_mean} m) and {n_confirm}/3 independent "
                      f"newer sources confirm meaningful vegetation nearby")
        elif not lidar_sees_veg and n_confirm >= 2:
            confidence = "POSSIBLY STALE"
            reason = (f"LiDAR CDSM shows little/no canopy (mean {cdsm_mean} m) but {n_confirm}/3 independent "
                      f"newer sources indicate real vegetation nearby - canopy may have grown in since the "
                      f"~2008-2015 LiDAR campaign, or LiDAR undercounted this specific area")
        elif lidar_sees_veg and n_confirm < 2:
            confidence = "PARTIALLY REPRESENTATIVE"
            reason = (f"LiDAR CDSM shows canopy (mean {cdsm_mean} m) but newer sources are more equivocal "
                      f"({n_confirm}/3 confirm) - possible canopy loss/thinning since LiDAR capture, or a "
                      f"real gap in one of the newer crowdsourced/administrative layers (see Phase 1.2 findings)")
        else:
            confidence = "PARTIALLY REPRESENTATIVE"
            reason = (f"LiDAR CDSM shows little canopy (mean {cdsm_mean} m) and newer sources are also "
                      f"equivocal ({n_confirm}/3 confirm) - consistent low-vegetation site, moderate confidence")

        rows.append({
            "asset_id": a["asset_id"], "name": a["name"],
            "lidar_cdsm_mean_m": cdsm_mean, "lidar_cdsm_max_m": cdsm_max,
            "madrid_tree_count_10m": madrid_n, "green_coverage_pct_10m": green_p,
            "copernicus_tcd_pct_10m": tcd_p,
            "n_newer_sources_confirming": n_confirm,
            "geometry_confidence": confidence, "reason": reason,
        })

    out = pd.DataFrame(rows)
    out_path = PROCESSED / "phase2_1_geometry_confidence.csv"
    out.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Wrote {out_path}")
    print(out[["asset_id", "name", "lidar_cdsm_mean_m", "madrid_tree_count_10m",
               "green_coverage_pct_10m", "copernicus_tcd_pct_10m", "geometry_confidence"]].to_string(index=False))
    print("\nConfidence distribution:")
    print(out["geometry_confidence"].value_counts())

    return out


if __name__ == "__main__":
    main()
