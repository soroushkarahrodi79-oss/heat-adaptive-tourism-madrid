"""
Phase 2.1 Audit 1: build the four solar-forcing scenarios for the robustness
audit. The Phase 2 BASELINE clear-sky forcing is NOT modified - it is
re-loaded from data/raw/phase2_met_forcing.csv (locked, historical) and
reproduced here unchanged; all other scenarios are new, separate rows.

Scenarios:
  BASELINE - Phase 2's original pvlib Ineichen clear-sky estimate (unchanged)
  REAL     - real, satellite-derived shortwave radiation for Madrid,
             2023-08-21, from Open-Meteo's historical archive API
             (source: EUMETSAT CM SAF SARAH3, a geostationary-satellite
             radiation retrieval product for Europe - NOT a station
             pyranometer measurement, but a genuine observational product,
             not a clear-sky model estimate). This is compared directly
             against BASELINE, per the task's "prefer real data" instruction.
  SENS_A   - BASELINE GHI/DNI/DHI x 0.90 (-10%), a synthetic UNCERTAINTY
             SCENARIO, not an observation
  SENS_B   - BASELINE GHI/DNI/DHI x 0.80 (-20%), a synthetic UNCERTAINTY
             SCENARIO, not an observation

Ta/RH/wind/pressure are held IDENTICAL to Phase 2 in every scenario - only
radiation varies, per the task's "do not change other model inputs between
runs" instruction.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

TIMESTAMPS = [("12:00", "10"), ("15:00", "13"), ("18:00", "16")]  # (local, hour_utc) - unchanged from Phase 2


def build():
    baseline = pd.read_csv(RAW / "phase2_met_forcing.csv")

    with open(RAW / "openmeteo_radiation" / "madrid_2023-08-21_radiation.json", "r", encoding="utf-8") as f:
        om = json.load(f)
    om_times = om["hourly"]["time"]
    om_ghi = dict(zip(om_times, om["hourly"]["shortwave_radiation"]))
    om_dni = dict(zip(om_times, om["hourly"]["direct_radiation"]))  # Open-Meteo "direct_radiation" = horizontal-plane direct beam
    om_dhi = dict(zip(om_times, om["hourly"]["diffuse_radiation"]))
    om_dni_normal = dict(zip(om_times, om["hourly"]["direct_normal_irradiance"]))
    om_cloud = dict(zip(om_times, om["hourly"]["cloud_cover"]))

    rows = []
    for _, r in baseline.iterrows():
        local_time = r["local_time"]
        key = f"2023-08-21T{local_time}"
        base_ghi = r["ghi_wm2"]

        rows.append({"scenario": "BASELINE", "local_time": local_time, "ta_c": r["ta_c"], "rh_pct": r["rh_pct"],
                      "ws_ms": r["ws_ms"], "pressure_hpa": r["pressure_hpa"],
                      "ghi_wm2": r["ghi_wm2"], "dni_wm2": r["dni_wm2"], "dhi_wm2": r["dhi_wm2"],
                      "source_note": "pvlib Ineichen clear-sky model (Phase 2 original, unchanged)"})

        rows.append({"scenario": "REAL_SATELLITE", "local_time": local_time, "ta_c": r["ta_c"], "rh_pct": r["rh_pct"],
                      "ws_ms": r["ws_ms"], "pressure_hpa": r["pressure_hpa"],
                      "ghi_wm2": om_ghi[key], "dni_wm2": om_dni_normal[key], "dhi_wm2": om_dhi[key],
                      "source_note": f"Open-Meteo historical archive API, EUMETSAT CM SAF SARAH3 satellite radiation "
                                     f"retrieval, real cloud_cover={om_cloud[key]}% at this hour"})

        rows.append({"scenario": "SENS_A_minus10pct", "local_time": local_time, "ta_c": r["ta_c"], "rh_pct": r["rh_pct"],
                      "ws_ms": r["ws_ms"], "pressure_hpa": r["pressure_hpa"],
                      "ghi_wm2": round(base_ghi * 0.90, 1), "dni_wm2": round(r["dni_wm2"] * 0.90, 1),
                      "dhi_wm2": round(r["dhi_wm2"] * 0.90, 1),
                      "source_note": "UNCERTAINTY SCENARIO (not an observation): baseline x 0.90"})

        rows.append({"scenario": "SENS_B_minus20pct", "local_time": local_time, "ta_c": r["ta_c"], "rh_pct": r["rh_pct"],
                      "ws_ms": r["ws_ms"], "pressure_hpa": r["pressure_hpa"],
                      "ghi_wm2": round(base_ghi * 0.80, 1), "dni_wm2": round(r["dni_wm2"] * 0.80, 1),
                      "dhi_wm2": round(r["dhi_wm2"] * 0.80, 1),
                      "source_note": "UNCERTAINTY SCENARIO (not an observation): baseline x 0.80"})

    out = pd.DataFrame(rows)
    out_path = RAW / "phase2_1_solar_scenarios.csv"
    out.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Wrote {out_path}")
    print(out[["scenario", "local_time", "ghi_wm2", "dni_wm2", "dhi_wm2"]].to_string(index=False))

    # Direct comparison table: BASELINE vs REAL_SATELLITE
    print("\n=== BASELINE (clear-sky) vs REAL_SATELLITE GHI delta ===")
    for local_time, _ in TIMESTAMPS:
        b = out[(out.scenario == "BASELINE") & (out.local_time == local_time)]["ghi_wm2"].iloc[0]
        s = out[(out.scenario == "REAL_SATELLITE") & (out.local_time == local_time)]["ghi_wm2"].iloc[0]
        pct = 100 * (s - b) / b
        print(f"  {local_time}: baseline={b:.1f} real={s:.1f} delta={s-b:+.1f} W/m2 ({pct:+.1f}%)")

    return out


if __name__ == "__main__":
    build()
