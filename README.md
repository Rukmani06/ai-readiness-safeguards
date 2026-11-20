# Ready to Build, Not Ready to Protect? Replication package

Data and code for:

> Keshav, Rukmani (2026). *Ready to Build, Not Ready to Protect? AI Readiness Scores and the Safeguards They Miss.* Working paper.

The paper compares three national measures across 128 countries: technical AI readiness (Oxford Insights Government AI Readiness Index 2025), the AI-policy measure (GIRAI 2026, AI Policy pillar) and institutional practice (six V-Dem v16 indicators). Every number, table and figure in the paper can be reproduced from this folder in a few minutes.

## Requirements
Python 3.10 or later, with the packages in `requirements.txt`:

```
pip install -r requirements.txt
```

Tested on 18 Nov 2026 with Python 3.13, pandas 3.0, numpy 2.5, scipy 1.18, matplotlib 3.11 and pycountry 26.2.

## How to run
Run the scripts from this folder, in this order. Each prints its results to the screen; the figure scripts save PNGs into this folder.

| # | Script | What it reproduces |
|---|---|---|
| 1 | `match.py` | Converts country names to ISO codes; writes `pdf/*_iso.csv` |
| 2 | `build.py` | Builds the 128-country table; writes `s.pkl`, which later scripts read |
| 3 | `check.py` | Main results: correlations 0.75 and 0.48, difference 0.27 (95% interval 0.14 to 0.42), percentiles, top-quarter counts, Appendix C |
| 4 | `income_check.py` | Within World Bank income groups |
| 5 | `within_group_checks.py` | Appendix G and Table G1: income and regime groups, the India recode, practice vs electoral democracy (0.84). Reads only the CSVs |
| 6 | `india_check.py` | The India recode (see the note on the full V-Dem file below) |
| 7 | `sensitivity.py` | Sensitivity checks on the AI-policy side (Civil Society Engagement; GIRAI dimensions without Labour & Skills) |
| 8 | `fig_dist2.py` | Figure 1 |
| 9 | `fig2_scatter.py` | Figure 2 |
| 10 | `fig_results.py` | Figures 3 to 7, and the robustness rows in Figure 6 |
| 11 | `fig8_only.py` | Figure 8 |

`parse_gi.py` is a helper that was used once to parse the GIRAI ranking table from the report text. It is kept to document how `pdf/girai2026_scores.csv` was made; it is not needed to reproduce the results.

All bootstrap intervals use 5,000 resamples of countries and the seed **20261113**, so they reproduce exactly.

`figures/` holds the PNGs as they appear in the paper.

## Files
**Final data**
- `unripe_base_128_countries.csv`: one row per country. The three national measures, the six V-Dem indicators and their z-scores, positions (1 = lowest, 128 = highest; ties share the average place) and percentile ranks (position ÷ 128 × 100).

**Source tables**
- `pdf/oxford2025_pillars.csv`: all six Oxford Insights pillars for 195 countries, transcribed from the Government AI Readiness Index 2025, "Full rankings" table, report pp. 59–68.
- `pdf/girai2026_scores.csv`: GIRAI 2026 overall score, five dimensions and three pillars for 135 countries, from the Annexures ranking table, report pp. 81–87.
- `pdf/*_iso.csv`: the same tables with ISO codes added by `match.py`.
- `vdem_subset.csv`: the six V-Dem v16 indicators for 2023–2025, extracted from `V-Dem-CY-Full+Others-v16.csv`.
- `vdem_regime_polyarchy_2025.csv`: V-Dem v16, 2025 values of Regimes of the World (`v2x_regime`) and the electoral democracy index (`v2x_polyarchy`) for the 128 countries.
- `regime_groups.csv`: `v2x_regime` 2025 with a democracy/autocracy flag (democracy = electoral or liberal democracy).
- `wb_income.txt`, `income_groups.csv`: World Bank income groups, read from the World Bank country API on 13 Nov 2026.

## Sample
GIRAI covers 135 countries. Seven are excluded:
- Hong Kong and Kosovo: no Oxford Insights scores.
- Antigua and Barbuda, Belize and Saint Lucia: not in V-Dem.
- Guinea and State of Palestine: no 2023 access-to-services value.

That leaves n = 128. V-Dem has no access-to-services values for 2024 or 2025, so 2023 is used for that indicator.

## Measures
- **Technical readiness**: the mean of the Oxford Insights AI Infrastructure and Development & Diffusion pillars (0–100).
- **AI-policy measure**: the GIRAI 2026 AI Policy pillar (0–100). GIRAI's penalty factors apply only to the overall score, so this pillar is unaffected by them.
- **Institutional practice**: the mean of six V-Dem indicators, each standardised across the 128 countries: access to justice, government social media monitoring (restraint), transparent laws with predictable enforcement, access to public services by income (2023), impartial public administration, and equal civil liberties across social groups.

## Names matched by hand to ISO codes
| As printed | Code | Report |
|---|---|---|
| Bolivia (Plurinational State of) | BOL | both |
| Democratic Republic of the Congo | COD | both |
| Gambia (Republic of The) | GMB | Oxford Insights |
| Guinea Bissau | GNB | Oxford Insights |
| Iran (Islamic Republic of) | IRN | Oxford Insights |
| Micronesia (Federated States of) | FSM | Oxford Insights |
| Republic of Korea | KOR | Oxford Insights (automatic matching picked North Korea) |
| State of Palestine | PSE | both |
| China Hong Kong Special Administrative Region | HKG | GIRAI |
| Cote d'Ivoire | CIV | GIRAI |
| Kosovo | XKX | GIRAI (automatic matching picked Serbia) |

