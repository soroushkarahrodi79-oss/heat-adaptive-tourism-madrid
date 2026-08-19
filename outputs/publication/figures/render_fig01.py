"""FIG01 — Study design and screening architecture. Panel A: Madrid pilot study area +
27 assets (from locked geometry). Panel B: constraint-first architecture schematic
(from locked decision-architecture doc). No new analysis. PDF + SVG + PNG."""
import csv, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
import geopandas as gpd

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "text.color": "#333333",
                     "axes.edgecolor": "#333333", "svg.fonttype": "none"})
INK, GREY, ACCENT = "#333333", "#8C8C8C", "#4C4C4C"

# ---- data (locked), reproject to metric EPSG:25830 ----
area = gpd.read_file(os.path.join(ROOT, "data/processed/study_area.geojson")).to_crs(25830)
rows = list(csv.DictReader(open(os.path.join(ROOT, "data/processed/pilot_assets.csv"), encoding="utf-8")))
pts = gpd.GeoDataFrame(rows, geometry=gpd.points_from_xy(
    [float(r["longitude"]) for r in rows], [float(r["latitude"]) for r in rows]), crs=4326).to_crs(25830)
n_in = sum(r["indoor_outdoor"] == "indoor" for r in rows)
n_out = sum(r["indoor_outdoor"] == "outdoor" for r in rows)
assert (len(rows), n_in, n_out) == (27, 13, 14)

fig = plt.figure(figsize=(7.5, 4.3))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.18], wspace=0.10, left=0.02, right=0.985, top=0.88, bottom=0.06)

# ================= Panel A: map =================
axA = fig.add_subplot(gs[0, 0])
area.boundary.plot(ax=axA, color=INK, lw=1.2)
area.plot(ax=axA, color="#F2F2F2", zorder=0)
for io, mk, col, lab in [("outdoor", "^", ACCENT, "Outdoor asset (14)"), ("indoor", "o", GREY, "Indoor asset (13)")]:
    sub = pts[pts["indoor_outdoor"] == io]
    axA.scatter(sub.geometry.x, sub.geometry.y, marker=mk, s=42, facecolor=col,
                edgecolor="white", linewidth=0.6, zorder=5, label=lab)
axA.set_aspect("equal"); axA.axis("off")
xmin, ymin, xmax, ymax = area.total_bounds
# scale bar 500 m
sb = 500; x0 = xmin + (xmax - xmin) * 0.06; y0 = ymin + (ymax - ymin) * 0.05
axA.plot([x0, x0 + sb], [y0, y0], color=INK, lw=2.4, solid_capstyle="butt")
axA.text(x0 + sb / 2, y0 + (ymax - ymin) * 0.02, "500 m", ha="center", fontsize=7, color=INK)
# north arrow
nx = xmax - (xmax - xmin) * 0.06; ny = ymax - (ymax - ymin) * 0.16
axA.annotate("N", xy=(nx, ny + (ymax - ymin) * 0.09), xytext=(nx, ny),
             ha="center", fontsize=8, color=INK,
             arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
axA.legend(loc="upper left", frameon=False, fontsize=7, handletextpad=0.3, borderpad=0.2)
axA.set_title("A  Madrid pilot study area", loc="left", fontsize=9, fontweight="bold", color=INK, pad=4)
axA.text(xmin, ymin - (ymax - ymin) * 0.03, "Prado–Retiro–Atocha, central Madrid · ≈ 3.5 km² · 27 curated tourism assets",
         fontsize=7, color="#555555")

# ================= Panel B: architecture schematic =================
axB = fig.add_subplot(gs[0, 1]); axB.axis("off"); axB.set_xlim(0, 10); axB.set_ylim(0, 10)
axB.set_title("B  Constraint-first screening architecture", loc="left", fontsize=9, fontweight="bold", color=INK, pad=4)

def box(x, y, w, h, text, fs=7.2, bold=False, fc="white", ec=INK, lw=1.0):
    axB.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.12",
                  fc=fc, ec=ec, lw=lw))
    axB.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
             color=INK, fontweight=("bold" if bold else "normal"), wrap=True)

def arrow(x0, y0, x1, y1):
    axB.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=10,
                  color=INK, lw=1.0, shrinkA=0, shrinkB=0))

# assets
box(3.0, 9.0, 4.0, 0.8, "27 curated tourism assets", bold=True)
arrow(4.0, 9.0, 3.4, 8.35); arrow(6.0, 9.0, 6.6, 8.35)
# two EQUAL representation boxes
box(0.4, 7.3, 4.5, 1.05, "Simple operational proxy\nair temperature + nearby trees", fs=7.0)
box(5.1, 7.3, 4.5, 1.05, "Physically based model\nSOLWEIG → Tmrt → UTCI", fs=7.0)
axB.text(5.0, 7.82, "vs", ha="center", va="center", fontsize=7.5, color="#888888", style="italic")
arrow(2.65, 7.3, 4.3, 6.65); arrow(7.35, 7.3, 5.7, 6.65)
# constraint-first screen
box(1.2, 4.7, 7.6, 1.95, "", ec=INK, lw=1.2)
axB.text(5.0, 6.35, "Constraint-first screen  (first failing gate wins)", ha="center", fontsize=7.4, fontweight="bold", color=INK)
gates = ["open?", "reachable?", "thermally\nfeasible?", "evidence\nsufficient?", "meaningful\nimprovement?"]
gx = [1.75, 3.35, 4.95, 6.45, 8.0]
for i, (g, x) in enumerate(zip(gates, gx)):
    axB.text(x, 5.35, g, ha="center", va="center", fontsize=6.5, color=INK)
    if i < len(gates) - 1:
        axB.annotate("", xy=(gx[i + 1] - 0.55, 5.35), xytext=(x + 0.55, 5.35),
                     arrowprops=dict(arrowstyle="-|>", color="#999999", lw=0.8))
arrow(3.4, 4.7, 3.4, 4.0); arrow(6.6, 4.7, 6.6, 4.0)
# outcomes (equal weight)
box(0.7, 2.7, 4.2, 1.05, "Surviving\nalternatives", fs=7.4, bold=True)
box(5.1, 2.7, 4.2, 1.05, "No defensible\nalternative", fs=7.4, bold=True)
axB.text(5.0, 1.9, "Thermal state · decision confidence · evidence confidence · exclusion reason\nkept separate — no composite score",
         ha="center", va="center", fontsize=6.4, color="#555555")

fig.suptitle("Two thermal representations feed one transparent, constraint-first tourism-opportunity screen",
             fontsize=10, fontweight="bold", color=INK, x=0.02, ha="left", y=0.97)

base = os.path.join(HERE, "FIG01_STUDY_DESIGN_v0.1")
for ext, dpi in [("pdf", None), ("svg", None), ("png", 400)]:
    fig.savefig(f"{base}.{ext}", dpi=dpi, bbox_inches="tight")
print("wrote", base, "| assets 27 =", n_in, "indoor +", n_out, "outdoor")
