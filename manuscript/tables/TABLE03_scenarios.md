# Table 3. Scenario comparison: constraint-first screening versus nearest-open baseline (S1–S8)

Source of values: `outputs/tables/phase3_hati_vs_baseline.csv`, `data/processed/phase3_scenarios_summary.csv` (locked). All values are exact, not recalculated. Reach = straight-line walking radius. "Removed" counts open, in-radius candidates removed on thermal/evidence grounds.

| Scenario | Source (asset) | Time | Reach (m) | Nearest-open pick | Baseline survives screening? | Surviving alternatives | Removed (thermal/evid.) | Outcome |
|---|---|---|---|---|---|---|---|---|
| S1 | Fuente de Neptuno | 15:00 | 800 | Museo Thyssen-Bornemisza | yes | 9 | 2 | ALTERNATIVES_FOUND |
| S2 | Fuente de Cibeles | 15:00 | 800 | Palacio de Cibeles - Ayuntamiento de Madrid | no (OUTDOOR_EXPOSURE_TOO_HIGH) | 6 | 3 | ALTERNATIVES_FOUND |
| S3 | Puerta de Alcalá | 18:00 | 800 | Retiro | yes | 4 | 6 | ALTERNATIVES_FOUND |
| S4 | Monumento a Alfonso XII | 18:00 | 800 | Parque del Retiro | yes | 8 | 1 | ALTERNATIVES_FOUND |
| S5 | Real Observatorio de Madrid | 15:00 | 800 | Estación del Arte | yes | 7 | 3 | ALTERNATIVES_FOUND |
| S6 | Estatua de Goya | 18:00 | 800 | Fuente de Neptuno | no (OUTDOOR_EXPOSURE_TOO_HIGH) | 9 | 2 | ALTERNATIVES_FOUND |
| S7 | La Rosaleda | 18:00 | 800 | Palacio de Cristal | yes | 6 | 0 | ALTERNATIVES_FOUND |
| S8 | Parque del Retiro | 15:00 | 500 | Palacio de Cristal | no (OUTDOOR_EXPOSURE_TOO_HIGH) | 0 | 6 | NO_DEFENSIBLE_ALTERNATIVE |

**Totals:** candidate set changed in 7 of 8 scenarios (unchanged in S7); nearest-open pick removed by screening in 3 of 8 (S2, S6, S8; each `OUTDOOR_EXPOSURE_TOO_HIGH`); 23 open, in-radius options removed on thermal/evidence grounds; S8 evaluated 26 candidates, 0 survived (`NO_DEFENSIBLE_ALTERNATIVE`).

*Abbreviations:* `OUTDOOR_EXPOSURE_TOO_HIGH`, `NO_DEFENSIBLE_ALTERNATIVE`, `ALTERNATIVES_FOUND` are machine-readable engine states (see Table 2).
