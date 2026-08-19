"""FIG05 — Decision robustness under tested uncertainty. Panel A: solar-forcing decision
changes. Panel B: decision-confidence distribution (A24@18:00 sole UNSTABLE). Locked data
only; no new analysis. PDF + SVG + PNG."""
import csv, os
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "text.color": "#333333",
                     "axes.edgecolor": "#333333", "svg.fonttype": "none"})
INK, ROB, BND, UNS = "#333333", "#4C4C4C", "#9E9E9E", "#0072B2"

# ---- Panel A data: solar-forcing decision changes ----
sf = list(csv.DictReader(open(os.path.join(ROOT, "outputs/tables/solar_forcing_sensitivity.csv"), encoding="utf-8")))
chg = {r["scenario"]: float(r["value"]) for r in sf if r["metric"] == "decision_changes_vs_phase2_baseline"}
pct = {r["scenario"]: float(r["value"]) for r in sf if r["metric"] == "decision_changes_pct"}
assert chg["REAL_SATELLITE"] == 1 and chg["SENS_A_minus10pct"] == 0 and chg["SENS_B_minus20pct"] == 0

# ---- Panel B data: confidence distribution ----
cd = [r for r in csv.DictReader(open(os.path.join(ROOT, "data/processed/phase2_2_decision_confidence.csv"), encoding="utf-8"))]
conf = Counter(r["decision_confidence"] for r in cd)
assert conf["ROBUST"] == 35 and conf["BOUNDARY"] == 6 and conf["UNSTABLE"] == 1
unstable = [(r["asset_id"], r["timestamp"]) for r in cd if r["decision_confidence"] == "UNSTABLE"]
assert unstable == [("A24", "18:00")]

fig = plt.figure(figsize=(7.2, 3.5))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.05], wspace=0.30, left=0.09, right=0.98, top=0.80, bottom=0.16)

# ================= Panel A =================
axA = fig.add_subplot(gs[0, 0])
labels = ["Real satellite\n(EUMETSAT)", "−10% GHI", "−20% GHI"]
keys = ["REAL_SATELLITE", "SENS_A_minus10pct", "SENS_B_minus20pct"]
vals = [chg[k] for k in keys]
xs = range(3)
axA.bar(xs, vals, width=0.6, color=ACCENT if False else INK, edgecolor="none")
for x, k in zip(xs, keys):
    axA.text(x, chg[k] + 0.06, f"{int(chg[k])}/42\n({pct[k]:.1f}%)", ha="center", va="bottom", fontsize=7.4, color=INK)
axA.set_xticks(list(xs)); axA.set_xticklabels(labels, fontsize=7.2)
axA.set_ylim(0, 3); axA.set_yticks([0, 1, 2, 3])
axA.set_ylabel("Outdoor decisions changed\nvs clear-sky baseline (of 42)", fontsize=7.6)
for sp in ("top", "right"): axA.spines[sp].set_visible(False)
axA.tick_params(length=2)
axA.set_title("A  Solar-forcing sensitivity", loc="left", fontsize=9, fontweight="bold", color=INK, pad=4)

# ================= Panel B =================
axB = fig.add_subplot(gs[0, 1])
order = ["ROBUST", "BOUNDARY", "UNSTABLE"]
cols = {"ROBUST": ROB, "BOUNDARY": BND, "UNSTABLE": UNS}
hatch = {"ROBUST": "", "BOUNDARY": "..", "UNSTABLE": "xx"}
vals = [conf[k] for k in order]
bars = axB.bar(range(3), vals, width=0.6, color=[cols[k] for k in order],
               edgecolor="white", hatch=[hatch[k] for k in order])
for x, k in zip(range(3), order):
    axB.text(x, conf[k] + 0.6, f"{conf[k]}/42\n({conf[k]/42*100:.1f}%)", ha="center", va="bottom", fontsize=7.4, color=INK)
axB.annotate("sole UNSTABLE case:\nA24 @ 18:00 (46 °C boundary)", xy=(2, 1.2), xytext=(1.15, 12),
             fontsize=6.8, color=INK, ha="left",
             arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9))
axB.set_xticks(range(3)); axB.set_xticklabels(order, fontsize=7.6)
axB.set_ylim(0, 40); axB.set_yticks([0, 10, 20, 30, 40])
axB.set_ylabel("Outdoor observations (of 42)", fontsize=7.6)
for sp in ("top", "right"): axB.spines[sp].set_visible(False)
axB.tick_params(length=2)
axB.set_title("B  Decision-confidence distribution", loc="left", fontsize=9, fontweight="bold", color=INK, pad=4)

fig.suptitle("Decision robustness under tested uncertainty", fontsize=10.5, fontweight="bold",
             color=INK, x=0.02, ha="left", y=0.965)
fig.text(0.02, 0.90, "Tested uncertainty only: solar forcing (4 realizations) + targeted canopy geometry (2 assets) — not total uncertainty; not a validation of the modelled field",
         fontsize=6.8, color="#555555")

base = os.path.join(HERE, "FIG04_TESTED_UNCERTAINTY_v0.1")
for ext, dpi in [("pdf", None), ("svg", None), ("png", 400)]:
    fig.savefig(f"{base}.{ext}", dpi=dpi, bbox_inches="tight")
print("wrote", base, "| solar 1/0/0; conf 35/6/1; UNSTABLE", unstable)
