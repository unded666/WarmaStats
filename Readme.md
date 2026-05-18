# WarmaStats

Simple WarmaStats simulation and analytics toolkit, including a web UI that runs `WMDice` experiments and visualizes probability and cumulative distributions.

## Local run

```powershell
cd C:\PersonalProjects\WarmaStats
.\_venv\Scripts\python.exe -m pip install -r requirements.txt
.\_venv\Scripts\python.exe web_app.py
```

Then open `http://127.0.0.1:5000`.

## What the UI does

- Collects user-selected experiment parameters
- Runs `WM_Analytics.run_wm_analytics(...)`
- Uses `WMDice.experiment` for simulation
- Uses `Analyse_Results.analyse_results` for expectation + PMF/CDF
- Displays summary metrics, charts, and a tabular distribution view

## Deploy to Render

This repo includes both `Procfile` and `render.yaml`.

### Option A: Blueprint deploy (recommended)

1. Push this repo to GitHub.
2. In Render, create a new **Blueprint** and select the repo.
3. Render reads `render.yaml` and creates the web service.

### Option B: Manual Web Service

- **Environment**: Python
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn web_app:app`

## Run tests

```powershell
cd C:\PersonalProjects\WarmaStats
.\_venv\Scripts\python.exe -m unittest discover -s Tests -p "*_tests.py" -v
```
