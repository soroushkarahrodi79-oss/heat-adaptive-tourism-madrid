"""GATE 3A (3A.5/3A.6/3A.7) — QA the fields, sample the frozen routes at time-resolved
traversal times, compute the FROZEN Gate-2 metrics (intensity vs duration separated),
and run temporal-discretization QA. No path change; baseline only.
"""
import os, json, pathlib
_rd=pathlib.Path(__import__("rasterio").__file__).parent
os.environ["PROJ_DATA"]=str(_rd/"proj_data"); os.environ["PROJ_LIB"]=str(_rd/"proj_data")
os.environ["GDAL_DATA"]=str(_rd/"gdal_data")
import numpy as np, rasterio, csv
from math import hypot

ROOT=pathlib.Path(__file__).resolve().parents[1]
GEOM=ROOT/"data/interim/pedestrian-heat/gate3a"; SW=GEOM/"solweig"
DS=5.0; V=1.25; BUF=10.0  # Delta s=5m; baseline speed 1.25 m/s; locked-pilot 10 m buffer-mean
DEPARTURES={"14:00":["1400","1415","1430","1445"],"17:00":["1700","1715","1730","1745"]}
STEP_MIN=[0,15,30,45]
CATS=[("no_stress",9,26),("moderate",26,32),("strong",32,38),("very_strong",38,46),("extreme",46,99)]

def load_field(label,var):
    with rasterio.open(SW/f"{var}_{label}.tif") as s:
        a=s.read(1).astype("float64"); nod=s.nodata
        if nod is not None: a[a==nod]=np.nan
        return a, s.transform, s.width, s.height, s.bounds
# preload all UTCI + Tmrt fields
FI={}
for dep,labels in DEPARTURES.items():
    for lb in labels:
        FI[("utci",lb)]=load_field(lb,"utci"); FI[("tmrt",lb)]=load_field(lb,"tmrt")
_,T0,W,H,BND=FI[("utci","1400")]
def rc(x,y):
    col=int((x-T0.c)/T0.a); row=int((y-T0.f)/T0.e); return row,col

def buffer_mean(field,x,y,rad=BUF):
    r0,c0=rc(x,y); pr=int(rad/abs(T0.a))
    r1,r2=max(0,r0-pr),min(H,r0+pr+1); c1,c2=max(0,c0-pr),min(W,c0+pr+1)
    if r1>=r2 or c1>=c2: return np.nan,False
    sub=field[r1:r2,c1:c2]
    yy,xx=np.ogrid[r1:r2,c1:c2]
    mask=((yy-r0)**2+(xx-c0)**2)<=pr**2
    vals=sub[mask]; vals=vals[~np.isnan(vals)]
    inside=(0<=r0<H and 0<=c0<W)
    return (float(vals.mean()) if vals.size else np.nan), inside

def densify(coords):
    pts=[]; cum=[0.0]
    for i in range(len(coords)-1):
        (x1,y1),(x2,y2)=coords[i],coords[i+1]
        seg=hypot(x2-x1,y2-y1); n=max(1,int(seg//DS))
        for k in range(n):
            f=k/n; pts.append((x1+(x2-x1)*f, y1+(y2-y1)*f))
        cum.append(cum[-1]+seg)
    pts.append(coords[-1])
    # cumulative distance per densified point
    d=[0.0]
    for i in range(1,len(pts)):
        d.append(d[-1]+hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]))
    return pts,d

def nearest15(tmin): return min(45,int(round(tmin/15.0)*15))

def sample_route(name,coords,dep):
    pts,dist=densify(coords)
    labels=DEPARTURES[dep]; step_to_label=dict(zip(STEP_MIN,labels))
    utci=[]; tmrt=[]; off=[]; inside_all=True; nan_ct=0
    for (x,y),dd in zip(pts,dist):
        tmin=(dd/V)/60.0; step=nearest15(tmin); lb=step_to_label[step]
        u,ins=buffer_mean(FI[("utci",lb)][0],x,y)
        t,_=buffer_mean(FI[("tmrt",lb)][0],x,y)
        if not ins: inside_all=False
        if np.isnan(u): nan_ct+=1
        utci.append(u); tmrt.append(t); off.append(step)
    utci=np.array(utci); return pts,dist,utci,np.array(tmrt),off,inside_all,nan_ct

ROUTES={}
for name in "AB":
    gj=json.loads((ROOT/f"data/processed/pedestrian-heat/OD1_Route_{name}_epsg25830.geojson").read_text())
    ROUTES[name]=gj["features"][0]["geometry"]["coordinates"]

