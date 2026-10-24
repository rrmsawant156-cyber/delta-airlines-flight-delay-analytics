# Client Data Preparation and Operational User Guide

## 1. Purpose and scope

The Delta Air Lines Predictive–Prescriptive Analytics Application is an academic decision-support prototype developed for BUSI6029 Business Analytics.

The system combines a schedule-only Random Forest model for flight arrival-delay prediction with a mixed-integer linear programming (MILP) model for identifying potentially beneficial aircraft rotation exchanges.

The application supports three modes:

| Mode | Purpose | Required inputs |
|---|---|---|
| Predict | Estimate arrival delay for scheduled flights | Flight CSV and trained model |
| Recover | Identify mathematical aircraft swap candidates | Prepared recovery-block CSV |
| Integrated | Predict incoming-flight readiness and optimise aircraft exchanges | Incoming-flight CSV, aircraft rotation CSV and trained model |

**The application does not issue operational dispatch instructions.** Any identified swap requires independent verification of aircraft compatibility, crews, maintenance, airport infrastructure and other operational commitments.

---

## 2. Client data requirements

Client input files must use CSV format, contain a header row, and use the exact column names described below.

The application expects one row per flight in prediction mode and one row per eligible aircraft rotation block in recovery mode.

### 2.1 Flight prediction input

Required file: `future_flights.csv`

| Column | Description | Example | Requirements |
|---|---|---|---|
| MONTH | Scheduled flight month | 3 | Integer 1–12 |
| DAY_OF_WEEK | Day of the week | 1 | Integer 1–7, following the training convention |
| IS_WEEKEND | Weekend indicator | 0 | 0 or 1 |
| CRS_DEP_HOUR | Scheduled departure hour | 7 | Integer 0–23 |
| CRS_ARR_HOUR | Scheduled arrival hour | 9 | Integer 0–23 |
| CRS_ELAPSED_TIME | Scheduled flight duration | 120 | Positive minutes |
| DISTANCE | Scheduled route distance | 760 | Positive miles, consistent with training |
| ORIGIN | Origin airport | JFK | Three-letter airport code |
| DEST | Destination airport | ATL | Three-letter airport code |

Optional additional columns, such as `FLIGHT_ID`, may be retained for identification and reporting.

**Important:** The client must follow the same time, weekday and distance conventions used during model training. The application checks certain numeric ranges and airport-code formatting, but it does not establish that every combination represents a valid flight.

### 2.2 Aircraft recovery input

Required file: `aircraft_rotation_blocks.csv`

| Column | Description | Example |
|---|---|---|
| BLOCK_ID | Unique aircraft rotation identifier | 1001 |
| TAIL_NUM | Aircraft registration or unique tail identifier | TEST_A |
| DEST | Outstation for the ATL round trip | JFK |
| BLOCK_START_MIN | Scheduled departure time of the rotation | 600 |
| BLOCK_END_MIN | Scheduled return/completion time | 800 |
| FOLLOWING_DEP_MIN | Next recorded departure commitment for the original aircraft | 1000 |
| REMOTE_GROUND_MIN | Scheduled turnaround time at the outstation | 70 |
| PRED_READY_MIN | Predicted aircraft availability time before the rotation | 630 |

All time values must use **one continuous minute-based timeline**.

For example, if midnight at the beginning of the operating date is minute zero, 10:00 AM is minute 600, and 1:00 AM on the next day is minute 1500.

Do not reset the time counter at midnight for overnight operations.

The current optimisation model is specifically structured around ATL-origin round-trip blocks. It must not be applied to arbitrary airport networks without additional validation and redevelopment.

### 2.3 Integrated mode: incoming-flight input

Required file: `incoming_flights.csv`

In addition to the nine flight prediction features, the integrated incoming-flight CSV requires:

| Column | Description |
|---|---|
| BLOCK_ID | Unique identifier matching a rotation block |
| INCOMING_SCHED_ARR_MIN | Scheduled arrival of the aircraft into ATL, expressed on the continuous minute timeline |

The system calculates:

**Predicted aircraft readiness = Scheduled incoming arrival + Predicted arrival delay + Required turnaround allowance**

The current standalone implementation uses a fixed 45-minute turnaround allowance.

This is a modelling assumption, not a verified aircraft-specific minimum.

The integrated rotation-block CSV requires the recovery fields except `PRED_READY_MIN`. The application generates this value from the incoming-flight forecasts.

Every incoming-flight record must match exactly one rotation block by `BLOCK_ID`.

---

## 3. Preparing client data before execution

### Step 1: Identify the source systems

Determine where the client stores scheduled flight information, aircraft registrations, flight rotation sequences and operational restrictions.

