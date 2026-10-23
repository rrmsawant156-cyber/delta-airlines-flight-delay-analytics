
# Reproducibility Guide

## Delta Air Lines — Flight Delay Analytics
**Course:** BUSI6029 — Business Analytics Project 1

## 1. Purpose

This guide documents the environment, datasets and
execution requirements for the Delta Air Lines
predictive and prescriptive analytics project.

The repository supports methodological transparency
and version control.

Full reproducibility requires access to the original
datasets and the final preprocessing procedures.

## 2. Software Environment

The original project was developed using:

- Python 3.13.5 (Anaconda)
- NumPy 2.1.3
- pandas 2.2.3
- SciPy 1.15.3
- scikit-learn 1.6.1
- Matplotlib 3.10.0
- Seaborn 0.13.2
- Jupyter 1.1.1

The installed versions are documented in
`requirements.txt`.

## 3. Environment Setup

Clone the repository:

git clone https://github.com/rrmsawant156-cyber/delta-airlines-flight-delay-analytics.git

Navigate into the repository:

cd delta-airlines-flight-delay-analytics

Create a Python virtual environment:

python3 -m venv .venv

Activate it on macOS:

source .venv/bin/activate

Install the documented dependencies:

python -m pip install -r requirements.txt

Launch Jupyter:

jupyter notebook

These commands are intended for an environment with
a compatible Python installation.

Dependency installation and full notebook execution
have not been independently verified on a clean machine.

## 4. Required Datasets

The analysis references three principal datasets:

1. Delta_2023_2025_Raw.csv
2. Delta_2023_2025_Engineered.csv
3. Delta_2023_2025_Recovery_Model.csv

The raw dataset contains original historical flight
records.

The engineered dataset includes cleaned data and
scheduled flight characteristics.

The recovery-model dataset includes additional aircraft
sequence and recovery-related features.

The files are not distributed through this repository.
Data acquisition and redistribution permissions must
be verified separately.

## 5. Local Dataset Configuration

The original notebook uses a machine-specific folder:

~/Downloads/BA Project 1/ASS 1 files copy/

For another computer, place the required datasets in
an accessible local directory.

Update the notebook's DATA_DIR variable to point to
the directory containing these CSV files.

Example:

from pathlib import Path

DATA_DIR = Path.home() / "Downloads" / "BA Project 1" / "ASS 1 files copy"

Check the directory and filenames before running
the downstream modelling cells.

This is the original author's local configuration,
not a portable default.

## 6. Analysis Workflow

The project notebook covers:

1. Data loading and quality assessment.
2. Exploratory and descriptive analysis.
3. Feature preparation and predictive modelling.
4. Temporal model development and evaluation.
5. Aircraft rotation block construction.
6. Binary integer optimisation of candidate swaps.
7. Scheduling and sensitivity checks.
8. Forecast-assisted candidate screening.
9. Historical feasibility evaluation.
10. Consolidated findings and limitations.

The forecasting experiments reuse previously fitted
models stored in the active notebook session.

The notebook should be executed in its intended order
because some later steps depend on objects created
in earlier cells.

## 7. Model Evaluation

The predictive models use a temporal data split:

- Training: 2023
- Validation: 2024
- Holdout: 2025

The selected recovery-enhanced Random Forest achieved
a holdout MAE of approximately 12.76 minutes.

The January 2024 aircraft recovery experiment is
retrospective and should not be treated as a new
independent predictive holdout test.

## 8. Prescriptive Experiment

The recovery case study examines 171 eligible
aircraft rotation blocks on 16 January 2024.

The optimisation uses illustrative turnaround and
scheduling constraints to select reciprocal aircraft
block exchanges.

The objective measures modelled turnaround shortfall,
not actual realised flight-delay savings.

## 9. Forecast-Assisted Experiment

A schedule-only Random Forest forecasts incoming
aircraft delays.

Forecasts support candidate screening and binary
optimisation.

The resulting recommendations are then evaluated
against observed historical arrivals.

This is a retrospective simulation rather than
a deployed operational system.

## 10. Reproducibility Limitations

Important limitations include:

- Large input CSV files are not included.
- Local dataset paths require configuration.
- Some notebook cells rely on earlier in-memory objects.
- Exact raw-data acquisition steps are not yet documented.
- Clean-environment execution has not been verified.
- Aircraft compatibility, crew and maintenance
  constraints are incomplete.

Accordingly, the repository currently provides
documented analytical code and results, but does not
yet guarantee end-to-end reproduction by an
independent user.

## 11. Academic Disclaimer

This project was prepared for academic assessment.

It is not affiliated with or endorsed by Delta Air
Lines and does not constitute an operational flight
dispatch or aircraft recovery system.
