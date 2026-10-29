[← Portfolio home](../README.md) · [Data source](implementation/docs/SOURCE.md) · [Technical notes](implementation/docs/TECHNICAL_NOTES.md)

<img src="../assets/customer-rfm.svg" width="100%" alt="Customer RFM Segmentation"/>

# Customer RFM Segmentation
**Turning purchase history into useful customer groups.**

Python/pandas · SQLite/SQL · Power BI project files · DAX  
Educational portfolio study · AI-assisted implementation

## The question
How can historical purchasing behavior help us propose more relevant follow-up for different customers?

## Data and starting point
The educational **2014–2017 Superstore sample** used in the sales project. Here, the unit of analysis changes from product/order line to customer. Names are omitted; customer IDs are used for grouping. [Source and attribution →](implementation/docs/SOURCE.md)

## From data to report

| Stage | Work covered |
|---|---|
| **1. Prepare purchase records** | Read and validate the transaction data, keeping customer IDs, order IDs, purchase dates, and sales values. |
| **2. Create customer summaries** | Calculate days since the last purchase, count distinct orders, and sum spending for each customer. |
| **3. Score the RFM measures** | Map each measure to a 1–4 score using percentile ranks. Reverse recency so more recent purchases receive a higher score. |
| **4. Apply segment rules** | Assign each customer to one of five groups using ordered rules, ensuring exactly one segment per customer. |
| **5. Compare the segments** | Prepare segment totals, customer-level results, charts, and Power BI files to review differences in historical purchasing. |

## Analysis preview

![Customer RFM Segmentation — analysis preview](dashboard_preview.png)

*This preview is generated in Python from the analysis outputs. It is not a Power BI screenshot.*

## Findings
| Measure | Result |
|---|---:|
| Customers analyzed | 793 |
| Customer segments | 5 |
| Champions' share of historical sales | 33.4% |
| Customers matching the At risk rule | 133 |

**The segments suggest different follow-up hypotheses.** Champions could be considered for loyalty-focused communication; customers matching the At risk rule could be considered for a re-engagement test. No campaign was run, and no retention uplift is claimed.

[Segment summary](implementation/outputs/segments.csv) · [Customer-level RFM](implementation/outputs/rfm_customers.csv)

## An important analysis decision
The snapshot is fixed at **31 December 2017**. Recency means days since the last purchase; Frequency counts distinct orders; Monetary sums sales. Scores remain fixed when report filters change. These are transparent rules, not a machine-learning churn model.

## Skills practiced
This study provides practice in moving from transaction rows to customer-level analysis, defining business rules, and interpreting customer groups without treating historical patterns as predictions.

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
Download the repository and open a terminal in `customer-rfm/implementation`:

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

الفكرة هي تقسيم العملاء حسب آخر عملية شراء، وعدد الطلبات، وإجمالي المشتريات. بعد حساب هذه القيم، تُطبق قواعد لتوزيع العملاء على خمس مجموعات تساعد في اقتراح أساليب متابعة مختلفة.

</details>

---
[← Explore all four projects](../README.md)
