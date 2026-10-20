# Open in Power BI Desktop

1. Keep this folder intact and open the `.pbip` file with current Power BI Desktop (Windows).
2. Select Refresh. Tables use embedded, compressed source snapshots: no local file paths or database credentials are required.
3. Inspect the model relationships and measures; compare totals to `../outputs/summary.json`.
4. Save as PBIX if desired and publish to your own workspace after review.

This PBIP was generated programmatically. JSON schema checks and numeric checks were performed, but Power BI Desktop refresh/render has NOT been run in this environment. The PNG and HTML previews are independent Python/web renderings, not screenshots of Power BI. If Desktop reports an issue, the cleaned CSVs, SQL and DAX are supplied separately.

To refresh with changed data, rerun `python analysis.py` from the project root. This rebuilds the embedded snapshot. Do not sum population across years. RFM scores refer to the documented historical snapshot, not current customer activity.
