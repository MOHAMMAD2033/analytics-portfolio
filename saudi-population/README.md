[← All projects](../README.md)

<img src="../assets/saudi-population.svg" alt="Saudi Population Analysis" width="100%"/>

## See the regional picture.

An exploration of official historical population data, with regional comparisons and a clear view of change over time.

**Python/pandas · SQLite/SQL · Power BI project files · DAX**

## Work covered

1. Prepared official GASTAT data by region and year.
2. Separated national totals to avoid counting population twice.
3. Compared regional population and historical growth with SQL and charts.

## Outcome

**Compared 13 regions across the 2010–2022 historical series.**

The results describe historical population patterns, not current population estimates.

## Analysis preview

![Saudi Population Analysis — computed analysis preview](dashboard_preview.png)

*Rendered in Python from the analysis outputs; not a Power BI screenshot.*

[**View the result table →**](outputs/regions_2022.csv) · [SQL queries](sql/) · [Power BI files](powerbi/)

<details>
<summary>Source, implementation, and validation</summary>

- [Data source and attribution](docs/SOURCE.md)
- [Python implementation](src/) · [Run the analysis](analysis.py)
- [Data quality report](outputs/quality_report.json)
- [Method and setup](docs/TECHNICAL_NOTES.md)
- [Power BI opening instructions](powerbi/OPEN_IN_POWER_BI.md)

This is an educational project developed with AI assistance. Power BI project definitions are supplied; Desktop refresh/render and Service publication remain unverified. Results describe sample or historical data.

</details>

<details>
<summary>الملخص بالعربي</summary>

تحليل بيانات سكانية رسمية لمقارنة مناطق المملكة عبر السنوات، مع تنظيم البيانات وتجنب تكرار الإجماليات.

</details>

---
[← All four projects](../README.md)
