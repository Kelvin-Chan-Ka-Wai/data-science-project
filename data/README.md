# Datasets

| File | Source | Rows x columns | Licence / permission |
|---|---|---|---|
| `world_population.csv` | World Bank **World Development Indicators**, indicator `EN.POP.DNST` (population density, people per km²) | 264 x 60 (1960-2016) | CC BY 4.0 - public statistics, attribution: World Bank WDI |
| `automobiles.csv` | **UCI Machine Learning Repository**, *Automobile* dataset (1985) | 201 x 14 | CC BY 4.0 - public research dataset, attribution: UCI ML Repository |
| `olympia2016_athletes.csv` | **Rio 2016 Olympic athletes** dataset, distributed with the CISC7204 tutorial (originally Kaggle) | 11,538 x 11 | Public dataset; only public Olympic record fields (name, nationality, sport, medals) |

Notes:

- The files are copies of the datasets supplied with the CISC7204 tutorial pages, kept small
  (about 1 MB in total) so the analysis is reproducible without any download step.
- They contain **no** passwords, API keys, personal contact details or otherwise restricted
  material - only aggregated national statistics and public sports records.
- The large `stock_prices.csv` dataset from the tutorial (50 MB) is **not** redistributed here
  because its licence terms are unclear; `notebooks/03_olympics_dashboard.ipynb` therefore
  analyses the Olympic data only.
