"""
Phase 1.2 agreement analysis: consumes data/processed/shade_proxy_comparison.csv
(built by src/shade_proxy_comparison.py using the pre-registered 50 m buffer)
and computes every metric required by the task spec:
  1. raw percentage agreement
  2. confusion matrices
  3. per-asset instability
  4. direction of disagreement
  5. agreement by morphology (plaza/street/park/attraction-exterior)
  6. timestamp-specific disagreement
  7. Cohen's kappa (computed, not relied on alone)

Writes outputs/tables/shade_proxy_agreement.csv (summary metrics table) and
prints full detail for docs/PHASE1_2_SHADE_EVIDENCE_GATE.md to quote from.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shade_proxy_comparison import cohens_kappa

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "outputs" / "tables"

FEAS_LABELS = ["FEASIBLE", "FEASIBLE WITH CONDITIONS", "NOT RECOMMENDED", "INSUFFICIENT EVIDENCE"]
PROXY_PAIRS = [
    ("OSM", "Madrid"), ("OSM", "TCD"), ("OSM", "green"),
    ("Madrid", "TCD"), ("Madrid", "green"), ("TCD", "green"),
]


def pct_agreement(df, col_a, col_b):
    valid = df.dropna(subset=[col_a, col_b])
    if len(valid) == 0:
        return None, 0
    agree = (valid[col_a] == valid[col_b]).sum()
    return 100 * agree / len(valid), len(valid)


def confusion(df, col_a, col_b, label_a, label_b):
    valid = df.dropna(subset=[col_a, col_b])
    ct = pd.crosstab(valid[col_a], valid[col_b], rownames=[label_a], colnames=[label_b])
    return ct


def main():
    df = pd.read_csv(PROCESSED / "shade_proxy_comparison.csv")
    outdoor = df[df["indoor_outdoor"] == "outdoor"].copy()
    n_outdoor_rows = len(outdoor)
    n_outdoor_assets = outdoor["asset_id"].nunique()

    print(f"Outdoor rows: {n_outdoor_rows} ({n_outdoor_assets} assets x 3 timestamps)")

    summary_rows = []

    # --- 1+7. Raw % agreement + kappa, all pairs, feasibility level ---
    print("\n=== 1&7. Feasibility agreement + Cohen's kappa (all pairs, all timestamps) ===")
    for a, b in PROXY_PAIRS:
        col_a, col_b = f"feasibility_{a}", f"feasibility_{b}"
        pct, n = pct_agreement(outdoor, col_a, col_b)
        valid = outdoor.dropna(subset=[col_a, col_b])
        kappa = cohens_kappa(valid[col_a].tolist(), valid[col_b].tolist(), FEAS_LABELS) if n else None
        print(f"  {a} vs {b}: {pct:.1f}% agreement (n={n}), Cohen's kappa={kappa:.3f}")
        summary_rows.append({"metric": "feasibility_agreement_pct", "proxy_a": a, "proxy_b": b,
                              "value": round(pct, 1), "n": n, "cohens_kappa": round(kappa, 3)})

    # --- 2. Confusion matrices for the two gate-critical pairs ---
    print("\n=== 2. Confusion matrices ===")
    print("\n-- Madrid vs TCD (feasibility) --")
    cm_mt = confusion(outdoor, "feasibility_Madrid", "feasibility_TCD", "Madrid", "TCD")
    print(cm_mt)
    print("\n-- OSM(baseline) vs Madrid (feasibility) --")
    print(confusion(outdoor, "feasibility_OSM", "feasibility_Madrid", "OSM", "Madrid"))
    print("\n-- OSM(baseline) vs TCD (feasibility) --")
    print(confusion(outdoor, "feasibility_OSM", "feasibility_TCD", "OSM", "TCD"))

    # --- 3. Per-asset instability ---
    print("\n=== 3. Per-asset instability (proxy_sensitive = True at >=1 timestamp) ===")
    asset_instab = outdoor.groupby("asset_id")["proxy_sensitive"].any()
    n_unstable = asset_instab.sum()
    print(f"Unstable outdoor assets: {n_unstable} / {n_outdoor_assets} ({100*n_unstable/n_outdoor_assets:.1f}%)")
    print(asset_instab[asset_instab].index.tolist())
    summary_rows.append({"metric": "unstable_outdoor_assets_pct", "proxy_a": "ALL", "proxy_b": "ALL",
                          "value": round(100 * n_unstable / n_outdoor_assets, 1), "n": n_outdoor_assets,
                          "cohens_kappa": None})

    # --- 4. Direction of disagreement ---
    print("\n=== 4. Direction of disagreement (MAJOR = spans FEASIBLE<->NOT RECOMMENDED) ===")
    dir_counts = outdoor[outdoor["proxy_sensitive"]]["disagreement_direction"].value_counts()
    print(dir_counts)
    n_major = (outdoor["disagreement_direction"].str.startswith("MAJOR", na=False)).sum()
    print(f"MAJOR disagreement rows: {n_major} / {n_outdoor_rows}")
    major_assets = outdoor[outdoor["disagreement_direction"].str.startswith("MAJOR", na=False)]["asset_id"].unique()
    print(f"Assets with >=1 MAJOR disagreement (>=2 feasibility levels apart): {sorted(set(major_assets))}")

    # --- 5. Agreement by morphology ---
    print("\n=== 5. Agreement by morphology ===")
    morph_rows = []
    for morph, g in outdoor.groupby("morphology"):
        for a, b in [("Madrid", "TCD"), ("OSM", "Madrid"), ("OSM", "TCD")]:
            pct, n = pct_agreement(g, f"feasibility_{a}", f"feasibility_{b}")
            morph_rows.append({"morphology": morph, "pair": f"{a} vs {b}", "agreement_pct": round(pct, 1) if pct is not None else None, "n": n})
    morph_df = pd.DataFrame(morph_rows)
    print(morph_df.to_string(index=False))
    for _, r in morph_df.iterrows():
        summary_rows.append({"metric": "morphology_agreement_pct", "proxy_a": r["pair"].split(" vs ")[0],
                              "proxy_b": r["pair"].split(" vs ")[1] + f" [{r['morphology']}]",
                              "value": r["agreement_pct"], "n": r["n"], "cohens_kappa": None})

    # --- 6. Timestamp-specific disagreement ---
    print("\n=== 6. Timestamp-specific agreement (Madrid vs TCD) ===")
    ts_rows = []
    for ts, g in outdoor.groupby("timestamp"):
        pct, n = pct_agreement(g, "feasibility_Madrid", "feasibility_TCD")
        local = ts.split("T")[1][:5]
        print(f"  {local}: {pct:.1f}% (n={n}), hazard={g['exposure_state_Madrid'].notna().sum() and g.iloc[0].get('morphology','')}")
        ts_rows.append({"timestamp": local, "agreement_pct": round(pct, 1), "n": n})
        summary_rows.append({"metric": "timestamp_agreement_pct", "proxy_a": "Madrid", "proxy_b": f"TCD [{local}]",
                              "value": round(pct, 1), "n": n, "cohens_kappa": None})

    # --- Systematic vs random check: does disagreement concentrate in specific morphologies? ---
    print("\n=== Systematic vs random disagreement check ===")
    disagree_by_morph = outdoor[outdoor["proxy_sensitive"]]["morphology"].value_counts()
    total_by_morph = outdoor["morphology"].value_counts()
    rate_by_morph = (disagree_by_morph / total_by_morph * 100).round(1)
    print("Disagreement rate (%) by morphology (rows where proxy_sensitive=True):")
    print(rate_by_morph)

    out_path = TABLES / "shade_proxy_agreement.csv"
    TABLES.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(summary_rows).to_csv(out_path, index=False, encoding="utf-8")
    print(f"\nWrote {out_path}")

    return outdoor, pd.DataFrame(summary_rows)


if __name__ == "__main__":
    main()
