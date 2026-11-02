# Time-critical aircraft-recovery decision support: stakeholder use case

## The practical question

When a current inbound aircraft is delayed and another compatible aircraft may be available, airline operations controllers need to decide quickly: **keep the original assignment, review an exchange candidate, or reject intervention**.

This academic system explores how forecasts, rotation constraints, and **assumed economic value** could be assembled to assist that decision at a critical operational moment.

**Decision support does not mean decision authority.** This prototype is not connected to Delta operational systems, is not ready for real-time dispatch, and does not issue instructions to change live aircraft assignments.

## Intended stakeholder workflow (proposed, not deployed)

| Step | Proposed evidence supplied to a decision-maker | Decision implication |
|---|---|---|
| 1. Detect | Updated incoming-aircraft delay and readiness observations, timestamped at decision time | Identify a shortfall risk |
| 2. Screen | Candidate reciprocal swaps, aircraft exclusivity and feasibility constraints | Remove impossible or conflicting options |
| 3. Compare | No-action baseline against the modelled readiness proxy after each swap | Quantify forecast benefits and uncertainty |
| 4. Value | Assumed avoided-delay conversion, marginal value of delay and fully estimated swap costs | Estimate scenario-specific net financial value |
| 5. Review | Aircraft type, crew legality, maintenance, gates, both-aircraft downstream rotations and human controller judgement | Accept, defer or reject a candidate |
| 6. Learn | Log recommendation time, approval reason, actual flight outcomes, counterfactual evaluation design and net incremental costs | Test prospective model value |

The currently committed standalone app automates only portions of prediction, candidate optimisation and review flagging. It **does not** perform the new cost-aware financial MILP. See [application gap audit](application_financial_gap_audit.md).

## Conditions for a considered exchange

- Forecast inputs available **before** the real intervention deadline, with measured uncertainty.
- Aircraft and crew operational compatibility confirmed, including both aircraft's future commitments.
- Positive net **expected** value under credible **measured** incremental cost estimates, not just assumed financial scenarios.
- An available *no-swap* alternative, explicit confidence and material-risk warnings.
- Independently verified operational feasibility and final authority retained by appropriately qualified operations personnel.

A sufficiently time-constrained or uncertain situation should produce **NO ACTION / REVIEW REQUIRED** rather than an automated reassignment.

## What the research establishes and does not establish

**Established in the academic analysis:** historical association between consecutive flight delays; predictive model metrics; mathematically optimised proxy improvement in an ATL case; scenario-sensitive financial choices; limited retrospective feasibility findings.

**Not established:** positive realised airline financial savings; causal benefits of swaps never operated; live decision latency; calibrated probabilities for specific disrupted operational conditions; compliance with all safety, maintenance, crew or network constraints; suitability for actual dispatch.

## Path toward potential business value

1. Freeze a reproducible notebook and backtest multiple dates and airports.
2. Implement, test and validate the financial objective using actual or appropriately calibrated marginal costs.
3. Build time-stamped, forecast-time eligibility checks and full aircraft/crew/network screening.
4. Conduct a monitored **shadow-mode** pilot without any actual swaps.
5. Compare results with a defensible no-intervention benchmark and measure actual incremental costs.
6. Advance toward a controlled human-authorised trial only if evidence supports it.

The value proposition is **better evidence for time-critical human decisions**, not replacing professional airline dispatchers.
