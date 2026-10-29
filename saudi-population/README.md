# Saudi Population Analysis

[← Back to all four projects](../README.md)

**How did population distribution change across Saudi regions?**

A historical analysis of official Saudi population data, presented as regional comparisons and trends over time.

## Tools and data

**Tools:** Python/pandas · SQLite/SQL · Power BI project files · DAX

**Data:** General Authority for Statistics (GASTAT), historical population series for 2010–2022. [Source details](docs/SOURCE.md)

## Work covered

- Prepared population values and organized the data by region and year.
- Separated national totals from regional records to avoid double counting.
- Used SQL and visual summaries to compare regions and historical growth.

This is an educational portfolio simulation developed with AI assistance.

## Main outcome

A clear comparison of 13 Saudi regions over 2010–2022. The analysis describes historical population, not current estimates.

## Evidence

[View the result table](outputs/regions_2022.csv) · [Data quality checks](outputs/quality_report.json)

## Preview

![Saudi Population Analysis preview](dashboard_preview.png)

*Python-rendered preview, not a Power BI screenshot. Power BI Desktop refresh/render and online publication remain unverified.*

## Explore the work

- [SQL queries](sql/)
- [Analysis results](outputs/)
- [Power BI files](powerbi/) · [Opening instructions](powerbi/OPEN_IN_POWER_BI.md)
- [Python implementation](src/) · [Run entry point](analysis.py)
- [Method and setup](docs/TECHNICAL_NOTES.md)

## بالعربي

تحليل بيانات سكانية رسمية لمقارنة مناطق المملكة وتغير السكان عبر السنوات. يشمل تنظيم البيانات وتجنب تكرار الإجماليات وعرض الاتجاهات.


---
[← Portfolio](../README.md) · [How to explore this repository](../docs/PORTFOLIO_GUIDE.md)
