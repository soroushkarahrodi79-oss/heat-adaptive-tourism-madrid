"""FIG03 — Model-derived UTCI field across the day (12:00/15:00/18:00), shared scale.
Renders locked SOLWEIG UTCI rasters; no new analysis. PDF + PNG (raster) + SVG."""
import csv, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
import rasterio
import geopandas as gpd

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "text.color": "#333333",
                     "axes.edgecolor": "#333333", "svg.fonttype": "none"})
INK = "#333333"

times = [("1200", "12:00"), ("1500", "15:00"), ("1800", "18:00")]
VMIN, VMAX = 30.0, 48.0                      # shared quantitative scale (all panels)
cmap = plt.get_cmap("cividis")               # perceptually uniform, colour-blind-safe, no red/green
norm = Normalize(VMIN, VMAX)

# outdoor asset points (secondary overlay), reprojected to raster CRS 25830
rows = list(csv.DictReader(open(os.path.join(ROOT, "data/processed/pilot_assets.csv"), encoding="utf-8")))
out = [r for r in rows if r["indoor_outdoor"] == "outdoor"]
pts = gpd.GeoDataFrame(out, geometry=gpd.points_from_xy(
    [float(r["longitude"]) for r in out], [float(r["latitude"]) for r in out]), crs=4326).to_crs(25830)

fig, axes = plt.subplots(1, 3, figsize=(7.5, 3.2))
noon_min = None
for ax, (code, label) in zip(axes, times):
    with rasterio.open(os.path.join(ROOT, f"outputs/maps/utci_{code}.tif")) as ds:
        a = ds.read(1).astype(float)
        a[~np.isfinite(a)] = np.nan
        b = ds.bounds
    extent = (b.left, b.right, b.bottom, b.top)
    if code == "1200":
        noon_min = float(np.nanmin(a))
    im = ax.imshow(a, extent=extent, origin="upper", cmap=cmap, norm=norm, interpolation="nearest")
    # category breaks at 32 and 46 C
    ax.contour(np.flipud(a), levels=[32, 46], colors="white", linewidths=0.7,
               extent=extent, origin="lower")
    ax.scatter(pts.geometry.x, pts.geometry.y, s=10, facecolor="none",
               edgecolor="white", linewidth=0.7, zorder=5)
    ax.set_title(label, fontsize=9, fontweight="bold", color=INK, pad=3)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("#999999"); sp.set_linewidth(0.6)
# scale bar on first panel
axf = axes[0]
with rasterio.open(os.path.join(ROOT, "outputs/maps/utci_1200.tif")) as ds:
    b = ds.bounds
x0 = b.left + (b.right - b.left) * 0.06; y0 = b.bottom + (b.top - b.bottom) * 0.06
axf.plot([x0, x0 + 500], [y0, y0], color="white", lw=2.6, solid_capstyle="butt")
axf.text(x0 + 250, y0 + (b.top - b.bottom) * 0.03, "500 m", ha="center", fontsize=6.6, color="white")

assert abs(noon_min - 32.0) < 0.05, noon_min

fig.subplots_adjust(left=0.02, right=0.90, top=0.80, bottom=0.06, wspace=0.06)
cax = fig.add_axes([0.915, 0.10, 0.017, 0.66])
cb = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax)
cb.set_label("Model-derived UTCI (°C)", fontsize=7.6)
cb.set_ticks([30, 32, 34, 38, 42, 46, 48])
cb.ax.tick_params(labelsize=6.8)
cb.ax.axhline((32 - VMIN) / (VMAX - VMIN), color="white", lw=0.8)
cb.ax.axhline((46 - VMIN) / (VMAX - VMIN), color="white", lw=0.8)

fig.suptitle("Model-derived UTCI across the day (SOLWEIG/UTCI, 2.5 m; shared scale)",
             fontsize=10, fontweight="bold", color=INK, x=0.02, ha="left", y=0.965)
fig.text(0.02, 0.855, "White contours mark the 32 °C and 46 °C category breaks · white rings = outdoor assets · at 12:00 the field is ≥ 32 °C everywhere modelled",
         fontsize=6.7, color="#555555")

base = os.path.join(HERE, "SFIG01_UTCI_FIELD_v0.1")
for ext, dpi in [("pdf", 300), ("svg", None), ("png", 400)]:
    fig.savefig(f"{base}.{ext}", dpi=dpi, bbox_inches="tight")
print("wrote", base, "| shared scale 30-48; noon min =", round(noon_min, 1))
