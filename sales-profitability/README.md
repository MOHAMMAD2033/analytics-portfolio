[← Portfolio home](../README.md) · [Data source](implementation/docs/SOURCE.md) · [Technical notes](implementation/docs/TECHNICAL_NOTES.md)

<img src="../assets/sales-profitability.svg" width="100%" alt="Superstore Sales & Profitability"/>

# Superstore Sales & Profitability
**Understanding the gap between revenue and profit.**

Python/pandas · SQLite/SQL · Power BI project files · DAX  
Educational portfolio study · AI-assisted implementation

## The question
Which product groups generate sales but lose money—and what should be reviewed next?

## Data and starting point
An educational Superstore sample supplied with the original project. It contains retail order lines from **2014–2017**. Customer names are omitted from the portfolio copy. [Source and attribution →](implementation/docs/SOURCE.md)

## From data to report

| Stage | Work covered |
|---|---|
| **1. Prepare the data** | Read the source CSV with Python/pandas, parse dates as day/month/year, trim text, and validate numeric fields and shipment dates. |
| **2. Preserve the right records** | Use Row IDs to distinguish order lines. Repeated business values with different Row IDs are retained rather than automatically removed. |
| **3. Analyze with SQL** | Load the prepared records into SQLite and summarize sales, profit, discounts, monthly trends, and regional performance. |
| **4. Build the reporting structure** | Prepare a sales fact table and Date, Product, Customer, and Region dimensions, plus report files and DAX measures. |
| **5. Check the results** | Reconcile output totals and retain a quality report so the displayed findings can be traced back to the analysis. |

## Analysis preview

![Superstore Sales & Profitability — analysis preview](dashboard_preview.png)

*This preview is generated in Python from the analysis outputs. It is not a Power BI screenshot.*

## Findings
| Measure | Result |
|---|---:|
| Order lines | 9,994 |
| Distinct orders | 5,009 |
| Overall profit margin | 12.47% |
| Tables aggregate profit | −$17,725.48 |

**Tables is the main investigation point.** Its negative aggregate profit shows why ranking products only by sales can miss a problem. The next step would be to examine individual products and discount patterns before testing a pricing change.

[Product results](implementation/outputs/subcategories.csv) · [Discount analysis](implementation/outputs/discounts.csv) · [Monthly trends](implementation/outputs/monthly.csv)

## An important analysis decision
Profit margin is calculated as **total profit ÷ total sales**. Averaging individual row margins would answer a different question. Orders are counted by distinct Order ID, because an order may contain multiple product lines.

## Skills practiced
This study provides practice in preparing retail data, distinguishing sales from profit, writing summary queries, and explaining a finding without claiming that a proposed action has already improved performance.

## Explore the work

| File area | What you can review |
|---|---|
| [Python implementation](implementation/src/) | Data preparation and report-generation modules. |
| [SQL queries](implementation/sql/) | Calculations and summaries behind the findings. |
| [Computed outputs](implementation/outputs/) | Result tables and prepared model data. |
| [Power BI files](implementation/powerbi/) | Report definitions, data model, and DAX measures. |
| [Quality report](implementation/outputs/quality_report.json) | Data checks and preparation decisions. |
| [Validation checks](implementation/tests/) | Checks for output consistency. |

## Run it locally
Download the repository and open a terminal in `sales-profitability/implementation`:

```bash
pip install -r requirements.txt
python analysis.py
python -m unittest discover -s tests
```

The pipeline generates the analysis outputs and an offline `dashboard.html`. Open that generated HTML file locally to explore the report. For Power BI, follow the [opening instructions](implementation/powerbi/OPEN_IN_POWER_BI.md).

## Project scope
This is an educational, AI-assisted study. The findings describe the supplied sample or historical series; they do not demonstrate a commercial improvement. Power BI definitions are included, but Desktop refresh/render and Service publication remain unverified.

<details>
<summary>شرح المشروع بالعربي</summary>

المشروع يجاوب عن سؤال: هل المنتجات الأعلى مبيعًا هي الأعلى ربحًا؟ يبدأ بتجهيز بيانات المتجر وفحصها، ثم تحليلها بـ SQL وعرض النتائج. ظهرت فئة الطاولات كفئة خاسرة، ولذلك يُقترح مراجعة منتجاتها وخصوماتها قبل اتخاذ قرار.

</details>

---
[← Explore all four projects](../README.md)