def metrics(utci,L):
    u=utci[~np.isnan(utci)]
    dur_min=L/V/60.0
    dwell=DS/V/60.0  # min per sample
    m={"M1_trip_min":round(dur_min,2),
       "M2_timeweighted_mean_UTCI":round(float(u.mean()),2),
       "M3_min":round(float(u.min()),2),"M3_p25":round(float(np.percentile(u,25)),2),
       "M3_median":round(float(np.median(u)),2),"M3_p75":round(float(np.percentile(u,75)),2),
       "M3_max":round(float(u.max()),2),"M3_IQR":round(float(np.percentile(u,75)-np.percentile(u,25)),2),
       "M5_p95_descriptor":round(float(np.percentile(u,95)),2)}
    for cn,lo,hi in CATS:
        cnt=int(((u>=lo)&(u<hi)).sum()); m[f"M4_min_{cn}"]=round(cnt*dwell,1)
        m[f"M4_prop_{cn}"]=round(cnt/len(u),3)
    return m

rows=[]; qa={}
for dep in DEPARTURES:
    res={}
    for name in "AB":
        pts,dist,utci,tmrt,off,ins,nanct=sample_route(name,ROUTES[name],dep)
        L=dist[-1]
        m=metrics(utci,L); m.update({"route":name,"departure":dep,"n_samples":len(utci),
              "L_m":round(L,1),"speed_ms":V,"buffer_m":BUF,"off_raster":(not ins),"nan_samples":nanct,
              "tmrt_mean":round(float(np.nanmean(tmrt)),2)})
        rows.append(m); res[name]=(utci,m)
    # intensity vs duration comparison
    dA,dB=res["A"][1],res["B"][1]
    qa[dep]={"M2_A":dA["M2_timeweighted_mean_UTCI"],"M2_B":dB["M2_timeweighted_mean_UTCI"],
             "M2_diff_A_minus_B":round(dA["M2_timeweighted_mean_UTCI"]-dB["M2_timeweighted_mean_UTCI"],2),
             "M1_A":dA["M1_trip_min"],"M1_B":dB["M1_trip_min"],
             "verystrong+extreme_min_A":round(dA["M4_min_very_strong"]+dA["M4_min_extreme"],1),
             "verystrong+extreme_min_B":round(dB["M4_min_very_strong"]+dB["M4_min_extreme"],1)}

# ---- temporal-discretization QA (+/-7.5 min): resample using the OTHER bracketing field ----
def sample_alt(name,coords,dep,shift):
    pts,dist=densify(coords); labels=DEPARTURES[dep]; step_to_label=dict(zip(STEP_MIN,labels))
    vals=[]
    for (x,y),dd in zip(pts,dist):
        tmin=(dd/V)/60.0
        step=min(45,max(0,int(round((tmin+shift)/15.0)*15)))
        u,_=buffer_mean(FI[("utci",step_to_label[step])][0],x,y); vals.append(u)
    v=np.array(vals); v=v[~np.isnan(v)]; return float(v.mean())
tempqa={}
for dep in DEPARTURES:
    row={}
    for sh,tag in [(-7.5,"minus7.5"),(0,"nearest"),(7.5,"plus7.5")]:
        mA=sample_alt("A",ROUTES["A"],dep,sh); mB=sample_alt("B",ROUTES["B"],dep,sh)
        row[tag]={"M2_A":round(mA,3),"M2_B":round(mB,3),"A_minus_B":round(mA-mB,3)}
    tempqa[dep]=row

# write results
outdir=ROOT/"docs/research/pedestrian-heat/gate3a"; outdir.mkdir(parents=True,exist_ok=True)
cols=["route","departure","n_samples","L_m","speed_ms","buffer_m","off_raster","nan_samples",
      "M1_trip_min","M2_timeweighted_mean_UTCI","M3_min","M3_p25","M3_median","M3_p75","M3_max","M3_IQR","M5_p95_descriptor","tmrt_mean"]+\
     [f"M4_min_{c[0]}" for c in CATS]+[f"M4_prop_{c[0]}" for c in CATS]
with open(outdir/"GATE3A_BASELINE_RESULTS.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
    for r in rows: w.writerow({k:r.get(k) for k in cols})
print("=== INTENSITY vs DURATION summary ===")
print(json.dumps(qa,indent=2))
print("\n=== TEMPORAL-DISCRETIZATION QA (+/-7.5 min) ===")
print(json.dumps(tempqa,indent=2))
(GEOM/"gate3a_metrics_qa.json").write_text(json.dumps({"intensity_duration":qa,"temporal_qa":tempqa},indent=2),encoding="utf-8")
print("\nwrote GATE3A_BASELINE_RESULTS.csv")
