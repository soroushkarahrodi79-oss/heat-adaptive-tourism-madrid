# HUMAN_INPUT_REQUIRED.md — HATI-Madrid

Everything below is a real, currently-open placeholder found in the repository (`CITATION.cff`,
`manuscript/MANUSCRIPT_TMP_v0.2.md` front matter and Declarations, `submission/SUBMISSION_INVENTORY_v0.1.md`).
Nothing has been invented to fill these. Each item states where it blocks.

---

1. **FIELD:** Author name(s), order, and corresponding author.
   **WHY NEEDED:** Manuscript title page, `CITATION.cff`, Zenodo record, ENTER27 submission.
   **WHERE USED:** `manuscript/MANUSCRIPT_TMP_v0.2.md` lines 5–11; `CITATION.cff`;
   `submission/final/ZENODO/`.
   **EXACT VALUE NEEDED:** Full legal name(s) in publication order; which author is
   corresponding, with their institutional email.
   **BLOCKING:** YES — before journal submission (title page cannot be uploaded without it)
   and before DOI release.

2. **FIELD:** Author affiliation(s).
   **WHY NEEDED:** Journal title page; institutional-name verification (TMP screens this).
   **WHERE USED:** Manuscript front matter; `CITATION.cff`.
   **EXACT VALUE NEEDED:** Full or standard-abbreviated institution name(s) per author.
   **BLOCKING:** YES — before journal submission.

3. **FIELD:** ORCID(s).
   **WHY NEEDED:** Increasingly required/strongly requested at Elsevier submission.
   **WHERE USED:** Manuscript front matter; `CITATION.cff`; optionally Zenodo.
   **EXACT VALUE NEEDED:** ORCID iD per author.
   **BLOCKING:** YES for journal submission (Editorial Manager typically requires it at
   account/author-entry stage) — NO for Zenodo (optional there).

4. **FIELD:** Funding statement.
   **WHY NEEDED:** Required Declarations field.
   **WHERE USED:** `manuscript/MANUSCRIPT_TMP_v0.2.md` line 967.
   **EXACT VALUE NEEDED:** Either a grant/funder statement, or the standard "This research
   received no specific grant..." sentence if true.
   **BLOCKING:** YES — before journal submission.

5. **FIELD:** Declaration of competing interest.
   **WHY NEEDED:** Required Declarations field.
   **WHERE USED:** `manuscript/MANUSCRIPT_TMP_v0.2.md` line 971.
   **EXACT VALUE NEEDED:** Standard no-conflict sentence, or actual disclosure.
   **BLOCKING:** YES — before journal submission.

6. **FIELD:** CRediT author-contribution roles.
   **WHY NEEDED:** Required by Tourism Management Perspectives.
   **WHERE USED:** `manuscript/MANUSCRIPT_TMP_v0.2.md` line 986.
   **EXACT VALUE NEEDED:** Per-author CRediT roles (Conceptualization, Methodology, Software,
   Formal analysis, Data curation, Writing, Visualization, etc.) — cannot be assigned without
   knowing the author list (see item 1).
   **BLOCKING:** YES — before journal submission.

7. **FIELD:** Acknowledgements.
   **WHY NEEDED:** Declarations field (can be "Not applicable.").
   **WHERE USED:** `manuscript/MANUSCRIPT_TMP_v0.2.md` line 990.
   **EXACT VALUE NEEDED:** Text, or confirmation that "Not applicable" is correct.
   **BLOCKING:** YES — before journal submission (trivial to close if none apply).

8. **FIELD:** Generative-AI disclosure statement.
   **WHY NEEDED:** Elsevier requires disclosure of GenAI tool use in manuscript preparation;
   the actual wording must reflect the author's real tool use, not be drafted on their behalf.
   **WHERE USED:** `manuscript/MANUSCRIPT_TMP_v0.2.md` line 996; also relevant to this
   closeout session's own AI-assisted packaging work.
   **EXACT VALUE NEEDED:** Soroush's own account of any GenAI assistance used anywhere in
   preparing the manuscript (analysis, writing, editing) — this audit cannot state that on
   the author's behalf.
   **BLOCKING:** YES — before journal submission.

