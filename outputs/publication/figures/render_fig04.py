"""FIG04 — Screening consequence vs conventional nearest-open baseline.
Renders from locked scenario tables only. No new analysis. PDF + SVG + PNG."""
import csv, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8, "text.color": "#333333",
    "axes.edgecolor": "#333333", "svg.fonttype": "none",
})
INK, ACCENT, ATT = "#333333", "#4C4C4C", "#0072B2"

h = {x["scenario"]: x for x in csv.DictReader(open(os.path.join(ROOT, "outputs/tables/phase3_hati_vs_baseline.csv"), encoding="utf-8"))}
s = {x["scenario"]: x for x in csv.DictReader(open(os.path.join(ROOT, "data/processed/phase3_scenarios_summary.csv"), encoding="utf-8"))}
scen = [f"S{i}" for i in range(1, 9)]

n_changed = sum(h[k]["candidate_set_changed"] == "True" for k in scen)
n_fail = sum(h[k]["baseline_pick_survives_hati"] == "False" for k in scen)
n_removed = sum(int(h[k]["n_removed_by_hati_thermal_or_evidence"]) for k in scen)
assert (n_changed, n_fail, n_removed) == (7, 3, 23), (n_changed, n_fail, n_removed)
assert s["S8"]["recommendation"] == "NO_DEFENSIBLE_ALTERNATIVE" and s["S8"]["n_candidate_alternatives"] == "0"

def short(name, n=24):
    return name if len(name) <= n else name[:n - 1] + "…"

fig = plt.figure(figsize=(7.6, 4.7))
ax = fig.add_axes([0.005, 0.06, 0.99, 0.80]); ax.axis("off")
ax.set_xlim(0, 100); ax.set_ylim(0, 9)

# column x-anchors (rebalanced)
X_SCN = 1.0            # scenario label (source/time/radius)
X_MK = 30.5           # baseline survive marker
X_BASE = 32.0         # baseline pick text
X_BAR0 = 57.0         # surviving-alternatives bar start
X_BARW = 22.0         # bar full width (=9 alternatives)
X_REM = 92.0          # removed count

# headers
ax.text(X_SCN, 8.62, "Scenario (source · time · reach)", fontsize=8, fontweight="bold", color=INK)
ax.text(X_MK - 0.4, 8.62, "Nearest-open baseline pick", fontsize=8, fontweight="bold", color=INK)
ax.text(X_MK - 0.4, 8.30, "● passes screening · ○ removed by screening", fontsize=6.4, color="#666666")
ax.text(X_BAR0, 8.62, "Surviving alternatives (0–9)", fontsize=8, fontweight="bold", color=INK)
ax.text(X_REM, 8.62, "Removed", fontsize=8, fontweight="bold", color=INK, ha="center")
ax.text(X_REM, 8.30, "(thermal/evid.)", fontsize=6.4, color="#666666", ha="center")

for i, k in enumerate(scen):
    y = 8 - i - 0.5
    hh, ss = h[k], s[k]
    is_s8 = (k == "S8")
    if is_s8:
        ax.add_patch(FancyBboxPatch((X_SCN - 0.6, y - 0.44), 98.0, 0.9,
                     boxstyle="round,pad=0.02,rounding_size=0.08",
                     fill=False, ec=ATT, lw=1.6, zorder=5))
    ax.text(X_SCN, y + 0.10, f"{k}  {short(ss['source_name'])}", fontsize=7.4, va="center", color=INK, fontweight="bold")
    ax.text(X_SCN, y - 0.24, f"{ss['timestamp']} · {ss['access_radius_m']} m", fontsize=6.6, va="center", color="#666666")
    # baseline pick + survive status
    surv = hh["baseline_pick_survives_hati"] == "True"
    ax.plot(X_MK, y, marker="o", ms=7, mfc=(ACCENT if surv else "white"), mec=INK, mew=1.0, linestyle="none")
    ax.text(X_BASE, y + 0.10, short(hh["baseline_pick_name"], 22), fontsize=7.1, va="center", color=INK)
    ax.text(X_BASE, y - 0.24, "passes screening" if surv else "removed · OUTDOOR_EXPOSURE_TOO_HIGH",
            fontsize=6.3, va="center", color=("#666666" if surv else ATT))
    # surviving-alternatives bar
    nalt = int(ss["n_candidate_alternatives"])
    ax.add_patch(Rectangle((X_BAR0, y - 0.22), X_BARW, 0.44, fill=False, ec="#CCCCCC", lw=0.6))
    if nalt > 0:
        ax.add_patch(Rectangle((X_BAR0, y - 0.22), X_BARW * nalt / 9, 0.44,
                     facecolor=(ATT if is_s8 else ACCENT), edgecolor="none"))
        ax.text(X_BAR0 + X_BARW * nalt / 9 + 0.8, y, str(nalt), fontsize=7.2, va="center", color=INK)
    else:
        ax.text(X_BAR0 + 0.4, y, "0 of 26 survive → NO_DEFENSIBLE_ALTERNATIVE",
                fontsize=6.6, va="center", color=ATT, fontweight="bold")
    ax.text(X_REM, y, hh["n_removed_by_hati_thermal_or_evidence"], fontsize=7.6, va="center", ha="center", color=INK)

fig.text(0.02, 0.025,
         "Candidate set changed in 7 of 8 scenarios   ·   nearest-open pick removed by screening in 3 of 8   ·   "
         "23 open, in-radius options removed on thermal/evidence grounds",
         fontsize=7.5, color=INK)

fig.suptitle("Heat-aware screening changes the option set a nearest-open tool returns",
             fontsize=10.5, fontweight="bold", color=INK, x=0.02, ha="left", y=0.975)
fig.text(0.02, 0.905,
         "S8 (outlined) returns no defensible alternative under the 500 m reach — an architectural outcome, not a ranked pick",
         fontsize=7.3, color="#555555")

base = os.path.join(HERE, "FIG03_SCREENING_CONSEQUENCE_v0.1")
for ext, dpi in [("pdf", None), ("svg", None), ("png", 400)]:
    fig.savefig(f"{base}.{ext}", dpi=dpi, bbox_inches="tight")
print("wrote", base)
print("checks OK: changed 7/8, baseline_fail 3/8, removed 23, S8 -> NO_DEFENSIBLE_ALTERNATIVE")
