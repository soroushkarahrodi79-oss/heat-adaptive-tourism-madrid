# PUBLISHING_RUNBOOK.md — HATI-Madrid

Read this file top to bottom. It is written for someone with no prior context on this
project who has access to the publication accounts. Nothing in this package or this
runbook has published anything — every irreversible action (submit, publish DOI, post
preprint) is still a human decision, gated below.

---

## A. FINAL VERDICT

**Status: NOT READY.**

The manuscript's own four-reviewer QA process (`docs/PHASE5_4B2_PRE_SUBMISSION_REVISION_PLAN.md`)
identified 4 MAJOR issues in the current text — two explicitly flagged as capable of causing
desk rejection or credibility damage at Tourism Management Perspectives. README.md and
CITATION.cff both state this revision "has been completed," but the branch they cite
(`phase-5.4b3-targeted-revision`) does not exist in the repository, and the issue register
(`docs/PHASE5_4B2_MASTER_ISSUE_REGISTER.csv`) shows all 13 tracked issues, including all 4
MAJORs, still `OPEN`. Only a separate, earlier phase (reference verification) was actually
merged into the canonical manuscript. Full evidence:
`submission/final/ADMIN/SCIENTIFIC_INTEGRITY_FINDINGS.md`, Finding 1.

Separately, author identity, affiliation, ORCID, funding, competing-interest, CRediT,
acknowledgements, and licence are all unresolved placeholders (never fabricated by this
audit — see `submission/final/ADMIN/HUMAN_INPUT_REQUIRED.md`).

Everything that **could** be prepared without touching scientific content has been prepared
and is ready to use the moment the two blockers above close: manuscript and supplementary
exports, figures, highlights, graphical abstract, and every guide in this folder.

---

## 1. The paper we are publishing

**Title:** *Thermal representation as a decision variable in heat-adaptive tourism
opportunity screening: evidence from a Madrid pilot*
**Canonical manuscript:** `manuscript/MANUSCRIPT_TMP_v0.2.md`
**Target journal:** Tourism Management Perspectives (Elsevier / ScienceDirect)
**Article type:** Research article (standard full-length submission; reconfirm the exact
article-type label offered in Editorial Manager at submission time — `WEB VERIFICATION
REQUIRED`, see §C)

---

## B. EXACT FILE INVENTORY

| # | Exact file | Purpose | Destination | Required? | Ready? |
|---|---|---|---|---|---|
| 1 | `submission/final/TMP/HATI_Madrid_Manuscript_TMP_v1.0.docx` | Main manuscript | TMP / Editorial Manager | Yes | Content YES, admin fields NO (11 placeholders) |
| 2 | `submission/final/TMP/HATI_Madrid_Highlights_TMP_v1.0.txt` | Highlights (5 bullets) | TMP / Editorial Manager | Yes | YES |
| 3 | `submission/final/TMP/HATI_Madrid_Graphical_Abstract_v1.0.png` | Graphical abstract | TMP / Editorial Manager | Yes | YES (PDF/SVG originals also exist in `outputs/publication/graphical_abstract/` if the system prefers vector) |
| 4 | `submission/final/TMP/HATI_Madrid_Figure_01_Study_Design_v1.0.pdf` | Figure 1 | TMP / Editorial Manager | Yes | YES |
| 5 | `submission/final/TMP/HATI_Madrid_Figure_02_Thermal_Method_Divergence_v1.0.pdf` | Figure 2 | TMP / Editorial Manager | Yes | YES |
| 6 | `submission/final/TMP/HATI_Madrid_Figure_03_Screening_Consequence_v1.0.pdf` | Figure 3 | TMP / Editorial Manager | Yes | YES |
| 7 | `submission/final/TMP/HATI_Madrid_Figure_04_Tested_Uncertainty_v1.0.pdf` | Figure 4 | TMP / Editorial Manager | Yes | YES |
| 8 | `submission/final/TMP/HATI_Madrid_Supplementary_Material_v1.0.pdf` | Supplementary material | TMP / Editorial Manager | Yes | Content YES, 1 admin placeholder (repository DOI, pending Zenodo) |
| 9 | `submission/final/PREPRINT/HATI_Madrid_Preprint_v1.0.pdf` | Preprint upload | SSRN (recommended) | Optional but recommended | Content YES, admin fields NO |
| 10 | `submission/final/ZENODO/ZENODO_METADATA.md` / `ZENODO_RELEASE_CHECKLIST.md` | Zenodo prep | Internal | Yes (before DOI release) | Guides ready; licence + authors still open |
| 11 | `submission/final/ENTER27/ENTER27_SUBMISSION_GUIDE.md` | ENTER27 prep | Internal | Yes (before ENTER27 submission) | Guide ready; official CFP not independently re-verified this session |
| 12 | `submission/final/ADMIN/*.md` | Findings, blockers, licence audit | Internal | Yes (read first) | Ready |
| 13 | `submission/final/FILE_MANIFEST.csv` | SHA-256 + metadata for every final artifact | Internal record | Yes | Ready |
| 14 | `submission/final/MASTER_PUBLICATION_CHECKLIST.md` | Execution checklist | Internal | Yes | Ready |

