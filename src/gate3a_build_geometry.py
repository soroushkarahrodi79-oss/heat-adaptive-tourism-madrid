"""GATE 3A (3A.2) — build SOLWEIG geometry for the OD1 model domain from the FROZEN
Gate-2 baseline architecture (with AMENDMENT_001: terrain = Madrid MDT 2023, same 2023
campaign as MDS 2023). Bounded to Route A + Route B + a 150 m shadow buffer; NOT
city-wide. No thermal input; no manual raster editing.

nSH = MDS 2023 - MDT 2023 (normalized surface height).
Building height = nSH within Catastro INSPIRE footprints.
Canopy height   = nSH within a vegetation mask (OSM green polygons + municipal tree
                  buffers + Copernicus TCD>=30%) AND outside building footprints.
Outputs (data/interim/pedestrian-heat/gate3a/): dem_2m.tif, dsm_2m.tif, cdsm_2m.tif.
"""
import os, io, json, math, hashlib, pathlib
# Point PROJ/GDAL at rasterio's own bundled data (the system PostGIS PROJ and pyproj's
# PROJ are both version-incompatible with rasterio's GDAL). Avoid pyproj entirely.
import rasterio as _r
_rd=pathlib.Path(_r.__file__).parent
os.environ["PROJ_DATA"]=str(_rd/"proj_data"); os.environ["PROJ_LIB"]=str(_rd/"proj_data")
os.environ["GDAL_DATA"]=str(_rd/"gdal_data")
os.environ["GDAL_DISABLE_READDIR_ON_OPEN"]="EMPTY_DIR"
os.environ["CPL_VSIL_CURL_ALLOWED_EXTENSIONS"]=".tif"
os.environ["GDAL_HTTP_MAX_RETRY"]="3"; os.environ["GDAL_HTTP_RETRY_DELAY"]="2"
import numpy as np, requests, rasterio
from rasterio.transform import from_origin
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
from rasterio.features import rasterize
from rasterio.crs import CRS
from rasterio.warp import reproject, transform as rio_transform
from shapely.geometry import box, Polygon

C4326=CRS.from_epsg(4326)
def to25830(lons,lats):
    xs,ys=rio_transform(C4326,CRS.from_epsg(25830),list(lons),list(lats)); return xs,ys
def to4326(xs,ys):
    lons,lats=rio_transform(CRS.from_epsg(25830),C4326,list(xs),list(ys)); return lons,lats

ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/"data/interim/pedestrian-heat/gate3a"; OUT.mkdir(parents=True,exist_ok=True)
C25830=CRS.from_epsg(25830)

# ---- domain (EPSG:25830) ----
RES=2.0; X0=440996.0; Y1=4474830.0; NX=370; NY=1081
X1=X0+NX*RES; Y0=Y1-NY*RES
transform=from_origin(X0,Y1,RES,RES)
domain=box(X0,Y0,X1,Y1)
print(f"domain 25830 x[{X0},{X1}] y[{Y0},{Y1}] {NX}x{NY}px @ {RES}m")

MDS="https://servpub.madrid.es/fsdescargas/IDEAM_WBGEOPORTAL/ELEVACIONES/2023/MDS/COG/{}.tif"
MDT="https://servpub.madrid.es/fsdescargas/IDEAM_WBGEOPORTAL/ELEVACIONES/2023/MDT/COG/{}.tif"
tiles=[f"{e}-{n}" for e in (440,441) for n in (4473,4474,4475)]

def mosaic(url_tmpl):
    dest=np.full((NY,NX),np.nan,dtype="float64"); hashes={}
    for t in tiles:
        url="/vsicurl/"+url_tmpl.format(t)
        with rasterio.open(url) as ds:
            tb=ds.bounds
            ix0=max(X0,tb.left); ix1=min(X1,tb.right)
            iy0=max(Y0,tb.bottom); iy1=min(Y1,tb.top)
            if ix0>=ix1 or iy0>=iy1: continue
            win=from_bounds(ix0,iy0,ix1,iy1,ds.transform)
            ow=int(round((ix1-ix0)/RES)); oh=int(round((iy1-iy0)/RES))
            if ow<=0 or oh<=0: continue
            arr=ds.read(1,window=win,out_shape=(oh,ow),resampling=Resampling.bilinear).astype("float64")
            nod=ds.nodata
            if nod is not None: arr[arr==nod]=np.nan
            col0=int(round((ix0-X0)/RES)); row0=int(round((Y1-iy1)/RES))
            dest[row0:row0+oh,col0:col0+ow]=arr
        hashes[t]=url_tmpl.format(t)
    return dest,hashes

