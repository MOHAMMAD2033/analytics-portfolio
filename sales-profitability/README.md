# Superstore Sales & Profitability

[← Back to all four projects](../README.md)

**Which products generate sales but lose money?**

An educational analysis of the Superstore sales sample. The aim is to make sales and profit performance easier to compare before suggesting areas for further review.

## Tools and data

**Tools:** Python/pandas · SQLite/SQL · Power BI project files · DAX

**Data:** Superstore sample supplied with my project files (2014–2017). [Source details](SOURCE.md)

## Work covered in my AI-assisted project

- Prepared order data and checked dates and numeric values.
- Used SQL to compare sales, profit, products, and regions.
- Organized the results into visual summaries and prepared Power BI model/report files.

This is an educational portfolio simulation developed with AI assistance.

## Main outcome

The Tables subcategory had negative total profit in the sample, making it a useful starting point for a closer review of discounts and product mix.

## Preview

![Superstore Sales & Profitability preview](dashboard_preview.png)

*Python-rendered preview, not a Power BI screenshot. Power BI Desktop refresh/render and online publication remain unverified.*

## Explore the work

- [SQL queries](sql/)
- [Analysis results](outputs/)
- [Power BI files](powerbi/) · [Opening instructions](powerbi/OPEN_IN_POWER_BI.md)
- [Python entry point](analysis.py)

## بالعربي

تحليل بيانات متجر لفهم المبيعات والأرباح وتحديد المنتجات الخاسرة. يشمل تجهيز البيانات، المقارنة باستخدام SQL، وعرض النتائج في تقارير واضحة.

<details>
<summary>Technical notes, method, and run instructions</summary>


**Portfolio simulation · AI-assisted implementation · October 2026**

## Business question

Which product groups generate revenue but lose money?

## Results

- 5,009 distinct orders from 793 customers across 9,994 order lines.
- Overall profit margin is 12.47%, calculated as total profit / total sales.
- Tables has the lowest aggregate profit ($-17,725.48); review product mix and discount policy before making changes.

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

- Parse source dates explicitly as day/month/year.
- Strip whitespace, validate numeric ranges and shipment chronology, preserve distinct Row IDs.
- Retain one pair of repeated business rows with distinct Row IDs; duplication is not proven.
- Store line-level data in SQLite. Use GROUP BY, CASE, CTE and LAG queries.
- Model Sales with Date, Product, Customer and Region dimensions.
- Profit margin = SUM(profit) / SUM(sales), not the mean of row-level margins.
- Orders = distinct Order IDs; customer IDs are counted distinctly. Amounts remain in USD.


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

Review Tables, Bookcases and Supplies at product/discount level. Test a limited discount-policy change; measure results before claiming improvement. Associations here do not establish causality.


</details>
