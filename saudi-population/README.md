# Saudi Population Analysis

[← Back to all four projects](../README.md)

**How did population distribution change across Saudi regions?**

A historical analysis of official Saudi population data, presented as regional comparisons and trends over time.

## Tools and data

**Tools:** Python/pandas · SQLite/SQL · Power BI project files · DAX

**Data:** General Authority for Statistics (GASTAT), historical population series for 2010–2022. [Source details](SOURCE.md)

## Work covered in my AI-assisted project

- Prepared population values and organized the data by region and year.
- Separated national totals from regional records to avoid double counting.
- Used SQL and visual summaries to compare regions and historical growth.

This is an educational portfolio simulation developed with AI assistance.

## Main outcome

A clear comparison of 13 Saudi regions over 2010–2022. The analysis describes historical population, not current estimates.

## Preview

![Saudi Population Analysis preview](dashboard_preview.png)

*Python-rendered preview, not a Power BI screenshot. Power BI Desktop refresh/render and online publication remain unverified.*

## Explore the work

- [SQL queries](sql/)
- [Analysis results](outputs/)
- [Power BI files](powerbi/) · [Opening instructions](powerbi/OPEN_IN_POWER_BI.md)
- [Python entry point](analysis.py)

## بالعربي

تحليل بيانات سكانية رسمية لمقارنة مناطق المملكة وتغير السكان عبر السنوات. يشمل تنظيم البيانات وتجنب تكرار الإجماليات وعرض الاتجاهات.

<details>
<summary>Technical notes, method, and run instructions</summary>


**Portfolio simulation · AI-assisted implementation · October 2026**

## Business question

How concentrated was the population across Saudi regions, and how did it change from 2010 to 2022?

## Results

- 32,175,224 residents in the 2022 regional total across 13 regions.
- The three largest regions account for 67.6% of the 2022 total.
- Population increased 34.2% between 2010 and 2022; this historical series is not a 2026 population estimate.

![Independently rendered dashboard preview](dashboard_preview.png)

The image is a Python-rendered preview, not a Power BI screenshot. Run `python analysis.py` to generate `dashboard.html`, then open it locally for an interactive preview with filters and CSV export.

## Reproduce

```bash
python -m venv .venv
# Activate the environment for your operating system.
pip install -r requirements.txt
python analysis.py
python -m unittest discover -s tests
```

The pipeline reads the bundled source snapshot, cleans it with Python/pandas, loads SQLite, runs the SQL queries, writes CSV results, generates charts, and rebuilds a Power BI project. No API keys or paid service are needed for local analysis.

## Method and controls

- Download the official GASTAT CSV from the public Tableau view with default All gender / All nationality selections.
- Convert comma-separated numeric strings into integer population counts.
- Exclude 13 All national aggregate rows from the regional fact table to prevent double counting.
- Retain 169 observations: 13 regions × 13 years, with no repeated region-year keys.
- Reconcile yearly regional sums to the source national totals (small rounding differences tolerated and reported).
- Compare 2010 and 2022 endpoints. Population is not additive across time: headline cards use the latest selected year.
- This is a historical exercise, not the latest population estimate or a sufficient standalone basis for expansion decisions.


## Power BI

Open the `.pbip` under `powerbi/` in current Power BI Desktop for Windows, then Refresh. The model contains embedded source snapshots so no machine-specific data path is required. Measures are also supplied in `powerbi/measures.dax`; prepared tables are in `outputs/model_*.csv`.

**Validation boundary:** Python/SQL totals, output checks and web-preview logic have been tested. Power BI JSON definitions are checked against official schemas during packaging, but Desktop refresh/render and Service publication have not been performed. See `powerbi/OPEN_IN_POWER_BI.md`.

## Files

- `data/source.csv`: reproducible input snapshot; see `SOURCE.md`.
- `analysis.py` and companion Python files: executable pipeline.
- `sql/`: readable analytical queries (SQLite dialect).
- `outputs/analysis.sqlite`: SQL database generated when the pipeline runs.
- `outputs/quality_report.json`: data quality decisions and source SHA-256.
- `outputs/summary.json` and CSV files: computed results.
- `dashboard_preview.png`: preview image. The pipeline generates the offline `dashboard.html`.
- `powerbi/`: PBIP report, model, relationships and DAX.
- `tests/`: numeric reconciliation checks.

## Attribution and use

See `SOURCE.md`. This project was prepared with AI assistance for learning and portfolio review. The owner should rerun and explain the analysis before presenting it as a personal skill demonstration. No professional employment, certification, or commercial impact is implied.

## Suggested next actions

Combine this historical population view with current demand, income, competition and operating cost data before any site-selection decision. Do not infer causal drivers from this table.


</details>
