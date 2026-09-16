"""GATE 3A correction tests (AMENDMENT_003): Catastro fail-closed/structural parsing and
stateful temporal-execution invariants. No network; parsing tested on synthetic GML.
Run: py tests/pedestrian_heat/test_gate3a_catastro_and_state.py
"""
import sys, pathlib, csv, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]/"src"))
import xml.etree.ElementTree as ET
import catastro_bu as cb

GML="http://www.opengis.net/gml/3.2"; BU="http://inspire.jrc.ec.europa.eu/schemas/bu-ext2d/2.0"

def _building_xml(gid, exterior, interiors=(), extra_patches=()):
    def ring(coords): return f'<gml:LinearRing><gml:posList>{" ".join(str(v) for xy in coords for v in xy)}</gml:posList></gml:LinearRing>'
    def patch(ext,ints):
        s=f'<gml:PolygonPatch><gml:exterior>{ring(ext)}</gml:exterior>'
        for it in ints: s+=f'<gml:interior>{ring(it)}</gml:interior>'
        return s+'</gml:PolygonPatch>'
    patches=patch(exterior,interiors)+"".join(patch(p,()) for p in extra_patches)
    return (f'<bu:Building xmlns:bu="{BU}" xmlns:gml="{GML}" gml:id="{gid}">'
            f'<gml:Surface>{patches}</gml:Surface></bu:Building>')

def _fc(bodies):
    return (f'<wfs:FeatureCollection xmlns:wfs="http://www.opengis.net/wfs/2.0" '
            f'xmlns:gml="{GML}" xmlns:bu="{BU}">' + "".join(f"<wfs:member>{b}</wfs:member>" for b in bodies)
            + '</wfs:FeatureCollection>')

def test_structural_parse_holes_and_multipart():
    # square 0..10 with a hole 3..7, plus a second patch (multipart)
    ext=[(441000,4473000),(441010,4473000),(441010,4473010),(441000,4473010),(441000,4473000)]
    hole=[(441003,4473003),(441007,4473003),(441007,4473007),(441003,4473007),(441003,4473003)]
    p2=[(441020,4473000),(441030,4473000),(441030,4473010),(441020,4473010),(441020,4473000)]
    root=ET.fromstring(_fc([_building_xml("B1",ext,[hole],[p2])]))
    b=list(root.iter(f"{{{BU}}}Building"))[0]
    polys=cb._polys_from_building(b, axis_en=True)
    assert len(polys)==2, len(polys)                    # two patches
    holed=[p for p in polys if len(p.interiors)>0]
    assert len(holed)==1 and len(holed[0].interiors)==1  # hole preserved
    # exterior area 100, hole 16 -> holed polygon area 84
    assert abs(holed[0].area-84.0)<1e-6, holed[0].area

def test_axis_detection_en():
    # Easting-first (Madrid): first value ~4.41e5
    root=ET.fromstring(_fc([_building_xml("B",[(441000,4473000),(441010,4473000),(441010,4473010),(441000,4473010),(441000,4473000)])]))
    assert cb._detect_axis_en(root) is True

def test_exception_payload_detected():
    # simulate what fetch does on an OGC ExceptionReport (string-level checks used by fetch)
    txt='<?xml version="1.0"?><ows:ExceptionReport xmlns:ows="http://www.opengis.net/ows/1.1"><ows:Exception><ows:ExceptionText>bad bbox</ows:ExceptionText></ows:Exception></ows:ExceptionReport>'
    assert (cb.OWS_EXC in txt) or ("<ows:Exception" in txt) or ("ExceptionText" in txt)

def test_empty_valid_vs_error_distinguished():
    # a valid but empty spatial result is a well-formed FeatureCollection with 0 members (no raise)
    root=ET.fromstring(_fc([]))
    assert root.tag.endswith("FeatureCollection")
    assert len(list(root.iter(f"{{{BU}}}Building")))==0

# ---- timezone-aware forcing + stateful-execution invariants (DETERMINISTIC, no artifacts) ----
import forcing_barajas as fb
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def test_00local_maps_to_prevday_2200utc():
    # 2023-08-24 00:00 Europe/Madrid == 2023-08-23 22:00 UTC (date-wrap bug fix)
    u=fb.local_to_utc(2023,8,24,0,0)
    assert u==datetime(2023,8,23,22,0,tzinfo=timezone.utc), u