Possible source systems include flight scheduling platforms, operational databases and approved data exports.

Confirm that the client is authorised to use the information for the proposed analysis.

### Step 2: Extract the relevant records

Export the information required for the intended application mode.

For prediction, extract scheduled flight attributes.

For recovery, construct eligible ATL round-trip aircraft rotation blocks and their recorded follow-on commitments.

For integrated analysis, prepare both incoming-flight and matching rotation-block records.

### Step 3: Standardise column names

Rename exported source columns to match the required application schema.

For example:

| Client source field | Application field |
|---|---|
| DepartureAirport | ORIGIN |
| ArrivalAirport | DEST |
| ScheduledDuration | CRS_ELAPSED_TIME |
| AircraftRegistration | TAIL_NUM |
| RotationIdentifier | BLOCK_ID |

These are illustrative mappings. The actual mapping must be checked against the client's data dictionary.

### Step 4: Standardise units and formats

Before execution:

- Convert duration and rotation times into minutes.
- Use miles for `DISTANCE`, consistent with the training dataset.
- Ensure airport codes are standardised to uppercase three-letter identifiers.
- Use the documented weekday convention.
- Ensure incoming arrival and rotation times share the same timeline.
- Confirm that each `BLOCK_ID` uniquely identifies one eligible rotation.

Do not assume that a time-zone conversion is unnecessary. Scheduled departure and arrival fields may originate in different local time zones.

### Step 5: Identify missing and inconsistent information

Inspect missing values, duplicate identifiers, implausible times, conflicting aircraft assignments and incomplete operational commitments.

Do not automatically replace missing aircraft readiness values with zero or substitute guessed operational details.

If mandatory information cannot be established reliably, stop the affected analysis and obtain corrected data.

---

## 4. Mandatory data quality checkpoints

The following checks should be completed before trusting a decision-support run.

| Checkpoint | Required condition | Action if unsuccessful |
|---|---|---|
| File readability | CSV opens and contains the expected headers | Correct file formatting |
| Required columns | All mandatory fields are present | Map or obtain missing fields |
| Numeric validity | Numeric data are finite and within expected ranges | Correct the source values |
| Airport codes | Origin and destination are valid and consistent | Verify against an authoritative airport reference |
| Temporal consistency | Dates, hours and elapsed times follow the same conventions | Recalculate or correct timestamps |
| Identifier uniqueness | `BLOCK_ID` is unique in each relevant input | Investigate duplicate records |
| Integrated matching | Exactly one incoming record matches each rotation block | Fix unmatched or duplicate identifiers |
| Rotation chronology | Block start precedes block end, and next departure follows block end | Investigate schedule sequence |
| Aircraft assignment | Tail identifiers and rotation sequences are consistent | Reconstruct affected rotations |
| Forecast availability | Predictions use information available at the intended decision time | Exclude unavailable or hindsight information |
| Operational feasibility | Equipment, crew, maintenance, gates and other commitments are verified | Retain REVIEW_REQUIRED or reject |
| Model applicability | Data resemble the setting and definitions used for model development | Assess data drift and retraining requirements |

**Implementation distinction:** The application already checks selected schema, numeric, identifier and chronology conditions. Other checks above are mandatory **analyst or client validation responsibilities**, not automated features of the current application.

A successful program execution does not mean all business and operational checks passed.

---

## 5. Running the application

Open Terminal and navigate to the project repository.

### 5.1 Install dependencies

```bash
python -m pip install -r requirements.txt
```

Use a compatible Python environment and the tested dependency versions.

The trained model must be obtained from a trusted source and supplied separately. It is not included in the public GitHub repository.

### 5.2 Predict mode

```bash
python src/app.py predict \
  --flights "/path/to/future_flights.csv" \
  --model "/path/to/schedule_rf_pipeline.joblib" \
  --output-dir "/path/to/prediction_results"
```

The application produces `predicted_flight_delays.csv`.

### 5.3 Recover mode

```bash
python src/app.py recover \
  --blocks "/path/to/aircraft_rotation_blocks.csv" \
  --output-dir "/path/to/recovery_results"
```

The application produces screened candidates, reviewed swap recommendations, a screening summary and a JSON results summary.

### 5.4 Integrated mode

```bash
python src/app.py integrated \
  --incoming "/path/to/incoming_flights.csv" \
  --blocks "/path/to/rotation_blocks.csv" \
  --model "/path/to/schedule_rf_pipeline.joblib" \
  --output-dir "/path/to/integrated_results"
```

The application generates predicted incoming-aircraft readiness, matches it to the rotation blocks, runs candidate screening and MILP optimisation, and applies the safety-review gate.

If execution fails, correct the underlying issue and rerun the application. Do not bypass validation checks simply to obtain an output.

