"""
Phase 2 meteorological forcing for SOLWEIG.

Real observed inputs (Madrid/Barajas, AEMET indicativo 3129 / WMO 08221,
data/raw/episode_aug2023_barajas_raw.csv, same station and file already used
and documented throughout Phase 1/1.1): air temperature, relative humidity
(derived from dewpoint), wind speed, pressure, for the three real hourly
readings on 2023-08-21 matching the project's canonical timestamps.

ESTIMATED input: global horizontal irradiance (GHI). Barajas'
hourly archive (Meteostat-relayed AEMET/NOAA feed) does NOT include a
pyranometer/radiation column - see data/raw/README.md. SOLWEIG's Weather
class requires global_rad as a direct argument. Rather than leave it
unphysical or invent a number, GHI is estimated with pvlib's Ineichen
clear-sky model (real solar geometry for the true date/time/location, real
bundled Linke-turbidity climatology - NOT a fabricated value), justified by
the REAL, confirmed weather condition code at Barajas for all three target
hours: coco=1 ("clear") in the same archive - see verification below. This
is standard practice in urban-climate modelling when a station lacks a
pyranometer and is explicitly documented as ESTIMATED, not measured,
throughout every downstream output.

Documented limitation (Phase 1.1 Audit 1 lineage): Barajas is ~9 km NE of the
study area; the same spatial-representativeness caveat applies to this
forcing as to every prior use of this station in this project.
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

# Real study-area centroid (WGS84), used for solar geometry - matches
# data/processed/study_area.geojson.
LAT, LON = 40.4125, -3.68675
ALTITUDE_M = 650  # approx real mean elevation, from the DEM built in this phase

EPISODE_DATE = "2023-08-21"
TIMESTAMPS = [("12:00", "10"), ("15:00", "13"), ("18:00", "16")]  # (local, hour_utc)


def load_observed():
    df = pd.read_csv(RAW / "episode_aug2023_barajas_raw.csv", dtype={"hour_utc": str})
    df = df[df["date"] == EPISODE_DATE]
    rows = []
    for local_time, utc_hour in TIMESTAMPS:
        r = df[df["hour_utc"] == utc_hour.zfill(2)].iloc[0]
        ta = float(r["temp_c"])
        dewpoint = float(r["dwpt_c"])
        # Magnus formula RH from T/Td - standard meteorological relation,
        # cross-checked against the archive's own rhum_pct column below.
        import math
        es = lambda t: 6.112 * math.exp((17.62 * t) / (243.12 + t))
        rh_calc = 100 * es(dewpoint) / es(ta)
        rows.append({
            "local_time": local_time, "hour_utc": utc_hour,
            "ta_c": ta, "rh_pct": float(r["rhum_pct"]), "rh_pct_recomputed": round(rh_calc, 1),
            "ws_ms": round(float(r["wspd_kmh"]) / 3.6, 2),
            "pressure_hpa": float(r["pres_hpa"]),
            "coco": int(r["coco"]),
        })
    return pd.DataFrame(rows)


def add_clearsky_ghi(obs_df):
    import pvlib
    times = pd.DatetimeIndex([
        pd.Timestamp(f"{EPISODE_DATE} {h.zfill(2)}:00:00", tz="UTC")
        for h in obs_df["hour_utc"]
    ])
    site = pvlib.location.Location(LAT, LON, tz="UTC", altitude=ALTITUDE_M)
    cs = site.get_clearsky(times, model="ineichen")  # real Linke-turbidity climatology
    solpos = site.get_solarposition(times)
    obs_df = obs_df.copy()
    obs_df["ghi_wm2"] = cs["ghi"].values.round(1)
    obs_df["dni_wm2"] = cs["dni"].values.round(1)
    obs_df["dhi_wm2"] = cs["dhi"].values.round(1)
    obs_df["solar_zenith_deg"] = solpos["apparent_zenith"].values.round(1)
    obs_df["solar_elevation_deg"] = solpos["apparent_elevation"].values.round(1)
    return obs_df


def build():
    obs = load_observed()
    print("Real observed inputs (Barajas, 2023-08-21):")
    print(obs[["local_time", "ta_c", "rh_pct", "ws_ms", "pressure_hpa", "coco"]].to_string(index=False))
    assert (obs["coco"] == 1).all(), "Expected clear-sky (coco=1) at all 3 hours - re-check before using clear-sky GHI model"

    full = add_clearsky_ghi(obs)
    print("\nWith ESTIMATED clear-sky irradiance (pvlib Ineichen model, real solar geometry):")
    print(full[["local_time", "ghi_wm2", "dni_wm2", "dhi_wm2", "solar_elevation_deg"]].to_string(index=False))

    out_path = RAW / "phase2_met_forcing.csv"
    full.to_csv(out_path, index=False, encoding="utf-8")
    print(f"\nWrote {out_path}")
    return full


if __name__ == "__main__":
    build()
