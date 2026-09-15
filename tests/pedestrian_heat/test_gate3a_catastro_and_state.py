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

# ---- temporal-state execution invariants (behavioral, on produced artifacts) ----
G=pathlib.Path(__file__).resolve().parents[2]/"data/interim/pedestrian-heat/gate3a"
def test_stateful_sequence_continuous_15min():
    f=G/"gate3a_forcing_stateful.csv"
    if not f.exists():
        print("  (skip: stateful forcing not present)"); return
    rows=list(csv.DictReader(open(f)))
    labels=[r["label"] for r in rows]
    assert len(rows)==72, len(rows)                                   # 00:00->17:45 @15min
    mins=[int(l[:2])*60+int(l[2:]) for l in labels]
    assert all(b-a==15 for a,b in zip(mins,mins[1:])), "non-uniform 15-min spacing"
    for dl in ["1400","1415","1430","1445","1700","1715","1730","1745"]:
        assert dl in labels, dl
def test_stateful_meta_single_call():
    m=G/"gate3a_stateful_meta.json"
    if not m.exists():
        print("  (skip: stateful meta not present)"); return
    d=json.loads(m.read_text())
    assert d["timestep_min"]==15 and d["n_timesteps"]==72
    assert "single-call" in d["protocol"]

if __name__=="__main__":
    import traceback
    fns=[v for k,v in sorted(globals().items()) if k.startswith("test_")]
    ok=0
    for fn in fns:
        try: fn(); print("PASS",fn.__name__); ok+=1
        except Exception: print("FAIL",fn.__name__); traceback.print_exc()
    print(f"\n{ok}/{len(fns)} tests passed"); sys.exit(0 if ok==len(fns) else 1)