9. **FIELD:** Repository/software licence decision.
   **WHY NEEDED:** README.md states "no repository-wide licence has yet been assigned";
   Zenodo requires a licence before publishing a record.
   **WHERE USED:** `CITATION.cff` line 28; Zenodo record; GitHub repository settings.
   **EXACT VALUE NEEDED:** A licence decision — see `submission/final/ADMIN/LICENSE_AUDIT.md`
   for a recommended structure (this audit recommends but does not choose).
   **BLOCKING:** YES — before Zenodo/DOI release. NOT blocking for journal submission itself
   (the manuscript's data/code-availability text can say "on reasonable request" until then).

10. **FIELD:** Public archive URL/DOI for derived outputs and code (i.e., completing the
    Zenodo release).
    **WHY NEEDED:** Data availability / Code availability statements currently read "on
    reasonable request", which is a weaker statement than most reviewers/editors prefer.
    **WHERE USED:** `manuscript/MANUSCRIPT_TMP_v0.2.md` lines 975–984.
    **EXACT VALUE NEEDED:** The Zenodo DOI, once minted (see item 9's dependency).
    **BLOCKING:** CAN BE COMPLETED LATER — acceptable to submit to the journal with "on
    reasonable request" and update at proof stage, though completing it before submission is
    preferable.

11. **FIELD:** Cover letter content.
    **WHY NEEDED:** `submission/SUBMISSION_INVENTORY_v0.1.md` marks this "not drafted;
    scheduled for a later phase"; TMP's Editorial Manager instance may request one.
    **WHERE USED:** TMP submission upload.
    **EXACT VALUE NEEDED:** A short author-voice letter (journal fit, novelty claim in the
    author's own words, confirmation of no prior/concurrent submission) — this audit does not
    draft it, since a cover letter is inherently an author statement, not packaging.
    **BLOCKING:** CAN BE COMPLETED LATER if the Editorial Manager submission flow does not
    hard-require it at upload; otherwise YES.

12. **FIELD:** Suggested reviewers (if the submission system requires them).
    **WHY NEEDED:** Some Elsevier journals request 3–5 suggested reviewers with no conflicts.
    **WHERE USED:** TMP submission form, if presented.
    **EXACT VALUE NEEDED:** Names/emails of qualified, non-conflicted reviewers — this audit
    will not invent names.
    **BLOCKING:** YES only if the Editorial Manager form makes the field mandatory (see
    `PUBLISHING_RUNBOOK.md` STEP 15 — verify at submission time).

13. **FIELD:** GitHub repository visibility decision (public vs. stays private) and any
    curation of `docs/` before any public exposure.
    **WHY NEEDED:** README.md states the internal phase-gate/audit record in `docs/` "would be
    curated before any public release." A public GitHub↔Zenodo integration requires the repo
    to be public.
    **WHERE USED:** Zenodo release path (item 9/10); ENTER27 "link to GitHub" field, if used.
    **EXACT VALUE NEEDED:** Soroush's decision on whether/when to make the repository public,
    and whether `docs/` phase-gate material should be trimmed or kept.
    **BLOCKING:** YES for the Zenodo GitHub-integration path specifically (a manual-upload
    Zenodo path does not require this). NOT blocking for journal submission.

14. **FIELD:** The Finding 1 MAJOR revision items (M1–M4) in
    `SCIENTIFIC_INTEGRITY_FINDINGS.md`.
    **WHY NEEDED:** These are scientific-interpretation prose edits identified by the
    project's own reviewer panel as capable of causing rejection; this audit is not
    authorized to make them.
    **WHERE USED:** `manuscript/MANUSCRIPT_TMP_v0.2.md` §3.1, §3.2, §4.1, §4.2, §4.3, Intro,
    Discussion §4.5, Conclusion.
    **EXACT VALUE NEEDED:** Author (or authorized editor) implementation of the four smallest-
    defensible-change edits scoped in `docs/PHASE5_4B2_PRE_SUBMISSION_REVISION_PLAN.md`.
    **BLOCKING:** YES — before Tourism Management Perspectives submission.
