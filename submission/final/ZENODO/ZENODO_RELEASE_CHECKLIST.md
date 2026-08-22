# ZENODO_RELEASE_CHECKLIST.md — HATI-Madrid

Step-by-step for cutting the first citable Zenodo archival release. **Do not execute this
checklist until the BLOCKING items in `ZENODO_METADATA.md` are resolved** (author identity,
licence). This document only prepares the process; nothing here publishes anything.

## 1. Which branch/tag should represent the release

- Current repository state: single `main` branch (this closeout branch mirrors it).
- The scientific snapshot tag already in the repo is **`pre-targeted-revision-v0.2`**
  (points at commit `beedbb1`) — this is the checkpoint **before** the reference-verification
  and (still-incomplete) targeted revision. It is **not** the release candidate.
- **Recommended:** create a new annotated tag on the commit that will actually be submitted
  to the journal, once the manuscript's MAJOR revision items (M1–M4, see
  `submission/final/ADMIN/SCIENTIFIC_INTEGRITY_FINDINGS.md`) are resolved and the commit is
  final. Suggested tag name: `v1.0-preprint` (or `v1.0` if this release is cut only after
  journal submission, per Soroush's preference).
- Do **not** tag and release before the licence decision and the MAJOR revision items are
  closed — a Zenodo DOI is effectively permanent once minted.

## 2. What GitHub Release to create

- On GitHub: **Releases → Draft a new release**, target the tag above, target commit = the
  final pre-submission commit.
- Title: `HATI-Madrid v1.0`
- Body: short description (reuse the Zenodo description field), a link to the manuscript
  (journal submission or preprint, once available), and a note that this release is a
  research-software/data snapshot, not the manuscript itself.

## 3. Exact name recommended

`HATI-Madrid v1.0`

## 4. Tag recommended

`v1.0-preprint` (fallback: `v1.0`)

## 5. Description to use

See `ZENODO_METADATA.md` → Description field. Keep it consistent with the manuscript
abstract; do not add claims not present in the locked manuscript.

## 6. Authors

`[AUTHOR NAME(S) TO VERIFY]` — **BLOCKING.** Do not publish until confirmed by Soroush.

## 7. ORCID

`[ORCID(S) TO VERIFY]` — optional field on Zenodo but should match the journal submission
if supplied there.

## 8. Title

`HATI-Madrid: Heat-Adaptive Tourism Opportunity Screening (Madrid pilot) — v1.0`

## 9. Description

See item 5 / `ZENODO_METADATA.md`.

## 10. Keywords

`urban tourism`; `extreme heat`; `UTCI`; `tourism decision support`; `SOLWEIG`;
`uncertainty-aware decision-making`

## 11. Licence

**Not yet decided.** See `submission/final/ADMIN/LICENSE_AUDIT.md`. Zenodo requires a
licence to be selected before publishing; whichever licence is chosen for the **code** must
be the one declared here (third-party data retains its own licences and should be described
in the record's Notes field, not relicensed).

## 12. Related identifiers

- `isSupplementTo`: journal manuscript DOI (add once assigned) or preprint DOI (add once the
  preprint is live — see `submission/final/PREPRINT/`).
- `isIdenticalTo` / `isSourceOf`: `https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid`
  (repository is currently **private** — see note in item 16).

## 13. Journal relationship

This Zenodo record is a **data/code companion**, not a duplicate submission. Reference it
from the manuscript's Data availability / Code availability statements once the DOI exists
(those statements currently read "on reasonable request" pending this release — see
`manuscript/MANUSCRIPT_TMP_v0.2.md` Declarations).

## 14. What files should be included

- `src/` (analysis pipeline scripts)
- `outputs/tables/`, `outputs/maps/`, `outputs/publication/` (locked results and figures)
- `docs/DATA_SOURCE_INVENTORY.csv`, `docs/PHASE1_DATA_PROVENANCE.md`
- `REPRODUCIBILITY.md`, `requirements.txt`, `app/requirements*.txt`
- `CITATION.cff` (updated with the final DOI after minting — see item 19)
- Either the full repository (via the GitHub→Zenodo integration, which archives the whole
  repo automatically) or a curated zip — **recommend the automatic whole-repo archive** for
  simplicity, since `data/raw/` inputs are open data already documented for provenance.

## 15. What files should NOT be included

- Nothing should be manually excluded if using the GitHub→Zenodo automatic archive (it
  archives the full repository at the tag). If a manual zip is used instead, exclude:
  local virtual environments (already git-ignored), any `.env`/credentials (none exist in
  this repo currently — reconfirm before release), and editor/IDE files.
- The `submission/final/` package itself does not need to be part of the Zenodo software
  archive — it is a publication-logistics folder, not part of the research compendium. Its
  inclusion is harmless but not required.

## 16. How to connect GitHub with Zenodo

1. Go to `https://zenodo.org/account/settings/github/` (login with the ORCID/GitHub account
   that will be the Zenodo record owner).
2. Because this repository is currently **private**, either (a) make it public before
   connecting — this is a bigger decision, not a formatting one, and depends on the licence
   decision and on curating `docs/` per README's note ("internal research/QA record... would
   be curated before any public release"), or (b) use Zenodo's manual upload path instead of
   the GitHub integration for a private repo.
3. If going the public-repo + GitHub-integration route: toggle the repository "on" in the
   Zenodo GitHub settings **before** creating the GitHub Release (Zenodo listens for the
   release webhook).

## 17. When to press Publish (Zenodo)

Only after: (a) the repository visibility decision is made deliberately (public or manual
upload), (b) the licence is chosen, (c) authors/ORCID are confirmed, (d) the GitHub Release
in item 2 exists. **Never publish speculatively** — a Zenodo DOI cannot be deleted, only a
new version can be added.

## 18. When to copy the DOI to the manuscript

Immediately after Zenodo mints the DOI: update the manuscript's Data availability / Code
availability statements (replace "on reasonable request" language) **only if the manuscript
has not yet been typeset by the journal** — if it is already in production, add the DOI at
the proof-correction stage instead, per the journal's instructions.

## 19. How to update CITATION.cff

Replace `version:`, `date-released:`, `repository-code:`, and `license:` fields with the
real values, and add a `doi:` field with the Zenodo-issued DOI once minted. Do this in the
main repository (not only in this closeout package).
