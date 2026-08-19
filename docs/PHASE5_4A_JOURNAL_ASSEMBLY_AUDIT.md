# PHASE5_4A_JOURNAL_ASSEMBLY_AUDIT.md — HATI-Madrid Phase 5.4A

Version 1.0 · 2026-08-18. Audit of the journal-ready assembly
`manuscript/MANUSCRIPT_TMP_v0.1.md`. No scientific analysis, numerical result, modelling
choice, visual claim, title, Abstract claim, or literature positioning was changed. Assembly
edits were mechanical and are logged below (produced by
`scripts_assembly/assemble_tmp_manuscript.py`).

---

## 1. Exact assembly edits

Applied to the locked body; prose otherwise verbatim.

- **Front/back matter added:** title + author placeholders; Abstract (verbatim from
  `00_ABSTRACT_v0.1.md`); keywords; Declarations; References (23); Figure captions (1–4);
  Table captions (1–3). No approved sentence rewritten.
- **Section renumbering (harmonisation):** headings `# 3→2 Methods`, `# 4→3 Results`,
  `# 5→4 Discussion`, `# 6→5 Limitations`, `# 7→6 Conclusion`; subsections Methods 3.x→2.x
  (9), Results 4.x→3.x (3), Discussion 5.x→4.x (5), Limitations 6.x→5.x (7).
- **Internal cross-references:** `Section 3.4→2.4` (×2), `Section 3.2→2.2` (×1),
  `Section 4.1→3.1` (×1).
- **Figure cross-references:** `Fig. 3→Fig. S1` (×1, the UTCI field, now supplementary);
  `Fig. 6→Fig. 3` (×2, screening). Fig. 2 and Fig. 4 unchanged.
- **Table cross-references:** `Table 3→Table S1` (×2, thermal-method, now supplementary);
  `Table 4→Table 3` (×2, scenarios).
- **Figure/table citations added (cross-ref completeness, parentheticals only):** `(Fig. 1a)`
  in Methods 2.1; `(Table 1)` in Methods 2.2; `(Table 2)` and `(Fig. 1b)` in Methods 2.7.
- **Citation-format normalization:** in-text journal names stripped and keys harmonised to a
  single `(short-key, year)` / `(Author et al., year)` style (19 distinct in-text citation
  strings normalised; verbatim log in the assembly script output).
- **Removed** the leading HTML assembly comment.

## 2. Figure-reference integrity

Main figures cited in ascending order: **Fig. 1 (Methods) < Fig. 2 (Results 3.1) < Fig. 3
(Results 3.2) < Fig. 4 (Results 3.3)** — verified mechanically by first-occurrence position.
`Fig. S1` appears only as a supplementary reference (Results 3.1). No `Fig. 5`/`Fig. 6`
remains; no dashboard/screenshot reference in the body. Every main figure is cited naturally;
none inserted purely for ordering. ✓

## 3. Table-reference integrity

`Table 1` (Methods 2.2), `Table 2` (Methods 2.7), `Table 3` (Results 3.2) all cited; `Table
S1` (Results 3.1) cited as supplementary. No `Table 4` remains. Editable tables exist at
`manuscript/tables/TABLE01–03*.md` (+ `TABLE03_scenarios.csv`); no table rendered as an
image. ✓

## 4. Reference-list integrity

`docs/PHASE5_4A_REFERENCE_AUDIT.csv`: **23 citations, 23 with exactly one reference entry,
0 orphans, 0 missing entries.** 5 entries carry author names (Bröde, Colaninno, Gál &
Kántor, Lindberg, OECD); 18 are flagged `[REFERENCE METADATA TO VERIFY]` for author
list/volume/pages/DOI — none fabricated. Titles, journals, and years come from the locked
literature record. ✓ (flagged, not clean, by design)

## 5. Citation-style consistency

One author–year style throughout: `(Author et al., year)` where authors are known,
`(short-key, year)` otherwise; multiple citations separated by `;` within one parenthesis;
`OECD (2026)` as an organisational author; no in-text journal names remain (scan clean).
Section cross-references use `Section n.n`. ✓

## 6. Declaration placeholders

Present with explicit placeholders: Funding, Competing interest, Data availability (bounded
draft + repo-URL placeholder), Code availability (placeholder), CRediT, Acknowledgements,
Ethics (bounded: no human subjects), Generative-AI disclosure (publisher-requirement
placeholder, not drafted on authors' behalf). No administrative fact invented. ✓

## 7. Supplementary architecture

`supplementary/SUPPLEMENTARY_MATERIAL_v0.1.md`: Figure S1 (UTCI field); Table S1
(thermal-method exact rates incl. morphology); Table S2 (solar-forcing + confidence +
BOUNDARY/UNSTABLE detail); Table S3 (exclusion-reason frequencies); Table S4 (opening-hours
provenance); S5 (software/reproducibility). Each item justified (reproducibility or exact
detail behind a main figure); no repository dump. All referenced from the main text. ✓

## 8. Word counts

`docs/PHASE5_4A_WORD_COUNT_MAP.md`: Abstract 247; main text 8,746 (Intro 1,267 · Methods
2,818 · Results 1,209 · Discussion 1,841 · Limitations 1,212 · Conclusion 399); figure
captions 497; table captions 118; supplementary 667; references 23. Measurement only; no
compression performed this phase. ✓

## 9. Claim-protection pass (captions/tables/supplementary + body)

Every occurrence of accurate/accuracy/correct/validation/validated/ground truth/recommend/
real heat reviewed: all are negations, technical terms (canopy *correction*), engine state
names (`NOT RECOMMENDED`, `no-recommendation`), the baseline name (nearest-open
*recommender*), or the "Validation strategy" section title. `better/superior/underestimated/
overestimated/safer/optimal/incorrect` → **zero occurrences.** Figure 2 caption states "not
the correctness of either"; Figure 4 caption states robustness is "not total uncertainty …
not a validation"; Figure S1/Table captions use "model-derived UTCI". No caption or table
heading implies physical model = truth. ✓

## 10. Unresolved administrative inputs

Author names/affiliations/corresponding author/ORCID; funding; competing-interest statement;
CRediT roles; acknowledgements; public data/code repository URL + release DOI; generative-AI
disclosure wording; reference metadata (author lists/volumes/pages/DOIs) for 18 references;
journal-template format export (.docx/.pdf, figure TIFF); cover letter and suggested
reviewers (later phase). All are captured as explicit placeholders in the manuscript and in
`submission/SUBMISSION_INVENTORY_v0.1.md`.

## 11. Remaining scientific inconsistency

**None found.** No locked numerical result, claim, framing, figure, or literature-positioning
statement was altered; the body prose is verbatim except the logged mechanical edits;
section/figure/table numbering is final and internally consistent; and the claim ceiling is
intact throughout the assembled document, captions, tables, and supplementary.

---

## GATE

Complete manuscript assembled in journal order; no locked scientific claim changed; figure
numbering final and consistent (1–4 main, S1 supplementary; no obsolete Fig 5/6 or Table 4);
editable tables integrated (none as images); supplementary material coherent and fully
cross-referenced; reference/citation integrity clean or explicitly flagged
(`[REFERENCE METADATA TO VERIFY]`, no fabrication); captions scientifically bounded with no
superiority/behavioural drift; declarations present or transparently placeholdered; and the
remaining administrative inputs are listed.

**JOURNAL MANUSCRIPT ASSEMBLED**
