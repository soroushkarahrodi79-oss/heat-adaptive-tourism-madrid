"""GATE 3A (3A.3/3A.4) — BASELINE-ONLY time-resolved SOLWEIG run.
Departures 14:00 & 17:00 Europe/Madrid; Delta t = 15 min fields per the frozen Gate-2
temporal method (GATE2_METRIC_SPEC.md 0.1). 8 timestamps total. Forcing = Barajas 08221
hourly (2023-08-24) linearly interpolated to each timestamp; clear-sky GHI via pvlib
Ineichen. Geometry = data/interim/pedestrian-heat/gate3a/{dem,dsm,cdsm}_2m.tif.
No perturbations. No path optimisation. Outputs per-timestamp Tmrt & UTCI GeoTIFFs.
"""
import os, json, hashlib, pathlib
_rd=pathlib.Path(__import__("rasterio").__file__).parent
os.environ["PROJ_DATA"]=str(_rd/"proj_data"); os.environ["PROJ_LIB"]=str(_rd/"proj_data")
os.environ["GDAL_DATA"]=str(_rd/"gdal_data")
import numpy as np, pandas as pd, solweig, pvlib
from datetime import datetime

ROOT=pathlib.Path(__file__).resolve().parents[1]
GEOM=ROOT/"data/interim/pedestrian-heat/gate3a"
OUT=ROOT/"data/interim/pedestrian-heat/gate3a/solweig"; OUT.mkdir(parents=True,exist_ok=True)
CACHE=ROOT/"data/interim/pedestrian-heat/gate3a/svf_cache"; CACHE.mkdir(parents=True,exist_ok=True)

UTC_OFFSET=2  # CEST 2023-08-24
DATE="2023-08-24"
# domain-centre lat/lon for solar geometry
import rasterio
with rasterio.open(GEOM/"dem_2m.tif") as ds:
    cx=(ds.bounds.left+ds.bounds.right)/2; cy=(ds.bounds.bottom+ds.bounds.top)/2
    from rasterio.warp import transform as rio_transform
    lon,lat=rio_transform(ds.crs,rasterio.crs.CRS.from_epsg(4326),[cx],[cy])
    LON=lon[0]; LAT=lat[0]; ALT=650.0
print(f"domain centre lat/lon = {LAT:.5f},{LON:.5f}")

# ---- Barajas hourly forcing for 2023-08-24 (UTC hour -> value) ----
baraj={12:(37.0,17,11.2,1011.0),13:(39.0,13,13.0,1016.0),14:(40.0,13,6.0,1015.0),
       15:(40.0,12,6.0,1015.0),16:(40.0,11,14.8,1015.0),17:(40.0,12,11.2,1015.0)}
def interp(utc_h_float, idx):
    lo=int(np.floor(utc_h_float)); hi=int(np.ceil(utc_h_float))
    f=utc_h_float-lo
    if lo not in baraj: lo=min(baraj);
    if hi not in baraj: hi=lo
    a=baraj[lo][idx]; b=baraj[hi][idx]
    return a+(b-a)*f

# ---- timestamps: 15-min fields for each departure ----
departures=["14:00","17:00"]
steps=[0,15,30,45]
rows=[]
for dep in departures:
    dh,dm=map(int,dep.split(":"))
    for s in steps:
        tot=dh*60+dm+s
        hh=tot//60; mm=tot%60
        local=f"{hh:02d}:{mm:02d}"
        utc_h=hh+mm/60 - UTC_OFFSET
        rows.append({"departure":dep,"local_time":local,"utc_h":utc_h,
                     "ta_c":round(interp(utc_h,0),2),"rh_pct":round(interp(utc_h,1),1),
                     "ws_ms":round(interp(utc_h,2)/3.6,2),"pressure_hpa":round(interp(utc_h,3),1)})
fdf=pd.DataFrame(rows).drop_duplicates("local_time").reset_index(drop=True)
# clear-sky GHI per timestamp
times=pd.DatetimeIndex([pd.Timestamp(f"{DATE} {r.local_time}:00",tz="Europe/Madrid") for r in fdf.itertuples()])
site=pvlib.location.Location(LAT,LON,tz="Europe/Madrid",altitude=ALT)
cs=site.get_clearsky(times,model="ineichen"); solpos=site.get_solarposition(times)
fdf["ghi_wm2"]=cs["ghi"].values.round(1)
fdf["solar_elev_deg"]=solpos["apparent_elevation"].values.round(2)
fdf["solar_azimuth_deg"]=solpos["azimuth"].values.round(2)
print("\nForcing table (baseline, interpolated + pvlib clear-sky):")
print(fdf.to_string(index=False))
fdf.to_csv(GEOM/"gate3a_forcing.csv",index=False)

# ---- prepare surface (SVF/shadow) once ----
print("\nPreparing surface (SVF + shadow matrices)...")
surface=solweig.SurfaceData.prepare(dsm=str(GEOM/"dsm_2m.tif"),cdsm=str(GEOM/"cdsm_2m.tif"),
        dem=str(GEOM/"dem_2m.tif"),working_dir=str(CACHE),dsm_relative=False,cdsm_relative=True)
location=solweig.Location.from_surface(surface,utc_offset=UTC_OFFSET,altitude=ALT)
print("location:",location)

# ---- run per timestamp ----
import shutil
hashes={}
for r in fdf.itertuples():
    hh,mm=map(int,r.local_time.split(":"))
    weather=solweig.Weather(datetime=datetime(2023,8,24,hh,mm),ta=float(r.ta_c),rh=float(r.rh_pct),
             global_rad=float(r.ghi_wm2),ws=float(r.ws_ms),pressure=float(r.pressure_hpa))
    label=f"{hh:02d}{mm:02d}"
    od=CACHE/f"run_{label}"
    print(f"\n=== {r.local_time} (dep {r.departure}) ta={r.ta_c} rh={r.rh_pct} ghi={r.ghi_wm2} ws={r.ws_ms} elev={r.solar_elev_deg} ===")
    summary=solweig.calculate(surface=surface,weather=weather,location=location,
             output_dir=str(od),outputs=["tmrt","utci","shadow"])
    for var in ("tmrt","utci"):
        src=od/var/f"{var}_20230824_{label}.tif"
        dst=OUT/f"{var}_{label}.tif"
        if src.exists():
            shutil.copy(src,dst); hashes[f"{var}_{label}"]=hashlib.sha256(dst.read_bytes()).hexdigest()
            with rasterio.open(dst) as d:
                a=d.read(1); print(f"  {var}_{label}: min {np.nanmin(a):.1f} max {np.nanmax(a):.1f} mean {np.nanmean(a):.2f}")
        else:
            print(f"  MISSING {src}")
(GEOM/"gate3a_solweig_hashes.json").write_text(json.dumps(hashes,indent=2),encoding="utf-8")
print("\nSOLWEIG BASELINE RUN COMPLETE:",len(hashes),"rasters")
