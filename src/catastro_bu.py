"""Hardened, FAIL-CLOSED Catastro INSPIRE BU Building acquisition (Gate-3A correction,
AMENDMENT-driven). Requests bu:Building (the WFS-advertised feature type; returned members
are bu-ext2d:Building) directly in EPSG:25830. Structural GML parse (exterior/interior rings,
multipart Surface/PolygonPatch), dedup by gml:id, per-subtile provenance + hashes. Any HTTP
error, OGC ExceptionReport, or unparseable payload raises -> caller must abort.
"""
import hashlib, math
import xml.etree.ElementTree as ET
import requests
from shapely.geometry import Polygon, MultiPolygon

GML="http://www.opengis.net/gml/3.2"
BU_EXT="http://inspire.jrc.ec.europa.eu/schemas/bu-ext2d/2.0"
OWS_EXC="ExceptionReport"
WFS_URL="https://ovc.catastro.meh.es/INSPIRE/wfsBU.aspx"

class CatastroError(RuntimeError): pass

def _rings_from_poslist(text, axis_en=True):
    v=[float(x) for x in text.split()]
    pts=[(v[i],v[i+1]) if axis_en else (v[i+1],v[i]) for i in range(0,len(v),2)]
    return pts

def _polys_from_building(bld, axis_en=True):
    """Return list of shapely Polygons (one per PolygonPatch, with holes)."""
    polys=[]
    for patch in bld.iter(f"{{{GML}}}PolygonPatch"):
        ext=patch.find(f"{{{GML}}}exterior")
        if ext is None: continue
        er=ext.find(f".//{{{GML}}}posList")
        if er is None or not er.text: continue
        shell=_rings_from_poslist(er.text, axis_en)
        holes=[]
        for inter in patch.findall(f"{{{GML}}}interior"):
            ir=inter.find(f".//{{{GML}}}posList")
            if ir is not None and ir.text:
                holes.append(_rings_from_poslist(ir.text, axis_en))
        if len(shell)>=4:
            try:
                p=Polygon(shell,holes)
                if p.is_valid or p.buffer(0).is_valid:
                    polys.append(p if p.is_valid else p.buffer(0))
            except Exception:
                pass
    return polys

def _detect_axis_en(root):
    """EPSG:25830 axis order in this service: check a posList first pair — Easting ~4-5e5,
    Northing ~4.4e6. Return True if (E,N)."""
    pl=root.find(f".//{{{GML}}}posList")
    if pl is None or not pl.text: return True
    a,b=[float(x) for x in pl.text.split()[:2]]
    # Northing for Madrid ~4.47e6; Easting ~4.4e5
    return a<1e6  # if first value ~4.4e5 it's Easting-first

def fetch_footprints(x0,y0,x1,y1,step=200.0,timeout=60,session=None):
    """Tile [x0,y0,x1,y1] (EPSG:25830) into `step` subtiles; every subtile MUST succeed.
    Returns (list[shapely geom], provenance dict). Fail-closed."""
    s=session or requests.Session()
    prov={"feature_type":"bu:Building (returned bu-ext2d:Building)","srsname":"EPSG:25830",
          "wfs_url":WFS_URL,"step_m":step,"subtiles":[]}
    by_id={}; axis_en=None; nsub=0
    ny=int(math.ceil((y1-y0)/step)); nx=int(math.ceil((x1-x0)/step))
    for iy in range(ny):
        for ix in range(nx):
            sx0=x0+ix*step; sy0=y0+iy*step; sx1=min(sx0+step,x1); sy1=min(sy0+step,y1)
            bbox=f"{sx0},{sy0},{sx1},{sy1},urn:ogc:def:crs:EPSG::25830"
            params={"service":"WFS","version":"2.0.0","request":"GetFeature","typenames":"bu:Building",
                    "srsname":"urn:ogc:def:crs:EPSG::25830","bbox":bbox}
            resp=s.get(WFS_URL,params=params,timeout=timeout)
            nsub+=1
            if resp.status_code!=200:
                raise CatastroError(f"HTTP {resp.status_code} on subtile {bbox}")
            h=hashlib.sha256(resp.content).hexdigest()
            txt=resp.text
            if OWS_EXC in txt or "<ows:Exception" in txt or "ExceptionText" in txt:
                raise CatastroError(f"OGC ExceptionReport on subtile {bbox}: {txt[:200]}")
            try:
                root=ET.fromstring(resp.content)
            except ET.ParseError as e:
                raise CatastroError(f"GML parse error on subtile {bbox}: {e}")
            if not root.tag.endswith("FeatureCollection"):
                raise CatastroError(f"Unexpected root {root.tag} on subtile {bbox}")
            blds=list(root.iter(f"{{{BU_EXT}}}Building"))
            if axis_en is None and blds:
                axis_en=_detect_axis_en(root)
            n_here=0
            for b in blds:
                gid=b.get(f"{{{GML}}}id") or b.get("id") or f"anon_{len(by_id)}"
                if gid in by_id: continue  # dedup across tiles (deterministic: first occurrence)
                polys=_polys_from_building(b, axis_en if axis_en is not None else True)
                if polys:
                    by_id[gid]=polys[0] if len(polys)==1 else MultiPolygon([p for p in polys if p.geom_type=="Polygon"] or None)
                    n_here+=1
            prov["subtiles"].append({"bbox":[sx0,sy0,sx1,sy1],"http":resp.status_code,
                                     "sha256":h,"n_building_members":len(blds),"n_kept":n_here})
    prov["n_subtiles"]=nsub; prov["n_unique_buildings"]=len(by_id); prov["axis_easting_first"]=bool(axis_en)
    return list(by_id.values()), prov

if __name__=="__main__":
    import json
    geoms,prov=fetch_footprints(441100,4473700,441500,4474100,step=200.0)
    print("unique buildings:",len(geoms),"axis_EN:",prov["axis_easting_first"])
    print("subtiles:",prov["n_subtiles"],"members per tile:",[t["n_building_members"] for t in prov["subtiles"]])
    b=geoms[0]; print("sample geom type:",b.geom_type,"bounds:",[round(c) for c in b.bounds])
    # sanity: bounds should be within the requested box (E ~441xxx, N ~4473xxx-4474xxx)
    xs=[g.centroid.x for g in geoms]; ys=[g.centroid.y for g in geoms]
    print("centroid X range:",round(min(xs)),round(max(xs)),"| Y range:",round(min(ys)),round(max(ys)))
