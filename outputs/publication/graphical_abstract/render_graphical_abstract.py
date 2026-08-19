"""Graphical abstract — HATI-Madrid. Landscape 1:2.5, method-neutral. Inherits F2's
divergence semantics and F4's screening vocabulary. Visible text per
docs/PHASE5_3A_GRAPHICAL_ABSTRACT_SPEC.md. No new analysis.
Master SVG + PDF; PNG export 2656 x 1062 px."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(__file__)
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": "#333333", "svg.fonttype": "none"})
INK, MORE, LESS, PANEL = "#333333", "#0072B2", "#E69F00", "#F4F4F4"

fig = plt.figure(figsize=(13.28, 5.31))            # 1:2.5 landscape; 200 dpi -> 2656x1062
ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
ax.set_xlim(0, 100); ax.set_ylim(0, 40)
YC = 21.0

def box(cx, cy, w, h, lines, fs, bold=False, fc="white", ec=INK, lw=1.4):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                 boxstyle="round,pad=0.1,rounding_size=0.4", fc=fc, ec=ec, lw=lw, zorder=3))
    ax.text(cx, cy, lines, ha="center", va="center", fontsize=fs, color=INK,
            fontweight=("bold" if bold else "normal"), zorder=4)

def arrow(x0, x1, y, ms=22, lw=2.0):
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="-|>", mutation_scale=ms,
                 color=INK, lw=lw, zorder=2))

# ---- pivot banner ----
ax.text(50, 38.3, "Method choice, not method accuracy", ha="center", va="center",
        fontsize=19, fontweight="bold", color=INK)

# ---- Stage 1: context ----
box(8.5, YC, 14, 14, "Urban tourism\nopportunities\nunder extreme\nheat", 12, bold=True, fc=PANEL)
arrow(16.0, 19.5, YC)

# ---- Stage 2: two EQUAL representations ----
ax.text(31, YC + 8.4, "Two thermal representations", ha="center", fontsize=11, fontweight="bold", color=INK)
box(31, YC + 4.0, 17, 6.2, "Simple operational proxy\nair temperature + nearby trees", 9.5, fc="white")
box(31, YC - 4.0, 17, 6.2, "Physically based model\nSOLWEIG → Tmrt → UTCI", 9.5, fc="white")
ax.text(31, YC, "vs", ha="center", va="center", fontsize=11, color="#888888", style="italic", zorder=5)
arrow(40.5, 44.0, YC)

# ---- Stage 3: decision effect (both directions) ----
box(57, YC, 18, 15, "", 12, fc=PANEL)
ax.text(57, YC + 4.7, "Feasibility\nclassifications changed", ha="center", va="center", fontsize=11, fontweight="bold", color=INK)
ax.text(57, YC - 0.8, "33.3%  (14/42)", ha="center", va="center", fontsize=16, fontweight="bold", color=INK)
ax.plot(50.5, YC - 5.0, marker="^", ms=10, color=MORE, mec=INK, mew=0.6, zorder=5)
ax.plot(63.5, YC - 5.0, marker="v", ms=10, color=LESS, mec=INK, mew=0.6, zorder=5)
ax.text(57, YC - 5.0, "in both directions", ha="center", va="center", fontsize=9.5, color=INK)
arrow(66.5, 70.0, YC)

# ---- Stage 4: constraint-first screen -> two equal outcomes ----
ax.text(85, YC + 8.4, "Constraint-first screening", ha="center", fontsize=11, fontweight="bold", color=INK)
box(85, YC + 4.0, 27, 5.0,
    "open?  ·  reachable?  ·  thermally feasible?\n·  evidence?  ·  improvement?", 8.3, fc="white")
ax.add_patch(FancyArrowPatch((80, YC + 1.5), (78.5, YC - 0.9), arrowstyle="-|>", mutation_scale=15, color=INK, lw=1.5, zorder=2))
ax.add_patch(FancyArrowPatch((90, YC + 1.5), (91.5, YC - 0.9), arrowstyle="-|>", mutation_scale=15, color=INK, lw=1.5, zorder=2))
box(78.5, YC - 4.2, 12, 5.4, "Surviving\nalternatives", 10, bold=True, fc="white")
box(91.5, YC - 4.2, 12, 5.4, "No defensible\nalternative", 10, bold=True, fc="white")

# ---- footer stat ----
ax.text(50, 2.4, "Candidate set changed in 7 of 8 scenarios", ha="center", va="center",
        fontsize=12, color=INK)

base = os.path.join(HERE, "HATI_graphical_abstract_v0.1")
fig.savefig(f"{base}.svg")
fig.savefig(f"{base}.pdf")
fig.savefig(f"{base}.png", dpi=200)
print("wrote", base, "(svg/pdf/png)")