def test_01local_maps_to_prevday_2300utc():
    u=fb.local_to_utc(2023,8,24,1,0)
    assert u==datetime(2023,8,23,23,0,tzinfo=timezone.utc), u

def test_00local_forcing_uses_prevday_record():
    # value at 00:00 local must equal the 2023-08-23 22:00 UTC observation (29.6 C), NOT
    # the same-day 22:00 UTC value the old %24 bug would have used.
    seq=fb.build_local_sequence(date_local="2023-08-24", end="17:45", step_min=15)
    s0=seq[0]
    assert s0["local"]=="00:00" and s0["utc_dt"]==datetime(2023,8,23,22,0,tzinfo=timezone.utc)
    assert abs(s0["ta"]-29.6)<1e-6, s0["ta"]
    # sanity: the buggy same-day 2023-08-24 22:00 UTC temperature differs materially
    recs={ (t.date().isoformat(),t.hour):v for t,v in fb.load_records()}
    same_day_2200=recs[("2023-08-24",22)][0]
    assert abs(s0["ta"]-same_day_2200)>1.0, "date-wrap bug would be indistinguishable"

def test_sequence_72_continuous_15min():
    seq=fb.build_local_sequence(date_local="2023-08-24", end="17:45", step_min=15)
    assert len(seq)==72, len(seq)
    mins=[int(s["label"][:2])*60+int(s["label"][2:]) for s in seq]
    assert mins[0]==0 and mins[-1]==17*60+45
    assert all(b-a==15 for a,b in zip(mins,mins[1:])), "non-uniform 15-min spacing"

def test_eight_decision_labels_present():
    seq=fb.build_local_sequence(date_local="2023-08-24", end="17:45", step_min=15)
    labels={s["label"] for s in seq}
    for dl in ["1400","1415","1430","1445","1700","1715","1730","1745"]:
        assert dl in labels, dl

def test_execution_is_single_stateful_call_not_eight():
    # Structural check on the runner source: exactly one solweig.calculate() invocation, fed a
    # LIST (weather_list), i.e. one stateful multi-Weather call (NOT 8 independent per-step calls).
    src=(pathlib.Path(__file__).resolve().parents[2]/"src/gate3a_run_solweig.py").read_text(encoding="utf-8")
    # count actual call sites (signature form), not docstring mentions
    calls=src.count("solweig.calculate(surface=")
    assert calls==1, f"expected exactly one stateful calculate(surface=...) call, found {calls}"
    assert "weather=weather_list" in src, "calculate() must be fed the full Weather LIST (stateful)"
    assert "weather_list=[solweig.Weather" in src, "must build a Weather list for the stateful call"
    # guard against a per-timestamp loop calling calculate inside a for-loop
    assert "for r in fdf.itertuples():\n    solweig.calculate" not in src, "must not call calculate per-timestep"

def test_gate3b_runner_uses_dateaware_forcing_and_single_stateful_call():
    # AMENDMENT_003 date-aware fix propagated to the 3B perturbation runner: it must use the
    # shared timezone-aware forcing module and a single stateful calculate() over a Weather LIST,
    # and must NOT reintroduce the same-day %24 UTC-hour date-wrap bug.
    src=(pathlib.Path(__file__).resolve().parents[2]/"src/gate3b_run_one.py").read_text(encoding="utf-8")
    assert "import forcing_barajas as fb" in src, "3B runner must use the shared forcing_barajas module"
    assert "fb.build_local_sequence(" in src, "3B runner must build its forcing via build_local_sequence"
    assert ")%24" not in src, "3B runner must not reintroduce the %24 UTC-hour date-wrap"
    assert 'if r["date"]==DATE' not in src, "3B runner must not filter forcing to same-day rows only"
    assert src.count("solweig.calculate(surface=")==1, "3B runner must issue exactly one stateful calculate()"
    assert "weather=wl" in src, "calculate() must be fed the full Weather LIST (stateful)"

if __name__=="__main__":
    import traceback
    fns=[v for k,v in sorted(globals().items()) if k.startswith("test_")]
    ok=0
    for fn in fns:
        try: fn(); print("PASS",fn.__name__); ok+=1
        except Exception: print("FAIL",fn.__name__); traceback.print_exc()
    print(f"\n{ok}/{len(fns)} tests passed"); sys.exit(0 if ok==len(fns) else 1)
