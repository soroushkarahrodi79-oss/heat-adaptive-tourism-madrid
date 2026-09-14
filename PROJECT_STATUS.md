# Project status

**Audit date: 2026-09-14. Status: `RELEASE_LOCKED`.**

This file is the canonical status record for HATI-Madrid. It exists to reconcile any
first-page or badge wording with the actual evidence in this repository and its two
public archival records. Where this file and any other document disagree, this file
governs.

---

## 1. Status classification

**`RELEASE_LOCKED`**

The scientific content this repository documents — the single Madrid pilot (21 Aug
2023), the 27 curated assets, the operational-proxy vs SOLWEIG/UTCI comparison, the
eight decision scenarios, the locked result tables, and the four publication figures —
is **fixed**. It is archived under an immutable DOI and republished as a preprint. The
repository's job now is to preserve and correctly describe that locked release, not to
extend it.

Why this label and not another:

- Not `ACTIVE_BOUNDED`: there is no open research work item. Zero open issues, zero
  open pull requests, and the last five merged PRs (2026-09-01 through 2026-09-14)
  changed only documentation/status text — no new science, table, or figure was added
  or altered.
- Not `PAUSED_PENDING_EVIDENCE`: the repository is not idling while waiting on a
  specific external trigger to resume development. Nothing is blocked; the release is
  simply finished and locked.
- Not plain `MAINTENANCE_ONLY`: that label would be accurate too, but it doesn't
  capture *why* — the constraint is that the archived DOI'd artifact (Zenodo
  `10.5281/zenodo.22707470`) is immutable, so any edit to the scientific content here
  would desynchronize the repository from the thing it documents. `RELEASE_LOCKED`
  names that constraint explicitly.

## 2. Current reference

