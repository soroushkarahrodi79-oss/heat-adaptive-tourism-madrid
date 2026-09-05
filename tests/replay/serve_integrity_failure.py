"""Browser fixture: corrupt a temporary copy, never the scientific baseline."""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app import data_loader as dl
from app.replay_contract import manifest

with tempfile.TemporaryDirectory(prefix="hati-integrity-test-") as directory:
    root = Path(directory)
    files = {}
    for key, spec in manifest()["artifacts"].items():
        path = root / spec["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(dl.DATA_FILES[key].read_bytes())
        files[key] = path
    files["scenarios"].write_bytes(files["scenarios"].read_bytes() + b"\n")
    dl.REPO_ROOT, dl.DATA_FILES = root, files
    dl._load_all.cache_clear()
    from app.app import app
    app.run(host="127.0.0.1", port=8051, debug=False)
