"""
Phase 3 step 4: scenario map (small multiples, one panel per scenario). Each
panel shows the pilot assets, the scenario SOURCE (red star), the surviving
CANDIDATE_ALTERNATIVEs (green, linked to source), and closed/excluded assets in
grey. Schematic lat/lon plot - the study area is small enough that lon/lat with
an aspect correction is adequate for a locator map (no basemap dependency).
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
MAPS = ROOT / "outputs" / "maps"


def main():
    cat = pd.read_csv(PROCESSED / "phase3_asset_catalog.csv").set_index("asset_id")
    scen = pd.read_csv(PROCESSED / "phase3_scenarios.csv")
    summ = pd.read_csv(PROCESSED / "phase3_scenarios_summary.csv")

    lat0 = cat["latitude"].mean()
    aspect = 1.0 / np.cos(np.radians(lat0))  # lon degrees are shorter

    order = list(summ["scenario"])
    fig, axes = plt.subplots(2, 4, figsize=(20, 11))
    axes = axes.ravel()

    for ax, sid in zip(axes, order):
        s = summ[summ.scenario == sid].iloc[0]
        rows = scen[scen.scenario == sid]
        src = cat.loc[s["source_id"]]
        # all assets faint
        ax.scatter(cat["longitude"], cat["latitude"], s=18, c="#d0d0d0", zorder=1)
        # excluded (in this scenario) grey, alternatives green
        for _, r in rows.iterrows():
            c = cat.loc[r["candidate_id"]]
            if r["status"] == "CANDIDATE_ALTERNATIVE":
                ax.plot([src["longitude"], c["longitude"]], [src["latitude"], c["latitude"]],
                        c="#2e8b57", lw=1.0, alpha=0.7, zorder=2)
                marker = "s" if r["indoor_outdoor"] == "indoor" else "o"
                ax.scatter(c["longitude"], c["latitude"], s=70, c="#2e8b57",
                           marker=marker, edgecolors="k", linewidths=0.4, zorder=4)
                ax.annotate(r["candidate_id"], (c["longitude"], c["latitude"]),
                            fontsize=6.5, xytext=(2, 2), textcoords="offset points")
        # source star
        ax.scatter(src["longitude"], src["latitude"], s=260, c="#c0392b", marker="*",
                   edgecolors="k", linewidths=0.6, zorder=6)
        ax.annotate(s["source_id"], (src["longitude"], src["latitude"]),
                    fontsize=9, fontweight="bold", color="#c0392b", xytext=(4, 4), textcoords="offset points")
        rec = s["recommendation"]
        title_c = "#c0392b" if rec == "NO_DEFENSIBLE_ALTERNATIVE" else "#1a1a1a"
        ax.set_title(f"{sid}: {s['source_name'][:24]} @{s['timestamp']} (r={s['access_radius_m']}m)\n"
                     f"{rec} — {s['n_candidate_alternatives']} alt", fontsize=9.5, color=title_c)
        ax.set_aspect(aspect)
        ax.tick_params(labelsize=6)
        ax.grid(True, alpha=0.2)

    handles = [
        plt.Line2D([], [], marker="*", color="w", markerfacecolor="#c0392b", markersize=16, markeredgecolor="k", label="scenario source"),
        plt.Line2D([], [], marker="s", color="w", markerfacecolor="#2e8b57", markersize=10, markeredgecolor="k", label="indoor alternative"),
        plt.Line2D([], [], marker="o", color="w", markerfacecolor="#2e8b57", markersize=10, markeredgecolor="k", label="outdoor alternative"),
        plt.Line2D([], [], marker="o", color="w", markerfacecolor="#d0d0d0", markersize=10, label="other pilot asset (closed/excluded)"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=4, fontsize=10, frameon=False)
    fig.suptitle("HATI-Madrid Phase 3 — heat-adaptive tourism opportunity screening (2023-08-21, 8 scenarios)",
                 fontsize=14, y=0.98)
    fig.tight_layout(rect=[0, 0.04, 1, 0.96])
    MAPS.mkdir(parents=True, exist_ok=True)
    out = MAPS / "phase3_scenario_map.png"
    fig.savefig(out, dpi=140)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
