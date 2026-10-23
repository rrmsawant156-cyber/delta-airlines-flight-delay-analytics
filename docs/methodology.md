
# Research Methodology

## Delta Air Lines — Predictive and Prescriptive Analytics

**Course:** BUSI6029 — Business Analytics Project 1  
**Study period:** 2023–2025  
**Recovery case study:** 16 January 2024

## 1. Research Objective

This academic project investigates whether historical
flight records can support arrival-delay prediction and
illustrative aircraft recovery decisions.

The study addresses three analytical questions:

1. How accurately can machine learning predict
   non-negative flight arrival delays?
2. What reductions in modelled turnaround shortfall
   are possible through constrained aircraft exchanges?
3. How does forecast uncertainty affect the feasibility
   and expected benefit of aircraft recovery decisions?

## 2. Data Preparation

The project uses three primary datasets:

- Delta_2023_2025_Raw.csv
- Delta_2023_2025_Engineered.csv
- Delta_2023_2025_Recovery_Model.csv

The recovery-model dataset contains 2,078,304 records.

Data processing includes flight-level cleaning,
feature engineering, aircraft movement sequencing,
and validation of aircraft-rotation relationships.

The recovery dataset is a filtered analytical sample
and does not represent every airline movement.

## 3. Predictive Modelling

The predictive target is ARR_DELAY_NEW, representing
non-negative arrival delay in minutes.

The recovery-enhanced Random Forest uses 11 features:

- MONTH
- DAY_OF_WEEK
- IS_WEEKEND
- CRS_DEP_HOUR
- CRS_ARR_HOUR
- CRS_ELAPSED_TIME
- DISTANCE
- ORIGIN
- DEST
- PREV_ARR_DELAY
- SCHED_GROUND_MIN

A separate schedule-only Random Forest excludes the
final two aircraft recovery features.

The schedule-only model supports a retrospective
forecast-assisted recovery experiment using nine
scheduled flight characteristics.

## 4. Temporal Validation

Data were separated chronologically:

| Year | Role | Records |
|------|------|---------|
| 2023 | Training | 680,913 |
| 2024 | Validation | 696,776 |
| 2025 | Final holdout | 700,615 |

The final recovery-enhanced Random Forest used:

- 60 estimators
- Maximum tree depth: 12
- Minimum samples per leaf: 20
- Maximum features fraction: 0.8
- Random state: 42

The selected model was evaluated on the 2025 holdout
without using that holdout to perform further tuning.

## 5. Predictive Results

| Metric | 2024 Validation | 2025 Holdout |
|--------|-----------------|--------------|
| MAE | 11.06 min | 12.76 min |
| RMSE | 31.57 min | 36.21 min |
| R-squared | 0.3846 | 0.3454 |

The 2024 schedule-only Random Forest achieved:

- MAE: 16.33 minutes
- RMSE: 40.02 minutes

The recovery-enhanced model performed better in the
retrospective validation setting. However, recovery
features may not be available before operational
decisions are made.

## 6. Prescriptive Analytics

The illustrative recovery experiment focuses on
eligible Atlanta (ATL) aircraft rotation blocks
on 16 January 2024.

The analysis identified 171 eligible blocks with
recorded subsequent ATL commitments.

Each eligible block represents a scheduled round trip
from ATL to an outstation and back to ATL.

Candidate exchanges are reciprocal swaps of blocks
between different aircraft.

The objective is to maximise the reduction in
modelled turnaround-readiness shortfall.

A simplified formulation is:

Maximise:

    sum(benefit_j * x_j)

Where:

- x_j is a binary decision variable for swap j.
- benefit_j is the modelled shortfall reduction.
- x_j = 1 indicates the exchange is selected.

Aircraft-use constraints prevent an aircraft from
participating in more than one selected exchange.

The model also screens candidates using represented
turnaround, departure-window, return commitment,
and intermediate-airport constraints.

The optimisation is implemented using SciPy's
mixed-integer linear programming solver.

## 7. Retrospective Optimisation

The original hindsight optimisation selected
17 non-conflicting reciprocal block exchanges.

Historical baseline shortfall:

    1,816 minutes

Modelled reduction:

    361 minutes

Percentage reduction:

    19.88%

A more conservative hindsight scenario applied
a 10-minute additional scheduling margin and
a 15-minute decision lead.

It selected seven exchanges with a modelled
reduction of 108 minutes, or 5.95%.

These values are mathematical shortfall proxies,
not demonstrated reductions in actual flight delays.

## 8. Predictive–Prescriptive Integration

The previously fitted schedule-only Random Forest
was applied to the 171 eligible incoming-flight records.

Predicted incoming delays were converted into
forecast-based aircraft-readiness estimates.

Candidate exchanges were subsequently screened using
forecasted readiness rather than observed delays.

A binary integer programme selected a non-conflicting
combination of forecast-generated exchanges.

Observed historical arrival times were retained for
retrospective evaluation after selection.

The experiment identified:

- 19 positive-benefit forecast-based candidates.
- Eight optimisation-selected exchanges.
- 81.82 minutes of predicted shortfall reduction.
- Four exchanges passing historical scheduling checks.
- Zero observed shortfall reduction among passing swaps.

## 9. Sensitivity Analysis

Forecast-based optimisation was repeated using
additional scheduling margins of:

10, 15, 20, 30, 45, and 60 minutes.

Increasing the margin reduced forecast-based
exchange opportunities.

No positive-benefit exchanges were selected
at 30 minutes or above in the tested scenarios.

The buffers are illustrative scheduling assumptions
rather than statistically calibrated prediction bounds.

## 10. Interpretation and Limitations

The analysis demonstrates that mathematical
optimisation can identify apparently beneficial
recovery decisions while remaining vulnerable
to inaccurate arrival-time predictions.

Additional limitations include:

- Retrospective selection of the recovery population.
- Missing aircraft equipment compatibility checks.
- Incomplete crew and maintenance constraints.
- Incomplete airline-wide operational information.
- No validated live decision-time information flow.
- No counterfactual flight-delay outcomes.

The models support research and decision-support
exploration, not automated operational deployment.

## 11. Reproducibility

The source notebook is available in the
notebooks/ directory.

Library versions are listed in requirements.txt.

Variable definitions are documented in
docs/data_dictionary.md.

The large input datasets are not distributed
through the repository.

Complete independent reproduction requires access
to the original datasets and verification of
the notebook execution sequence.
