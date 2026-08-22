# MASTER_PUBLICATION_CHECKLIST.md — HATI-Madrid

Executable checklist. Boxes already checked reflect what this closeout audit verified as
true on 2026-08-22; nothing scientific was changed to check a box.

## Before TMP submission

- [x] Canonical manuscript confirmed (`manuscript/MANUSCRIPT_TMP_v0.2.md` — see
      `submission/final/ADMIN/SCIENTIFIC_INTEGRITY_FINDINGS.md` for the evidence trail)
- [ ] **MAJOR revision items M1–M4 implemented in the manuscript body** (Finding 1 — currently
      OPEN; BLOCKING)
- [ ] Authors confirmed
- [ ] Affiliations confirmed
- [ ] ORCIDs confirmed
- [ ] Corresponding author + email confirmed
- [ ] Funding statement confirmed
- [ ] Declaration of competing interest confirmed
- [ ] CRediT roles assigned
- [ ] Acknowledgements confirmed (or "Not applicable")
- [ ] Generative-AI disclosure statement written in the author's own words
- [ ] Licence decision made for the repository (only needed before Zenodo, not before TMP)
- [ ] Cover letter drafted (verify whether Editorial Manager requires one at upload)
- [ ] Suggested reviewers compiled, if the submission form requires them
- [x] Highlights ready and validated (`submission/final/TMP/HATI_Madrid_Highlights_TMP_v1.0.txt`)
- [x] Graphical abstract ready (`submission/final/TMP/HATI_Madrid_Graphical_Abstract_v1.0.png`)
- [x] Figures 1–4 exported to final PDF (`submission/final/TMP/HATI_Madrid_Figure_0*_v1.0.pdf`)
- [x] Supplementary material exported to final PDF, figure embedded, QA passed
      (`submission/final/TMP/HATI_Madrid_Supplementary_Material_v1.0.pdf`)
- [x] Manuscript exported to docx, QA passed except expected admin placeholders
      (`submission/final/TMP/HATI_Madrid_Manuscript_TMP_v1.0.docx`)
- [ ] TMP guide-for-authors reconfirmed on the official ScienceDirect page (this session's
      network could not reach `sciencedirect.com`/`easychair.org` directly — see
      `PUBLISHING_RUNBOOK.md` §C for what was and was not independently verified)

## TMP submission

- [ ] M1–M4 confirmed implemented (repeat check — do not submit otherwise)
- [ ] Editorial Manager account created/logged in
- [ ] Article type selected
- [ ] All files uploaded in the order/designation specified in `PUBLISHING_RUNBOOK.md` §C
- [ ] Title, abstract, keywords pasted and proofread against the canonical manuscript
- [ ] Author metadata entered exactly as confirmed above
- [ ] Declarations entered exactly as confirmed above
- [ ] Generated submission PDF reviewed end-to-end before final submit
- [ ] Submission confirmation email saved; manuscript ID recorded

## Zenodo release

- [ ] Licence decision made (`submission/final/ADMIN/LICENSE_AUDIT.md`)
- [ ] Authors/ORCID confirmed
- [ ] Repository-visibility decision made (public vs. manual upload — see
      `submission/final/ZENODO/ZENODO_RELEASE_CHECKLIST.md` item 16)
- [ ] Final pre-submission commit tagged (`v1.0-preprint` recommended)
- [ ] GitHub Release created
- [ ] Zenodo metadata entered
- [ ] DOI reserved/published (only after the above)
- [ ] DOI copied into manuscript Data/Code availability statements (if not yet in production)
- [ ] `CITATION.cff` updated with the DOI, licence, version, date

## Preprint

- [ ] M1–M4 confirmed implemented (do not preprint an already-flagged-defective version)
- [ ] Author/declarations fields confirmed
- [ ] Venue confirmed (recommendation: SSRN — see `submission/final/PREPRINT/PREPRINT_UPLOAD_GUIDE.md`)
- [ ] Preprint uploaded
- [ ] Preprint DOI/URL recorded and cross-linked to the Zenodo record

## ENTER27

- [ ] Official CFP re-verified directly (deadline, page limit, portal — flagged
      `WEB VERIFICATION REQUIRED` in this session; `ifitt.net`/`easychair.org` were
      unreachable from this session's network)
- [ ] Poster & Demo abstract drafted using the official ENTER27 template (not yet available
      in this repository)
- [ ] Submission made via EasyChair before the confirmed deadline
- [ ] Confirm no self-plagiarism conflict with the TMP submission before submitting

## Post-submission

- [ ] Day 0: submission confirmed, manuscript ID logged
- [ ] Track status in Editorial Manager
- [ ] If desk rejected: read editor's reason, decide revise-and-resubmit-elsewhere vs. address
      and resubmit; do not resubmit to a second journal without addressing the reason
- [ ] If sent to review: standard wait; do not chase before the journal's stated timeline
- [ ] If revise & resubmit: implement using existing evidence only, per this project's own
      "no new data, no new study" discipline demonstrated in
      `docs/PHASE5_4B2_PRE_SUBMISSION_REVISION_PLAN.md`
- [ ] After acceptance: sign the publishing agreement/licence-to-publish (or pay OA APC if
      open access is chosen — verify current TMP APC, `WEB VERIFICATION REQUIRED`); provide
      final author list/affiliations for typesetting
- [ ] After DOI publication: update `README.md` badges/status, `CITATION.cff`
      `preferred-citation`, and cross-link the Zenodo record's `isSupplementTo` field to the
      published DOI
