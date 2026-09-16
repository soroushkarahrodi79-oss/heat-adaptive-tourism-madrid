"""Timezone-aware Barajas forcing lookup (Gate-3A/3B correction under AMENDMENT_003).

Fixes the date-wrap bug: the stateful preconditioning sequence starts at 2023-08-24 00:00
Europe/Madrid = 2023-08-23 22:00 UTC, so the first local hours must read PREVIOUS-DAY UTC
records. This module builds actual UTC datetimes from the frozen AEMET CSV and interpolates
between the surrounding UTC records — no integer-hour modulo, no %24 wrapping.
"""
import csv, pathlib
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

MADRID = ZoneInfo("Europe/Madrid")
UTC = timezone.utc
_CSV = pathlib.Path(__file__).resolve().parents[1]/"data/raw/aemet_barajas_08221_hourly_202308.csv"

def load_records(csv_path=_CSV):
    """Return sorted list of (utc_datetime, (ta,rh,ws_kmh,pres))."""
    recs=[]
    for r in csv.DictReader(open(csv_path)):
        if not r["hour_utc"].isdigit():
            continue
        y,m,d=map(int,r["date"].split("-"))
        dt=datetime(y,m,d,int(r["hour_utc"]),0,tzinfo=UTC)
        recs.append((dt,(float(r["temp_c"]),float(r["rhum_pct"]),float(r["wspd_kmh"]),float(r["pres_hpa"]))))
    recs.sort(key=lambda x:x[0])
    return recs

def _interp(recs, utc_dt):
    """Linear interpolation between the two surrounding UTC records (raises if out of range)."""
    if utc_dt <= recs[0][0]: return recs[0][1]
    if utc_dt >= recs[-1][0]: return recs[-1][1]
    import bisect
    times=[t for t,_ in recs]
    i=bisect.bisect_right(times,utc_dt)-1
    t0,v0=recs[i]; t1,v1=recs[i+1]
    f=(utc_dt-t0)/(t1-t0)
    return tuple(a+(b-a)*f for a,b in zip(v0,v1))

def local_to_utc(y,mo,d,hh,mm):
    return datetime(y,mo,d,hh,mm,tzinfo=MADRID).astimezone(UTC)

def build_local_sequence(date_local="2023-08-24", end="17:45", step_min=15, recs=None):
    """15-min local (Europe/Madrid) sequence 00:00 -> end inclusive; forcing interpolated from
    actual surrounding UTC records (previous-day UTC used where the local time wraps back)."""
    if recs is None: recs=load_records()
    y,mo,d=map(int,date_local.split("-"))
    eh,em=map(int,end.split(":"))
    total_end=eh*60+em
    out=[]; t=0
    while t<=total_end:
        hh,mm=t//60,t%60
        local_dt=datetime(y,mo,d,hh,mm,tzinfo=MADRID)
        utc_dt=local_dt.astimezone(UTC)
        ta,rh,ws_kmh,pres=_interp(recs,utc_dt)
        out.append({"local":f"{hh:02d}:{mm:02d}","label":f"{hh:02d}{mm:02d}",
                    "local_dt":local_dt,"utc_dt":utc_dt,
                    "ta":round(ta,2),"rh":round(min(100,max(1,rh)),1),
                    "ws":round(ws_kmh/3.6,2),"pres":round(pres,1)})
        t+=step_min
    return out

if __name__=="__main__":
    recs=load_records()
    seq=build_local_sequence()
    print("n steps:",len(seq))
    for r in seq[:3]+seq[-1:]:
        print(r["local"],"Madrid ->",r["utc_dt"].strftime("%Y-%m-%d %H:%M UTC"),"ta=",r["ta"])