---

## 6. Understanding the results

### Predicted arrival delay

`PREDICTED_ARR_DELAY_MIN` estimates the non-negative arrival-delay quantity returned by the schedule-only Random Forest pipeline.

It is a model prediction, not an observed or guaranteed arrival delay. Early-arrival predictions are clipped to zero in the current implementation.

### Predicted aircraft readiness

`PRED_READY_MIN` represents the estimated time when an incoming aircraft becomes available after its forecast arrival and the configured turnaround allowance.

### Predicted baseline shortfall

The baseline is the sum of positive differences between predicted aircraft readiness and the scheduled start of its assigned block.

This is a mathematical measure of forecast-based start shortfall, not the total delay experienced by passengers.

### Predicted swap benefit

The optimiser calculates the reduction in this proxy objective when aircraft exchange eligible rotation blocks under the implemented scheduling rules.

For example, a reported benefit of 26.54 minutes means that the tested scenario's **forecast-based shortfall proxy** decreases by 26.54 minutes.

It does not mean the airline saved 26.54 minutes of realised operational delay.

### Optimisation status

`OPTIMAL` indicates that the mathematical optimisation problem was solved to optimality under the implemented model and solver configuration.

`NO_SWAP` indicates that no positive-benefit exchange was selected.

Neither status establishes real-world aircraft dispatch feasibility.

### Operational review status

| Status | Interpretation | Permitted action |
|---|---|---|
| REVIEW_REQUIRED | Required operational evidence is incomplete | Refer for independent review |
| REJECT | At least one supplied operational check failed | Do not action the candidate |
| CHECKS_REPORTED_PASSED | All supplied checks are reported as passing | Still requires human dispatch authorisation |

The prototype sets `OPERATIONALLY_AUTHORISED` to `False` for all selected mathematical exchanges.

---

## 7. Troubleshooting and corrective actions

| Problem | Likely cause | Recommended response |
|---|---|---|
| Missing required columns | Incorrect source-to-schema mapping | Rename columns or amend the source export |
| Invalid numeric values | Incorrect units, blanks or malformed data | Check source values and conversions |
| Duplicate BLOCK_ID | Repeated or incorrectly combined rotations | Resolve duplicates in the source system |
| Unmatched incoming records | Inconsistent identifiers or missing flights | Reconcile incoming and rotation files |
| Model file not found | Incorrect path or model not supplied | Obtain the trusted model and verify its path |
| Model feature mismatch | Incorrect saved model or feature schema | Verify model provenance and training configuration |
| No beneficial swaps | No pair passes screening or offers positive proxy benefit | Inspect screening results; do not force an exchange |
| Solver error | Numerical, configuration or optimisation failure | Review solver diagnostics; do not treat as a valid solution |
| Operational review required | Missing verified feasibility information | Obtain evidence from authorised personnel |

If results differ materially from the tested reference cases, investigate data definitions, software versions, model provenance, optimisation parameters and input quality.

---

## 8. Operational limitations and responsible use

The prototype must not be deployed as an autonomous airline dispatch system.

The schedule-only Random Forest showed weak predictive explanatory power in the 2024 validation assessment, with R² approximately 0.0112.

Forecasts may therefore be unreliable for individual flights, especially when unexpected weather, air traffic constraints or disruption events occur.

The optimiser does not comprehensively enforce all aircraft movement, maintenance, crew, equipment, airport and fleet constraints.

Before any real-world operational evaluation, the organisation would need to:

1. Establish a reliable, time-valid operational data pipeline.
2. Verify the model on representative current data.
3. Evaluate forecast errors and uncertainty.
4. Implement and test complete operational constraints.
5. Require independent human authorisation.
6. Conduct controlled evaluation before considering deployment.

The system is best interpreted as an educational prototype demonstrating how predictive analytics can be connected to constrained optimisation and decision review.

---

## 9. Reproducibility and testing evidence

The standalone application has been tested using:

- A three-flight independent CSV prediction scenario.
- A synthetic recovery scenario with one mathematically beneficial exchange.
- A synthetic integrated prediction-to-recovery scenario.
- A historical January 16, 2024 ATL regression scenario containing 171 eligible blocks.
- Input-validation tests involving missing columns and duplicate block identifiers.
- A fail-closed operational review test.

The January 16 historical test reproduced 19 positive-benefit candidates, eight selected mathematical swaps and approximately 81.82 minutes of predicted proxy improvement.

These results demonstrate consistency across the tested implementations. They do not establish that equivalent improvements would be achieved in live operations.

For reliable reproduction, retain the applicable source code version, dependency versions, trusted model artifact, input schemas, optimisation parameters and test outputs.
