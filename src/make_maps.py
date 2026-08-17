"""
Static scientific maps for the Phase 1 spike. No dashboard, no web basemap
dependency (offline-reproducible): context is provided by the real OSM layers
already extracted (green polygons, trees, study-area box) rather than tiles.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
INTERIM = ROOT / "data" / "interim"
OUT = ROOT / "outputs" / "maps"
OUT.mkdir(parents=True, exist_ok=True)

WGS84 = "EPSG:4326"


def load_common():
    study_area = gpd.read_file(PROCESSED / "study_area.geojson")
    assets = pd.read_csv(PROCESSED / "pilot_assets.csv")
    assets_gdf = gpd.GeoDataFrame(
        assets, geometry=gpd.points_from_xy(assets.longitude, assets.latitude), crs=WGS84
    )
    trees = gpd.read_file(INTERIM / "trees.geojson")
    green_poly = gpd.read_file(INTERIM / "green_polygons.geojson")
    return study_area, assets_gdf, trees, green_poly


def _basemap(ax, study_area, trees, green_poly, title):
    green_poly.plot(ax=ax, color="#c8e6c9", edgecolor="#66bb6a", linewidth=0.6, zorder=1, alpha=0.8)
    trees.plot(ax=ax, color="#2e7d32", markersize=2, alpha=0.35, zorder=2)
    study_area.boundary.plot(ax=ax, color="black", linewidth=1.2, linestyle="--", zorder=5)
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_aspect(1 / 0.7615)  # approx correction for latitude ~40.41N (cos(40.41deg))


def map_study_area():
    study_area, assets_gdf, trees, green_poly = load_common()
    fig, ax = plt.subplots(figsize=(8, 9))
    _basemap(ax, study_area, trees, green_poly,
             "HATI-Madrid Phase 1 pilot study area\nPrado - Retiro - Atocha (bounded box, ~3.5 km2)")

    props = study_area.iloc[0]["properties"] if "properties" in study_area.columns else None
    landmarks = {
        "Puerta de Alcalá": (40.4201, -3.6883),
        "Est. Puerta de Atocha (bldg centroid)": (40.40456, -3.68868),
        "CaixaForum (W ref.)": (40.4113, -3.6936),
        "Jard. Cecilio Rodríguez (E ref.)": (40.41335, -3.67797),
    }
    for name, (lat, lon) in landmarks.items():
        ax.plot(lon, lat, marker="*", color="#d84315", markersize=14, zorder=6)
        ax.annotate(name, (lon, lat), textcoords="offset points", xytext=(6, 4), fontsize=8)

    legend_handles = [
        mpatches.Patch(color="#c8e6c9", label="OSM leisure=park/garden polygon"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#2e7d32", markersize=5, label=f"OSM natural=tree (n={len(trees)})"),
        plt.Line2D([0], [0], color="black", linestyle="--", label="Study-area boundary"),
        plt.Line2D([0], [0], marker="*", color="w", markerfacecolor="#d84315", markersize=12, label="Boundary reference landmark"),
    ]
    ax.legend(handles=legend_handles, loc="lower left", fontsize=7, framealpha=0.9)
    fig.text(0.5, 0.01, "Data: OpenStreetMap contributors (ODbL), fetched 2026-08-17. CRS: WGS84.",
              ha="center", fontsize=7, color="gray")
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(OUT / "01_study_area.png", dpi=200)
    plt.close(fig)
    print("Wrote 01_study_area.png")


CATEGORY_COLORS = {
    "museum_indoor": "#1565c0",
    "transit_hub": "#6a1b9a",
    "transit_hub_green": "#00897b",
    "monument_outdoor": "#e65100",
    "park_general": "#2e7d32",
    "garden_outdoor": "#43a047",
    "outdoor_pavilion_shaded": "#00695c",
    "outdoor_attraction_mixed_shade": "#f9a825",
}
CATEGORY_LABELS = {
    "museum_indoor": "Museum / indoor attraction",
    "transit_hub": "Transport-accessible alternative",
    "transit_hub_green": "Transit-adjacent indoor green refuge",
    "monument_outdoor": "Outdoor monument (open plaza)",
    "park_general": "Green area (park)",
    "garden_outdoor": "Shaded/vegetated garden",
    "outdoor_pavilion_shaded": "Outdoor pavilion, tree-shaded",
    "outdoor_attraction_mixed_shade": "Outdoor attraction, mixed shade",
}


def map_assets():
    study_area, assets_gdf, trees, green_poly = load_common()
    fig, ax = plt.subplots(figsize=(8, 9))
    _basemap(ax, study_area, trees, green_poly,
             "Pilot tourism assets (n=27)\nreal, named, sourced from OpenStreetMap")

    for cat, sub in assets_gdf.groupby("category"):
        color = CATEGORY_COLORS.get(cat, "#999999")
        ax.scatter(sub.geometry.x, sub.geometry.y, color=color, s=55, edgecolor="white",
                   linewidth=0.6, zorder=7, label=CATEGORY_LABELS.get(cat, cat))
    for _, r in assets_gdf.iterrows():
        ax.annotate(r["asset_id"], (r.geometry.x, r.geometry.y), fontsize=6,
                    textcoords="offset points", xytext=(4, 3), zorder=8)

    ax.legend(loc="lower left", fontsize=6.5, framealpha=0.9, title="Asset category", title_fontsize=7)
    fig.text(0.5, 0.01, "Data: OpenStreetMap contributors (ODbL). See data/processed/pilot_assets.csv for full attribution.",
              ha="center", fontsize=7, color="gray")
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(OUT / "02_pilot_assets.png", dpi=200)
    plt.close(fig)
    print("Wrote 02_pilot_assets.png")


def map_exposure():
    study_area, assets_gdf, trees, green_poly = load_common()
    cls = pd.read_csv(PROCESSED / "pilot_classifications.csv")
    exp = cls[["asset_id", "exposure_state", "tree_count_50m"]].drop_duplicates("asset_id")
    gdf = assets_gdf.merge(exp, on="asset_id", how="left")

    fig, ax = plt.subplots(figsize=(8, 9))
    _basemap(ax, study_area, trees, green_poly,
             "On-site exposure differentiation (shade/vegetation proxy)\ntree_count within real site extent, tercile-classified")

    colors = {"LOW": "#1b5e20", "MODERATE": "#fdd835", "HIGH": "#c62828"}
    labels = {"LOW": "LOW exposure (well shaded, top tercile)",
              "MODERATE": "MODERATE exposure (mid tercile)",
              "HIGH": "HIGH exposure (poor shade, bottom tercile)"}
    outdoor = gdf[gdf["indoor_outdoor"] == "outdoor"]
    indoor = gdf[gdf["indoor_outdoor"] == "indoor"]
    for state, sub in outdoor.groupby("exposure_state"):
        ax.scatter(sub.geometry.x, sub.geometry.y, color=colors.get(state, "gray"), s=70,
                   edgecolor="black", linewidth=0.5, zorder=7, label=labels.get(state, state))
    ax.scatter(indoor.geometry.x, indoor.geometry.y, color="#90a4ae", marker="s", s=45,
               edgecolor="black", linewidth=0.4, zorder=7, label="Indoor (exposure gate bypassed)")
    for _, r in gdf.iterrows():
        ax.annotate(r["asset_id"], (r.geometry.x, r.geometry.y), fontsize=6,
                    textcoords="offset points", xytext=(4, 3), zorder=8)

    ax.legend(loc="lower left", fontsize=6.5, framealpha=0.9)
    fig.text(0.5, 0.01,
              "Proxy = real tree count within site extent (50m buffer, or actual polygon+15m for parks/gardens). "
              "NOT a measured canopy/shadow model.", ha="center", fontsize=7, color="gray")
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(OUT / "03_exposure_differentiation.png", dpi=200)
    plt.close(fig)
    print("Wrote 03_exposure_differentiation.png")


def map_feasibility():
    study_area, assets_gdf, trees, green_poly = load_common()
    cls = pd.read_csv(PROCESSED / "pilot_classifications.csv")
    timestamps = sorted(cls["timestamp"].unique())

    fig, axes = plt.subplots(1, 3, figsize=(20, 8))
    colors = {
        "FEASIBLE": "#2e7d32",
        "FEASIBLE WITH CONDITIONS": "#f9a825",
        "NOT RECOMMENDED": "#c62828",
        "INSUFFICIENT EVIDENCE": "#616161",
    }
    for ax, ts in zip(axes, timestamps):
        sub = cls[cls["timestamp"] == ts]
        gdf = assets_gdf.merge(sub, on="asset_id", how="left")
        _basemap(ax, study_area, trees, green_poly, "")
        local_time = ts.split("T")[1][:5]
        temp = sub["temp_c_barajas"].iloc[0]
        hz = sub["meteorological_hazard_state"].iloc[0]
        ax.set_title(f"{local_time} local (CEST)\nBarajas {temp} C - met. hazard: {hz}", fontsize=11, fontweight="bold")
        for state, s in gdf.groupby("feasibility_state"):
            ax.scatter(s.geometry.x, s.geometry.y, color=colors.get(state, "gray"), s=65,
                       edgecolor="black", linewidth=0.5, zorder=7, label=state)
        ax.legend(loc="lower left", fontsize=6, framealpha=0.9)

    fig.suptitle("Tourism feasibility classification across the 2023-08-21 heat episode\n"
                 "(constraint-first baseline, real AEMET Barajas hourly hazard + real on-site exposure/adaptation proxies)",
                 fontsize=13, fontweight="bold")
    fig.text(0.5, 0.01, "Source: data/processed/pilot_classifications.csv (method_version=phase1-baseline-v1.0)",
              ha="center", fontsize=8, color="gray")
    fig.tight_layout(rect=[0, 0.03, 1, 0.93])
    fig.savefig(OUT / "04_feasibility_by_timestamp.png", dpi=180)
    plt.close(fig)
    print("Wrote 04_feasibility_by_timestamp.png")


def map_unstable_assets():
    """Phase 1.1 Audit 4: map assets whose feasibility_state is sensitive to
    the choice of shade proxy (tree count vs. green coverage vs. building
    density) - see src/audit4_shade_proxy_test.py and
    data/processed/audit4_unstable_assets.csv."""
    study_area, assets_gdf, trees, green_poly = load_common()
    unstable_path = PROCESSED / "audit4_unstable_assets.csv"
    if not unstable_path.exists():
        print("Skipping unstable-assets map: run src/audit4_shade_proxy_test.py first")
        return
    unstable = pd.read_csv(unstable_path)
    unstable_ids = set(unstable["asset_id"].unique())

    fig, ax = plt.subplots(figsize=(8, 9))
    _basemap(ax, study_area, trees, green_poly,
             "Phase 1.1 Audit 4: shade-proxy-sensitive assets\n"
             "(tree count vs. green coverage vs. building density)")

    outdoor = assets_gdf[assets_gdf["indoor_outdoor"] == "outdoor"]
    stable = outdoor[~outdoor["asset_id"].isin(unstable_ids)]
    unstable_pts = outdoor[outdoor["asset_id"].isin(unstable_ids)]
    indoor = assets_gdf[assets_gdf["indoor_outdoor"] == "indoor"]

    ax.scatter(indoor.geometry.x, indoor.geometry.y, color="#90a4ae", marker="s", s=45,
               edgecolor="black", linewidth=0.4, zorder=7, label="Indoor (proxy-invariant by design)")
    ax.scatter(stable.geometry.x, stable.geometry.y, color="#2e7d32", s=70,
               edgecolor="black", linewidth=0.5, zorder=7, label="Outdoor, stable across all 3 proxies")
    ax.scatter(unstable_pts.geometry.x, unstable_pts.geometry.y, color="#c62828", marker="X", s=110,
               edgecolor="black", linewidth=0.7, zorder=8, label="Outdoor, UNSTABLE (proxy-sensitive)")
    for _, r in assets_gdf.iterrows():
        ax.annotate(r["asset_id"], (r.geometry.x, r.geometry.y), fontsize=6,
                    textcoords="offset points", xytext=(4, 3), zorder=9)

    n_unstable = len(unstable_ids)
    n_outdoor = len(outdoor)
    ax.legend(loc="lower left", fontsize=6.5, framealpha=0.9,
              title=f"{n_unstable}/{n_outdoor} outdoor assets unstable", title_fontsize=7)
    fig.text(0.5, 0.01,
              "Unstable = feasibility_state differs between >=2 of 3 shade proxies at >=1 timestamp. "
              "See docs/PHASE1_1_SENSITIVITY_REPORT.md.", ha="center", fontsize=7, color="gray")
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(OUT / "05_audit4_unstable_assets.png", dpi=200)
    plt.close(fig)
    print("Wrote 05_audit4_unstable_assets.png")


def map_shade_proxy_instability():
    """Phase 1.2: assets whose feasibility differs across the 4 shade-proxy
    families (P0 OSM baseline, P1 Madrid official trees, P2 Copernicus TCD,
    P3 green-polygon coverage) at the pre-registered 50 m buffer - see
    src/shade_proxy_comparison.py, docs/PHASE1_2_SHADE_EVIDENCE_GATE.md."""
    study_area, assets_gdf, trees, green_poly = load_common()
    comp_path = PROCESSED / "shade_proxy_comparison.csv"
    if not comp_path.exists():
        print("Skipping shade-proxy instability map: run src/shade_proxy_comparison.py first")
        return
    comp = pd.read_csv(comp_path)
    outdoor_comp = comp[comp["indoor_outdoor"] == "outdoor"]
    unstable_ids = set(outdoor_comp.groupby("asset_id")["proxy_sensitive"].any().pipe(lambda s: s[s].index))

    fig, ax = plt.subplots(figsize=(8, 9))
    _basemap(ax, study_area, trees, green_poly,
             "Phase 1.2: feasibility instability across 4 shade-proxy families\n"
             "(OSM baseline / Madrid official trees / Copernicus TCD / green coverage, 50m buffer)")

    outdoor = assets_gdf[assets_gdf["indoor_outdoor"] == "outdoor"]
    stable = outdoor[~outdoor["asset_id"].isin(unstable_ids)]
    unstable_pts = outdoor[outdoor["asset_id"].isin(unstable_ids)]
    indoor = assets_gdf[assets_gdf["indoor_outdoor"] == "indoor"]

    ax.scatter(indoor.geometry.x, indoor.geometry.y, color="#90a4ae", marker="s", s=45,
               edgecolor="black", linewidth=0.4, zorder=7, label="Indoor (proxy-invariant by design)")
    ax.scatter(stable.geometry.x, stable.geometry.y, color="#2e7d32", s=70,
               edgecolor="black", linewidth=0.5, zorder=7, label="Outdoor, stable across all 4 proxies")
    ax.scatter(unstable_pts.geometry.x, unstable_pts.geometry.y, color="#c62828", marker="X", s=110,
               edgecolor="black", linewidth=0.7, zorder=8, label="Outdoor, UNSTABLE (proxy-sensitive)")
    for _, r in assets_gdf.iterrows():
        ax.annotate(r["asset_id"], (r.geometry.x, r.geometry.y), fontsize=6,
                    textcoords="offset points", xytext=(4, 3), zorder=9)

    n_unstable, n_outdoor = len(unstable_ids), len(outdoor)
    ax.legend(loc="lower left", fontsize=6.5, framealpha=0.9,
              title=f"{n_unstable}/{n_outdoor} outdoor assets unstable ({100*n_unstable/n_outdoor:.0f}%)",
              title_fontsize=7)
    fig.text(0.5, 0.01,
              "Unstable = feasibility_state differs between >=2 of 4 proxies at >=1 timestamp. "
              "See docs/PHASE1_2_SHADE_EVIDENCE_GATE.md.", ha="center", fontsize=7, color="gray")
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(OUT / "shade_proxy_instability.png", dpi=200)
    plt.close(fig)
    print("Wrote shade_proxy_instability.png")


def map_phase2_1_robustness():
    """Phase 2.1 Audit 3: map ROBUST/BOUNDARY/UNSTABLE classification per
    outdoor asset (worst robustness across its 3 timestamps), from
    data/processed/phase2_1_robustness.csv."""
    study_area, assets_gdf, trees, green_poly = load_common()
    robust_path = PROCESSED / "phase2_1_robustness.csv"
    if not robust_path.exists():
        print("Skipping Phase 2.1 robustness map: run src/decision_robustness.py first")
        return
    robust = pd.read_csv(robust_path)
    rank = {"ROBUST": 0, "BOUNDARY": 1, "UNSTABLE": 2}
    robust["rank"] = robust["robustness"].map(rank)
    worst = robust.loc[robust.groupby("asset_id")["rank"].idxmax()][["asset_id", "robustness"]]
    worst_map = dict(zip(worst["asset_id"], worst["robustness"]))

    fig, ax = plt.subplots(figsize=(8, 9))
    _basemap(ax, study_area, trees, green_poly,
             "Phase 2.1: decision robustness under solar + geometry uncertainty\n"
             "(worst classification across the 3 timestamps per asset)")

    outdoor = assets_gdf[assets_gdf["indoor_outdoor"] == "outdoor"].copy()
    outdoor["robustness"] = outdoor["asset_id"].map(worst_map)
    indoor = assets_gdf[assets_gdf["indoor_outdoor"] == "indoor"]

    colors = {"ROBUST": "#2e7d32", "BOUNDARY": "#f9a825", "UNSTABLE": "#c62828"}
    markers = {"ROBUST": "o", "BOUNDARY": "^", "UNSTABLE": "X"}
    ax.scatter(indoor.geometry.x, indoor.geometry.y, color="#90a4ae", marker="s", s=40,
               edgecolor="black", linewidth=0.4, zorder=7, label="Indoor (not modelled by SOLWEIG)")
    for label, sub in outdoor.groupby("robustness"):
        ax.scatter(sub.geometry.x, sub.geometry.y, color=colors[label], marker=markers[label],
                   s=100, edgecolor="black", linewidth=0.8, zorder=8, label=f"{label} (worst of 3 timestamps)")
    for _, r in assets_gdf.iterrows():
        ax.annotate(r["asset_id"], (r.geometry.x, r.geometry.y), fontsize=6,
                    textcoords="offset points", xytext=(4, 3), zorder=9)

    counts = robust["robustness"].value_counts()
    ax.legend(loc="lower left", fontsize=6.5, framealpha=0.9,
              title=f"Rows (n=42): {counts.get('ROBUST',0)} ROBUST / {counts.get('BOUNDARY',0)} BOUNDARY / "
                    f"{counts.get('UNSTABLE',0)} UNSTABLE", title_fontsize=6.5)
    fig.text(0.5, 0.01,
              "Per-asset worst-case across 12:00/15:00/18:00. See docs/PHASE2_1_ROBUSTNESS_REPORT.md.",
              ha="center", fontsize=7, color="gray")
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(OUT / "phase2_1_unstable_assets.png", dpi=200)
    plt.close(fig)
    print("Wrote phase2_1_unstable_assets.png")


if __name__ == "__main__":
    map_study_area()
    map_assets()
    map_exposure()
    map_feasibility()
    map_unstable_assets()
    map_shade_proxy_instability()
    map_phase2_1_robustness()
