"""
Exploratory sensitivity analysis of HATI-Madrid classifications (manuscript draft v0.3).

Reads ONLY versioned CSVs (no rasters, no SOLWEIG, no network) and needs only numpy and
pandas. It reproduces, for the 42 outdoor asset x hour observations of 21 Aug 2023:

  A  sensitivity of the tourism classes of each system to rules, thresholds, data sources
     and spatial supports, one variant at a time, each against its own baseline;
  B  Kendall tau-b between four shade/tree proxies and the modelled UTCI (descriptive).

The study is exploratory. The data had been inspected before this script was written, so
nothing here is a pre-registered or confirmatory test, and no significance test, interval
or equivalence claim is produced. Air temperature (deg C of air) and UTCI (index of
physiological heat stress) are never compared as equivalent quantities: each system is
only compared through its own classified output.

Inputs (read-only):
  data/processed/pilot_classifications.csv            system A (air temperature + trees)
  data/processed/phase2_asset_thermal_exposure.csv    system B (UTCI) and spatial supports
  data/processed/shade_proxy_comparison.csv           four shade/tree proxies
  data/processed/phase2_1_solar_scenario_assets.csv   irradiance variants of B
  data/raw/aemet_barajas_08221_hourly_202308.csv      Barajas hourly Ta (UTC)
  data/raw/madrid_meteo_municipal/meteo_municipal_202308.csv   Escuelas Aguirre Ta
  outputs/tables/proxy_vs_physical_comparison.csv     locked table, cross-checked only
  src/thresholds.py                                   AEMET thresholds (imported)

Outputs (new files; nothing existing is overwritten):
  outputs/tables/exploratory/exploratory_A_crosstab.csv
  outputs/tables/exploratory/exploratory_A_disagreements.csv
  outputs/tables/exploratory/exploratory_A_variants.csv
  outputs/tables/exploratory/exploratory_A_temperature_alignment.csv
  outputs/tables/exploratory/exploratory_A_physiological_categories.csv
  outputs/tables/exploratory/exploratory_B_kendall.csv

Run:  python src/exploratory_sensitivity.py
The script stops (AssertionError) if an integrity check or a headline value fails.
"""
import itertools
import sys

sys.dont_write_bytecode = True  # do not create __pycache__ in the repository
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thresholds as th  # noqa: E402  (pure-Python constants; AEMET warning thresholds)

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"
OUT = ROOT / "outputs" / "tables" / "exploratory"
HOURS = ["12:00", "15:00", "18:00"]
F, FWC, NR = "FEASIBLE", "FEASIBLE WITH CONDITIONS", "NOT RECOMMENDED"
PROXIES = {"OSM_tree_proxy": "OSM", "Madrid_tree_proxy": "Madrid",
           "Copernicus_TCD_proxy": "TCD", "green_polygon_proxy": "green"}
STUDY_DAY = pd.Timestamp(2023, 8, 21)


# ----------------------------------------------------------------------------- rules
def hour_of(ts):
    ts = str(ts)
    return ts[11:16] if "T" in ts else ts[:5]


def outdoor_rule(hazard, exposure):
    """Outdoor feasibility rule of system A, numbered as in src/thresholds.py
    (FEASIBILITY_RULES_OUTDOOR). Verified below against the stored classification."""
    if hazard == "EXTREME":
        return 1, NR
    if hazard == "SEVERE" and exposure == "HIGH":
        return 2, NR
    if hazard == "SEVERE":
        return 3, FWC
    if hazard == "ELEVATED" and exposure == "HIGH":
        return 4, FWC
    if hazard == "ELEVATED":
        return 5, FWC
    if hazard == "LOW" and exposure == "HIGH":
        return 6, FWC
    return 7, F


def utci_to_state(u):
    """Project feasibility mapping of system B (src/extract_asset_thermal_exposure.py):
    HATI's tourism classes, NOT the physiological UTCI categories."""
    return NR if u >= 46 else FWC if u >= 32 else F


CATS = ["<26 (no stress)", "26-32 moderate", "32-38 strong", "38-46 very strong", ">=46 extreme"]


def stress_category(u):
    """Standard UTCI heat-stress categories (Broede et al. 2012), computed from the numeric
    value. The category-label columns stored in the locked CSVs are NOT used (see manuscript
    v0.3, Section 8: their labels are shifted by one level relative to this standard)."""
    return CATS[int(np.digitize(u, [26, 32, 38, 46]))]


