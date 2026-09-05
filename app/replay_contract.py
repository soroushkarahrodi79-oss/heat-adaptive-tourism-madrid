"""Validate immutable artifact bytes before loading a presentation snapshot.

The cached loader serves only these verified bytes, never re-read unverified
data. Restart the server to load a snapshot again. No scientific computation.
"""
import hashlib
import io
import json
from functools import lru_cache
from pathlib import Path

import pandas as pd

MANIFEST_PATH = Path(__file__).with_name("replay_manifest.json")


class IntegrityError(ValueError):
    """The replay must not display scientific records from this input."""


@lru_cache(maxsize=1)
def manifest():
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise IntegrityError("Replay manifest unavailable or invalid.") from exc


def validate_frames(frames, contract):
    for key, spec in contract["artifacts"].items():
        frame = frames[key]
        if list(frame.columns) != spec["columns"] or len(frame) != spec["rows"]:
            raise IntegrityError(f"Schema/row count mismatch: {spec['path']}")
        if frame[spec["keys"]].isna().any().any() or frame.duplicated(spec["keys"]).any():
            raise IntegrityError(f"Missing or duplicate row identity: {spec['path']}")
    cat, scr, scn, summary = (frames[k] for k in ("catalog", "screening", "scenarios", "summary"))
    ids = set(cat.asset_id)
    times = set(contract["timestamps"])
    if ids != {f"A{i:02}" for i in range(1, 28)}:
        raise IntegrityError("Unexpected asset identifiers.")
    if set(zip(scr.asset_id, scr.timestamp)) != {(a, t) for a in ids for t in times}:
        raise IntegrityError("Asset/time coverage mismatch.")
    if set(summary.scenario) != {f"S{i}" for i in range(1, 9)}:
        raise IntegrityError("Scenario identifiers mismatch.")
    for _, row in summary.iterrows():
        candidates = scn[scn.scenario == row.scenario]
        if (row.timestamp not in times or row.timestamp == "12:00"
                or row.source_id not in ids
                or set(candidates.candidate_id) != ids - {row.source_id}
                or not candidates.timestamp.eq(row.timestamp).all()
                or not candidates.source_id.eq(row.source_id).all()
                or not candidates.access_radius_m.eq(row.access_radius_m).all()):
            raise IntegrityError(f"Scenario binding mismatch: {row.scenario}")
        if not set(candidates.status) <= {"CANDIDATE_ALTERNATIVE", "EXCLUDED"}:
            raise IntegrityError("Unknown scenario status.")
        survivors = candidates[candidates.status == "CANDIDATE_ALTERNATIVE"]
        excluded = candidates[candidates.status == "EXCLUDED"]
        expected = set(str(row.alternative_ids).split(",")) if pd.notna(row.alternative_ids) else set()
        if (set(survivors.candidate_id) != expected or len(survivors) != row.n_candidate_alternatives
                or survivors.exclusion_reason.notna().any() or excluded.exclusion_reason.isna().any()
                or not set(excluded.exclusion_reason) <= set(contract["exclusion_tokens"])):
            raise IntegrityError(f"Recorded outcome mismatch: {row.scenario}")
    for field, allowed in contract["screening_enums"].items():
        if not set(scr[field]) <= set(allowed):
            raise IntegrityError(f"Unknown screening value: {field}")
    if scr[scr.indoor_outdoor == "indoor"][["utci_baseline", "utci_envelope_low", "utci_envelope_high"]].notna().any().any():
        raise IntegrityError("Indoor thermal values must remain null.")


def load_verified(root, data_files):
    contract = manifest()
    try:
        if contract["schema_version"] != "1.0.0" or set(data_files) != set(contract["artifacts"]):
            raise IntegrityError("Unrecognized replay data contract.")
        frames = {}
        for key, spec in contract["artifacts"].items():
            path = Path(data_files[key])
            if path.resolve() != (Path(root) / spec["path"]).resolve():
                raise IntegrityError(f"Unapproved artifact path: {key}")
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != spec["sha256"]:
                raise IntegrityError(f"SHA-256 mismatch: {spec['path']}")
            frames[key] = pd.read_csv(io.BytesIO(raw), encoding="utf-8", dtype={"timestamp": str})
        validate_frames(frames, contract)
        return frames
    except IntegrityError:
        raise
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        raise IntegrityError(f"Replay integrity check failed: {exc}") from exc
