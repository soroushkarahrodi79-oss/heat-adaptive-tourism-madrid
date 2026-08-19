"""Phase 5.4A — assemble MANUSCRIPT_TMP_v0.1.md from the locked body with authorized
mechanical edits only (section renumbering, figure/table cross-ref remap, citation-format
normalization, minimal figure/table citations). Prose otherwise verbatim. Logs every edit."""
import re, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
body = open(os.path.join(ROOT, "manuscript/MANUSCRIPT_v0.1.md"), encoding="utf-8").read()
log = []

# 0. strip leading HTML assembly comment
body = re.sub(r"^<!--.*?-->\s*", "", body, flags=re.DOTALL); log.append("removed leading HTML assembly comment")

# 1. collapse whitespace inside parenthetical citations (…YEAR…) to single spaces
def _collapse(m):
    return re.sub(r"\s+", " ", m.group(0))
body = re.sub(r"\([^()]*?(?:19|20)\d\d[^()]*?\)", _collapse, body)
log.append("collapsed internal whitespace in parenthetical citations")

# 2. citation-format normalization (strip in-text journal names; harmonize keys)
CITES = {
 "(extreme heat reshapes urban mobility, 2025)": "(Extreme heat and urban mobility, 2025)",
 "(heat risk action planning for tourism, Annals of Tourism Research 2026; OECD Tourism Trends and Policies 2026)": "(Heat risk action planning for tourism, 2026; OECD, 2026)",
 "(tourism in a warming climate, Sustainability 2026)": "(Tourism in a warming climate, 2026)",
 "(tourist demand and destination development under climate change, Journal of Sustainable Tourism 2025)": "(Tourist demand under climate change, 2025)",
 "(mapping tourism exposure to weather extremes, ERL 2024)": "(Tourism exposure to weather extremes, 2024)",
 "(outdoor thermal comfort and tourist visits in Madrid and Sevilla plazas, Env Sci Pollut Res 2022)": "(Plaza thermal comfort in Madrid and Sevilla, 2022)",
 "(HCI/TCI inter-comparison, Atmosphere 2016; recent HCI/TCI applications, IJB 2025)": "(HCI/TCI inter-comparison, 2016; Hungarian HCI/TCI, 2025)",
 "(reliability and usability of tourism climate indices, Earth Perspectives 2016)": "(Reliability of tourism climate indices, 2016)",
 "(WRF-UCM-SOLWEIG mapping, Sustainable Cities and Society 2024)": "(WRF-UCM-SOLWEIG mapping, 2024)",
 "(Tmrt validation ranges, Gál & Kántor 2019)": "(Gál & Kántor, 2019)",
 "(Cool Routes, Building and Environment 2026; CoolWalks, Scientific Reports 2025)": "(Cool Routes, 2026; CoolWalks, 2025)",
 "(UTCI-adjusted pedestrian accessibility, Sustainable Cities and Society 2026)": "(UTCI-adjusted pedestrian accessibility, 2026)",
 "(Barcelona climate-shelter accessibility, Cities 2025)": "(Barcelona climate-shelter accessibility, 2025)",
 "(decision-making under uncertainty in participatory GIS, IJGIS 2025; Monte-Carlo reliability of UTCI and PET, Scientific Reports 2025)": "(Participatory-GIS under uncertainty, 2025; Monte-Carlo UTCI/PET reliability, 2025)",
 '(the "beyond land surface temperature" argument, 2026)': "(Beyond land surface temperature, 2026)",
 "(beyond land surface temperature, 2026)": "(Beyond land surface temperature, 2026)",
 "(heat risk action planning for tourism, 2026)": "(Heat risk action planning for tourism, 2026)",
 "(HCI/TCI inter-comparison, 2016; reliability of tourism climate indices, 2016)": "(HCI/TCI inter-comparison, 2016; Reliability of tourism climate indices, 2016)",
 "(Monte-Carlo UTCI/PET reliability, 2025; decision-making under uncertainty in participatory GIS, 2025)": "(Monte-Carlo UTCI/PET reliability, 2025; Participatory-GIS under uncertainty, 2025)",
}
for a, b in CITES.items():
    if a in body: body = body.replace(a, b); log.append(f"citation normalized: {a[:40]}… -> {b[:40]}…")
    else: log.append(f"WARN citation not found verbatim: {a[:50]}")

# 3. section-heading renumbering (low source first to avoid cascade)
HEAD = [("# 3. Methods", "# 2. Methods"), ("# 4. Results", "# 3. Results"),
        ("# 5. Discussion", "# 4. Discussion"),
        ("# 6. Limitations and scope conditions", "# 5. Limitations and scope conditions"),
        ("# 7. Conclusion", "# 6. Conclusion")]
for a, b in HEAD:
    body = body.replace(a, b); log.append(f"heading: {a} -> {b}")

# 4. subsection renumbering (Methods 3.x->2.x, Results 4.x->3.x, Discussion 5.x->4.x, Limitations 6.x->5.x)
for src, dst in [("3", "2"), ("4", "3"), ("5", "4"), ("6", "5")]:
    body, n = re.subn(rf"(?m)^## {src}\.(\d)", rf"## {dst}.\1", body)
    log.append(f"subsections ## {src}.x -> ## {dst}.x ({n})")

# 5. internal Section cross-references
for a, b in [("Section 3.4", "Section 2.4"), ("Section 3.2", "Section 2.2")]:
    body, n = re.subn(re.escape(a), b, body); log.append(f"xref {a} -> {b} ({n})")
body, n = re.subn(r"Section\s+4\.1", "Section 3.1", body); log.append(f"xref Section 4.1 -> Section 3.1 ({n})")

# 6. figure cross-reference remap (order: 3->S1 first, then 6->3)
body, n = re.subn(r"Fig\. 3\b", "Fig. S1", body); log.append(f"Fig. 3 -> Fig. S1 ({n})")
body, n = re.subn(r"Fig\. 6\b", "Fig. 3", body); log.append(f"Fig. 6 -> Fig. 3 ({n})")

# 7. table cross-reference remap (order: 3->S1 first, then 4->3)
body, n = re.subn(r"Table 3\b", "Table S1", body); log.append(f"Table 3 -> Table S1 ({n})")
body, n = re.subn(r"Table 4\b", "Table 3", body); log.append(f"Table 4 -> Table 3 ({n})")

# 8. minimal figure/table citations for otherwise-uncited main figures/tables
def ins(pattern, repl, label):
    global body
    body, n = re.subn(pattern, repl, body, count=1)
    log.append(f"insert {label} ({n})")
ins(r"keep every asset individually\s+inspectable\.", "keep every asset individually inspectable (Fig. 1a).", "Fig. 1a in Methods 2.1")
ins(r"All inputs are open data with documented provenance\.", "All inputs are open data with documented provenance (Table 1).", "Table 1 in Methods 2.2")
ins(r"traceable to a single most-fundamental\s+cause\.", "traceable to a single most-fundamental cause (Table 2).", "Table 2 in Methods 2.7")
ins(r"There is no weighted composite score anywhere\s+in the chain\.", "There is no weighted composite score anywhere in the chain (Fig. 1b).", "Fig. 1b in Methods 2.7")

open(os.path.join(ROOT, "scripts_assembly/_body_transformed.md"), "w", encoding="utf-8").write(body)
print("BODY TRANSFORM LOG:")
for l in log: print("  -", l)