| Artifact | Identifier | Date |
|---|---|---|
| **Repository HEAD / default branch (`main`)** | commit `c6c1190` | 2026-09-14 |
| **GitHub release (citable code snapshot)** | tag [`v0.1.0`](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/releases/tag/v0.1.0) | 2026-09-01 |
| **Preserved pre-revision science checkpoint** | tag `pre-targeted-revision-v0.2` | — |
| **Archived preprint (version-specific)** | Zenodo DOI [`10.5281/zenodo.22707470`](https://doi.org/10.5281/zenodo.22707470) | recorded 2026-09-14 |
| **Archived preprint (concept, always latest)** | Zenodo concept DOI `10.5281/zenodo.22707469` | — |
| **Preprint text (human-readable)** | [ResearchGate](https://www.researchgate.net/publication/414226835_Thermal_representation_as_a_decision_variable_in_heat-adaptive_tourism_opportunity_screening_evidence_from_a_Madrid_pilot) | recorded 2026-09-14 |

**Known gap, flagged rather than fixed here:** the GitHub release tag (`v0.1.0`,
2026-09-01) predates the confirmed ResearchGate/Zenodo publication (2026-09-11 →
confirmed 2026-09-14) and four subsequent merged documentation PRs. `main` and the
Zenodo/ResearchGate text are consistent with each other, but there is currently no
GitHub tag/release that matches the repository's present `main`. Cutting a new tag
(e.g. `v1.0.0`) once the release-status wording below is reviewed would close this
gap — that is a repository-owner action, not made here.

## 3. Demonstrated vs. simulated / derived / provisional / unvalidated

| Demonstrated (in-repo, reproducible) | Simulated / derived / provisional / unvalidated |
|---|---|
| Operational-proxy classification from AEMET hazard bands + OSM tree-count exposure | SOLWEIG-modelled Tmrt and the UTCI derived from it are **model outputs**, never observed thermal comfort |
| Constraint-first, first-failing-gate screening logic and its outputs for the 8 scenarios | "Robust / Boundary / Unstable" confidence labels reflect stability under the *tested* uncertainty dimensions only (solar-forcing realization + targeted canopy geometry), not accuracy or field validation |
| The 14/42 (33.3%) reclassification count and its 9-more-restrictive / 5-less-restrictive split | No field measurement of Tmrt/UTCI exists anywhere in the project |
| The 7/8 scenario change vs. proximity-only baseline, and the S8 no-survivor state | Opening-hours data recorded in 2026 applied retrospectively to the 2023 study day |
| Figure render scripts assert their headline numbers against the locked tables before saving | "Indoor refuge" is an assumed thermal-buffering state, not a physically measured condition |
| ResearchGate URL and Zenodo DOI, owner-confirmed against the live Zenodo record | No tourist behaviour, substitution, or outcome is measured or claimed |
| Publication status (public preprint, non-peer-reviewed, no journal selected) | Author affiliation/ORCID metadata: unresolved, marked `UNKNOWN` in `submission/researchgate/PUBLIC_TRUTH_AUDIT.md`, not invented |

This table summarizes; the authoritative source is the README's *What the project does
not claim* and *Limitations* sections, and `submission/researchgate/PUBLIC_TRUTH_AUDIT.md`.

## 4. Claim ceiling

HATI-Madrid does **not** claim, and this status record does not raise that ceiling:

- SOLWEIG/UTCI as ground truth, or the physical method as more accurate than the proxy;
- that the physical method supplied a richer categorical decision signal (in this
  configuration, all 42 physical-outdoor observations fell into one category);
- any change in tourist behaviour, visitor flow, or safety/health outcome;
- behavioural optimality of any specific alternative;
- generalisation beyond this single bounded Madrid pilot and study day;
- peer review, journal acceptance, or operational/real-time product status;
- validation of `ROBUST` beyond the tested uncertainty dimensions.

## 5. Allowed maintenance changes

Consistent with `RELEASE_LOCKED`, the following are in scope without changing this
status:

- Fixing broken links, typos, formatting, and outdated status wording (as this and the
  prior four merged PRs did);
- Correcting or completing citation/publication metadata (DOIs, ResearchGate/Zenodo
  URLs, `CITATION.cff`) as new *confirming* evidence arrives (e.g., a human verifies
  affiliation/ORCID text);
- Cutting a new GitHub tag/release that matches the current, already-locked `main`, to
  close the gap noted in §2;
- Adding a licence file if the owner selects one (the licence choice itself is not
  made here — see the ambiguity noted below);
- Non-scientific repository administration (visibility, description, README badges)
  that does not alter or reinterpret a locked number, table, or figure.

Out of scope while `RELEASE_LOCKED` holds: new scenarios, new thermal methods, new
study days/areas, changed thresholds, regenerated/altered locked tables or figures,
new claims of validation, or presentation-layer features beyond the existing read-only
replay prototype in `app/`.

## 6. What would reopen development

Any of the following would be grounds to move this status back toward
`ACTIVE_BOUNDED`:

- Field validation data for Tmrt/UTCI (e.g., in-situ sensor readings) that could be
  compared against the modelled field;
- A journal review decision (the manuscript is not currently submitted anywhere; a new
  submission and its outcome would be new evidence);
- A concrete external user/stakeholder need to extend the pilot to a new day, season,
  or district, with the resources to do so under the same evidence standards;
- Observed-behaviour or usability data from the `app/` prototype beyond the existing
  bounded owner desk review recorded in PR #2.

Until one of these occurs, the repository stays in maintenance/documentation mode.

## 7. Open issues and pull requests

As of 2026-09-14: **0 open issues, 0 open pull requests.**

| # | Title | Disposition |
|---|---|---|
| [#1](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/1) | docs: align HATI public status and evidence framing | Merged 2026-09-01. Documentation-only; superseded by later status updates. |
| [#2](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/2) | HATI Spatial Decision Replay — linked scenario inspection | Merged 2026-09-05. Read-only presentation layer over locked outputs; no new science. Desk-reviewed by owner, not field/usability validated. |
| [#3](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/3) | Release/researchgate v1.0 | Merged 2026-09-11. Prepared bounded preprint release package. |
| [#4](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/4) | docs: neutralize preprint release for Zenodo archival | Merged 2026-09-11. Platform-neutral PDF/metadata prep; no scientific content changed. |
| [#5](https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid/pull/5) | docs: confirm ResearchGate + Zenodo publication status | Merged 2026-09-14. Recorded owner-confirmed live ResearchGate and Zenodo records. |

No issue tracker activity has occurred (0 issues opened to date).

---

## Ambiguity flagged, not resolved here

**Repository licence.** No `LICENSE` file exists in this repository. The README
states: *"No repository-wide licence has yet been assigned... until then, please
treat the code and text as 'all rights reserved' and contact the author before
reuse."* This is a genuine open decision for the repository owner, not a gap this
audit can close — assigning a licence is a substantive legal choice, not a
documentation fix, so it is intentionally left unresolved and unassigned here. Note
that the Zenodo record's own licensing terms (if any were set during deposit) may
differ from the repository's code/text licensing; that is outside this repository's
version control and was not verified as part of this audit.