print("reading MDS 2023 (windowed COG)..."); mds,mds_urls=mosaic(MDS)
print("reading MDT 2023 (windowed COG, AMENDMENT_001)..."); mdt,mdt_urls=mosaic(MDT)
print(f"  MDS nan%={np.isnan(mds).mean()*100:.1f} range {np.nanmin(mds):.1f}..{np.nanmax(mds):.1f}")
print(f"  MDT nan%={np.isnan(mdt).mean()*100:.1f} range {np.nanmin(mdt):.1f}..{np.nanmax(mdt):.1f}")
nsh=np.clip(mds-mdt,0,None); nsh[np.isnan(mds)|np.isnan(mdt)]=0.0
print(f"  nSH range {np.nanmin(nsh):.1f}..{np.nanmax(nsh):.1f} mean {np.nanmean(nsh):.2f}")

# ---- Catastro building footprints (WFS, EPSG:25830) ----
def catastro_footprints():
    """Catastro WFS caps bbox area, so tile the domain into ~200 m sub-bboxes and merge."""
    import re
    url="https://ovc.catastro.meh.es/INSPIRE/wfsBU.aspx"
    polys=[]; h=hashlib.sha256(); step=200.0; nsub=0
    yy=Y0
    while yy<Y1:
        xx=X0
        while xx<X1:
            sx1=min(xx+step,X1); sy1=min(yy+step,Y1)
            (lo0,lo1),(la0,la1)=to4326([xx,sx1],[yy,sy1])
            params={"service":"WFS","version":"2.0.0","request":"GetFeature",
                    "typenames":"bu:Building","srsname":"urn:ogc:def:crs:EPSG::4326",
                    "bbox":f"{la0},{lo0},{la1},{lo1},urn:ogc:def:crs:EPSG::4326"}
            try:
                r=requests.get(url,params=params,timeout=60); h.update(r.content); nsub+=1
                for m in re.finditer(r'<gml:posList[^>]*>([^<]+)</gml:posList>',r.text):
                    nums=[float(x) for x in m.group(1).split()]
                    lats=[nums[i] for i in range(0,len(nums),2)]; lons=[nums[i+1] for i in range(0,len(nums),2)]
                    if len(lons)<4: continue
                    xs,ys=to25830(lons,lats)
                    polys.append(Polygon(list(zip(xs,ys))))
            except Exception as e:
                print("   catastro subtile err",e)
            xx+=step
        yy+=step
    print(f"   catastro sub-requests: {nsub}")
    return polys, h.hexdigest(), len(polys)

print("fetching Catastro footprints...")
foot_polys,foot_hash,nfoot=catastro_footprints()
foot_in=[p for p in foot_polys if p.intersects(domain)]
print(f"  Catastro polygons: {nfoot} fetched, {len(foot_in)} intersect domain")
building_mask=rasterize([(p,1) for p in foot_in],out_shape=(NY,NX),transform=transform,
                        fill=0,dtype="uint8",all_touched=False).astype(bool) if foot_in else np.zeros((NY,NX),bool)
print(f"  building footprint coverage: {building_mask.mean()*100:.1f}% of domain")

# ---- vegetation mask ----
veg=np.zeros((NY,NX),bool)
# OSM green polygons (in-repo)
for fn in ("osm_all_green_polygons_raw.json","osm_green_polygons_raw.json"):
    p=ROOT/"data/raw/osm"/fn
    if not p.exists(): continue
    j=json.loads(p.read_text(encoding="utf-8"))
    gpolys=[]
    for el in j.get("elements",[]):
        g=el.get("geometry")
        if g and el.get("type")=="way" and len(g)>=4:
            xs,ys=to25830([pt["lon"] for pt in g],[pt["lat"] for pt in g])
            try:
                poly=Polygon(list(zip(xs,ys)))
                if poly.is_valid and poly.area>0: gpolys.append(poly)
            except Exception: pass
    gpolys=[p for p in gpolys if p.intersects(domain)]
    if gpolys:
        m=rasterize([(p,1) for p in gpolys],out_shape=(NY,NX),transform=transform,fill=0,dtype="uint8").astype(bool)
        veg|=m
print(f"  veg after OSM green: {veg.mean()*100:.1f}%")
# municipal tree points buffered 4 m
tree_polys=[]
for fn in ("arbolado_parques_historicos_live.geojson","arbolado_street_greenzone_live.geojson"):
    j=json.loads((ROOT/"data/raw/madrid_arbolado"/fn).read_text(encoding="utf-8"))
    lons=[];lats=[]
    for f in j.get("features",[]):
        g=f.get("geometry") or {}
        if g.get("type")=="Point":
            lons.append(g["coordinates"][0]);lats.append(g["coordinates"][1])
    if not lons: continue
    xs,ys=to25830(lons,lats)
    for x,y in zip(xs,ys):
        if X0-10<=x<=X1+10 and Y0-10<=y<=Y1+10:
            tree_polys.append(box(x-4,y-4,x+4,y+4))
