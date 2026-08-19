"""FIG02 — Thermal-method divergence (hero figure). Renders from locked evidence only.
No new analysis: reads per-row proxy vs physical feasibility states and the locked
timestamp-rate table. Outputs PDF + SVG + PNG."""
import csv, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle
from matplotlib.lines import Line2D

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

# ---- style ----
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8, "axes.edgecolor": "#333333",
    "axes.linewidth": 0.8, "text.color": "#333333", "axes.labelcolor": "#333333",
    "xtick.color": "#333333", "ytick.color": "#333333", "svg.fonttype": "none",
})
NEUTRAL, DIR_MORE, DIR_LESS, INK = "#BFBFBF", "#0072B2", "#E69F00", "#333333"

# ---- data (locked) ----
rows = [x for x in csv.DictReader(open(os.path.join(ROOT, "data/processed/phase2_asset_thermal_exposure.csv"), encoding="utf-8"))
        if x["indoor_outdoor"] == "outdoor"]
assets = sorted(set(x["asset_id"] for x in rows))          # A14..A27 (14)
times = ["12:00", "15:00", "18:00"]
def state(x):
    if x["reclassified"] == "False": return "agree"
    return "MORE" if "MORE" in x["reclassification_direction"] else "LESS"
cell = {(x["asset_id"], x["timestamp"]): state(x) for x in rows}

# locked aggregate checks
n_obs = len(rows); n_change = sum(1 for v in cell.values() if v != "agree")
n_more = sum(1 for v in cell.values() if v == "MORE"); n_less = sum(1 for v in cell.values() if v == "LESS")
assert (n_obs, n_change, n_more, n_less) == (42, 14, 9, 5), (n_obs, n_change, n_more, n_less)
# locked timestamp rates
rate = {r["group"]: float(r["value"]) for r in csv.DictReader(
    open(os.path.join(ROOT, "outputs/tables/proxy_vs_physical_comparison.csv"), encoding="utf-8"))
    if r["metric"] == "reclassification_rate_by_timestamp_pct"}
assert rate["12:00"] == 64.3 and rate["15:00"] == 0.0 and rate["18:00"] == 35.7

COL = {"agree": NEUTRAL, "MORE": DIR_MORE, "LESS": DIR_LESS}
HATCH = {"agree": "", "MORE": "//", "LESS": "\\\\"}
MARK = {"agree": "o", "MORE": "^", "LESS": "v"}

fig = plt.figure(figsize=(7.1, 4.5))
gs = fig.add_gridspec(2, 2, width_ratios=[1.15, 1.0], height_ratios=[1.0, 0.42],
                      wspace=0.32, hspace=0.42, left=0.08, right=0.985, top=0.88, bottom=0.10)

# ---- Panel A: asset x timestamp divergence matrix ----
axA = fig.add_subplot(gs[:, 0])
for j, a in enumerate(assets):
    yy = len(assets) - 1 - j
    for i, t in enumerate(times):
        s = cell[(a, t)]
        axA.add_patch(Rectangle((i, yy), 1, 1, facecolor=COL[s], edgecolor="white",
                                lw=1.0, hatch=HATCH[s]))
        if s != "agree":
            axA.plot(i + 0.5, yy + 0.5, marker=MARK[s], color="white", ms=5.5,
                     mec=INK, mew=0.6, linestyle="none")
axA.set_xlim(0, 3); axA.set_ylim(0, len(assets))
axA.set_xticks([i + 0.5 for i in range(3)]); axA.set_xticklabels(times, fontsize=8)
axA.set_yticks([len(assets) - 1 - j + 0.5 for j in range(len(assets))])
axA.set_yticklabels(assets, fontsize=7)
axA.tick_params(length=0)
for sp in axA.spines.values(): sp.set_visible(False)
axA.set_title("A  Agreement by asset × timestamp", loc="left",
              fontsize=9, fontweight="bold", color=INK, pad=6)
axA.text(0, -0.9, "14 outdoor assets × 3 timestamps = 42 observations", fontsize=7.5, color=INK)

# ---- Panel B: timestamp divergence summary (100% stacked) ----
axB = fig.add_subplot(gs[0, 1])
order = ["MORE", "agree", "LESS"]
counts = {t: {k: sum(1 for a in assets if cell[(a, t)] == k) for k in order} for t in times}
ypos = [2, 1, 0]
for yy, t in zip(ypos, times):
    left = 0
    for k in order:
        w = counts[t][k] / 14 * 100
        if w > 0:
            axB.barh(yy, w, left=left, height=0.62, color=COL[k], hatch=HATCH[k],
                     edgecolor="white", lw=0.8)
            if w >= 10:
                axB.text(left + w / 2, yy, f"{w:.1f}%", ha="center", va="center",
                         fontsize=7, color="white" if k != "agree" else INK)
        left += w
    axB.text(101, yy, f"{rate[t]:.1f}% changed", va="center", fontsize=7.5, color=INK)
axB.set_yticks(ypos); axB.set_yticklabels(times, fontsize=8)
axB.set_xlim(0, 100); axB.set_xticks([0, 25, 50, 75, 100])
axB.set_xticklabels(["0", "25", "50", "75", "100"], fontsize=7)
axB.set_xlabel("Share of the 14 outdoor assets (%)", fontsize=8)
axB.tick_params(length=0)
for sp in ("top", "right", "left"): axB.spines[sp].set_visible(False)
axB.set_title("B  Divergence direction by timestamp", loc="left",
              fontsize=9, fontweight="bold", color=INK, pad=6)

# ---- Panel C: aggregate annotation + legend ----
axC = fig.add_subplot(gs[1, 1]); axC.axis("off")
axC.text(0, 0.92, "Overall: 14 / 42 observations reclassified (33.3%)", fontsize=8.5,
         color=INK, fontweight="bold")
axC.text(0, 0.66, "9 physical more restrictive  ·  5 physical less restrictive  ·  28 agree",
         fontsize=7.8, color=INK)
handles = [
    Patch(facecolor=NEUTRAL, edgecolor="white", label="Agreement (both methods same state)"),
    Patch(facecolor=DIR_MORE, hatch="//", edgecolor="white", label="Physical more restrictive than proxy"),
    Patch(facecolor=DIR_LESS, hatch="\\\\", edgecolor="white", label="Physical less restrictive than proxy"),
]
axC.legend(handles=handles, loc="lower left", bbox_to_anchor=(0, -0.05), frameon=False,
           fontsize=7.3, handlelength=1.4, handleheight=1.1, labelspacing=0.5)

fig.suptitle("Thermal-method choice changes feasibility classifications — in both directions",
             fontsize=10.5, fontweight="bold", color=INK, x=0.02, ha="left", y=0.975)

base = os.path.join(HERE, "FIG02_THERMAL_METHOD_DIVERGENCE_v0.1")
for ext, dpi in [("pdf", None), ("svg", None), ("png", 400)]:
    fig.savefig(f"{base}.{ext}", dpi=dpi, bbox_inches="tight")
print("wrote", base, "(pdf/svg/png)")
print("checks OK: 42/14/9/5; rates 64.3/0.0/35.7")
