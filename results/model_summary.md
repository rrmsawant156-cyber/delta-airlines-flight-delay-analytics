
# Integrated Analytics Results

## Delta Air Lines — BUSI6029

**Analysis period:** 2023–2025  
**Aircraft recovery case study:** 16 January 2024

## 1. Predictive Model Results

The selected recovery-enhanced Random Forest
achieved the following performance:

| Metric | 2024 Validation | 2025 Holdout |
|--------|-----------------|--------------|
| MAE (min) | 11.06 | 12.76 |
| RMSE (min) | 31.57 | 36.21 |
| R-squared | 0.3846 | 0.3454 |

The 2024 schedule-only Random Forest achieved
an MAE of approximately 16.33 minutes.

Recovery-related features improved retrospective
prediction accuracy, but their availability
at operational decision time requires verification.

## 2. Historical Aircraft Recovery Optimisation

The retrospective recovery analysis examined
171 eligible ATL aircraft rotation blocks.

Historical baseline shortfall:

    1,816 minutes

Original hindsight solution:

    Selected swaps: 17
    Modelled reduction: 361 minutes
    Reduction: 19.88%

Constrained hindsight solution:

    Selected swaps: 7
    Additional margin: 10 minutes
    Decision lead: 15 minutes
    Modelled reduction: 108 minutes
    Reduction: 5.95%

These values are turnaround-shortfall proxies,
not realised reductions in airline delays.

## 3. Forecast Readiness Diagnostics

The schedule-only Random Forest estimated
incoming delays for all 171 eligible blocks.

| Measure | Result |
|---------|--------|
| Eligible blocks | 171 |
| Distinct aircraft | 120 |
| Readiness MAE | 32.58 min |
| Readiness RMSE | 51.50 min |
| Mean signed readiness error | +10.20 min |
| Largest optimistic error | 248.82 min |
| Blocks ready later than forecast | 71 |
| Blocks ready earlier than forecast | 100 |

These figures describe the selected
retrospective January 2024 population.

## 4. Forecast-Assisted Optimisation

Forecast-based no-swap shortfall:

    232.78 minutes

Historical no-swap shortfall:

    1,816 minutes

Forecast-based candidate screening:

    Distinct-tail pairs within time window: 5,453
    Pairs passing forecast start checks: 1,172
    Pairs passing additional scheduling checks: 257
    Positive-benefit candidates: 19

Optimisation selected:

    8 exchanges

Predicted objective improvement:

    81.82 minutes

Predicted improvement percentage:

    35.15% of forecast baseline

Historical evaluation:

    Passing exchanges: 4
    Failing exchanges: 4
    Proxy reduction among passing exchanges: 0 min

The percentage above represents a forecast-derived
expectation, not achieved operational improvement.

## 5. Forecast Safety-Margin Sensitivity

| Extra Margin | Swaps | Predicted Benefit | Historical Passes |
|--------------|-------|-------------------|-------------------|
| 10 min | 8 | 81.82 min | 4 |
| 15 min | 5 | 63.73 min | 1 |
| 20 min | 3 | 24.24 min | 0 |
| 30 min | 0 | 0 min | 0 |
| 45 min | 0 | 0 min | 0 |
| 60 min | 0 | 0 min | 0 |

The additional scheduling margins were
illustrative rather than statistically calibrated.

## 6. Interpretation

The hindsight optimisation identified meaningful
mathematical recovery opportunities.

However, forecast-only candidate generation
underestimated severe incoming-flight disruption.

This caused an important gap between predicted
and historically evaluated optimisation results.

The findings highlight the need for:

- More timely aircraft-arrival observations.
- Forecast uncertainty assessment.
- Robust scheduling and compatibility checks.
- Human approval and operational safeguards.
- Prospective evaluation before deployment.

## 7. Responsible Reporting

The following figures must not be presented
as interchangeable operational improvements:

- 19.88%: retrospective hindsight proxy.
- 5.95%: constrained hindsight proxy.
- 35.15%: forecast-derived objective improvement.
- 0%: historical proxy improvement among passing
  forecast-selected exchanges.

The underlying assumptions and baselines differ.

No actual post-swap airline delay savings
were established in this academic experiment.
