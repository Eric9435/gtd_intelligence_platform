# GT&D Intelligence Platform

A Streamlit engineering prototype for generation, transmission, distribution, and electricity-business analysis.

## Application areas

- Generation capacity, transformer loading, and feeder analysis.
- Dashboard and executive summaries.
- Sales, revenue, ROI, and export scenarios.
- Demand/generation forecasts and what-if scenarios.
- Data-quality checks, threshold-based risks, and recommendations.
- Geographic views, saved history, comparisons, and CSV/PDF reports.

## Technology

Python, Streamlit, Pandas, NumPy, Plotly, SQLite, and ReportLab.

## Local development

Use Python 3 and an isolated virtual environment. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On Windows, activate the environment with `.venv\Scripts\activate` instead. Open the local URL printed by Streamlit, usually http://localhost:8501.

## Demo access

The local prototype defines demonstration accounts in `auth/login.py` for admin, engineer, and viewer roles. These fixed accounts are development-only; replace them with a proper identity system before deployment.

## Repository map

- `core/` — engineering calculations, forecasting, scenarios, and services.
- `ui/` — pages, charts, maps, and interface components.
- `auth/` — demonstration login and permissions.
- `storage/` and `database/` — SQLite persistence.
- `data/geo/` — geographic CSV inputs.
- `reports/` — report exports.
- `config.py` — defaults and alarm thresholds.

## Current boundaries

Several planned API, AI, and supporting modules are empty. Existing calculations and risk rules should be treated as engineering prototypes; there is no evidence here of validated live-grid integration or a trained production prediction model. Default thresholds and economic assumptions need review for each application.

No automated test suite is currently included. Validate calculations against independent reference cases before operational use.

## Maintainer

[Aung Phone Myat (Eric)](https://github.com/Eric9435)
