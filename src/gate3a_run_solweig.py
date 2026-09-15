"""GATE 3A (CORRECTED per AMENDMENT_003) — STATEFUL time-resolved SOLWEIG.

Fix: a single solweig.calculate(surface, weather=[...continuous 15-min list...]) call so
ThermalState (surface/wall heat storage) is carried across timesteps. Continuous sequence
00:00 -> 17:45 local (72 steps @ 15 min); pre-17:00 steps are model preconditioning/state
continuity, NOT decision observations. Forcing = frozen hourly Barajas (2023-08-24)
interpolated to 15 min; pvlib Ineichen clear-sky recomputed per actual timestamp. Only the 8
frozen decision fields (14:00/15/30/45, 17:00/15/30/45) are copied out for route metrics.
If RAM prevents the single stateful run -> exits with RESOURCE_BLOCKED (no per-timestamp fallback).
"""
import os, sys, csv, json, shutil, pathlib, traceback
_rd=pathlib.Path(__import__("rasterio").__file__).parent
os.environ["PROJ_DATA"]=str(_rd/"proj_data"); os.environ["PROJ_LIB"]=str(_rd/"proj_data"); os.environ["GDAL_DATA"]=str(_rd/"gdal_data")
import numpy as np, pandas as pd, solweig, pvlib, rasterio
from datetime import datetime
from rasterio.warp import transform as rio_transform

ROOT=pathlib.Path(__file__).resolve().parents[1]
GEOM=ROOT/"data/interim/pedestrian-heat/gate3a"
OUT=GEOM/"solweig"; OUT.mkdir(parents=True,exist_ok=True)
CACHE=GEOM/"svf_cache"; CACHE.mkdir(parents=True,exist_ok=True)
FULLDIR=GEOM/"solweig_stateful_full"; FULLDIR.mkdir(parents=True,exist_ok=True)
UTC_OFFSET=2; ALT=650.0; DATE="2023-08-24"
DECISION=["1400","1415","1430","1445","1700","1715","1730","1745"]

with rasterio.open(GEOM/"dem_2m.tif") as ds:
    cx=(ds.bounds.left+ds.bounds.right)/2; cy=(ds.bounds.bottom+ds.bounds.top)/2
    lon,lat=rio_transform(ds.crs,rasterio.crs.CRS.from_epsg(4326),[cx],[cy]); LON,LAT=lon[0],lat[0]

# ---- full-day Barajas hourly (2023-08-24) from frozen file ----
rows=list(csv.DictReader(open(ROOT/"data/raw/aemet_barajas_08221_hourly_202308.csv")))
barj={}
for r in rows:
    if r["date"]==DATE and r["hour_utc"].isdigit():
        barj[int(r["hour_utc"])]=(float(r["temp_c"]),float(r["rhum_pct"]),float(r["wspd_kmh"]),float(r["pres_hpa"]))
def interp_utc(uh,i):
    lo=int(np.floor(uh))%24; hi=int(np.ceil(uh))%24; f=uh-np.floor(uh)
    a=barj.get(lo); b=barj.get(hi)
    if a is None: a=barj[min(barj)]
    if b is None: b=a
    return a[i]+(b[i]-a[i])*f

# ---- continuous 15-min sequence 00:00 -> 17:45 local ----
steps=[]
t=0
while t<=17*60+45:
    hh,mm=t//60,t%60; steps.append((hh,mm)); t+=15
frows=[]
for hh,mm in steps:
    uh=hh+mm/60-UTC_OFFSET  # local->UTC
    frows.append({"local":f"{hh:02d}:{mm:02d}","label":f"{hh:02d}{mm:02d}",
                  "ta":round(interp_utc(uh,0),2),"rh":round(min(100,max(1,interp_utc(uh,1))),1),
                  "ws":round(interp_utc(uh,2)/3.6,2),"pres":round(interp_utc(uh,3),1)})
fdf=pd.DataFrame(frows)
times=pd.DatetimeIndex([pd.Timestamp(f"{DATE} {r.local}:00",tz="Europe/Madrid") for r in fdf.itertuples()])
site=pvlib.location.Location(LAT,LON,tz="Europe/Madrid",altitude=ALT)
cs=site.get_clearsky(times,model="ineichen"); solpos=site.get_solarposition(times)
fdf["ghi"]=np.round(cs["ghi"].values,1); fdf["solar_elev"]=np.round(solpos["apparent_elevation"].values,2)
fdf.to_csv(GEOM/"gate3a_forcing_stateful.csv",index=False)
print(f"continuous sequence: {len(fdf)} steps 00:00->17:45; decision labels: {DECISION}")

# ---- prepare surface once ----
surface=solweig.SurfaceData.prepare(dsm=str(GEOM/"dsm_2m.tif"),cdsm=str(GEOM/"cdsm_2m.tif"),
        dem=str(GEOM/"dem_2m.tif"),working_dir=str(CACHE),dsm_relative=False,cdsm_relative=True)
location=solweig.Location.from_surface(surface,utc_offset=UTC_OFFSET,altitude=ALT)

# ---- SINGLE stateful calculate() over the whole 15-min list ----
weather_list=[solweig.Weather(datetime=datetime(2023,8,24,int(r.local[:2]),int(r.local[3:5])),
              ta=float(r.ta),rh=float(r.rh),global_rad=float(r.ghi),ws=float(r.ws),pressure=float(r.pres))
              for r in fdf.itertuples()]
try:
    summary=solweig.calculate(surface=surface,weather=weather_list,location=location,
             output_dir=str(FULLDIR),outputs=["tmrt","utci"])
except (MemoryError,) as e:
    print("RESOURCE_BLOCKED: stateful single-call SOLWEIG ran out of memory:",e); sys.exit(3)
except Exception as e:
    tb=traceback.format_exc()
    if "MemoryError" in tb or "Unable to allocate" in tb or "not enough memory" in tb.lower():
        print("RESOURCE_BLOCKED: stateful single-call SOLWEIG memory failure\n",tb[-500:]); sys.exit(3)
    raise

# ---- copy out only the frozen decision fields ----
n_ok=0
for lb in DECISION:
    for var in ("tmrt","utci"):
        src=FULLDIR/var/f"{var}_20230824_{lb}.tif"
        if src.exists(): shutil.copy(src,OUT/f"{var}_{lb}.tif"); n_ok+= (var=="utci")
        else: print("  WARNING missing",src)
try:
    solweig.save_run_metadata(solweig.create_run_metadata(),str(GEOM/"gate3a_run_metadata.json"))
except Exception: pass
meta={"protocol":"AMENDMENT_003 stateful single-call","n_timesteps":len(fdf),
      "sequence":"00:00->17:45 local @15min","decision_labels":DECISION,
      "timestep_min":15,"utc_offset":UTC_OFFSET,"forcing":"Barajas 2023-08-24 hourly interp + pvlib clearsky"}
(GEOM/"gate3a_stateful_meta.json").write_text(json.dumps(meta,indent=1),encoding="utf-8")
print(f"STATEFUL RUN COMPLETE: {n_ok}/8 decision UTCI fields extracted")
