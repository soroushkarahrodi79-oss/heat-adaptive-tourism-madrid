"""GATE 3A (3A.5/3A.6/3A.7) — CORRECTED sampling (audit fix, 2026-09-15).

FIX: true GLOBAL CHAINAGE sampling at fixed Delta s along the whole route (0,5,10,... m
measured continuously from the origin, final partial interval included), with an explicit
REPRESENTED LENGTH (dwell weight) per sample. M2 is length-weighted; M4 minutes come from
represented traversal duration; the old n=seg//DS per-vertex restart is removed.

Baseline speed = 1.1 m/s (frozen E-P6 tourist value; AMENDMENT_002 — the earlier 1.25 m/s
midpoint was not a frozen value). 1.4 m/s is computed as a speed-robustness QA check only
(not the E-P6 perturbation matrix). Uses the EXISTING Gate-3A thermal rasters unchanged.

Importable functions (route_length, point_at_chainage, chainage_samples, metrics) are used
by tests/pedestrian_heat/test_gate3a_sampling.py.
"""
import os, json, pathlib
_rd=pathlib.Path(__import__("rasterio").__file__).parent
os.environ["PROJ_DATA"]=str(_rd/"proj_data"); os.environ["PROJ_LIB"]=str(_rd/"proj_data")
os.environ["GDAL_DATA"]=str(_rd/"gdal_data")
import numpy as np, rasterio, csv
from math import hypot

DS=5.0                     # true global chainage step (m)
BASELINE_V=1.1             # frozen E-P6 tourist value (AMENDMENT_002)
QA_V=1.4                   # frozen E-P6 brisk value, speed-robustness QA only
BUF=10.0                   # locked-pilot PRIMARY_BUFFER_M
CATS=[("no_stress",9,26),("moderate",26,32),("strong",32,38),("very_strong",38,46),("extreme",46,99)]
DEP_LABELS={"14:00":["1400","1415","1430","1445"],"17:00":["1700","1715","1730","1745"]}
STEP_MIN=[0,15,30,45]

# ---------- geometry: true global chainage ----------
def cumdist(coords):
    c=[0.0]
    for i in range(1,len(coords)):
        c.append(c[-1]+hypot(coords[i][0]-coords[i-1][0],coords[i][1]-coords[i-1][1]))
    return c
def route_length(coords): return cumdist(coords)[-1]
def point_at_chainage(coords,c,s):
    if s<=0: return coords[0]
    if s>=c[-1]: return coords[-1]
    import bisect
    i=bisect.bisect_right(c,s)-1
    seg=c[i+1]-c[i]; f=0.0 if seg==0 else (s-c[i])/seg
    return (coords[i][0]+(coords[i+1][0]-coords[i][0])*f, coords[i][1]+(coords[i+1][1]-coords[i][1])*f)
def chainage_samples(coords,ds=DS):
    """Intervals [0,ds),[ds,2ds),...,[k*ds, L]; sample at each interval MIDPOINT; the
    represented length is the interval length (last partial included). Sum(rep_len)==L."""
    L=route_length(coords); c=cumdist(coords)
    out=[]; a=0.0
    while a<L-1e-9:
        b=min(a+ds,L); mid=(a+b)/2.0; rep=b-a
        x,y=point_at_chainage(coords,c,mid)
        out.append({"chainage":mid,"rep_len":rep,"x":x,"y":y})
        a=b
    return out,L

# ---------- weighted metric helpers ----------
def wmean(v,w): v=np.asarray(v,float); w=np.asarray(w,float); return float((v*w).sum()/w.sum())
def wpercentile(v,w,q):
    v=np.asarray(v,float); w=np.asarray(w,float); o=np.argsort(v); v=v[o]; w=w[o]
    cw=np.cumsum(w)-0.5*w; cw/=w.sum()
    return float(np.interp(q/100.0,cw,v))
def metrics(values,rep_len,v_ms):
    values=np.asarray(values,float); rep_len=np.asarray(rep_len,float)
    ok=~np.isnan(values); values=values[ok]; rep_len=rep_len[ok]
    L=float(rep_len.sum()); dur_min=L/v_ms/60.0
    m={"L_repr_m":round(L,2),"M1_trip_min":round(dur_min,3),"M1_exact":dur_min,"L_exact":L,
       "M2_timeweighted_mean_UTCI":round(wmean(values,rep_len),3),
       "M3_min":round(float(values.min()),2),"M3_p25":round(wpercentile(values,rep_len,25),2),
       "M3_median":round(wpercentile(values,rep_len,50),2),"M3_p75":round(wpercentile(values,rep_len,75),2),
       "M3_max":round(float(values.max()),2),
       "M3_IQR":round(wpercentile(values,rep_len,75)-wpercentile(values,rep_len,25),2),
       "M5_p95_descriptor":round(wpercentile(values,rep_len,95),2)}
    m4sum=0.0
    for cn,lo,hi in CATS:
        sel=(values>=lo)&(values<hi); mins=float(rep_len[sel].sum())/v_ms/60.0; m4sum+=mins
        m[f"M4_min_{cn}"]=round(mins,3); m[f"M4_prop_{cn}"]=round(float(rep_len[sel].sum())/L,4)
    m["M4_min_sum_exact"]=m4sum
    return m

