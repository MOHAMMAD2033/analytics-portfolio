# Implementation

[← Project overview](../README.md)

This folder holds the supporting technical files. For the project story and preview, return to the overview above.

| Folder | Contents |
|---|---|
| [data](data/) | Source dataset snapshot. |
| [src](src/) | Python preparation and report-generation modules. |
| [sql](sql/) | Analysis queries. |
| [outputs](outputs/) | Computed results and quality reports. |
| [powerbi](powerbi/) | Report, model, DAX, and opening instructions. |
| [docs](docs/) | Methodology and source attribution. |
| [tests](tests/) | Output validation checks. |

Run commands from this folder:

```bash
pip install -r requirements.txt
python analysis.py
python -m unittest discover -s tests
```

Generated previews are written here. [See the published portfolio preview](../dashboard_preview.png).
