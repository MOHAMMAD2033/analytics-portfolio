# Customer RFM Segmentation

[← Back to all four projects](../README.md)

**How can customers be grouped by their buying activity?**

A learning project that turns purchase history into simple customer groups to support different follow-up ideas.

## Tools and data

**Tools:** Python/pandas · SQLite/SQL · Power BI project files · DAX

**Data:** The same historical Superstore sample used in the sales project. [Source details](SOURCE.md)

## Work covered in my AI-assisted project

- Summarized purchases for each customer.
- Calculated recency (how recently they bought), frequency (how often), and monetary value (how much they spent).
- Applied clear grouping rules and prepared segment summaries and report files.

This is an educational portfolio simulation developed with AI assistance.

## Main outcome

793 customers were grouped into five segments. These groups suggest different engagement approaches; no marketing campaign or revenue improvement was measured.

## Preview

![Customer RFM Segmentation preview](dashboard_preview.png)

*Python-rendered preview, not a Power BI screenshot. Power BI Desktop refresh/render and online publication remain unverified.*

## Explore the work

- [SQL queries](sql/)
- [Analysis results](outputs/)
- [Power BI files](powerbi/) · [Opening instructions](powerbi/OPEN_IN_POWER_BI.md)
- [Python entry point](analysis.py)

## بالعربي

تقسيم العملاء حسب آخر شراء، وعدد الطلبات، وقيمة المشتريات. الهدف فهم اختلاف العملاء واقتراح أسلوب متابعة مناسب لكل مجموعة.

<details>
<summary>Technical notes, method, and run instructions</summary>


**Portfolio simulation · AI-assisted implementation · October 2026**

## Business question

Which historical customers merit different retention or engagement approaches?

## Results

- 793 customers assigned to 5 mutually exclusive segments.
- Champions account for 33.4% of historical revenue.
- 133 customers meet the heuristic at-risk rule; a retention test is proposed, not an observed uplift.

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

- Recency = days between the fixed snapshot (2017-12-31) and the last purchase.
- Frequency = distinct Order IDs, not order lines. Monetary = sum of sales in USD.
- Equal metric values receive equal scores using average percentile ranks, mapped to 1–4. Recency is reversed.
- Rules in priority order: Champions (R>=3,F>=3,M>=3); At risk (R<=2,F>=3); Loyal (R>=3,F>=3); Promising (R>=3); otherwise Needs attention.
- All customers belong to exactly one segment. Scoring is fixed at the snapshot and does not recompute when report slicers change.
- These are transparent heuristic segments, not trained predictions or proof of customer churn.


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

Use different outreach hypotheses for Champions and At risk; validate with a controlled retention test. No campaign was run and no revenue uplift is claimed.


</details>