# ---------- run against existing rasters ----------
if __name__=="__main__":
    ROOT=pathlib.Path(__file__).resolve().parents[1]
    GEOM=ROOT/"data/interim/pedestrian-heat/gate3a"; SW=GEOM/"solweig"
    def load(label,var):
        with rasterio.open(SW/f"{var}_{label}.tif") as s:
            a=s.read(1).astype("float64"); nod=s.nodata
            if nod is not None: a[a==nod]=np.nan
            return a,s.transform,s.width,s.height
    FI={}
    for dep,labs in DEP_LABELS.items():
        for lb in labs:
            FI[("utci",lb)]=load(lb,"utci"); FI[("tmrt",lb)]=load(lb,"tmrt")
    _,T0,W,H=FI[("utci","1400")]
    def rc(x,y): return int((y-T0.f)/T0.e), int((x-T0.c)/T0.a)
    def bmean(field,x,y,rad=BUF):
        r0,c0=rc(x,y); pr=int(rad/abs(T0.a))
        r1,r2=max(0,r0-pr),min(H,r0+pr+1); c1,c2=max(0,c0-pr),min(W,c0+pr+1)
        inside=(0<=r0<H and 0<=c0<W)
        if r1>=r2 or c1>=c2: return np.nan,inside
        sub=field[r1:r2,c1:c2]; yy,xx=np.ogrid[r1:r2,c1:c2]
        mask=((yy-r0)**2+(xx-c0)**2)<=pr**2; vals=sub[mask]; vals=vals[~np.isnan(vals)]
        return (float(vals.mean()) if vals.size else np.nan), inside
    def nearest15(tmin): return min(45,max(0,int(round(tmin/15.0)*15)))
    def sample(coords,dep,v):
        samp,L=chainage_samples(coords); s2l=dict(zip(STEP_MIN,DEP_LABELS[dep]))
        u=[];t=[];rep=[];inside_all=True;nanct=0
        for s in samp:
            tmin=(s["chainage"]/v)/60.0; lb=s2l[nearest15(tmin)]
            uu,ins=bmean(FI[("utci",lb)][0],s["x"],s["y"]); tt,_=bmean(FI[("tmrt",lb)][0],s["x"],s["y"])
            if not ins: inside_all=False
            if np.isnan(uu): nanct+=1
            u.append(uu);t.append(tt);rep.append(s["rep_len"])
        return np.array(u),np.array(t),np.array(rep),L,inside_all,nanct
    ROUTES={n:json.loads((ROOT/f"data/processed/pedestrian-heat/OD1_Route_{n}_epsg25830.geojson").read_text())["features"][0]["geometry"]["coordinates"] for n in "AB"}

    rows=[]; summary={}
    for v_ms,vtag in [(BASELINE_V,"baseline_1.1"),(QA_V,"qa_1.4")]:
        for dep in DEP_LABELS:
            res={}
            for n in "AB":
                u,t,rep,L,ins,nanct=sample(ROUTES[n],dep,v_ms)
                m=metrics(u,rep,v_ms)
                # invariants
                inv_len=abs(m["L_exact"]-route_length(ROUTES[n]))<1e-6
                inv_dur=abs(m["M4_min_sum_exact"]-m["M1_exact"])<1e-9 if nanct==0 else None
                m.update({"route":n,"departure":dep,"speed_ms":v_ms,"speed_tag":vtag,
                          "n_samples":len(u),"off_raster":(not ins),"nan_samples":nanct,
                          "tmrt_mean":round(float(np.nanmean(t)),2),
                          "inv_replen_eq_L":inv_len,"inv_M4sum_eq_M1":inv_dur})
                rows.append(m); res[n]=m
            summary[f"{vtag}|{dep}"]={"M2_A":res["A"]["M2_timeweighted_mean_UTCI"],
                "M2_B":res["B"]["M2_timeweighted_mean_UTCI"],
                "A_minus_B":round(res["A"]["M2_timeweighted_mean_UTCI"]-res["B"]["M2_timeweighted_mean_UTCI"],3),
                "M1_A":res["A"]["M1_trip_min"],"M1_B":res["B"]["M1_trip_min"],
                "vstrong+ext_min_A":round(res["A"]["M4_min_very_strong"]+res["A"]["M4_min_extreme"],2),
                "vstrong+ext_min_B":round(res["B"]["M4_min_very_strong"]+res["B"]["M4_min_extreme"],2)}
    cols=["route","departure","speed_ms","speed_tag","n_samples","L_repr_m","off_raster","nan_samples",
          "inv_replen_eq_L","inv_M4sum_eq_M1","M1_trip_min","M2_timeweighted_mean_UTCI",
          "M3_min","M3_p25","M3_median","M3_p75","M3_max","M3_IQR","M5_p95_descriptor","tmrt_mean"]+\
         [f"M4_min_{c[0]}" for c in CATS]+[f"M4_prop_{c[0]}" for c in CATS]
    outdir=ROOT/"docs/research/pedestrian-heat/gate3a"
    with open(outdir/"GATE3A_BASELINE_RESULTS.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
        for r in rows: w.writerow({k:r.get(k) for k in cols})
    print("=== CORRECTED summary (M2 length-weighted) ===")
    print(json.dumps(summary,indent=2))
    print("\ninvariants all pass:",all(r["inv_replen_eq_L"] and (r["inv_M4sum_eq_M1"] in (True,None)) for r in rows))
    (GEOM/"gate3a_corrected_summary.json").write_text(json.dumps({"summary":summary},indent=2),encoding="utf-8")
