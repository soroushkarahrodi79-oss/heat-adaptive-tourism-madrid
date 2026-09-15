"""GATE 3A sampling invariants (audit fix). Run: py -m pytest tests/pedestrian_heat/test_gate3a_sampling.py
or plain `py tests/pedestrian_heat/test_gate3a_sampling.py`.
Tests the corrected global-chainage sampler + weighted metrics (no rasters needed)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]/"src"))
import numpy as np
from gate3a_sample_metrics import (route_length, chainage_samples, metrics, CATS, DS)

def _feed(samples, field_fn):
    """value each sample by a synthetic field function of chainage."""
    return np.array([field_fn(s["chainage"]) for s in samples]), np.array([s["rep_len"] for s in samples])

def test_replen_sums_to_route_length():
    coords=[(0,0),(100,0),(100,50),(0,50)]  # L = 100+50+100 = 250
    samp,L=chainage_samples(coords)
    assert abs(L-250.0)<1e-9
    assert abs(sum(s["rep_len"] for s in samp)-L)<1e-9

def test_M4_minutes_sum_equals_M1():
    coords=[(0,0),(2657.8,0)]  # straight, single segment
    samp,L=chainage_samples(coords)
    vals,rep=_feed(samp, lambda s: 40.0)  # all 'very_strong'
    m=metrics(vals,rep,1.1)
    assert abs(m["M4_min_sum_exact"]-m["M1_exact"])<1e-9
    assert abs(m["M1_exact"]-(L/1.1/60.0))<1e-9

def test_constant_field_M2_exact():
    coords=[(0,0),(37,0),(37,80),(200,80)]
    samp,_=chainage_samples(coords)
    vals,rep=_feed(samp, lambda s: 42.123)
    m=metrics(vals,rep,1.1)
    assert abs(m["M2_timeweighted_mean_UTCI"]-42.123)<1e-6

def test_vertex_segmentation_invariance():
    # same physical straight line, two different vertex segmentations
    A=[(0,0),(300,0)]
    B=[(0,0),(17,0),(58.5,0),(123,0),(200,0),(263.2,0),(300,0)]
    field=lambda s: 30.0+0.02*s  # linear in chainage
    sa,_=chainage_samples(A); sb,_=chainage_samples(B)
    va,ra=_feed(sa,field); vb,rb=_feed(sb,field)
    ma=metrics(va,ra,1.1); mb=metrics(vb,rb,1.1)
    for k in ("M2_timeweighted_mean_UTCI","M3_median","M3_p25","M3_p75","M1_trip_min",
              "M4_min_no_stress","M4_min_moderate","M4_min_strong","M4_min_very_strong"):
        assert abs(ma[k]-mb[k])<1e-6, (k,ma[k],mb[k])

def test_spacing_is_true_chainage():
    coords=[(0,0),(2657.8,0)]
    samp,L=chainage_samples(coords)
    # expected number of intervals = ceil(L/DS)
    import math
    assert len(samp)==math.ceil(L/DS)
    # interior samples spaced exactly DS in chainage
    ch=[s["chainage"] for s in samp]
    diffs=np.diff(ch[:-1])
    assert np.allclose(diffs, DS, atol=1e-9)

if __name__=="__main__":
    import traceback
    fns=[v for k,v in sorted(globals().items()) if k.startswith("test_")]
    ok=0
    for fn in fns:
        try: fn(); print("PASS",fn.__name__); ok+=1
        except Exception: print("FAIL",fn.__name__); traceback.print_exc()
    print(f"\n{ok}/{len(fns)} tests passed")
    sys.exit(0 if ok==len(fns) else 1)