def kendall_tau_b(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    conc = disc = tx = ty = txy = 0
    for i, j in itertools.combinations(range(len(x)), 2):
        dx, dy = np.sign(x[i] - x[j]), np.sign(y[i] - y[j])
        if dx == 0 and dy == 0:
            txy += 1; tx += 1; ty += 1
        elif dx == 0:
            tx += 1
        elif dy == 0:
            ty += 1
        elif dx == dy:
            conc += 1
        else:
            disc += 1
    n0 = len(x) * (len(x) - 1) // 2
    den = np.sqrt((n0 - tx) * (n0 - ty))
    return (conc - disc) / den if den > 0 else np.nan, n0, tx, ty, txy, conc, disc


# self-check of the tau-b implementation on cases with known value
assert abs(kendall_tau_b([1, 2, 3, 4], [1, 2, 3, 4])[0] - 1) < 1e-12
assert abs(kendall_tau_b([1, 2, 3, 4], [4, 3, 2, 1])[0] + 1) < 1e-12
assert abs(kendall_tau_b([1, 1, 2, 3], [1, 2, 2, 3])[0] - 0.8) < 1e-12
assert (th.AEMET_MADRID_METRO_YELLOW_C, th.AEMET_MADRID_METRO_ORANGE_C,
        th.AEMET_MADRID_METRO_RED_C) == (36.0, 39.0, 42.0)

# ------------------------------------------------------------------ load + integrity
pc = pd.read_csv(PROCESSED / "pilot_classifications.csv")
p2 = pd.read_csv(PROCESSED / "phase2_asset_thermal_exposure.csv")
sh = pd.read_csv(PROCESSED / "shade_proxy_comparison.csv")
sol = pd.read_csv(PROCESSED / "phase2_1_solar_scenario_assets.csv")
for d in (pc, p2, sh, sol):
    d["hour"] = d["timestamp"].map(hour_of)
    d["k"] = d["asset_id"] + "@" + d["hour"]

print("INTEGRITY")
for name, d in (("pilot_classifications", pc), ("phase2_asset_thermal_exposure", p2),
                ("shade_proxy_comparison", sh)):
    assert len(d) == 81 and d.k.is_unique, name
    assert d.asset_id.nunique() == 27 and sorted(d.hour.unique()) == HOURS, name
assert set(pc.k) == set(p2.k) == set(sh.k)
pc, p2, sh = [d[d.indoor_outdoor == "outdoor"].sort_values(["hour", "asset_id"]).reset_index(drop=True)
              for d in (pc, p2, sh)]
assert len(pc) == 42 and (pc.k == p2.k).all() and (pc.k == sh.k).all()
assert pc.asset_id.nunique() == 14
obs = pc[["asset_id", "name", "hour", "k", "temp_c_barajas", "meteorological_hazard_state",
          "tree_count_50m", "exposure_state", "feasibility_state"]].copy()
obs = obs.merge(p2[["k", "morphology", "utci_mean_10m", "utci_centroid", "utci_p90_10m",
                    "feasibility_phase2_physical"]], on="k")
obs = obs.merge(sh[["k"] + list(PROXIES) + ["exposure_state_" + v for v in PROXIES.values()] +
                   ["feasibility_" + v for v in PROXIES.values()]], on="k")
assert not obs[["temp_c_barajas", "meteorological_hazard_state", "tree_count_50m", "exposure_state",
                "feasibility_state", "utci_mean_10m", "utci_centroid", "utci_p90_10m",
                "feasibility_phase2_physical"] + list(PROXIES)].isna().any().any()
obs["rule"] = [outdoor_rule(h, e)[0] for h, e in zip(obs.meteorological_hazard_state, obs.exposure_state)]
A0 = obs.feasibility_state.reset_index(drop=True)
B0 = obs.feasibility_phase2_physical.reset_index(drop=True)
assert (pd.Series([outdoor_rule(h, e)[1] for h, e in zip(obs.meteorological_hazard_state,
                                                         obs.exposure_state)]) == A0).all()
assert (obs.temp_c_barajas.map(th.meteorological_hazard_state) == obs.meteorological_hazard_state).all()
assert (obs.utci_mean_10m.map(utci_to_state) == B0).all()
assert (obs.feasibility_OSM == A0).all() and (obs.tree_count_50m == obs.OSM_tree_proxy).all()
for v in PROXIES.values():
    rec = [outdoor_rule(h, e)[1] for h, e in zip(obs.meteorological_hazard_state, obs["exposure_state_" + v])]
    assert (pd.Series(rec) == obs["feasibility_" + v].reset_index(drop=True)).all(), v
assert (obs.groupby("asset_id")[list(PROXIES)].nunique() == 1).all().all()  # proxies constant per asset
assert sol.groupby("scenario").k.apply(lambda s: s.is_unique and set(s) == set(obs.k)).all()
print("  keys unique, 14 assets x 3 hours = 42 outdoor rows, no missing values, tables aligned;")
print("  rule A and mapping B reproduce the stored classifications 42/42")

# cross-check with the locked table (read only)
lk = pd.read_csv(ROOT / "outputs" / "tables" / "proxy_vs_physical_comparison.csv")
lkv = {(r.metric, r.group): r.value for r in lk.itertuples()}
disagree0 = A0 != B0
assert lkv[("overall_reclassification_rate_pct", "ALL")] == round(100 * disagree0.mean(), 1) == 33.3
for h in HOURS:
    assert lkv[("reclassification_rate_by_timestamp_pct", h)] == round(
        100 * disagree0[obs.hour == h].mean(), 1)
print("  matches the locked outputs/tables/proxy_vs_physical_comparison.csv (33.3 %, by hour)")

# --------------------------------------------------------------------------- A: base
OUT.mkdir(parents=True, exist_ok=True)
ct = (obs.assign(A=A0, B=B0).groupby(["hour", "A", "B"]).size().rename("n").reset_index())
ct.to_csv(OUT / "exploratory_A_crosstab.csv", index=False)

dis = obs[disagree0.values].assign(A_class=A0[disagree0], B_class=B0[disagree0])
dis = dis[["hour", "asset_id", "name", "morphology", "meteorological_hazard_state", "tree_count_50m",
           "exposure_state", "rule", "A_class", "utci_mean_10m", "B_class"]].rename(
    columns={"meteorological_hazard_state": "hazard_A", "rule": "rule_A_id",
             "exposure_state": "exposure_A", "utci_mean_10m": "utci_B"})
dis.sort_values(["hour", "rule_A_id", "asset_id"]).to_csv(OUT / "exploratory_A_disagreements.csv", index=False)
rule_tab = (obs.assign(dis=disagree0.values).groupby(["hour", "rule", "feasibility_state"])
            .agg(n=("k", "size"), disagreements=("dis", "sum")).reset_index())
print("\nA. disagreements by hour and rule:\n", rule_tab.to_string(index=False))

# ------------------------------------------------------------------ A: one-at-a-time
hz_idx = obs.hour.values


def summary(family, variant, system, detail, A, B):
    A, B = pd.Series(A).reset_index(drop=True), pd.Series(B).reset_index(drop=True)
    r = dict(family=family, variant=variant, system_varied=system, rows=len(obs), detail=detail)
    for tag, cur, base in (("A_changes", A, A0), ("B_changes", B, B0), ("disagreements", None, None)):
        for h in HOURS:
            m = hz_idx == h
            r[f"{tag}_{h}"] = int(((cur[m] != base[m]).sum()) if cur is not None else (A[m] != B[m]).sum())
        r[f"{tag}_total"] = sum(r[f"{tag}_{h}"] for h in HOURS)
    dv = set(obs.k[(A != B).values])
    r["disagreements_shared_with_baseline"] = len(dv & set(obs.k[disagree0.values]))
    ch = (A != A0) | (B != B0)
    r["rows_changed"] = ";".join(obs.k[ch.values])
    return r


rows = [summary("baseline", "baseline (Barajas instantaneous Ta, OSM trees, UTCI 10 m mean)", "none",
                "reference", A0, B0)]

# --- temperature sources and temporal definition (system A only; B fixed)
b = pd.read_csv(RAW / "aemet_barajas_08221_hourly_202308.csv")
bs = pd.Series(b.temp_c.values, index=pd.to_datetime(b.date) + pd.to_timedelta(b.hour_utc, unit="h")
               + pd.Timedelta(hours=2))  # hour_utc is UTC; CEST = UTC+2
mu = pd.read_csv(RAW / "madrid_meteo_municipal" / "meteo_municipal_202308.csv", sep=";")
mu = mu[(mu.ESTACION == 8) & (mu.MAGNITUD == 83)]  # Escuelas Aguirre, air temperature
ea = {}
for r in mu.itertuples(index=False):
    for n in range(1, 25):
        v, flag = getattr(r, f"H{n:02d}"), getattr(r, f"V{n:02d}")
        if flag == "V":
            ea[pd.Timestamp(2023, 8, int(r.DIA)) + pd.Timedelta(hours=n)] = float(v)  # Hnn: hour ending nn
ea = pd.Series(ea).sort_index()
T = {h: STUDY_DAY + pd.Timedelta(hours=int(h[:2])) for h in HOURS}
for h in HOURS:  # the Ta stored in the classification is the Barajas instantaneous value
    assert abs(bs[T[h]] - obs.temp_c_barajas[obs.hour == h].iloc[0]) < 1e-9
hr = pd.Timedelta(hours=1)
ta_sources = {
    "Barajas mean of (T-1h, T)": {h: (bs[T[h]] + bs[T[h] - hr]) / 2 for h in HOURS},
    "Escuelas Aguirre H(T), hour-ending mean": {h: ea[T[h]] for h in HOURS},
    "Escuelas Aguirre interpolated to T from [H(T), H(T+1)]": {h: (ea[T[h]] + ea[T[h] + hr]) / 2 for h in HOURS},
}
for name, tv in ta_sources.items():
    A = [outdoor_rule(th.meteorological_hazard_state(tv[h]), e)[1] for h, e in zip(obs.hour, obs.exposure_state)]
    rows.append(summary("A: air-temperature source", name, "A",
                        "Ta 12/15/18 h = " + "/".join(f"{tv[h]:.2f}" for h in HOURS), A, B0))
dm_b = bs[(bs.index >= STUDY_DAY) & (bs.index < STUDY_DAY + pd.Timedelta(days=1))]
dm_e = [float(getattr(mu[mu.DIA == 21].iloc[0], f"H{n:02d}")) for n in range(1, 25)]
assert len(dm_b) == 24 and len(dm_e) == 24
for src, v in (("Barajas", dm_b.max()), ("Escuelas Aguirre", max(dm_e))):
    A = [outdoor_rule(th.meteorological_hazard_state(v), e)[1] for e in obs.exposure_state]
    rows.append(summary("A: temporal definition of the AEMET rule",
                        f"AEMET warning thresholds applied to the daily maximum ({src})", "A",
                        f"daily max = {v:.1f} C for all three hours (sensitivity to the definition of the "
                        "rule, not an hourly equivalent)", A, B0))
# --- shade proxies (system A only)
for v in ("Madrid", "TCD", "green"):
    rows.append(summary("A: shade/tree proxy", f"exposure grade from {v} proxy", "A",
                        "tercile grade as stored in shade_proxy_comparison.csv", obs["feasibility_" + v], B0))
# --- irradiance (system B only)
sbase = sol.drop_duplicates("k").set_index("k")
for sc in sorted(sol.scenario.unique()):
    u = obs.k.map(sol[sol.scenario == sc].set_index("k").utci_mean_10m)
    dl = u - obs.utci_mean_10m
    rows.append(summary("B: irradiance", sc, "B", f"dUTCI min/median/max = {dl.min():.1f}/{dl.median():.1f}/"
                        f"{dl.max():.1f} C (within B only)", A0, u.map(utci_to_state)))
# --- spatial support (system B only)
for lab, col in (("centroid", "utci_centroid"), ("p90 within 10 m", "utci_p90_10m")):
    dl = obs[col] - obs.utci_mean_10m
    rows.append(summary("B: spatial support", f"UTCI {lab} instead of 10 m mean", "B",
                        f"dUTCI min/median/max = {dl.min():.1f}/{dl.median():.1f}/{dl.max():.1f} C (within B only)",
                        A0, obs[col].map(utci_to_state)))
var = pd.DataFrame(rows)
var.to_csv(OUT / "exploratory_A_variants.csv", index=False)
print("\nA. variants (changes vs own baseline; disagreements with the other system's baseline):")
print(var[["variant", "A_changes_total", "B_changes_total", "disagreements_12:00", "disagreements_15:00",
           "disagreements_18:00", "disagreements_total", "disagreements_shared_with_baseline"]].to_string(index=False))
dis_sets = [set(obs.k[(obs["feasibility_" + v].reset_index(drop=True) != B0).values]) for v in PROXIES.values()]
common_proxies = len(set.intersection(*dis_sets))
print("disagreement observations common to the four proxies:", common_proxies)
print("coverage: every variant above covers 42/42 rows; canopy-geometry variants cover only A23, A24, A27 "
      "(3 of 14 assets) and are excluded")

# --- temperature-source alignment (Escuelas Aguirre hour convention; documented, not assumed)
ea_s = ea.copy()
cand = {"Barajas local hour n": bs, "Barajas local hour n-1": bs.shift(freq=hr),
        "Barajas local hour n+1": bs.shift(freq=-hr), "Barajas mean of (n-1, n)": (bs + bs.shift(freq=hr)) / 2}
al = []
for scope, sel in (("all hours", lambda ix: np.ones(len(ix), bool)),
                   ("daytime 10-20 h", lambda ix: (ix.hour >= 10) & (ix.hour <= 20))):
    for name, s in cand.items():
        j = pd.concat([ea_s.rename("e"), s.rename("b")], axis=1, sort=True).dropna()
        j = j[sel(j.index)]
        d = j.e - j.b
        al.append(dict(scope=scope, EA_Hnn_compared_with=name, n=len(j), rmse_c=round(float(np.sqrt((d ** 2).mean())), 2),
                       bias_c=round(float(d.mean()), 2), sd_c=round(float(d.std()), 2)))
pd.DataFrame(al).to_csv(OUT / "exploratory_A_temperature_alignment.csv", index=False)
print("\nEA hour-convention check:\n", pd.DataFrame(al).to_string(index=False))

# --- physiological UTCI categories (distribution + sensitivity only; never crossed with A classes)
ucols = {"baseline (10 m mean)": obs.utci_mean_10m}
for sc in sorted(sol.scenario.unique()):
    ucols["irradiance " + sc] = obs.k.map(sol[sol.scenario == sc].set_index("k").utci_mean_10m)
ucols["centroid"], ucols["p90 within 10 m"] = obs.utci_centroid, obs.utci_p90_10m
base_cat = obs.utci_mean_10m.map(stress_category)
pr = []
for name, u in ucols.items():
    cat = u.map(stress_category)
    for h in HOURS:
        m = obs.hour == h
        pr.append(dict(variant=name, hour=h, **{c: int((cat[m] == c).sum()) for c in CATS},
                       category_changes_vs_baseline=int((cat[m] != base_cat[m]).sum())))
prd = pd.DataFrame(pr)
prd.to_csv(OUT / "exploratory_A_physiological_categories.csv", index=False)
print("\nPhysiological categories (standard UTCI):\n", prd.to_string(index=False))

# ------------------------------------------------------------------------------- B
res = []
for ucol, ulab in (("utci_mean_10m", "mean_10m (primary)"), ("utci_centroid", "centroid (secondary)"),
                   ("utci_p90_10m", "p90_10m (secondary)")):
    for h in HOURS:
        s = obs[obs.hour == h]
        for pcol, plab in PROXIES.items():
            t, n0, tx, ty, txy, c, dd = kendall_tau_b(s[pcol], s[ucol])
            res.append(dict(utci_variant=ulab, hour=h, proxy=plab, n_assets=len(s),
                            distinct_proxy_values=s[pcol].nunique(), distinct_utci_values=s[ucol].nunique(),
                            pairs=n0, pairs_tied_proxy=tx, pairs_tied_utci=ty, pairs_tied_both=txy,
                            concordant=c, discordant=dd, tau_b=round(t, 3)))
kd = pd.DataFrame(res)
prim = kd[kd.utci_variant.str.startswith("mean")].set_index(["hour", "proxy"]).tau_b
kd["sign_differs_from_primary"] = [
    bool(np.sign(r.tau_b) != np.sign(prim[(r.hour, r.proxy)])) if not r.utci_variant.startswith("mean") else False
    for r in kd.itertuples()]
kd.to_csv(OUT / "exploratory_B_kendall.csv", index=False)
print("\nB. Kendall tau-b:\n", kd.to_string(index=False))

# --------------------------------------------------------------- headline assertions
def tab(name):
    return var[var.variant.str.startswith(name)].iloc[0]


assert disagree0.sum() == 14 and [int(disagree0[obs.hour == h].sum()) for h in HOURS] == [9, 0, 5]
assert set(zip(dis.hour, dis.rule_A_id)) == {("12:00", 7), ("18:00", 2)}
assert (var.iloc[1:4].A_changes_total == 0).all() and (var.iloc[1:4].disagreements_total == 14).all()
x = tab("AEMET warning thresholds applied to the daily maximum (Barajas)")
assert x.A_changes_total == 19 and x.disagreements_total == 15 and \
    [x[f"disagreements_{h}"] for h in HOURS] == [5, 5, 5]
for v in ("Madrid", "TCD", "green"):
    y = tab(f"exposure grade from {v}")
    assert y.A_changes_total == 8 and y.disagreements_total == 14 and y.disagreements_shared_with_baseline == 10
assert common_proxies == 6
for sc, (cb, dt) in {"REAL_SATELLITE": (1, 15), "SENS_A_minus10pct": (0, 14), "SENS_B_minus20pct": (0, 14)}.items():
    y = tab(sc); assert (y.B_changes_total, y.disagreements_total) == (cb, dt), sc
assert (tab("UTCI centroid").B_changes_total, tab("UTCI centroid").disagreements_total) == (1, 15)
assert (tab("UTCI p90").B_changes_total, tab("UTCI p90").disagreements_total) == (2, 16)
assert var[var.variant == "REAL_SATELLITE"].rows_changed.iloc[0] == "A24@18:00"
chg = prd.groupby("variant").category_changes_vs_baseline.sum()
assert chg.to_dict() == {"baseline (10 m mean)": 0, "centroid": 5, "irradiance REAL_SATELLITE": 1,
                         "irradiance SENS_A_minus10pct": 0, "irradiance SENS_B_minus20pct": 1,
                         "p90 within 10 m": 8}
EXPECTED_TAU = {  # (utci variant prefix, hour, proxy) -> tau_b
    **{("mean", h, p): v for (h, p), v in {
        ("12:00", "OSM"): -0.271, ("12:00", "Madrid"): -0.023, ("12:00", "TCD"): -0.309, ("12:00", "green"): -0.139,
        ("15:00", "OSM"): -0.204, ("15:00", "Madrid"): 0.058, ("15:00", "TCD"): -0.326, ("15:00", "green"): -0.115,
        ("18:00", "OSM"): -0.356, ("18:00", "Madrid"): -0.126, ("18:00", "TCD"): -0.456, ("18:00", "green"): -0.266}.items()},
    **{("centroid", h, p): v for (h, p), v in {
        ("12:00", "OSM"): -0.543, ("12:00", "Madrid"): -0.234, ("12:00", "TCD"): -0.136, ("12:00", "green"): -0.168,
        ("15:00", "OSM"): 0.072, ("15:00", "Madrid"): 0.468, ("15:00", "TCD"): 0.317, ("15:00", "green"): 0.387,
        ("18:00", "OSM"): -0.241, ("18:00", "Madrid"): 0.164, ("18:00", "TCD"): 0.113, ("18:00", "green"): 0.206}.items()},
    **{("p90", h, p): v for (h, p), v in {
        ("12:00", "OSM"): -0.232, ("12:00", "Madrid"): 0.071, ("12:00", "TCD"): -0.320, ("12:00", "green"): -0.365,
        ("15:00", "OSM"): -0.293, ("15:00", "Madrid"): -0.024, ("15:00", "TCD"): -0.229, ("15:00", "green"): -0.156,
        ("18:00", "OSM"): -0.344, ("18:00", "Madrid"): 0.012, ("18:00", "TCD"): -0.242, ("18:00", "green"): -0.171}.items()}}
for r in kd.itertuples():
    assert abs(r.tau_b - EXPECTED_TAU[(r.utci_variant.split(" ")[0].split("_")[0], r.hour, r.proxy)]) < 1e-9, r
assert (kd.n_assets == 14).all() and (kd.pairs == 91).all()
assert int((prim < 0).sum()) == 11
assert int(kd[kd.utci_variant.str.startswith("centroid")].sign_differs_from_primary.sum()) == 6
print("\nAll integrity checks and headline values passed. Tables written to", OUT.relative_to(ROOT))
