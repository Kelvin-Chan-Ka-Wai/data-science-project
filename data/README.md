# Datasets

| File | Source | Rows x columns | Licence / permission |
|---|---|---|---|
| `world_population.csv` | World Bank **[World Development Indicators](https://data.worldbank.org/summary-terms-of-use)**, indicator `EN.POP.DNST` (population density, people per km²) | 264 x 60 (1960-2016) | CC BY 4.0 - public statistics, attribution: World Bank WDI |
| `automobiles.csv` | **[UCI Machine Learning Repository, Automobile (1985)](https://archive.ics.uci.edu/dataset/10/automobile)** | 201 x 14 | CC BY 4.0 - public research dataset, attribution: UCI ML Repository |
| `olympia2016_athletes.csv` | **[Rio 2016 Olympic athlete statistics](https://github.com/flother/rio2016)** (course tutorial copy, derived from the Rio 2016 official statistics) | 11,538 x 11 | Public source data; **no explicit redistribution licence found in the upstream repository**. Retained for course reproducibility, not offered under a separate licence. |

Notes:

- The files are copies of the datasets supplied with the CISC7204 tutorial pages, kept small
  (about 1 MB in total) so the analysis is reproducible without any download step.
- They contain **no** passwords, API keys, personal contact details or otherwise restricted
  material. The population and car analyses use aggregated statistics. The Olympic source is
  **individual-level public sports data**, including athlete name, sex, date of birth, height and
  weight; these public fields are used only for reproducibility and are aggregated by country
  for the figures.
- The large `stock_prices.csv` dataset from the tutorial (50 MB) is **not** redistributed here
  because its licence terms are unclear; `notebooks/03_olympics_dashboard.ipynb` therefore
  analyses the Olympic data only.
- The Olympic CSV contains public individual athlete records (name, nationality, sex, date of
  birth, height, weight, sport and medal counts). It is not anonymised. Only the country-level
  aggregates needed for the findings are presented in the figures.
- The World Bank data use CC BY 4.0 with the additional terms linked above; the UCI Automobile
  dataset is CC BY 4.0 and credited to Jeffrey Schlimmer (1985), DOI `10.24432/C5B01C`.