All other names matched automatically. Matches where the report's name differs from V-Dem's were checked by eye (for example Cabo Verde / Cape Verde, Myanmar / Burma/Myanmar).

## Transcription checks
**Oxford Insights.** The ranking table prints ranks and pillar scores but no overall score, so the check is on order. Recombining the six pillars at the published weights (10/25/15/15/25/10, Methodology Report 2025) puts 194 of 195 neighbouring pairs in published order. The one exception is Suriname (rank 181), whose total is 0.002 points above Sao Tome and Principe (rank 180), consistent with pillars printed to two decimals.

**GIRAI.** Recombining the three pillars at 60/10/30, the published score ÷ recombined score is within 0.1% of 1 for 100 countries (largest difference 0.008 points). For the other 35, the ratio equals one of GIRAI's documented penalty factors to within 0.0003: 0.96 (23 countries), 0.93 (8), 0.91 (2) and 0.90 (2). The GIRAI 2026 methodology, A.2.3 (p. 30), documents these factors and says 35 countries are penalised.

## Main results (n = 128)
- Pearson correlations: technical–AI policy 0.748; technical–practice 0.478; AI policy–practice 0.556. Spearman: 0.774 / 0.465 / 0.553.
- Difference between the two technical correlations: 0.270, 95% interval 0.143 to 0.420.
- Netherlands percentiles (technical / AI policy / practice): 92 / 100 / 91. India: 85 / 69 / 20. United States: 100 / 83 / 59.
- Top quarter (percentile above 75) on all three measures: **14 countries**.
- Top quarter on technical readiness and bottom half on practice: 9 countries (Bahrain, China, India, Indonesia, Malaysia, Saudi Arabia, Thailand, United Arab Emirates, Viet Nam).

## Sensitivity checks
| Version | Technical–AI policy | Technical–practice | Difference (95% interval) | Script |
|---|---|---|---|---|
| Main | 0.75 | 0.48 | 0.27 (0.14–0.42) | `check.py` |
| Rank correlations (Spearman) | 0.77 | 0.47 | 0.31 (0.17–0.46) | `fig_results.py` |
| V-Dem model estimates | 0.75 | 0.49 | 0.26 (0.13–0.41) | earlier run, see note |
| Without the 2023 indicator | 0.75 | 0.41 | 0.34 (0.20–0.50) | `fig_results.py` |
| AI Policy plus Civil Society Engagement | 0.76 | 0.48 | 0.28 (0.16–0.43)* | `sensitivity.py` |
| GIRAI dimensions excl. Labour & Skills | 0.79 | 0.48 | 0.32 (0.20–0.46) | `sensitivity.py` |
| Four practice indicators (two distant proxies dropped) | 0.75 | 0.51 | 0.24 (0.12–0.38) | `fig_results.py` |
| Within World Bank income groups | 0.55 | 0.10 | 0.45 (0.23–0.65) | `income_check.py` |
| Within regime types | 0.68 | 0.27 | 0.41 (0.22–0.61) | `within_group_checks.py` |

\* `sensitivity.py` gives 0.285 (0.15–0.44) for this row: the original script did not survive, and the recreated one (both pillars standardised, then averaged) matches the published correlations but not the interval to the second decimal. Figure 6 shows the published values.

**V-Dem model estimates.** This row uses V-Dem's measurement-model point estimates instead of the ordinal-scale (`_osp`) versions. Those variables are not in `vdem_subset.csv`, and the script that produced the row did not survive; the values in Figure 6 come from an earlier run. To redo it, download the full V-Dem file (below) and replace each `_osp` indicator with its model-estimate version.

## Within-group checks (Appendix G)
By income group, the difference is 0.29 for high-income countries (−0.06 to 0.52), 0.68 for upper-middle (0.10 to 1.14) and 0.45 for low and lower-middle (0.13 to 0.76). By regime: democracies only (n = 65) 0.21 (0.04 to 0.37); autocracies only (n = 63) 0.46 (0.18 to 0.75). The practice composite correlates 0.84 with V-Dem's electoral democracy index, so the within-regime check is a strict test.

## The full V-Dem file
`V-Dem-CY-Full+Others-v16.csv` is not included because it is several hundred megabytes. Everything except one line of `india_check.py` runs without it. To use it, download the Country-Year "Full+Others" v16 dataset from https://v-dem.net/data/the-v-dem-dataset/ and save it as `vdem/V-Dem-CY-Full+Others-v16.csv`. Without it, `india_check.py` shows India's 2025 values only.

## Data sources and terms of use
- **Oxford Insights**, *Government AI Readiness Index 2025*. Scores transcribed from the published report. The scores belong to Oxford Insights; cite the original report when using them.
- **Global Index on Responsible AI (GIRAI) 2026**. Scores transcribed from the published report. The scores belong to the GIRAI publishers; cite the original report when using them.
- **V-Dem**: Coppedge, Michael, et al. 2026. *V-Dem Country-Year Dataset v16.* Varieties of Democracy (V-Dem) Project, https://v-dem.net. Please also cite the V-Dem codebook and measurement-model paper as listed in V-Dem's suggested citation for v16. V-Dem data are licensed CC BY-SA 4.0.
- **World Bank** country and lending groups, via the World Bank API (CC BY 4.0).

## Licence
- Code (`*.py`): MIT License, see `LICENSE`.
- Data files compiled for this project: Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0), see `LICENSE-DATA`. Share-alike is used because the files include V-Dem data, which carry that licence. The Oxford Insights and GIRAI scores remain the property of their publishers.

## Contact
Rukmani Keshav. Questions and corrections are welcome through GitHub issues.
