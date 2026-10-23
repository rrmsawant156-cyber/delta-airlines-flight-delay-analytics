
# Delta Air Lines — Data Dictionary

**Course:** BUSI6029 — Business Analytics Project 1  
**Project:** Flight Delay Prediction and Aircraft Recovery  
**Period:** 2023–2025  
**Status:** Academic project documentation

## 1. Dataset Overview

The project uses historical Delta Air Lines flight records
to investigate arrival delays, aircraft rotations, and
illustrative recovery opportunities.

Three main datasets support the analysis:

| Dataset | Columns | Purpose |
|---------|---------|---------|
| Delta_2023_2025_Raw.csv | 46 | Original flight records |
| Delta_2023_2025_Engineered.csv | 66 | Cleaned and engineered flight-level data |
| Delta_2023_2025_Recovery_Model.csv | 82 | Aircraft recovery and rotation features |

The recovery-model dataset contains 2,078,304 records.

The datasets are not uploaded to GitHub because of their
size and the need to verify redistribution permissions.

## 2. Flight Identification Variables

| Variable | Description |
|----------|-------------|
| FL_DATE | Scheduled flight date |
| TAIL_NUM | Aircraft registration identifier |
| OP_CARRIER_FL_NUM | Operating carrier's flight number |
| ORIGIN | Departure airport code |
| DEST | Destination airport code |

## 3. Scheduled Flight Characteristics

| Variable | Description |
|----------|-------------|
| MONTH | Calendar month |
| DAY_OF_WEEK | Day-of-week indicator |
| IS_WEEKEND | Indicator identifying weekend flights |
| CRS_DEP_TIME | Scheduled departure time in HHMM format |
| CRS_ARR_TIME | Scheduled arrival time in HHMM format |
| CRS_DEP_HOUR | Scheduled departure hour |
| CRS_ARR_HOUR | Scheduled arrival hour |
| CRS_ELAPSED_TIME | Scheduled elapsed flight time, minutes |
| DISTANCE | Flight distance, in miles |

Scheduled departure and arrival times should not be
treated as absolute timestamps without accounting for
dates, time zones, or overnight flights.

## 4. Arrival Delay Variables

| Variable | Description |
|----------|-------------|
| ARR_DELAY | Signed arrival delay in minutes; negative values indicate early arrivals |
| ARR_DELAY_NEW | Non-negative arrival-delay measure; early arrivals are represented as zero |

The predictive modelling target is ARR_DELAY_NEW.

The full-feature Random Forest predicts non-negative
arrival delays rather than signed early-arrival times.

## 5. Aircraft Rotation Features

| Variable | Description |
|----------|-------------|
| PREV_DATE | Date associated with the preceding aircraft movement |
| PREV_DEST | Destination of the previous aircraft movement |
| PREV_ARR_DELAY | Signed arrival delay of the preceding aircraft movement |
| SCHED_GROUND_MIN | Scheduled ground interval between linked aircraft movements, in minutes |
| SAME_DAY_SEQUENCE | Flag identifying aircraft sequence relationships within the processed data |
| LOCATION_CONTINUOUS | Flag indicating whether consecutive linked movements have consistent locations |

These features depend on historical aircraft sequencing
and may not always be available at an advance decision time.

## 6. Prescriptive Optimisation Variables

The following fields are used in the notebook's derived
aircraft rotation and optimisation tables.

| Variable | Description |
|----------|-------------|
| BLOCK_START_MIN | Scheduled departure minute of an eligible ATL round-trip block |
| BLOCK_END_MIN | Scheduled completion minute of the block |
| INCOMING_ARRIVAL_MIN | Estimated actual arrival minute of the preceding aircraft movement at ATL |
| FOLLOWING_DEP_MIN | Scheduled departure minute of the subsequent ATL flight for the same aircraft |
| REMOTE_GROUND_MIN | Scheduled turnaround interval at the outstation |
| ORIGINAL_START_SHORTFALL | Modelled shortfall between required aircraft readiness and the block's scheduled departure |
| BLOCK_ID | Identifier assigned to a rotation block within the analysis |

The optimisation selects reciprocal exchanges of ATL
round-trip blocks subject to the modelled scheduling
constraints.

These variables are analytical constructs and should
not be interpreted as independent airline operational
records.

## 7. Predictive Model Input Features

The recovery-enhanced Random Forest uses 11 inputs:

1. MONTH
2. DAY_OF_WEEK
3. IS_WEEKEND
4. CRS_DEP_HOUR
5. CRS_ARR_HOUR
6. CRS_ELAPSED_TIME
7. DISTANCE
8. ORIGIN
9. DEST
10. PREV_ARR_DELAY
11. SCHED_GROUND_MIN

A separate schedule-only Random Forest uses the first
nine features.

The schedule-only model supports retrospective
forecast-assisted optimisation experiments without
requiring the two aircraft rotation-related features.

## 8. Dataset Coverage and Filtering

The recovery-model dataset contains 2,078,304 records
covering the 2023–2025 modelling period.

The selected aircraft recovery case study examines
171 eligible ATL rotation blocks on 16 January 2024.

These blocks were obtained after applying the project's
data-quality, rotation-linkage and operational screening
rules.

They do not represent all Delta Air Lines aircraft
movements or all operational recovery opportunities.

## 9. Data Quality and Limitations

Important considerations include:

- Missing and incomplete aircraft movement records.
- Aircraft rotations excluded by processing rules.
- Historical delay information unavailable in advance.
- Potential limitations in timestamp reconstruction.
- Aircraft-type and equipment compatibility not verified.
- Crew and maintenance restrictions not fully represented.
- Results dependent on modelling assumptions.

Incoming-flight records were checked against the
engineered and raw datasets to investigate missing
predecessor records.

The aircraft recovery analysis should therefore be
interpreted as a retrospective mathematical case study,
not a validated operational dispatch system.

## 10. Data Governance

The large datasets are retained outside the GitHub
repository.

The repository documents analytical methodology and
variable definitions without distributing the underlying
flight-record CSV files.

Source provenance, redistribution permissions, data
integrity and reproducibility should be verified before
external sharing.
