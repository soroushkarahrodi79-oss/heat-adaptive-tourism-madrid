"""GATE 3B — run ONE perturbation config's SOLWEIG (8 timestamps), save UTCI tifs, exit.
Separate process per config so memory is released between configs. Usage:
  python src/gate3b_run_one.py <config>
config in: EP1b_forcing_ea EP2b_canopy_pnoa EP2c_canopy_treeinv EP2d_canopy_tcd EP4b_building_pnoa
"""
import os, sys, json, shutil, pathlib
_rd=pathlib.Path(__import__("rasterio").__file__).parent
os.environ["PROJ_DATA"]=str(_rd/"proj_data"); os.environ["PROJ_LIB"]=str(_rd/"proj_data"); os.environ["GDAL_DATA"]=str(_rd/"gdal_data")
import numpy as np, pandas as pd, solweig, pvlib, rasterio
from datetime import datetime
from rasterio.warp import transform as rio_transform

ROOT=pathlib.Path(__file__).resolve().parents[1]
G3A=ROOT/"data/interim/pedestrian-heat/gate3a"; G3B=ROOT/"data/interim/pedestrian-heat/gate3b"
UTC_OFFSET=2; ALT=650.0
DEP_LABELS={"14:00":["1400","1415","1430","1445"],"17:00":["1700","1715","1730","1745"]}
with rasterio.open(G3A/"dem_2m.tif") as ds:
    cx=(ds.bounds.left+ds.bounds.right)/2; cy=(ds.bounds.bottom+ds.bounds.top)/2
    lon,lat=rio_transform(ds.crs,rasterio.crs.CRS.from_epsg(4326),[cx],[cy]); LON,LAT=lon[0],lat[0]
baraj={12:(37.0,17,11.2,1011.0),13:(39.0,13,13.0,1016.0),14:(40.0,13,6.0,1015.0),
       15:(40.0,12,6.0,1015.0),16:(40.0,11,14.8,1015.0),17:(40.0,12,11.2,1015.0)}
EA_DELTA={"14:00":(+0.1,+3.0),"17:00":(-0.1,+3.0)}
def interp(uh,i):
    lo=int(np.floor(uh));hi=int(np.ceil(uh));f=uh-lo
    lo=lo if lo in baraj else min(baraj); hi=hi if hi in baraj else lo
    return baraj[lo][i]+(baraj[hi][i]-baraj[lo][i])*f
def forcing_table(ea):
    rows=[]
    for dep in DEP_LABELS:
        dh,dm=map(int,dep.split(":"))
        for s in [0,15,30,45]:
            tot=dh*60+dm+s;hh,mm=tot//60,tot%60;uh=hh+mm/60-UTC_OFFSET
            ta=interp(uh,0);rh=interp(uh,1)
            if ea: ta+=EA_DELTA[dep][0];rh+=EA_DELTA[dep][1]
            rows.append({"local":f"{hh:02d}:{mm:02d}","label":f"{hh:02d}{mm:02d}","ta":round(ta,2),
                         "rh":round(rh,1),"ws":round(interp(uh,2)/3.6,2),"pres":round(interp(uh,3),1)})
    df=pd.DataFrame(rows).drop_duplicates("label").reset_index(drop=True)
    times=pd.DatetimeIndex([pd.Timestamp(f"2023-08-24 {r.local}:00",tz="Europe/Madrid") for r in df.itertuples()])
    site=pvlib.location.Location(LAT,LON,tz="Europe/Madrid",altitude=ALT)
    df["ghi"]=site.get_clearsky(times,model="ineichen")["ghi"].values.round(1)
    return df

CONF={
 "EP1b_forcing_ea":   ("dsm_2m.tif","cdsm_2m.tif","dem_2m.tif",True,"g3a"),
 "EP2b_canopy_pnoa":  ("dsm_2m.tif","cdsm_EP2b_pnoa.tif","dem_2m.tif",False,"mix"),
 "EP2c_canopy_treeinv":("dsm_2m.tif","cdsm_EP2c_treeinv.tif","dem_2m.tif",False,"mix"),
 "EP2d_canopy_tcd":   ("dsm_2m.tif","cdsm_EP2d_tcd.tif","dem_2m.tif",False,"mix"),
 "EP4b_building_pnoa":("dsm_EP4b_pnoa.tif","cdsm_2m.tif","dem_2m.tif",False,"mix"),
}
def path(fn,where): return str((G3A if where=="g3a" else (G3B if fn.startswith(("cdsm_EP","dsm_EP")) else G3A))/fn)

name=sys.argv[1]; only=sys.argv[2] if len(sys.argv)>2 else None
dsm,cdsm,dem,ea,_=CONF[name]
outdir=G3B/f"solweig_{name}"; outdir.mkdir(parents=True,exist_ok=True)
cache=G3B/f"cache_{name}"; cache.mkdir(parents=True,exist_ok=True)
fdf=forcing_table(ea)
# prepare loads the on-disk SVF cache if present (low memory), else computes it once.
surface=solweig.SurfaceData.prepare(dsm=path(dsm,"mix"),cdsm=path(cdsm,"mix"),dem=path(dem,"mix"),
        working_dir=str(cache),dsm_relative=False,cdsm_relative=True)
if only=="prep":
    print(f"PREP DONE {name}"); sys.exit(0)
loc=solweig.Location.from_surface(surface,utc_offset=UTC_OFFSET,altitude=ALT)
rows=[r for r in fdf.itertuples() if (only is None or r.label==only)]
for r in rows:
    hh,mm=map(int,r.local.split(":"))
    w=solweig.Weather(datetime=datetime(2023,8,24,hh,mm),ta=float(r.ta),rh=float(r.rh),global_rad=float(r.ghi),ws=float(r.ws),pressure=float(r.pres))
    solweig.calculate(surface=surface,weather=w,location=loc,output_dir=str(cache/f"r_{r.label}"),outputs=["utci"])
    src=cache/f"r_{r.label}"/"utci"/f"utci_20230824_{r.label}.tif"
    shutil.copy(src,outdir/f"utci_{r.label}.tif")
    shutil.rmtree(cache/f"r_{r.label}",ignore_errors=True)
print(f"DONE {name} {only or 'ALL'}: {len(rows)} raster(s)")
