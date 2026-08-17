"""HATI-Madrid — Phase 4.1 Visual Decision-Support MVP.

A read-only presentation/interaction layer over the locked Phase 0-3
scientific outputs. This package NEVER recomputes UTCI, feasibility,
candidate screening, or baseline picks, and NEVER writes into the
protected data directories. See docs/PHASE4_1_IMPLEMENTATION_REPORT.md.
"""

__all__ = ["constants", "data_loader"]
