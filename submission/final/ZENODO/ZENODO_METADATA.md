# ZENODO_METADATA.md — HATI-Madrid

Draft metadata for the Zenodo record that will archive the HATI-Madrid research-software
snapshot. **Nothing here has been submitted to Zenodo.** No DOI has been reserved or
published. Fields marked `TO VERIFY` require Soroush's confirmation before the record is
created; do not fill them from guesswork.

| Field | Value | Status |
|---|---|---|
| Title | `HATI-Madrid: Heat-Adaptive Tourism Opportunity Screening (Madrid pilot) — v1.0` | Draft, follows repository name; confirm before release |
| Upload type | Software | Fixed |
| Description | *(short version)* "Reproducible pilot analysis pipeline and locked outputs for HATI-Madrid, a constraint-first, uncertainty-aware screening architecture comparing an operational thermal proxy against a SOLWEIG/UTCI physically based configuration for urban-tourism opportunity screening under extreme heat in central Madrid (21 August 2023)." | Draft — may be lengthened; do not add claims beyond the manuscript abstract |
| Authors | `[AUTHOR NAME(S) TO VERIFY]` — README/Contact section names **Soroush Karahrodi** (GitHub `@soroushkarahrodi79-oss`) as the identified contact, but the full author list/order for the citable record has not been confirmed | **TO VERIFY — BLOCKING** |
| ORCID(s) | `[ORCID TO VERIFY]` | **TO VERIFY — BLOCKING for author identity, not for record creation (ORCID is optional on Zenodo)** |
| Affiliation(s) | `[AFFILIATION TO VERIFY]` | **TO VERIFY** |
| Version | `v1.0` (first public archival release) | Recommend, confirm before publish |
| Publication date | Date of GitHub Release creation (not today's audit date) | Set at release time |
| License | **Not yet chosen** — see `LICENSE DECISION REQUIRED` in README and `submission/final/ADMIN/LICENSE_AUDIT.md` in this package | **BLOCKING** |
| Keywords | `urban tourism`; `extreme heat`; `UTCI`; `tourism decision support`; `SOLWEIG`; `uncertainty-aware decision-making` (from `CITATION.cff`) | Ready |
| Related identifiers | `isSupplementTo` → the Tourism Management Perspectives manuscript (add the journal DOI once assigned, or the preprint DOI in the interim); `isSourceOf`/`isIdenticalTo` → the GitHub repository URL and the specific tagged commit | Draft — journal DOI not yet assigned |
| Communities | None selected | Optional — leave blank unless Soroush wants a Zenodo community |
| Grants/funding | `[FUNDING TO VERIFY]` — see manuscript Declarations | **TO VERIFY** |
| Access right | Open Access | Recommend, given all inputs are open data |
| Language | English (`eng`) | Fixed |
| Notes | This record archives the **code + locked outputs** snapshot, not the manuscript text itself (the manuscript goes to the journal and, optionally, to a preprint server — see `submission/final/PREPRINT/`). | — |

## What this record represents

A **software / research-compendium** archive of the repository state at the tagged release
(recommended tag: `v1.0-preprint` or `v1.0`, see the checklist below) — the analysis
pipeline (`src/`), locked result tables (`outputs/tables/`), publication figures
(`outputs/publication/`), and reproducibility documentation
(`REPRODUCIBILITY.md`, `docs/`). It is **not** a duplicate submission of the manuscript
itself.

## Explicit non-actions

- No DOI has been minted.
- No metadata below has been entered into Zenodo's web form.
- The GitHub↔Zenodo webhook has not been enabled (see checklist).
- This file will need a follow-up edit once: (a) the licence is decided, (b) author
  names/ORCIDs are confirmed, (c) a GitHub Release is actually cut.
