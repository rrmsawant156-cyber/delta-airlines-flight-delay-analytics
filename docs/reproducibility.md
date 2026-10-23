## Standalone Predictive–Prescriptive Application

### Overview

The project includes a standalone Python application located in `src/app.py`. It supports three execution modes:

1. **Predict:** Generate flight arrival-delay predictions using a trained schedule-only Random Forest.
2. **Recover:** Generate and optimise forecast-based aircraft rotation exchanges using mixed-integer linear programming (MILP).
3. **Integrated:** Combine incoming-flight delay prediction, aircraft readiness estimation, aircraft exchange optimisation and operational safety review.

The application can run without opening the original Jupyter Notebook.

### Environment

The standalone prototype was tested with Python 3.13.5 and the package versions recorded in `requirements.txt`.

Install dependencies using:

```bash
python -m pip install -r requirements.txt
```

### Model Availability

The application requires the previously trained `schedule_rf_pipeline.joblib` model file for prediction and integrated modes.

The trained model is not included in the public repository. It must be provided separately from a trusted source. Never load untrusted joblib files.

### Running the Application

Run the following commands from the repository root, replacing placeholder paths with local paths.

**Prediction mode:**

```bash
python src/app.py predict \
  --flights "/path/to/future_flights.csv" \
  --model "/path/to/schedule_rf_pipeline.joblib" \
  --output-dir "/path/to/output"
```

**Recovery mode:**

```bash
python src/app.py recover \
  --blocks "/path/to/aircraft_rotation_blocks.csv" \
  --output-dir "/path/to/output"
```

**Integrated mode:**

```bash
python src/app.py integrated \
  --incoming "/path/to/incoming_flights.csv" \
  --blocks "/path/to/aircraft_rotation_blocks.csv" \
  --model "/path/to/schedule_rf_pipeline.joblib" \
  --output-dir "/path/to/output"
```

### Required Inputs

Prediction mode requires the nine schedule-only features:

`MONTH`, `DAY_OF_WEEK`, `IS_WEEKEND`, `CRS_DEP_HOUR`, `CRS_ARR_HOUR`, `CRS_ELAPSED_TIME`, `DISTANCE`, `ORIGIN`, and `DEST`.

Recovery mode requires the following block-level fields:

`BLOCK_ID`, `TAIL_NUM`, `DEST`, `BLOCK_START_MIN`, `BLOCK_END_MIN`, `FOLLOWING_DEP_MIN`, `REMOTE_GROUND_MIN`, and `PRED_READY_MIN`.

Integrated mode requires an incoming-flight file containing the nine prediction features, `BLOCK_ID`, and `INCOMING_SCHED_ARR_MIN`, together with a rotation-block file containing the recovery fields other than `PRED_READY_MIN`.

Each block must correspond to exactly one incoming-flight record, identified by `BLOCK_ID`. All minute-based times must use the same continuous timeline.

### Validation Performed

The application was tested against:

- Three externally supplied synthetic flight records.
- A two-aircraft synthetic scenario producing one mathematical exchange and a predicted 30-minute reduction in turnaround shortfall.
- A fully integrated two-aircraft synthetic scenario producing one mathematical exchange and approximately 26.54 minutes of predicted shortfall reduction.
- A January 16, 2024, historical ATL test comprising 171 eligible blocks, 19 positive-benefit candidates, and eight selected mathematical exchanges, representing an estimated 81.82-minute reduction in the forecast-based shortfall proxy.
- Input-validation checks for missing prediction features, duplicate block identifiers and unverified operational requirements.

These are functional and historical-regression tests, not evidence of realised operational performance.

### Limitations

The application is an academic decision-support prototype rather than an operational airline dispatch platform.

The schedule-only Random Forest has limited predictive explanatory power on the 2024 validation data (R² approximately 0.0112). The optimisation objective measures forecast-based turnaround-start shortfall rather than actual flight-delay savings.

Aircraft equipment compatibility, crew feasibility, maintenance restrictions, complete network commitments, gate availability and decision-time information are not independently verified. Mathematical swap selections are therefore subjected to an operational review gate, and the application never grants dispatch authorisation.

The public repository does not include the proprietary or large underlying datasets or the trained model artifact. Reproduction of model predictions requires access to the trusted saved model and compatible inputs.
