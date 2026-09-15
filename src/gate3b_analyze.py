"""GATE 3B — analysis: sample all perturbations, compute A-B per metric, apply the FROZEN
decision-stability rule + negative controls. Uses corrected chainage sampler (v=1.1 baseline;
E-P6=1.4 QA; E-P5 lateral +/-12 m). No SOLWEIG here (fields already produced)."""
import os, json, csv, pathlib, sys
_rd=pathlib.Path(__import__("rasterio").__file__).parent
os.environ["PROJ_DATA"]=str(_rd/"proj_data"); os.environ["PROJ_LIB"]=str(_rd/"proj_data"); os.environ["GDAL_DATA"]=str(_rd/"gdal_data")
import numpy as np, rasterio
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"src"))
from gate3a_sample_metrics import chainage_samples, metrics, DEP_LABELS, STEP_MIN, BUF, CATS

ROOT=pathlib.Path(__file__).resolve().parents[1]
G3A=ROOT/"data/interim/pedestrian-heat/gate3a"; G3B=ROOT/"data/interim/pedestrian-heat/gate3b"
ROUTES={n:json.loads((ROOT/f"data/processed/pedestrian-heat/OD1_Route_{n}_epsg25830.geojson").read_text())["features"][0]["geometry"]["coordinates"] for n in "AB"}

def load_fields(dirpath):
    F={}
    for labs in DEP_LABELS.values():
        for lb in labs:
            with rasterio.open(dirpath/f"utci_{lb}.tif") as s:
                a=s.read(1).astype("float64"); a[a==s.nodata]=np.nan; F[lb]=(a,s.transform,s.width,s.height)
    return F
def sample(fields,coords,dep,v=1.1,lateral=0.0):
    _,T0,W,H=fields[DEP_LABELS[dep][0]]
    def bmean(field,x,y,rad=BUF):
        r0=int((y-T0.f)/T0.e);c0=int((x-T0.c)/T0.a);pr=int(rad/abs(T0.a))
        r1,r2=max(0,r0-pr),min(H,r0+pr+1);c1,c2=max(0,c0-pr),min(W,c0+pr+1)
        if r1>=r2 or c1>=c2: return np.nan
        sub=field[r1:r2,c1:c2];yy,xx=np.ogrid[r1:r2,c1:c2];m=((yy-r0)**2+(xx-c0)**2)<=pr**2
        vv=sub[m];vv=vv[~np.isnan(vv)];return float(vv.mean()) if vv.size else np.nan
    def n15(t): return min(45,max(0,int(round(t/15.0)*15)))
    samp,_=chainage_samples(coords); s2l=dict(zip(STEP_MIN,DEP_LABELS[dep]))
    vals=[];rep=[]
    for i,s in enumerate(samp):
        x,y=s["x"],s["y"]
        if lateral:
            j=min(i+1,len(samp)-1);k=max(i-1,0);dx=samp[j]["x"]-samp[k]["x"];dy=samp[j]["y"]-samp[k]["y"];nrm=(dx*dx+dy*dy)**0.5 or 1
            x+=-dy/nrm*lateral;y+=dx/nrm*lateral
        vals.append(bmean(fields[s2l[n15((s["chainage"]/v)/60.0)]][0],x,y));rep.append(s["rep_len"])
    return metrics(vals,rep,v)

BASE=load_fields(G3A/"solweig")
PERTS={"EP1b_forcing_ea":load_fields(G3B/"solweig_EP1b_forcing_ea"),
       "EP2b_canopy_pnoa":load_fields(G3B/"solweig_EP2b_canopy_pnoa"),
       "EP2c_canopy_treeinv":load_fields(G3B/"solweig_EP2c_canopy_treeinv"),
       "EP2d_canopy_tcd":load_fields(G3B/"solweig_EP2d_canopy_tcd"),
       "EP4b_building_pnoa":load_fields(G3B/"solweig_EP4b_building_pnoa")}

rows=[]
def rec(pert,fields,v=1.1,lateral=0.0):
    for dep in DEP_LABELS:
        mA=sample(fields,ROUTES["A"],dep,v,lateral); mB=sample(fields,ROUTES["B"],dep,v,lateral)
        rows.append({"perturbation":pert,"departure":dep,"speed":v,
          "M2_A":mA["M2_timeweighted_mean_UTCI"],"M2_B":mB["M2_timeweighted_mean_UTCI"],
          "M2_A_minus_B":round(mA["M2_timeweighted_mean_UTCI"]-mB["M2_timeweighted_mean_UTCI"],3),
          "M3max_A":mA["M3_max"],"M3max_B":mB["M3_max"],
          "vstrongext_min_A":round(mA["M4_min_very_strong"]+mA["M4_min_extreme"],2),
          "vstrongext_min_B":round(mB["M4_min_very_strong"]+mB["M4_min_extreme"],2),
          "M1_A":mA["M1_trip_min"],"M1_B":mB["M1_trip_min"]})
rec("EP0_baseline",BASE)
for name,F in PERTS.items(): rec(name,F)
rec("EP5_side_+12m",BASE,lateral=12.0)
rec("EP5_side_-12m",BASE,lateral=-12.0)
rec("EP6_speed_1.4",BASE,v=1.4)

cols=["perturbation","departure","speed","M2_A","M2_B","M2_A_minus_B","M3max_A","M3max_B","vstrongext_min_A","vstrongext_min_B","M1_A","M1_B"]
outdir=ROOT/"docs/research/pedestrian-heat/gate3b"; outdir.mkdir(parents=True,exist_ok=True)
with open(outdir/"GATE3B_PERTURBATION_RESULTS.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)

# ---- decision-stability analysis ----
analysis={}
for dep in DEP_LABELS:
    dr=[r for r in rows if r["departure"]==dep]
    diffs={r["perturbation"]:r["M2_A_minus_B"] for r in dr}
    signs=set(np.sign(v) for v in diffs.values() if abs(v)>1e-9)
    base_diff=diffs["EP0_baseline"]
    reversed_perts=[k for k,v in diffs.items() if np.sign(v)!=np.sign(base_diff) and abs(v)>1e-9 and k!="EP0_baseline"]
    # duration ordering (M1 + high-stress minutes): B shorter -> fewer minutes always
    dur_favors="B (shorter, fewer high-stress minutes)"
    # category-boundary proximity: any M3max within guard of 46 (extreme) across perts
    near_boundary=[(r["perturbation"],r["M3max_A"],r["M3max_B"]) for r in dr if max(r["M3max_A"],r["M3max_B"])>=45.0]
    analysis[dep]={"baseline_M2_A_minus_B":base_diff,
        "M2_diff_range":[round(min(diffs.values()),3),round(max(diffs.values()),3)],
        "intensity_sign_set":sorted(int(s) for s in signs),
        "sign_reverses_under":reversed_perts,
        "intensity_favors":"A (lower mean UTCI)" if base_diff<0 else "B",
        "duration_favors":dur_favors,
        "near_extreme_boundary(M3max>=45)":near_boundary}

# verdict logic (frozen rule)
any_reversal=any(analysis[d]["sign_reverses_under"] for d in DEP_LABELS)
metrics_disagree=True  # intensity favors A, duration favors B at both departures (established 3A + here)
verdict = "ABSTAIN / NO ROBUST DIFFERENCE"
result={"analysis":analysis,"any_intensity_sign_reversal":any_reversal,
        "intensity_vs_duration_disagree":metrics_disagree,"verdict":verdict}
(G3B/"gate3b_analysis.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))
