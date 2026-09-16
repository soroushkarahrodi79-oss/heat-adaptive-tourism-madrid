"""GATE 3B — build perturbation geometries (DSM/CDSM/DEM @ 2 m domain grid) for the FROZEN
E-P2 (canopy) and E-P4 (building) dimensions. Baseline (E-P2a/E-P4a) = the Gate-3A geometry.
Reuses the Gate-3A Catastro building_mask + nSH (re-read MDS/MDT windowed). No thermal input.

E-P2a canopy baseline : nSH within (OSM green + tree buffers + TCD>=30%) mask, outside footprints  [= Gate-3A cdsm]
E-P2b canopy PNOA     : PNOA veg nDSM 2008-2015 (domain WCS clip), resampled to 2 m
E-P2c canopy tree-inv : nSH within municipal tree-buffer mask only, outside footprints
E-P2d canopy TCD      : nSH within Copernicus TCD>=30% mask only, outside footprints
E-P4a building baseline: DEM + nSH within Catastro footprints  [= Gate-3A dsm]
E-P4b building PNOA    : DEM + PNOA building nDSM 2008-2015 (domain WCS clip), resampled to 2 m
"""
import os, json, hashlib, pathlib
_rd=pathlib.Path(__import__("rasterio").__file__).parent
os.environ["PROJ_DATA"]=str(_rd/"proj_data"); os.environ["PROJ_LIB"]=str(_rd/"proj_data"); os.environ["GDAL_DATA"]=str(_rd/"gdal_data")
os.environ["GDAL_DISABLE_READDIR_ON_OPEN"]="EMPTY_DIR"; os.environ["CPL_VSIL_CURL_ALLOWED_EXTENSIONS"]=".tif"
import numpy as np, rasterio
from rasterio.transform import from_origin
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
from rasterio.warp import reproject, transform as rio_transform
from rasterio.crs import CRS

ROOT=pathlib.Path(__file__).resolve().parents[1]
G3A=ROOT/"data/interim/pedestrian-heat/gate3a"
OUT=ROOT/"data/interim/pedestrian-heat/gate3b"; OUT.mkdir(parents=True,exist_ok=True)
C=CRS.from_epsg(25830)
RES=2.0; X0=440996.0; Y1=4474830.0; NX=370; NY=1081; X1=X0+NX*RES; Y0=Y1-NY*RES
transform=from_origin(X0,Y1,RES,RES)

def read_domain(path,res_resamp=Resampling.bilinear):
    with rasterio.open(path) as s:
        dst=np.full((NY,NX),np.nan,dtype="float64")
        reproject(source=rasterio.band(s,1),destination=dst,src_transform=s.transform,
                  src_crs=s.crs or C,dst_transform=transform,dst_crs=C,resampling=res_resamp,
                  src_nodata=s.nodata,dst_nodata=np.nan)
        return dst

# --- reuse Gate-3A layers ---
dem=read_domain(G3A/"dem_2m.tif")
building_mask=read_domain(G3A/"building_mask.tif",Resampling.nearest)>0.5
veg_mask_base=read_domain(G3A/"veg_mask.tif",Resampling.nearest)>0.5
cdsm_base=read_domain(G3A/"cdsm_2m.tif")

# --- re-read MDS/MDT windowed for nSH ---
MDS="https://servpub.madrid.es/fsdescargas/IDEAM_WBGEOPORTAL/ELEVACIONES/2023/MDS/COG/{}.tif"
MDT="https://servpub.madrid.es/fsdescargas/IDEAM_WBGEOPORTAL/ELEVACIONES/2023/MDT/COG/{}.tif"
tiles=[f"{e}-{n}" for e in (440,441) for n in (4473,4474,4475)]
def mosaic(t):
    dest=np.full((NY,NX),np.nan)
    for tl in tiles:
        with rasterio.open("/vsicurl/"+t.format(tl)) as ds:
            b=ds.bounds; ix0=max(X0,b.left);ix1=min(X1,b.right);iy0=max(Y0,b.bottom);iy1=min(Y1,b.top)
            if ix0>=ix1 or iy0>=iy1: continue
            w=from_bounds(ix0,iy0,ix1,iy1,ds.transform); ow=int(round((ix1-ix0)/RES));oh=int(round((iy1-iy0)/RES))
            a=ds.read(1,window=w,out_shape=(oh,ow),resampling=Resampling.bilinear).astype("float64")
            if ds.nodata is not None: a[a==ds.nodata]=np.nan
            c0=int(round((ix0-X0)/RES));r0=int(round((Y1-iy1)/RES)); dest[r0:r0+oh,c0:c0+ow]=a
    return dest