No hypothetical files are listed above that do not exist on disk; a cover letter and an
ENTER27 poster PDF are intentionally **not** in this table because they do not yet exist
(see §7 and `submission/final/ENTER27/ENTER27_SUBMISSION_GUIDE.md`).

---

## C. TOURISM MANAGEMENT PERSPECTIVES — CLICK-BY-CLICK

`WEB VERIFICATION REQUIRED` note: this session's network egress blocked direct access to
`sciencedirect.com` and the Editorial Manager domain; the requirements below are drawn from
what WebSearch could retrieve (search-result summaries citing the official ScienceDirect
guide-for-authors page) and from general, current Elsevier/Editorial-Manager convention.
**Before uploading, open the live guide-for-authors page yourself and re-confirm every field
below** — do not trust this runbook as the final word on exact character limits or field
names, which Elsevier updates periodically.

**STEP 1**
Open:
`https://www.sciencedirect.com/journal/tourism-management-perspectives/publish/guide-for-authors`
— confirm current requirements, then follow the "Submit your paper" link to the journal's
Editorial Manager instance (Elsevier journals submit via Editorial Manager, linked from this
page; `WEB VERIFICATION REQUIRED` for the exact URL, which this session could not load).

**STEP 2**
Click:
"Author Login" / "Register" on Editorial Manager, then "Submit New Manuscript."

