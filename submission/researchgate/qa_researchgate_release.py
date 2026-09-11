"""Assertions for the bounded HATI-Madrid ResearchGate release package."""

from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = Path(__file__).resolve().parent
PDF = PACKAGE / "HATI_Madrid_Preprint_v1.0.pdf"
TITLE = (
    "Thermal representation as a decision variable in heat-adaptive tourism opportunity "
    "screening: evidence from a Madrid pilot"
)


def rows(relative: str):
    with (ROOT / relative).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def check_headlines():
    thermal = rows("outputs/tables/proxy_vs_physical_comparison.csv")
    overall = next(r for r in thermal if r["metric"] == "overall_reclassification_rate_pct")
    assert (overall["value"], overall["n"]) == ("33.3", "42")
    directions = [int(float(r["value"])) for r in thermal if r["metric"] == "reclassification_direction_count"]
    assert sorted(directions) == [5, 9]

    scenarios = rows("outputs/tables/phase3_hati_vs_baseline.csv")
    assert len(scenarios) == 8
    assert sum(r["candidate_set_changed"] == "True" for r in scenarios) == 7
    assert sum(r["baseline_pick_survives_hati"] == "False" for r in scenarios) == 3
    assert sum(int(r["n_removed_by_hati_thermal_or_evidence"]) for r in scenarios) == 23
    s8 = next(r for r in scenarios if r["scenario"] == "S8")
    assert (s8["access_radius_m"], s8["n_hati_alternatives"]) == ("500", "0")

    access = next(r for r in rows("outputs/tables/phase3_accessibility_sensitivity.csv") if r["scenario"] == "S8")
    assert (access["n_alt_500m"], access["n_alt_800m"], access["n_alt_1200m"]) == ("0", "2", "7")

    confidence = rows("data/processed/phase2_2_decision_confidence.csv")
    counts = {name: sum(r["decision_confidence"] == name for r in confidence) for name in ("ROBUST", "BOUNDARY", "UNSTABLE")}
    assert counts == {"ROBUST": 35, "BOUNDARY": 6, "UNSTABLE": 1}
    unstable = [r for r in confidence if r["decision_confidence"] == "UNSTABLE"]
    assert [(r["asset_id"], r["timestamp"]) for r in unstable] == [("A24", "18:00")]


def check_files_and_local_links():
    expected = [
        "README.md",
        "PUBLIC_TRUTH_AUDIT.md",
        "RESEARCHGATE_METADATA.md",
        "FIGURE_INVENTORY.md",
        "build_researchgate_pdf.py",
        "HATI_Madrid_Preprint_v1.0.pdf",
    ]
    for name in expected:
        assert (PACKAGE / name).exists(), name

    for markdown in [ROOT / "README.md", *PACKAGE.glob("*.md")]:
        content = markdown.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
            if target.startswith(("http://", "https://", "#")):
                continue
            assert (markdown.parent / target).resolve().exists(), f"broken link in {markdown}: {target}"


def check_manuscript_and_pdf():
    source = (ROOT / "manuscript/MANUSCRIPT_TMP_v0.2.md").read_text(encoding="utf-8")
    assert source.splitlines()[0] == f"# {TITLE}"
    assert "14 of 42" in source and "7 of 8" in source

    reader = PdfReader(str(PDF))
    assert len(reader.pages) >= 20
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    compact = " ".join(text.split())
    assert TITLE in compact
    assert "Version 1.0 - public preprint - 2026-09-11" in compact
    assert "Non-peer-reviewed preprint / research work" in compact
    assert "Non-peer-reviewed preprint" in compact
    assert "Creative Commons Attribution 4.0 International (CC BY 4.0)" in compact
    assert re.search(r"ResearchGate\s+release\s+candidate", compact) is None
    assert "33.3%, 14 of 42" in compact
    assert "7 of 8" in compact
    assert "NO_DEFENSIBLE_ALTERNATIVE" in compact
    assert "Prepared for submission to" not in compact
    assert "TO VERIFY" not in compact
    assert "Tourism Management Perspectives" not in compact


def check_references_and_figure_manifest():
    manuscript = (ROOT / "manuscript/MANUSCRIPT_TMP_v0.2.md").read_text(encoding="utf-8")
    references = manuscript.split("# References", 1)[1].split("# Figure captions", 1)[0]
    assert len(re.findall(r"(?m)^\d+\. ", references)) == 23
    assert references.count("https://doi.org/") + references.count("https://arxiv.org/") == 23

    manifest = rows("docs/PHASE5_3B_RENDER_MANIFEST.csv")
    checked = set()
    for item in manifest:
        relative = item["output_file"]
        if relative in checked:
            continue
        checked.add(relative)
        content = (ROOT / relative).read_bytes()
        assert hashlib.sha256(content).hexdigest() == item["sha256"], relative
        assert item["new_analysis"] == "FALSE"


if __name__ == "__main__":
    check_headlines()
    check_files_and_local_links()
    check_manuscript_and_pdf()
    check_references_and_figure_manifest()
    print("ResearchGate release QA: PASS")