print("reading MDS/MDT windowed for nSH...")
nsh=np.clip(mosaic(MDS)-mosaic(MDT),0,None); nsh[np.isnan(nsh)]=0.0

# --- tree-only and TCD-only masks ---
# tree buffers: rebuild from arbolado (same as 3A, 4 m)
from rasterio.features import rasterize
from shapely.geometry import box
tree_polys=[]
for fn in ("arbolado_parques_historicos_live.geojson","arbolado_street_greenzone_live.geojson"):
    j=json.loads((ROOT/"data/raw/madrid_arbolado"/fn).read_text(encoding="utf-8"))
    lons=[];lats=[]
    for f in j.get("features",[]):
        g=f.get("geometry") or {}
        if g.get("type")=="Point": lons.append(g["coordinates"][0]);lats.append(g["coordinates"][1])
    xs,ys=rio_transform(CRS.from_epsg(4326),C,lons,lats)
    for x,y in zip(xs,ys):
        if X0-10<=x<=X1+10 and Y0-10<=y<=Y1+10: tree_polys.append(box(x-4,y-4,x+4,y+4))
tree_mask=rasterize([(p,1) for p in tree_polys],out_shape=(NY,NX),transform=transform,fill=0,dtype="uint8").astype(bool)
tcd=read_domain(ROOT/"data/raw/copernicus_tcd/tcd_2018_study_area.tif")
tcd_mask=np.nan_to_num(tcd)>=30

# --- PNOA domain nDSM (2.5 m) resampled to 2 m ---
pnoa_veg=np.clip(np.nan_to_num(read_domain(ROOT/"data/raw/pnoa_lidar_gate3a/veg_ndsm_domain.tif")),0,None)
pnoa_bld=np.clip(np.nan_to_num(read_domain(ROOT/"data/raw/pnoa_lidar_gate3a/building_ndsm_domain.tif")),0,None)

prof=dict(driver="GTiff",dtype="float32",count=1,width=NX,height=NY,crs=C,transform=transform,nodata=None,compress="deflate")
def write(name,arr):
    p=OUT/name
    with rasterio.open(p,"w",**prof) as d: d.write(arr.astype("float32"),1)
    return hashlib.sha256(p.read_bytes()).hexdigest()

H={}
# canopy variants (CDSM = height above ground)
H["cdsm_EP2b_pnoa.tif"]=write("cdsm_EP2b_pnoa.tif",pnoa_veg)
H["cdsm_EP2c_treeinv.tif"]=write("cdsm_EP2c_treeinv.tif",np.where(tree_mask&(~building_mask),nsh,0.0))
H["cdsm_EP2d_tcd.tif"]=write("cdsm_EP2d_tcd.tif",np.where(tcd_mask&(~building_mask),nsh,0.0))
# building variant (DSM = DEM + building height)
H["dsm_EP4b_pnoa.tif"]=write("dsm_EP4b_pnoa.tif",np.nan_to_num(dem,nan=float(np.nanmin(dem)))+pnoa_bld)
# report coverage
for nm,arr in [("EP2b_pnoa_veg",pnoa_veg),("EP2c_treeinv",np.where(tree_mask&(~building_mask),nsh,0.0)),
               ("EP2d_tcd",np.where(tcd_mask&(~building_mask),nsh,0.0)),("EP4b_pnoa_bld",pnoa_bld)]:
    print(f"  {nm}: cover(>0.5m) {(arr>0.5).mean()*100:.1f}%  max {arr.max():.1f}  mean(>0) {arr[arr>0].mean() if (arr>0).any() else 0:.1f}")
(OUT/"gate3b_geom_hashes.json").write_text(json.dumps(H,indent=1),encoding="utf-8")
print("PERTURBATION GEOMETRY BUILD COMPLETE:",list(H))
