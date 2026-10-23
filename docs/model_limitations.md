
# Model Limitations and Responsible Interpretation

## 1. Purpose

This document records the principal methodological,
predictive, prescriptive, and operational limitations
identified in the Delta Air Lines analytics project.

The objective is to support transparent reporting
and prevent mathematical modelling outputs from
being misrepresented as realised airline benefits.

## 2. Predictive Modelling Limitations

### Historical Relationships

Random Forest regression estimates relationships
between historical inputs and observed arrival delays.

Predictive performance does not establish causal
effects of aircraft recovery interventions.

### Decision-Time Availability

The best-performing model uses aircraft-rotation
features such as PREV_ARR_DELAY and SCHED_GROUND_MIN.

Some features may be unavailable or uncertain
at the time an aircraft recovery decision is made.

### Schedule-Only Forecast Accuracy

The schedule-only model uses nine scheduled flight
characteristics and excludes recovery-specific inputs.

In the selected 171-block January 2024 diagnostic:

- Readiness MAE: 32.58 minutes.
- Readiness RMSE: 51.50 minutes.
- Mean signed error: +10.20 minutes.
- Maximum optimistic error: 248.82 minutes.

Positive signed error means actual readiness
occurred later than forecasted.

These results describe the selected retrospective
sample, not independent holdout performance.

### Extreme Disruptions

Several highly delayed aircraft received
comparatively small schedule-only predictions.

Therefore, schedule-derived predictions alone
were insufficient to capture some severe disruptions.

## 3. Data Coverage Limitations

The recovery-model dataset is filtered.

Some incoming-flight records were absent from
the filtered rotation sample but were successfully
recovered from the original raw dataset.

Exact predecessor matching was performed using
aircraft identifiers, flight dates, scheduled
arrival times, and signed arrival delays.

All 171 selected incoming flights were later
uniquely matched in the engineered dataset.

This improves historical data provenance but
does not validate real-time information availability.

## 4. Prescriptive Model Limitations

The binary integer programme is based on
illustrative scheduling constraints.

It does not comprehensively verify:

- Aircraft fleet and equipment compatibility.
- Crew legality and assignment constraints.
- Maintenance requirements.
- Passenger and cargo implications.
- Airport and gate availability.
- Complete aircraft network continuity.
- Real-time dispatch authorisation.

Therefore, mathematically feasible swaps are
not necessarily operationally executable.

## 5. Objective Function Limitation

The optimisation minimises a turnaround-readiness
shortfall proxy.

A proxy reduction should not be interpreted as
a measured reduction in actual arrival delays.

The model does not estimate all downstream
consequences of reassignment.

## 6. Retrospective Information Advantage

Historical hindsight scenarios use observed
incoming-flight arrival information.

Those scenarios can identify opportunities
that would not necessarily have been known
at an earlier decision point.

The 17-swap, 361-minute result is therefore
a retrospective mathematical benchmark.

The more constrained seven-swap, 108-minute
scenario remains a retrospective benchmark,
even though decision-lead constraints were tested.

## 7. Forecast-Assisted Evaluation

The schedule-only model produced a forecasted
baseline shortfall of 232.78 minutes.

The historical baseline was 1,816 minutes.

The forecast-driven optimiser selected eight
exchanges with an expected 81.82-minute
proxy improvement.

Only four exchanges passed retrospective
scheduling checks.

Those four passing exchanges produced zero
observed turnaround-shortfall proxy improvement.

The complete set of eight proposals produced
a -64-minute arithmetic proxy change, but
included infeasible exchanges.

This figure is not a realised operational loss.

## 8. Sensitivity Analysis Limitations

Fixed additional scheduling margins of 10,
15, 20, 30, 45, and 60 minutes were examined.

Increasing the margin reduced forecast-based
exchange opportunities without consistently
improving historical feasibility.

These margins were illustrative and were not
calibrated as statistical prediction intervals.

## 9. Generalisability

The recovery experiment covers a selected
Atlanta-based aircraft rotation population
on 16 January 2024.

Findings cannot automatically be generalised
to all Delta Air Lines operations, airports,
aircraft fleets, or operating conditions.

## 10. Future Improvements

Future development should prioritise:

1. Reliable, time-stamped operational data.
2. Formal forecast uncertainty estimation.
3. Equipment and aircraft-type compatibility.
4. Crew, maintenance, gate and network constraints.
5. More representative historical scenario testing.
6. Prospective decision-time evaluation.
7. Transparent human approval and audit controls.

## 11. Responsible Conclusion

The research demonstrates analytical potential,
not a validated operational aircraft recovery system.

Reported percentage improvements should always
be identified as either forecast-derived
expectations or retrospective mathematical proxies.

No actual post-intervention airline delay savings
have been established.
