"""
Phase 3 step 0: harvest opening_hours (and related) tags for the 27 pilot
assets from the project's OWN already-fetched OSM raw extracts - no new fetch,
same ODbL provenance recorded in pilot_assets.csv `source`. Reports coverage so
the remaining gaps can be filled from documented authoritative institutional
sources (recorded explicitly, never invented).
"""
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OSM = ROOT / "data" / "raw" / "osm"
PROCESSED = ROOT / "data" / "processed"

TAG_KEYS = ["opening_hours", "opening_hours:covid19", "tourism", "amenity",
            "historic", "leisure", "name:en", "wikidata", "website"]


def load_all_elements():
    idx = {}
    for jf in OSM.glob("*.json"):
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
        except Exception:
            continue
        for el in data.get("elements", []):
            idx[(el.get("type"), el.get("id"))] = el.get("tags", {})
    return idx


def main():
    assets = pd.read_csv(PROCESSED / "pilot_assets.csv")
    idx = load_all_elements()
    print(f"Loaded {len(idx)} OSM elements from raw extracts\n")

    rows = []
    for _, a in assets.iterrows():
        m = re.search(r"(node|way|relation)/(\d+)", a["source"])
        tags = {}
        osm_ref = ""
        if m:
            osm_ref = f"{m.group(1)}/{m.group(2)}"
            tags = idx.get((m.group(1), int(m.group(2))), {})
        rec = {"asset_id": a["asset_id"], "name": a["name"], "osm_ref": osm_ref,
               "matched_in_raw": bool(tags)}
        for k in TAG_KEYS:
            rec[k] = tags.get(k, "")
        rows.append(rec)

    out = pd.DataFrame(rows)
    out_path = PROCESSED / "phase3_osm_opening_hours_raw.csv"
    out.to_csv(out_path, index=False, encoding="utf-8")
    cols = ["asset_id", "name", "osm_ref", "matched_in_raw", "opening_hours", "tourism", "amenity", "historic", "leisure"]
    pd.set_option("display.width", 240, "display.max_colwidth", 40)
    print(out[cols].to_string(index=False))
    print(f"\nmatched in raw: {out.matched_in_raw.sum()}/{len(out)}; "
          f"have opening_hours: {(out.opening_hours!='').sum()}/{len(out)}")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
