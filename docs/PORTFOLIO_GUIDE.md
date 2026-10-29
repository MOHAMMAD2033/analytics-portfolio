# Portfolio guide

[← Portfolio home](../README.md)

## For a quick review
1. Choose a project on the home page.
2. Read its question, work covered, and outcome.
3. Open the result table or preview.
4. Explore the code only if you want the implementation detail.

## File organization
Each analytics project follows the same layout:
- **README.md** — concise project story.
- **docs/** — methodology and data attribution.
- **data/** — source snapshot.
- **src/** — Python analysis and report-building modules.
- **sql/** — readable queries.
- **outputs/** — computed results and model tables.
- **powerbi/** — report definitions, model, DAX, and opening instructions.
- **tests/** — output checks.
- **analysis.py** — one command to run the workflow.

Smart Task keeps its web pages alongside **css/** and **js/** so it can be opened locally without a build process.

## Run an analytics project
Download the repository. In the chosen project folder:
```bash
pip install -r requirements.txt
python analysis.py
python -m unittest discover -s tests
```
Open the generated `dashboard.html` locally for the interactive preview. An HTML file viewed on GitHub shows source code, not a running dashboard.

## Open Power BI
Read the project's `powerbi/OPEN_IN_POWER_BI.md`. PBIP files are supplied; actual Power BI Desktop refresh/render and Service publication remain unverified.

## Scope and attribution
The analytics work is educational and AI-assisted. Sources are documented per project. Sample findings and suggested actions are not evidence of real business improvement. Smart Task uses local browser storage and manual priorities.
