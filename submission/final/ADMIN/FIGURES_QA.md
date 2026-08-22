# FIGURES_QA.md — HATI-Madrid

Per-figure registry for the TMP package. No figure was redrawn; each is copied unchanged
from the locked `outputs/publication/` source into `submission/final/TMP/` in its existing
PDF form (the format Elsevier vector-figure upload prefers). Dimensions were not
re-measured programmatically (no ImageMagick/`identify` in this session's environment);
file sizes and formats were verified directly.

| # | Source file | Final file | Format | Filesize | Manuscript caption match |
|---|---|---|---|---|---|
| 1 | `outputs/publication/figures/FIG01_STUDY_DESIGN_v0.1.pdf` (also `.png` 280,074 B, `.svg`) | `submission/final/TMP/HATI_Madrid_Figure_01_Study_Design_v1.0.pdf` | PDF (vector) | 36,517 B | PASS — matches "Figure 1. Study design and constraint-first screening architecture" in `MANUSCRIPT_TMP_v0.2.md` Figure captions and README.md |
| 2 | `outputs/publication/figures/FIG02_THERMAL_METHOD_DIVERGENCE_v0.1.pdf` (also `.png` 314,635 B, `.svg`) | `submission/final/TMP/HATI_Madrid_Figure_02_Thermal_Method_Divergence_v1.0.pdf` | PDF (vector) | 31,553 B | PASS — matches "Figure 2. Thermal-method choice changes feasibility classifications, in both directions" |
| 3 | `outputs/publication/figures/FIG03_SCREENING_CONSEQUENCE_v0.1.pdf` (also `.png` 397,516 B, `.svg`) | `submission/final/TMP/HATI_Madrid_Figure_03_Screening_Consequence_v1.0.pdf` | PDF (vector) | 43,392 B | PASS — matches "Figure 3. Heat-aware screening changes the option set relative to a conventional nearest-open baseline" |
| 4 | `outputs/publication/figures/FIG04_TESTED_UNCERTAINTY_v0.1.pdf` (also `.png` 222,437 B, `.svg`) | `submission/final/TMP/HATI_Madrid_Figure_04_Tested_Uncertainty_v1.0.pdf` | PDF (vector) | 44,279 B | PASS — matches "Figure 4. Decision robustness under tested uncertainty" |
| S1 | `outputs/publication/figures/SFIG01_UTCI_FIELD_v0.1.png` (2,306,261 B; also `.pdf` 1,407,363 B, `.svg`) | Embedded in `submission/final/TMP/HATI_Madrid_Supplementary_Material_v1.0.pdf` | PNG embedded in PDF | Supplementary PDF total 2,217,438 B | PASS — matches "Figure S1. Model-derived UTCI field at 12:00, 15:00 and 18:00" in `supplementary/SUPPLEMENTARY_MATERIAL_v0.1.md` |
| GA | `outputs/publication/graphical_abstract/HATI_graphical_abstract_v0.1.png` (131,227 B; also `.pdf` 31,340 B, `.svg`) | `submission/final/TMP/HATI_Madrid_Graphical_Abstract_v1.0.png` | PNG | 131,227 B | PASS — no separate caption text exists for the graphical abstract (Elsevier does not require one); content matches the manuscript's screening architecture and headline finding |

## Notes

- PDF and SVG originals also exist for every figure under `outputs/publication/`, in case
  Editorial Manager requests an alternate vector format (e.g. EPS/TIFF) not currently
  produced by the render scripts — regenerate from `outputs/publication/figures/render_fig0*.py`
  if the journal requires a format not already present.
- No figure was found cut off, pixelated at its native resolution, or missing a caption in
  the manuscript's "Figure captions" section.
- The graphical abstract PNG (`HATI_Madrid_Graphical_Abstract_v1.0.png`) measures
  **2656 × 1062 px** (verified by reading the PNG header directly). Elsevier's TMP
  guide-for-authors (per this session's web search) states a minimum of 531 × 1328 px
  (h × w) — this file exceeds both minimums. `WEB VERIFICATION REQUIRED` only for the
  preferred file *type* (TIFF/EPS/PDF/MS-Office are listed as preferred over PNG) — the PDF
  and SVG originals in `outputs/publication/graphical_abstract/` are available as
  alternates if Editorial Manager rejects PNG at upload.
- Supplementary Figure S1 source PNG measures 2967 × 1238 px — high resolution, no
  pixelation risk at print size.
