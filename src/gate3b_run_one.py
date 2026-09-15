"""GATE 3B (CORRECTED per AMENDMENT_003) — STATEFUL SOLWEIG for ONE perturbation config.
Single calculate() over the continuous 72-step 15-min sequence 00:00->17:45 local (thermal
state carried); only the 8 frozen decision fields are extracted. One config per process
(memory isolation). Usage: python src/gate3b_run_one.py <config>
config: EP1b_forcing_ea EP2b_canopy_pnoa EP2c_canopy_treeinv EP2d_canopy_tcd EP4b_building_pnoa
"""
import os, sys, csv, json, shutil, pathlib, traceback
_rd=pathlib.Path(__import__("rasterio").__file__).parent
os.environ["PROJ_DATA"]=str(_rd/"proj_data"); os.environ["PROJ_LIB"]=str(_rd/"proj_data"); os.environ["GDAL_DATA"]=str(_rd/"gdal_data")
import numpy as np, pandas as pd, solweig, pvlib, rasterio
from datetime import datetime
from rasterio.warp import transform as rio_transform

ROOT=pathlib.Path(__file__).resolve().parents[1]
G3A=ROOT/"data/interim/pedestrian-heat/gate3a"; G3B=ROOT/"data/interim/pedestrian-heat/gate3b"
UTC_OFFSET=2; ALT=650.0; DATE="2023-08-24"
DECISION=["1400","1415","1430","1445","1700","1715","1730","1745"]
with rasterio.open(G3A/"dem_2m.tif") as ds:
    cx=(ds.bounds.left+ds.bounds.right)/2; cy=(ds.bounds.bottom+ds.bounds.top)/2
    lon,lat=rio_transform(ds.crs,rasterio.crs.CRS.from_epsg(4326),[cx],[cy]); LON,LAT=lon[0],lat[0]

# full-day Barajas hourly (frozen file)
barj={}
for r in csv.DictReader(open(ROOT/"data/raw/aemet_barajas_08221_hourly_202308.csv")):
    if r["date"]==DATE and r["hour_utc"].isdigit():
        barj[int(r["hour_utc"])]=(float(r["temp_c"]),float(r["rhum_pct"]),float(r["wspd_kmh"]),float(r["pres_hpa"]))
def interp_utc(uh,i):
    lo=int(np.floor(uh))%24; hi=int(np.ceil(uh))%24; f=uh-np.floor(uh)
    a=barj.get(lo,barj[min(barj)]); b=barj.get(hi,a); return a[i]+(b[i]-a[i])*f

# E-P1b EA delta: measured EA-minus-Barajas at target hours (14:00 +0.1/+3 ; 17:00 -0.1/+3),
# linearly interpolated by local hour, flat outside [14,17]. Applied to the whole stateful seq.
def ea_delta(hh):
    h=min(17.0,max(14.0,hh)); f=(h-14.0)/3.0
    dTa=0.1+(-0.1-0.1)*f; dRH=3.0
    return dTa,dRH

CONF={  # (dsm, cdsm, dem, ea_adjust)
 "EP1b_forcing_ea":   (G3A/"dsm_2m.tif", G3A/"cdsm_2m.tif", G3A/"dem_2m.tif", True),
 "EP2b_canopy_pnoa":  (G3A/"dsm_2m.tif", G3B/"cdsm_EP2b_pnoa.tif", G3A/"dem_2m.tif", False),
 "EP2c_canopy_treeinv":(G3A/"dsm_2m.tif", G3B/"cdsm_EP2c_treeinv.tif", G3A/"dem_2m.tif", False),
 "EP2d_canopy_tcd":   (G3A/"dsm_2m.tif", G3B/"cdsm_EP2d_tcd.tif", G3A/"dem_2m.tif", False),
 "EP4b_building_pnoa":(G3B/"dsm_EP4b_pnoa.tif", G3A/"cdsm_2m.tif", G3A/"dem_2m.tif", False),
}
name=sys.argv[1]; dsm,cdsm,dem,ea=CONF[name]

# continuous 72-step forcing 00:00->17:45
steps=[]; t=0
while t<=17*60+45: steps.append((t//60,t%60)); t+=15
rows=[]
for hh,mm in steps:
    uh=hh+mm/60-UTC_OFFSET
    ta=interp_utc(uh,0); rh=interp_utc(uh,1)
    if ea:
        dTa,dRH=ea_delta(hh+mm/60); ta+=dTa; rh+=dRH
    rows.append({"local":f"{hh:02d}:{mm:02d}","label":f"{hh:02d}{mm:02d}",
                 "ta":round(ta,2),"rh":round(min(100,max(1,rh)),1),"ws":round(interp_utc(uh,2)/3.6,2),"pres":round(interp_utc(uh,3),1)})
fdf=pd.DataFrame(rows)
times=pd.DatetimeIndex([pd.Timestamp(f"{DATE} {r.local}:00",tz="Europe/Madrid") for r in fdf.itertuples()])
fdf["ghi"]=np.round(pvlib.location.Location(LAT,LON,tz="Europe/Madrid",altitude=ALT).get_clearsky(times,model="ineichen")["ghi"].values,1)

outdir=G3B/f"solweig_{name}"; outdir.mkdir(parents=True,exist_ok=True)
cache=G3B/f"cache_{name}"; cache.mkdir(parents=True,exist_ok=True)
full=G3B/f"full_{name}"; full.mkdir(parents=True,exist_ok=True)
surface=solweig.SurfaceData.prepare(dsm=str(dsm),cdsm=str(cdsm),dem=str(dem),working_dir=str(cache),dsm_relative=False,cdsm_relative=True)
loc=solweig.Location.from_surface(surface,utc_offset=UTC_OFFSET,altitude=ALT)
wl=[solweig.Weather(datetime=datetime(2023,8,24,int(r.local[:2]),int(r.local[3:5])),ta=float(r.ta),rh=float(r.rh),
     global_rad=float(r.ghi),ws=float(r.ws),pressure=float(r.pres)) for r in fdf.itertuples()]
try:
    solweig.calculate(surface=surface,weather=wl,location=loc,output_dir=str(full),outputs=["utci"])
except Exception as e:
    tb=traceback.format_exc()
    if isinstance(e,MemoryError) or "Unable to allocate" in tb or "not enough memory" in tb.lower():
        print(f"RESOURCE_BLOCKED {name}: {e}"); sys.exit(3)
    raise
n=0
for lb in DECISION:
    src=full/"utci"/f"utci_20230824_{lb}.tif"
    if src.exists(): shutil.copy(src,outdir/f"utci_{lb}.tif"); n+=1
shutil.rmtree(cache,ignore_errors=True); shutil.rmtree(full,ignore_errors=True)
print(f"DONE {name}: stateful 72-step; {n}/8 decision fields")