**STEP 3**
Select article type:
`WEB VERIFICATION REQUIRED` — confirm the exact label (commonly "Research Paper" or "Full
Length Article" for Elsevier tourism journals; do not guess blindly, check the dropdown).

**STEP 4**
Upload:
`submission/final/TMP/HATI_Madrid_Manuscript_TMP_v1.0.docx`
File designation:
"Manuscript" / "Main document" (exact label per the system's upload-item list)

**STEP 5**
Upload:
`submission/final/TMP/HATI_Madrid_Highlights_TMP_v1.0.txt`
File designation: "Highlights"

**STEP 6**
Upload:
`submission/final/TMP/HATI_Madrid_Graphical_Abstract_v1.0.png`
File designation: "Graphical Abstract"

**STEP 7**
Upload:
`submission/final/TMP/HATI_Madrid_Figure_01_Study_Design_v1.0.pdf` through
`HATI_Madrid_Figure_04_Tested_Uncertainty_v1.0.pdf`
File designation: "Figure" (one per upload slot, in order 1–4)

**STEP 8**
Upload:
`submission/final/TMP/HATI_Madrid_Supplementary_Material_v1.0.pdf`
File designation: "Supplementary material for review" / "Supplementary data"

**STEP 9**
Paste title:
`Thermal representation as a decision variable in heat-adaptive tourism opportunity
screening: evidence from a Madrid pilot`

**STEP 10**
Paste abstract (verbatim, do not shorten or paraphrase):
> Extreme heat is a time- and place-sensitive management problem for urban tourism, yet
> broad climate-suitability assessment operates at a coarse scale, while downstream thermal
> routing and heat-adjusted accessibility presuppose the candidate set, leaving open the
> upstream question of which tourism opportunities should remain feasible candidates at a
> given hour. This study develops a constraint-first, uncertainty-aware architecture for
> screening urban tourism opportunities under heat and tests how much the choice of thermal
> representation matters. On a documented extreme-heat day in Madrid, across 27 tourism
> assets at three times of day, feasibility was assessed two ways: with a simple operational
> proxy combining ambient air-temperature hazard thresholds and nearby tree-presence
> information, and with physically based SOLWEIG/UTCI modelling. Changing the thermal
> representation reclassified one third of outdoor asset-time observations (33.3%, 14 of
> 42), in both directions. Relative to a conventional nearest-open baseline, constraint-first
> screening changed the feasible-alternative set in 7 of 8 decision scenarios, the
> nearest-open option failed screening in 3 of 8, and one scenario returned an explicit
> no-defensible-alternative outcome when no candidate qualified. The analysis evaluates
> decision sensitivity to thermal-method choice rather than the accuracy of either method
> against ground truth. The findings indicate that thermal representation is a substantive
> modelling choice in heat-adaptive tourism decision support, and that a constraint-first
> architecture can expose that sensitivity while keeping uncertainty, evidence, and exclusion
> logic explicit and complementing downstream routing and accessibility methods. Results are
> limited to a single Madrid pilot without direct field validation of Tmrt/UTCI or observed
> tourist behaviour.

**STEP 11**
Keywords (paste exactly, one per field):
1. Urban tourism
2. Extreme heat
3. UTCI
4. Tourism decision support
5. SOLWEIG
6. Uncertainty-aware decision-making

**STEP 12**
Authors:
`[HUMAN INPUT REQUIRED — see submission/final/ADMIN/HUMAN_INPUT_REQUIRED.md items 1–3]`. Do
not proceed past this step until name(s), affiliation(s), ORCID(s), and the corresponding
author/email are confirmed.

**STEP 13**
Funding:
`[HUMAN INPUT REQUIRED — item 4]`

**STEP 14**
Conflict of interest:
`[HUMAN INPUT REQUIRED — item 5]`

**STEP 15**
Data availability (paste, once the Zenodo DOI exists; otherwise paste as-is with the
"on reasonable request" wording, which is truthful in the interim):
> This study uses only open data: meteorological observations from AEMET (Madrid/Barajas
> station); three-dimensional urban geometry from Spanish national LiDAR products
> (IGN/CNIG); and tourism assets, tree points, park/garden polygons, and opening-hours tags
> from OpenStreetMap (ODbL). The derived analytical tables and figures reported here are
> produced by the project pipeline from these locked inputs. [Insert the Zenodo DOI here once
> minted; until then: "A persistent public archive is being prepared; data are available on
> reasonable request from the corresponding author."]

**STEP 16**
Code availability (paste, same DOI caveat as Step 15):
> The screening pipeline and figure-rendering scripts are held in the project repository.
> [Insert the public repository URL / licence / release DOI here once available.]

**STEP 17**
Generative-AI disclosure:
`[HUMAN INPUT REQUIRED — item 8]`. Do not paste a disclosure statement this audit did not
verify against the author's actual tool use.

**STEP 18**
Suggested reviewers:
Only fill in if the Editorial Manager form marks this mandatory. `[HUMAN INPUT REQUIRED —
item 12]` — never invent names.

**STEP 19**
Review generated submission PDF:
Editorial Manager auto-assembles a single PDF from the uploads — check, in order: (a) figures
appear in the right order and are not cut off or pixelated; (b) the manuscript text and the
uploaded docx match (no silent reflow errors); (c) no `TO VERIFY` bracket text survived into
the final PDF (search it); (d) highlights and graphical abstract appear where expected; (e)
references render correctly with no broken numbering.

**STEP 20**
Final submit:
Immediately before clicking Submit, re-confirm: (1) M1–M4 from
`submission/final/ADMIN/SCIENTIFIC_INTEGRITY_FINDINGS.md` are implemented in the uploaded
docx — **do not submit otherwise**; (2) every `[HUMAN INPUT REQUIRED]` field above has a real
value, not a placeholder; (3) the corresponding author's email is correct (it receives all
future correspondence).

---

## D. DO NOT UPLOAD

- `README.md`
- Anything under `docs/` (phase gates, audits, reviewer attack maps, issue registers — these
  are the internal QA record, not submission material; per README.md they would be "curated
  before any public release" and were never meant for the journal)
- `manuscript/MANUSCRIPT_TMP_v0.1.md` and `manuscript/MANUSCRIPT_v0.1.md` (superseded drafts
  — see §28 disposition table below)
- `scripts_assembly/` internal build scripts
- Raw Git history, commit logs, or this closeout session's own working notes
- `app/` source code (the Dash prototype is for the ENTER27 demo track, not for the journal)
- Anything from `submission/final/ADMIN/` (these are internal findings/blocker documents
  written for Soroush, not for the journal)

---

## E. ZENODO — CLICK-BY-CLICK

See `submission/final/ZENODO/ZENODO_RELEASE_CHECKLIST.md` for the full 19-item checklist.
Summary:

- **WHERE TO GO:** `https://zenodo.org/account/settings/github/` to connect GitHub (only if
  making the repo public — see the checklist item 16 decision), or `https://zenodo.org/deposit/new`
  for a manual upload.
- **WHAT TO CLICK:** "New Upload" (manual path) or toggle the repo "on" then cut a GitHub
  Release (integration path).
- **WHAT RELEASE TO SELECT:** the final pre-submission commit, tagged `v1.0-preprint`.
- **WHAT TITLE TO USE:** `HATI-Madrid: Heat-Adaptive Tourism Opportunity Screening (Madrid pilot) — v1.0`
- **WHAT DESCRIPTION TO USE:** see `ZENODO_METADATA.md`.
- **WHAT AUTHORS:** `[HUMAN INPUT REQUIRED]`
- **WHAT ORCIDS:** `[HUMAN INPUT REQUIRED — optional field]`
- **WHAT LICENSE:** `[HUMAN INPUT REQUIRED — see LICENSE_AUDIT.md]`
- **WHAT KEYWORDS:** Urban tourism; Extreme heat; UTCI; Tourism decision support; SOLWEIG;
  Uncertainty-aware decision-making
- **WHAT VERSION:** v1.0
- **WHAT DATE:** the date the GitHub Release is actually cut (not the audit date above)
- **WHAT RELATED IDENTIFIER:** the journal manuscript DOI once assigned, or the SSRN preprint
  DOI in the interim (`isSupplementTo`)
- **WHEN TO RESERVE DOI:** only after the licence and author blockers close
- **WHEN TO PUBLISH DOI:** only after the GitHub Release exists and all metadata is final —
  Zenodo DOIs cannot be deleted
- **HOW TO VERIFY AFTERWARD:** open the DOI URL (`https://doi.org/10.5281/zenodo.XXXXXXX`)
  and confirm it resolves to the correct release title/version/files before citing it
  anywhere.

---

## F. PREPRINT — CLICK-BY-CLICK

See `submission/final/PREPRINT/PREPRINT_UPLOAD_GUIDE.md` for the full comparison and
recommendation (**SSRN**). Summary:

- **EXACT FILE TO UPLOAD:** `submission/final/PREPRINT/HATI_Madrid_Preprint_v1.0.pdf`
- **EXACT TITLE / ABSTRACT:** identical to §C Steps 9–10 above
- **EXACT AUTHORS:** `[HUMAN INPUT REQUIRED]`
- **EXACT KEYWORDS:** identical to §C Step 11
- **VERSION LABEL:** v1.0 (pre-journal-submission preprint)
- **RELATION TO JOURNAL SUBMISSION:** post before or alongside the TMP submission; update
  with the journal DOI once accepted (`WEB VERIFICATION REQUIRED`: reconfirm Elsevier/TMP's
  current preprint policy before posting)
- **REPOSITORY DOI:** cross-link to the Zenodo record once minted (§E)

---

## G. ENTER27 — CLICK-BY-CLICK

See `submission/final/ENTER27/ENTER27_SUBMISSION_GUIDE.md` for full reasoning. Summary:

- **SUBMISSION CATEGORY:** Poster & Demo (confirmed appropriate; do NOT submit a full paper —
  risks self-plagiarism conflict with the TMP submission)
- **OFFICIAL PORTAL:** EasyChair, `https://easychair.org/cfp/ENTER27` (unreachable from this
  session's network — `WEB VERIFICATION REQUIRED`)
- **DEADLINE:** `WEB VERIFICATION REQUIRED` — reported range September–November 2026 across
  categories; confirm the poster/demo-specific date directly
- **EXACT FILE:** not yet created — build from the official ENTER27 poster template once
  obtained (A2 format), reusing `submission/final/TMP/HATI_Madrid_Figure_0*_v1.0.pdf` and the
  graphical abstract
- **TITLE / ABSTRACT / AUTHORS / KEYWORDS:** same as §C, adapted to a poster-length abstract
  (not yet drafted — `WEB VERIFICATION REQUIRED` for the exact length/template)
- **DEMO DESCRIPTION:** the `app/` Dash prototype, described explicitly as illustrative /
  not a validated product (per README.md)
- **LINK TO LIVE DEMO / GITHUB:** only if the repository visibility decision (§ Zenodo item
  16) makes the repo public; otherwise do not link a private repository publicly
- **WHAT NOT TO SUBMIT:** the full manuscript; any framing implying the Dash prototype is
  validated software

---

## H. MASTER CHECKLIST

See `submission/final/MASTER_PUBLICATION_CHECKLIST.md`.

## I. FILE MANIFEST

See `submission/final/FILE_MANIFEST.csv` (SHA-256 + size + QA status for every artifact in
this package).

---

## 7. What I must NEVER upload

- `README.md`, `docs/`, superseded manuscript drafts, `scripts_assembly/`, raw Git history
  reports, this closeout session's internal notes, `app/` source as if it were the paper —
  see §D above for the full list and reasoning.

## 8. Human actions remaining (BLOCKERS BEFORE I CAN PRESS SUBMIT)

1. **BLOCKER:** MAJOR revision items M1–M4 not implemented in the manuscript body.
   **EXACT ACTION FOR SOROUSH:** apply the 4 smallest-defensible-change edits scoped in
   `docs/PHASE5_4B2_PRE_SUBMISSION_REVISION_PLAN.md` (§"MUST FIX BEFORE SUBMISSION") to
   `manuscript/MANUSCRIPT_TMP_v0.2.md`, then re-run this closeout's export step to regenerate
   `submission/final/TMP/HATI_Madrid_Manuscript_TMP_v1.0.docx` and the preprint PDF.
   **TIME/COMPLEXITY:** small — the plan states each fix is existing-evidence-only prose,
   roughly 1–2 paragraphs across 4 sections; a few hours of focused editing.
   **FILES AFFECTED:** `manuscript/MANUSCRIPT_TMP_v0.2.md` §§1, 3.1, 3.2, 4.1, 4.2, 4.3, 4.5,
   Conclusion.

2. **BLOCKER:** Author identity/affiliation/ORCID/corresponding author unresolved.
   **EXACT ACTION:** supply the real values (see `HUMAN_INPUT_REQUIRED.md` items 1–3).
   **TIME/COMPLEXITY:** trivial (a few minutes) once decided.
   **FILES AFFECTED:** `manuscript/MANUSCRIPT_TMP_v0.2.md`, `CITATION.cff`, all exports in
   `submission/final/`.

3. **BLOCKER:** Funding / competing-interest / CRediT / acknowledgements statements blank.
   **EXACT ACTION:** supply real text or the standard "none/not applicable" sentences.
   **TIME/COMPLEXITY:** trivial (minutes).
   **FILES AFFECTED:** `manuscript/MANUSCRIPT_TMP_v0.2.md` Declarations.

4. **BLOCKER:** Generative-AI disclosure statement not written.
   **EXACT ACTION:** Soroush states, in his own words, any GenAI tool use across the
   project's preparation (this closeout session's own AI-assisted packaging work included).
   **TIME/COMPLEXITY:** trivial (minutes) but requires the author's own account, not a
   drafted-for-them statement.
   **FILES AFFECTED:** `manuscript/MANUSCRIPT_TMP_v0.2.md` Declarations.

5. **BLOCKER:** Repository licence undecided.
   **EXACT ACTION:** choose a software licence (recommendation: MIT or Apache-2.0, see
   `LICENSE_AUDIT.md`) and add a `LICENSE` file; confirm no conflict with OSM/ODbL,
   IGN CC-BY 4.0, Copernicus, or EUMETSAT terms.
   **TIME/COMPLEXITY:** small (an hour, mostly decision time).
   **FILES AFFECTED:** new `LICENSE` file, `CITATION.cff`, Zenodo metadata.

6. **BLOCKER:** Repository-visibility decision (public vs. stays private) for the
   Zenodo↔GitHub integration path.
   **EXACT ACTION:** decide, and if going public, review `docs/` for anything Soroush does
   not want exposed (per README.md's own note that it "would be curated before any public
   release").
   **TIME/COMPLEXITY:** medium (requires actually reading through `docs/`, ~1 hour).
   **FILES AFFECTED:** GitHub repository settings; potentially `docs/` contents.

7. **BLOCKER:** TMP/Editorial Manager guide-for-authors not independently re-verified from
   the live page (this session's network could not reach `sciencedirect.com`).
   **EXACT ACTION:** open the guide-for-authors URL in §C Step 1 directly and confirm article
   type label, exact highlights character limit, and any recently changed requirement.
   **TIME/COMPLEXITY:** trivial (10 minutes).
   **FILES AFFECTED:** none — verification only, informs §C execution.

8. **BLOCKER:** ENTER27 official CFP not independently re-verified (network-blocked this
   session).
   **EXACT ACTION:** open `https://ifitt.net/event/enter27/` and
   `https://easychair.org/cfp/ENTER27` directly; confirm the Poster & Demo deadline and
   template.
   **TIME/COMPLEXITY:** trivial (10 minutes).
   **FILES AFFECTED:** none — verification only.

9. **BLOCKER:** Cover letter not drafted.
   **EXACT ACTION:** Soroush writes a short author-voice letter (journal fit, novelty claim,
   no concurrent submission confirmation); verify first whether Editorial Manager requires
   one at upload.
   **TIME/COMPLEXITY:** small (30–60 minutes).
   **FILES AFFECTED:** new file in `submission/final/TMP/` once drafted.

10. **BLOCKER:** Zenodo DOI not yet minted, so Data/Code availability statements still read
    "on reasonable request."
    **EXACT ACTION:** complete blockers 5–6 first, then execute
    `ZENODO_RELEASE_CHECKLIST.md`.
    **TIME/COMPLEXITY:** small once 5–6 are resolved (~30 minutes of clicking).
    **FILES AFFECTED:** `manuscript/MANUSCRIPT_TMP_v0.2.md` Declarations (only if updated
    before submission; otherwise updated at proof stage), `CITATION.cff`.

## 9. The exact order I should now follow

1 → resolve blocker 1 (M1–M4 manuscript revision) — this is the only item that touches
    scientific-interpretive text and must happen first, since every export downstream of it
    needs to be regenerated afterward.
2 → resolve blockers 2–4 (author identity, declarations, AI disclosure) in parallel with 1.
3 → re-export `HATI_Madrid_Manuscript_TMP_v1.0.docx` and `HATI_Madrid_Preprint_v1.0.pdf` from
    the revised `MANUSCRIPT_TMP_v0.2.md` (same pandoc/xelatex commands used to build this
    package — see `REPRODUCIBILITY.md`-style note: `pandoc manuscript/MANUSCRIPT_TMP_v0.2.md
    -f markdown -t docx -o ... --standalone`).
4 → resolve blocker 7 (TMP guide-for-authors live re-check).
5 → upload to Tourism Management Perspectives per §C.
6 → resolve blockers 5–6 (licence, repo visibility) → execute the Zenodo checklist (§E).
7 → post the preprint to SSRN (§F), cross-linked to the Zenodo DOI.
8 → resolve blocker 8 (ENTER27 CFP re-check) → prepare and submit the Poster & Demo (§G).
9 → track post-submission per `MASTER_PUBLICATION_CHECKLIST.md` "Post-submission" section.

## 10. GO / NO-GO

**NO-GO — FIX THESE BLOCKERS FIRST**
