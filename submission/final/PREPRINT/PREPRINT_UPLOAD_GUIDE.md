# PREPRINT_UPLOAD_GUIDE.md — HATI-Madrid

**Do not upload the preprint until the Finding 1 MAJOR revision items (M1–M4) are resolved
and the Human-Input-Required author/declarations fields are filled** — a preprint is a
timestamped, effectively permanent public record; uploading `MANUSCRIPT_TMP_v0.2.md` in its
current state would publish a version the project's own review panel has already flagged as
containing MAJOR unaddressed issues, with author/funding fields still blank.

## File

`submission/final/PREPRINT/HATI_Madrid_Preprint_v1.0.pdf` — generated directly from
`manuscript/MANUSCRIPT_TMP_v0.2.md` (the canonical manuscript; identical scientific content
to the journal-submission version, formatted as a single PDF with table of contents). 25
pages. Still contains the `[... TO VERIFY]` placeholders documented in
`submission/final/ADMIN/HUMAN_INPUT_REQUIRED.md` — these must be resolved before upload.

## Venue comparison

| Venue | Fit for HATI-Madrid | Notes |
|---|---|---|
| **Zenodo (as a preprint, not just the software record)** | Good | Zenodo accepts a "preprint" upload type distinct from the software record already planned in `submission/final/ZENODO/`. Would need a **second**, separate Zenodo record (upload type = Preprint) if used, or the two could be linked via `related_identifiers`. Simple, no editorial gate, DOI is fast and citable. Weak discoverability within the tourism/hospitality research community specifically. |
| **SSRN (Social Science Research Network)** | Good | Has a dedicated Tourism & Hospitality Research Network category; strong visibility to the tourism-management readership Tourism Management Perspectives itself draws on. Requires SSRN's own author/affiliation metadata (same blockers as the journal). Elsevier owns SSRN, so cross-linking to a TMP submission is a well-trodden path (SSRN preprints are commonly companion-posted alongside Elsevier tourism-journal submissions). |
| **Docta Complutense / UCM institutional repository** | Conditional | Only applicable if Soroush is formally affiliated with Universidad Complutense de Madrid — this audit does **not** know the author's institutional affiliation (see `HUMAN_INPUT_REQUIRED.md` item 2) and will not assume it. If UCM affiliation is confirmed, this is a strong option for institutional visibility and complies with typical open-access mandates, but it is not a general-purpose preprint server and its submission workflow/turnaround varies by faculty. |

## RECOMMENDED CANONICAL PREPRINT HOME

**SSRN (Tourism & Hospitality Research Network)**

**WHY:** It reaches the same disciplinary readership as Tourism Management Perspectives
(unlike Zenodo, which is discipline-agnostic and mainly serves as a software/data archive
here), it is Elsevier-affiliated so cross-referencing with a TMP submission is standard
practice, and — unlike Docta/UCM — it does not depend on an institutional affiliation this
audit cannot confirm. Use the Zenodo record (`submission/final/ZENODO/`) for the **code and
locked-outputs archive** regardless; that is a separate, complementary artifact, not a
competing preprint choice.

## Upload details (once blockers are resolved)

- **EXACT FILE TO UPLOAD:** `submission/final/PREPRINT/HATI_Madrid_Preprint_v1.0.pdf`
- **EXACT TITLE:** *Thermal representation as a decision variable in heat-adaptive tourism
  opportunity screening: evidence from a Madrid pilot* (the canonical `MANUSCRIPT_TMP_v0.2.md`
  title — do not use the older README/CITATION.cff title; see
  `submission/final/ADMIN/SCIENTIFIC_INTEGRITY_FINDINGS.md` Finding 3)
- **EXACT ABSTRACT:** copy verbatim from `manuscript/MANUSCRIPT_TMP_v0.2.md` Abstract section
  (lines 15–44) — do not paraphrase
- **EXACT AUTHORS:** `[TO VERIFY — see HUMAN_INPUT_REQUIRED.md item 1]`
- **EXACT KEYWORDS:** from `manuscript/00_TITLE_KEYWORDS_v0.1.md` / manuscript front matter
  (6 keywords; confirm they match `MANUSCRIPT_TMP_v0.2.md` exactly before pasting)
- **VERSION LABEL:** v1.0 (pre-journal-submission preprint)
- **RELATION TO JOURNAL SUBMISSION:** Post as a preprint **before or concurrently with** the
  Tourism Management Perspectives submission — Elsevier journals generally permit prior
  preprint posting (confirm current TMP/Elsevier preprint policy at submission time; flagged
  as `WEB VERIFICATION REQUIRED` in `PUBLISHING_RUNBOOK.md`). Update the SSRN/preprint entry
  with the journal DOI once accepted.
- **REPOSITORY DOI:** link to the Zenodo software/data record once minted
  (`submission/final/ZENODO/`), not the other way around — the preprint is the readable
  paper, Zenodo is the reproducibility archive.
