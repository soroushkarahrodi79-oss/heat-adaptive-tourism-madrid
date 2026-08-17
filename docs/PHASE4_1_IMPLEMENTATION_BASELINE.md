# PHASE4_1_IMPLEMENTATION_BASELINE.md — HATI-Madrid

Version 1.0 · 2026-08-18. This document freezes the pre-implementation
state of the repository. It is the immutable reference used to verify that
protected Phase 0–3 scientific artifacts are **not** modified by any
Phase 4.1 UI work.

## 1. Baseline Git commit

```
commit  901954e1dc8a07970715ff5be82634a9abcc270f
short   901954e
message HATI-Madrid through Phase 4.0 — science and visual architecture locked
```

This commit is the immutable pre-implementation reference. It contains the
complete Phase 0–3 science, the Phase 4.0 specification set, and no
application code. Existing scientific files were **not** rewritten or
reorganized for Git cleanliness.

## 2. What the baseline commit excludes (and why)

The `.gitignore` excludes only the following, none of which are protected
Phase 0–3 artifacts or consumed by the app:

- Virtual environments (`.venv/`, `.venv_solweig/`, `.venv_app/`).
- Python caches (`__pycache__/`, `.pytest_cache/`, etc.).
- Heavy regenerable SOLWEIG run caches / working dirs under
  `data/interim/solweig*/` (GeoTIFFs, SVF memmaps, shadow matrices).
- App runtime artifacts (`*.log`, `.dash_cache/`).

Verified at baseline: every file under `data/processed/`, `outputs/tables/`,
`outputs/maps/`, `data/raw/`, and all `docs/` and `src/` files are **tracked**
(not ignored). `.gitattributes` disables EOL conversion (`* -text`) so
scientific data files stay byte-identical across any checkout.

## 3. Protected data-contract file hashes (SHA-256)

These are the seven — and only — Phase 3 files the Phase 4.1 app is permitted
to read. The automated test `tests/phase4_1/test_contract.py::test_protected_file_hashes`
recomputes these and asserts they are unchanged.

| SHA-256 | File |
|---|---|
| `936d6dd51150e96d8c8445fec6910c40d273f005a99b5d945cff2f8b106b7b54` | `data/processed/phase3_asset_catalog.csv` |
| `deecfe44aa07f22cfc9d50718d090646943186befc246b5cc1a85be2f7fd28b2` | `data/processed/phase3_candidate_screening.csv` |
| `79ce49c174e9143cd937eaebb515be334efdf1e86989d65740e9d406200129cf` | `data/processed/phase3_scenarios.csv` |
| `9b6c406d30d47308beeb824a6d27c71e7f3c7b60998beba7f05bff56845132be` | `data/processed/phase3_scenarios_summary.csv` |
| `065babc59e0585c5f9693e4973ac213c3bfac92da68013858d98b4fa82b54f71` | `outputs/tables/phase3_exclusion_reasons.csv` |
| `7ab737038c680144b472cabff2d4f6937d5bf2c6449cd3436f9ef5fc4dd28650` | `outputs/tables/phase3_hati_vs_baseline.csv` |
| `2ded4494271d92aa2aefa63048b684cc1c05fc9ed79782d2adb8c062b0619ef0` | `outputs/tables/phase3_accessibility_sensitivity.csv` |

## 4. Whole-directory integrity check

Beyond the seven data-contract files, protected-artifact integrity is also
verifiable at any time against the baseline commit:

```bash
git diff --stat 901954e1dc8a07970715ff5be82634a9abcc270f -- \
  data/processed outputs/tables outputs/maps \
  docs/PHASE0_* docs/PHASE1_* docs/PHASE2_* docs/PHASE3_* \
  src/phase3_*.py
```

An empty diff confirms no protected artifact was touched. New Phase 4.1 code
lives only under `app/`, `tests/phase4_1/`, and new `docs/PHASE4_1_*` files.
