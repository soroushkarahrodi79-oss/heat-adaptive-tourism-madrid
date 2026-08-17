"""
Phase 2: render Tmrt and UTCI GeoTIFFs (outputs/maps/{tmrt,utci}_{1200,1500,1800}.tif)
as PNG maps with the study area boundary and pilot assets overlaid, matching
the visual style of the Phase 1/1.1/1.2 maps (src/make_maps.py).
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from rasterio.plot import show

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
MAPS = ROOT / "outputs" / "maps"
UTM30N = "EPSG:25830"
WGS84 = "EPSG:4326"

# Official UTCI thermal-stress category boundaries (Broede et al. 2012) -
# see docs/PHASE2_UTCI_METHOD.md. Used only for the colour scale / reference
# lines here, not re-derived.
UTCI_BREAKS = [26, 32, 38, 46]
UTCI_LABELS = ["Moderate", "Strong", "Very strong", "Extreme"]


def load_assets_utm():
    df = pd.read_csv(PROCESSED / "pilot_assets.csv")
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs=WGS84)
    return gdf.to_crs(UTM30N)


def load_study_area_utm():
    sa = gpd.read_file(PROCESSED / "study_area.geojson")
    return sa.to_crs(UTM30N)


def render(var, label, local_time, cmap, vmin, vmax, cbar_label):
    tif_path = MAPS / f"{var}_{label}.tif"
    assets = load_assets_utm()
    study_area = load_study_area_utm()

    fig, ax = plt.subplots(figsize=(8, 9))
    with rasterio.open(tif_path) as src:
        arr = src.read(1)
        arr = np.ma.masked_invalid(arr)
        left, bottom, right, top = src.bounds
    img = ax.imshow(arr, cmap=cmap, vmin=vmin, vmax=vmax, extent=(left, right, bottom, top),
                     origin="upper", zorder=1)

    study_area.boundary.plot(ax=ax, color="black", linewidth=1.2, linestyle="--", zorder=5)
    outdoor = assets[assets["indoor_outdoor"] == "outdoor"]
    indoor = assets[assets["indoor_outdoor"] == "indoor"]
    ax.scatter(outdoor.geometry.x, outdoor.geometry.y, facecolor="none", edgecolor="black",
               s=60, linewidth=1.1, zorder=7, label="Outdoor asset")
    ax.scatter(indoor.geometry.x, indoor.geometry.y, facecolor="white", edgecolor="black",
               marker="s", s=35, linewidth=0.8, zorder=7, label="Indoor asset")
    for _, r in assets.iterrows():
        ax.annotate(r["asset_id"], (r.geometry.x, r.geometry.y), fontsize=6,
                    textcoords="offset points", xytext=(4, 3), zorder=8, color="black")

    var_title = "Mean Radiant Temperature (Tmrt)" if var == "tmrt" else "UTCI"
    ax.set_title(f"{var_title} - {local_time} local (CEST), 2023-08-21\n"
                 f"SOLWEIG physical model, 2.5 m resolution", fontsize=12, fontweight="bold")
    ax.set_xlabel("Easting (m, EPSG:25830)")
    ax.set_ylabel("Northing (m, EPSG:25830)")
    ax.legend(loc="lower left", fontsize=7, framealpha=0.9)

    cbar = fig.colorbar(img, ax=ax, shrink=0.7, label=cbar_label)

    fig.text(0.5, 0.01,
              "Modelled physical quantity, NOT a direct measurement - see docs/PHASE2_VALIDATION_REPORT.md.",
              ha="center", fontsize=7, color="gray")
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    out_png = MAPS / f"{var}_{label}.png"
    fig.savefig(out_png, dpi=180)
    plt.close(fig)
    print(f"Wrote {out_png}")


def main():
    for local_time, label in [("12:00", "1200"), ("15:00", "1500"), ("18:00", "1800")]:
        render("tmrt", label, local_time, cmap="inferno", vmin=25, vmax=75,
               cbar_label="Tmrt (deg C)")
        render("utci", label, local_time, cmap="YlOrRd", vmin=20, vmax=50,
               cbar_label="UTCI (deg C)")


if __name__ == "__main__":
    main()