if tree_polys:
    m=rasterize([(p,1) for p in tree_polys],out_shape=(NY,NX),transform=transform,fill=0,dtype="uint8").astype(bool)
    veg|=m
print(f"  veg after tree buffers ({len(tree_polys)} trees): {veg.mean()*100:.1f}%")
# Copernicus TCD 2018 >=30%
tcdp=ROOT/"data/raw/copernicus_tcd/tcd_2018_study_area.tif"
if tcdp.exists():
    with rasterio.open(tcdp) as src:
        tcd=np.empty((NY,NX),dtype="float32")
        reproject(source=rasterio.band(src,1),destination=tcd,
                  src_transform=src.transform,src_crs=src.crs or C25830,
                  dst_transform=transform,dst_crs=C25830,resampling=Resampling.bilinear)
    veg|=(tcd>=30)
print(f"  veg after TCD>=30%: {veg.mean()*100:.1f}%")

# ---- classify nSH ----
building_h=np.where(building_mask,nsh,0.0)
canopy_h=np.where(veg & (~building_mask),nsh,0.0)
# unclassified tall nSH (not building, not veg) -> left as ground (documented QA item)
unclassified=(nsh>=2.0)&(~building_mask)&(~veg)
print(f"  building_h max {building_h.max():.1f} mean(>0) {building_h[building_h>0].mean() if (building_h>0).any() else 0:.1f}")
print(f"  canopy_h max {canopy_h.max():.1f} mean(>0) {canopy_h[canopy_h>0].mean() if (canopy_h>0).any() else 0:.1f}")
print(f"  unclassified tall(>=2m) pixels: {unclassified.sum()} ({unclassified.mean()*100:.2f}% of domain)")

dem=np.where(np.isnan(mdt),np.nanmin(mdt),mdt)  # bare-earth absolute
dsm=dem+building_h                              # ground+building absolute
cdsm=canopy_h                                   # canopy height above ground (relative)

prof=dict(driver="GTiff",dtype="float32",count=1,width=NX,height=NY,crs=C25830,
          transform=transform,nodata=None,compress="deflate")
hashes={}
for name,arr in [("dem_2m.tif",dem),("dsm_2m.tif",dsm),("cdsm_2m.tif",cdsm)]:
    p=OUT/name
    with rasterio.open(p,"w",**prof) as dst: dst.write(arr.astype("float32"),1)
    hashes[name]=hashlib.sha256(p.read_bytes()).hexdigest()
    print(f"wrote {name}: min {arr.min():.1f} max {arr.max():.1f} mean {arr.mean():.2f} sha {hashes[name][:12]}")
# also save masks for QA
with rasterio.open(OUT/"building_mask.tif","w",**{**prof,"dtype":"uint8"}) as dst: dst.write(building_mask.astype("uint8"),1)
with rasterio.open(OUT/"veg_mask.tif","w",**{**prof,"dtype":"uint8"}) as dst: dst.write(veg.astype("uint8"),1)

prov={"domain_epsg25830":{"x0":X0,"y0":Y0,"x1":X1,"y1":Y1,"res":RES,"nx":NX,"ny":NY,"buffer_m":150,
        "buffer_justification":"max ~50 m heritage-core building at ~20 deg late-afternoon (17:45) solar altitude -> ~140 m shadow"},
      "terrain":"Madrid MDT 2023 (AMENDMENT_001) COG windowed","surface":"Madrid MDS 2023 COG windowed",
      "mds_tiles":mds_urls,"mdt_tiles":mdt_urls,
      "catastro_footprints_wfs_sha256":foot_hash,"catastro_polys_in_domain":len(foot_in),
      "building_coverage_pct":round(float(building_mask.mean()*100),2),
      "veg_coverage_pct":round(float(veg.mean()*100),2),
      "unclassified_tall_pct":round(float(unclassified.mean()*100),3),
      "output_hashes":hashes,"resolution_m":RES,
      "resolution_justification":"2 m sidewalk-scale working grid; SVF-tractable over 370x1081 domain; fixed before any thermal output"}
(OUT/"geometry_provenance.json").write_text(json.dumps(prov,indent=2),encoding="utf-8")
print("\nGEOMETRY BUILD COMPLETE")
