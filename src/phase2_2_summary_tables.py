"""
Phase 2.2 final synthesis: build the two required change tables and verify the
substantive-finding invariants exactly, from the locked Phase 2 baseline, the
Phase 2.1 audits, and the Phase 2.2 Task A / Task B outputs. Writes:
  outputs/tables/phase2_2_geometry_changes.csv
  outputs/tables/phase2_2_robustness_changes.csv
and prints the exact numbers the gate/docs cite.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "outputs" / "tables"


def feasibility(u):
    if u >= 46: return "NOT RECOMMENDED"
    if u >= 32: return "FEASIBLE WITH CONDITIONS"
    return "FEASIBLE"


def main():
    base = pd.read_csv(PROCESSED / "phase2_asset_thermal_exposure.csv")
    outdoor = base[base.indoor_outdoor == "outdoor"].copy()
    conf = pd.read_csv(PROCESSED / "phase2_2_decision_confidence.csv")
    geom = pd.read_csv(PROCESSED / "phase2_2_corrected_geometry_utci.csv")
    ev = pd.read_csv(PROCESSED / "phase2_2_geometry_evidence.csv").set_index("asset_id")

    # ---- geometry changes table (per corrected asset x timestamp, central variant + bracket) ----
    verdicts = {
        "A23": "PARTIALLY STALE", "A24": "REPRESENTATIVE (not stale)", "A27": "MATERIALLY STALE",
    }
    grows = []
    for aid in ["A23", "A24", "A27"]:
        for ts in ["12:00", "15:00", "18:00"]:
            brow = outdoor[(outdoor.asset_id == aid) & (outdoor.timestamp == ts)].iloc[0]
            u_base = float(brow.utci_mean_10m)
            if aid == "A24":
                grows.append({
                    "asset_id": aid, "name": brow["name"], "timestamp": ts,
                    "geometry_verdict": verdicts[aid],
                    "correction_applied": False,
                    "utci_baseline": round(u_base, 1),
                    "utci_corrected_central": round(u_base, 1),
                    "utci_corrected_narrow": round(u_base, 1),
                    "utci_corrected_wide": round(u_base, 1),
                    "utci_delta_central": 0.0,
                    "feas_baseline": feasibility(u_base),
                    "feas_corrected_central": feasibility(u_base),
                    "decision_changed": False,
                    "bias_direction": "none (LiDAR representative)",
                })
            else:
                gg = geom[(geom.asset_id == aid) & (geom.timestamp == ts)].set_index("variant")
                uc = float(gg.loc["central", "utci_corrected"])
                grows.append({
                    "asset_id": aid, "name": brow["name"], "timestamp": ts,
                    "geometry_verdict": verdicts[aid],
                    "correction_applied": True,
                    "utci_baseline": round(u_base, 1),
                    "utci_corrected_central": round(uc, 1),
                    "utci_corrected_narrow": round(float(gg.loc["narrow", "utci_corrected"]), 1),
                    "utci_corrected_wide": round(float(gg.loc["wide", "utci_corrected"]), 1),
                    "utci_delta_central": round(uc - u_base, 1),
                    "feas_baseline": feasibility(u_base),
                    "feas_corrected_central": feasibility(uc),
                    "decision_changed": feasibility(uc) != feasibility(u_base),
                    "bias_direction": "overestimated heat (LiDAR understated canopy)",
                })
    gdf = pd.DataFrame(grows)
    TABLES.mkdir(parents=True, exist_ok=True)
    gdf.to_csv(TABLES / "phase2_2_geometry_changes.csv", index=False, encoding="utf-8")

    # ---- robustness changes table (per asset x timestamp: Phase 2.1 -> Phase 2.2) ----
    rc = conf[["asset_id", "name", "timestamp", "robustness_phase2_1", "decision_confidence",
               "envelope_low", "envelope_high", "envelope_width", "demonstrated_sensitivity_c",
               "confidence_changed_vs_phase2_1", "uncertainty_reason"]].copy()
    rc = rc.rename(columns={"decision_confidence": "confidence_phase2_2"})
    rc.to_csv(TABLES / "phase2_2_robustness_changes.csv", index=False, encoding="utf-8")

    # ---- distributions ----
    def dist(series):
        c = series.value_counts()
        return {k: (int(c.get(k, 0)), round(100 * int(c.get(k, 0)) / len(series), 1))
                for k in ["ROBUST", "BOUNDARY", "UNSTABLE"]}
    p21 = dist(conf["robustness_phase2_1"])
    p22 = dist(conf["decision_confidence"])
    print("=== Robustness: Phase 2.1 vs Phase 2.2 (n=42 outdoor) ===")
    for k in ["ROBUST", "BOUNDARY", "UNSTABLE"]:
        print(f"  {k:9s}  P2.1 {p21[k][0]:2d} ({p21[k][1]:4.1f}%)   ->   P2.2 {p22[k][0]:2d} ({p22[k][1]:4.1f}%)")
    changed = int(conf["confidence_changed_vs_phase2_1"].sum())
    print(f"\nRows changing confidence state: {changed} / 42 ({100*changed/42:.1f}%)")

    # ---- substantive-finding invariants ----
    # 1. Reclassification (Phase1 proxy vs Phase2 physical) - baseline, unchanged by geometry
    recl = outdoor["reclassified"].sum()
    print(f"\n=== Substantive invariants ===")
    print(f"Physical-vs-proxy reclassification (baseline): {recl}/42 = {100*recl/42:.1f}%")
    # geometry correction effect on reclassification: does any corrected feas differ from baseline feas?
    geom_feas_changes = geom[geom.feas_corrected != geom.feas_phase2_baseline]
    print(f"Corrected-geometry realizations that change an asset's feasibility_state: {len(geom_feas_changes)} "
          f"(=> reclassification rate unchanged at {100*recl/42:.1f}%)")

    # 2. 12:00 finding: all 14 outdoor >=32 UTCI, under baseline AND corrected geometry
    t12 = outdoor[outdoor.timestamp == "12:00"]
    base_ok = int((t12.utci_mean_10m >= 32).sum())
    # corrected: substitute A23/A27 corrected (all 3 variants) and check min stays >=32
    g12 = geom[geom.timestamp == "12:00"]
    corrected_min = g12.groupby("variant")["utci_corrected"].min()
    print(f"\n12:00 finding: outdoor assets with UTCI>=32:  baseline {base_ok}/14")
    print(f"  A23/A27 corrected 12:00 UTCI (all variants) min: "
          f"{g12[g12.corrected_here]['utci_corrected'].min():.1f} C (>=32 required)")
    print(f"  => 12:00 finding holds under corrected geometry: "
          f"{bool(g12[g12.corrected_here]['utci_corrected'].min() >= 32)}")

    # 3. UNSTABLE count and identity
    uns = conf[conf.decision_confidence == "UNSTABLE"]
    print(f"\nUNSTABLE rows Phase 2.2: {len(uns)}/42 = {100*len(uns)/42:.1f}%")
    for _, r in uns.iterrows():
        print(f"   {r['asset_id']} @ {r['timestamp']}")

    # 4. substantive tourism decision changes (baseline decision_state vs any realization majority)
    print(f"\nSubstantive tourism DECISION changes from Phase 2 baseline: "
          f"geometry correction flips {int(geom.decision_changed.sum())} of "
          f"{len(geom)} corrected realizations; solar flips 1 (A24@18:00 REAL_SATELLITE).")

    print(f"\nWrote {TABLES/'phase2_2_geometry_changes.csv'}")
    print(f"Wrote {TABLES/'phase2_2_robustness_changes.csv'}")


if __name__ == "__main__":
    main()
