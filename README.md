
# Delta Air Lines | Flight Delay Analytics & Aircraft Recovery

### BUSI6029 — Business Analytics Project 1
**Academic Project | 2026**

## Project Overview

This project investigates flight arrival delays and aircraft recovery opportunities using Delta Air Lines flight records from 2023 to 2025.

The project applies business analytics techniques to:

- Explore historical flight delay patterns.
- Predict non-negative arrival delays using machine learning.
- Identify aircraft recovery opportunities using optimisation.
- Evaluate sensitivity to turnaround and scheduling constraints.
- Assess the reliability of forecast-assisted recovery decisions.
- Propose organisational change management recommendations.

The project is an academic case study and is not affiliated
with or endorsed by Delta Air Lines.

## November 2026 assessment update

The latest research adds a **2024 sequential-flight delay comparison** and a **financially informed aircraft-swap MILP**. These are documented in [Sequential Delay Results](results/sequential_delay_2024.md), [Financial Optimisation Results](results/financial_optimisation.md), and the [Assessment Update](docs/assessment_2026_update.md).

**Publication status:** The existing notebook and `src/` application have intentionally not been replaced while the final notebook is being cleaned. Some new findings were generated in a later local Jupyter workflow and **cannot yet be reproduced end-to-end solely from this GitHub checkout**. See the [publication and reproduction checklist](docs/publishing_checklist.md). All dollar figures are **ordinary USD** and **hypothetical scenario values, not verified savings**.

### Headline new findings

- In 696,776 eligible consecutive-flight observations from 2024, **69.46%** of next flights departed 15+ minutes late after a preceding arrival at least 15 minutes late, compared with **8.62%** otherwise. This comparison is observational and involves *two groups of sequential flights*.
- The forecast-assisted original MILP chose **8 swaps** with **81.82 minutes of predicted turnaround-shortfall-proxy improvement** (35.15% of the 232.78-minute forecast baseline). This is *not observed departure-delay savings*.
- Cost-aware optimisation chose **0 / 2 / 7** swaps under conservative / base / optimistic financial assumptions, with modelled net values of **$0 / +$480.90 / +$4,513.94**.
- Of **19** candidate exchanges, **11** passed limited retrospective screening, but none of those passing candidates showed positive observed shortfall-proxy improvement. The alternative swaps were not actually operated.

## Analytical Framework

The project combines:

1. Descriptive Analytics — exploratory analysis of flight data.
2. Predictive Analytics — regression-based arrival delay models.
3. Prescriptive Analytics — binary integer programming for
   illustrative aircraft rotation exchanges.
4. Sensitivity Analysis — scheduling margins, decision timing,
   and feasibility checks.
5. Change Management — proposed adoption of analytics-based
   decision support in airline operations.

## Data and Methodology

Historical records cover 2023–2025.

The predictive modelling framework used a temporal split:

| Dataset | Year | Purpose |
|---------|------|---------|
| Training | 2023 | Model development |
| Validation | 2024 | Model evaluation and selection |
| Holdout | 2025 | Final predictive evaluation |

The final recovery-enhanced Random Forest uses 11 features, including scheduled flight characteristics and aircraft
rotation-related information.

The prescriptive case study examines selected aircraft
rotations at Atlanta (ATL) on 16 January 2024.

## Predictive Analytics Results

The selected recovery-enhanced Random Forest achieved the
following performance on the 2025 holdout:

| Metric | Result |
|--------|--------|
| MAE | 12.76 minutes |
| RMSE | 36.21 minutes |
| R-squared | 0.3454 |

These metrics describe predictive performance, not the
effect of any aircraft reassignment intervention.

## Prescriptive Analytics Results

The retrospective aircraft recovery experiment analysed
171 eligible rotation blocks.

| Scenario | Selected Swaps | Modelled Shortfall Reduction |
|----------|----------------|-----------------------------|
| Historical hindsight benchmark | 17 | 361 min (19.88%) |
| Constrained hindsight scenario | 7 | 108 min (5.95%) |

The constrained hindsight scenario incorporates a 10-minute
additional scheduling margin and a 15-minute decision lead.

These reductions are mathematical turnaround-shortfall
proxies, not verified reductions in actual airline delays.

## Forecast-Assisted Optimisation

A previously fitted schedule-only Random Forest was used
to estimate incoming aircraft arrival delays for 171
eligible rotation blocks.

Key findings:

- Readiness forecast MAE: 32.58 minutes.
- Largest optimistic readiness error: 248.82 minutes.
- Forecast-generated exchange candidates: 19.
- Optimisation-selected exchanges: 8.
- Forecasted shortfall improvement: 81.82 minutes.
- Historical scheduling checks passed: 4 of 8.
- Observed proxy improvement from passing swaps: 0 minutes.

The forecast-derived baseline was 232.78 minutes, compared
with the observed historical baseline of 1,816 minutes.

The findings illustrate how forecast errors can affect
the feasibility and usefulness of prescriptive decisions.

## Sensitivity Analysis

Additional forecast-based scheduling margins of 10, 15,
20, 30, 45 and 60 minutes were investigated.

Larger margins reduced the number of forecast-based
recovery opportunities without consistently improving
historical feasibility.

No positive-benefit exchanges were selected at margins
of 30 minutes or greater in this experiment.

## Financial scenarios and responsible interpretation

The financial extension uses an assumed fraction of predicted shortfall improvement converted into avoided delay minutes, valued at an assumed marginal delay-minute cost, minus an assumed **$500 per swap**. Conservative / base / optimistic scenarios use **25% × $50/min**, **50% × $75/min**, and **100% × $100/min**, respectively. The reported BTS 2024 Delta domestic average accounting expense benchmark (~$118.47 per airborne minute) is **not** a measured marginal ground-delay cost. See [financial methods, comparisons and limitations](results/financial_optimisation.md).

## Repository Structure

- `notebooks/` — Jupyter Notebook containing project analysis.
- `README.md` — Project overview, methodology and findings.
- `results/sequential_delay_2024.md` — Latest Step 44 descriptive comparison.
- `results/financial_optimisation.md` — Cost-aware MILP scenarios and historical checks.
- `docs/assessment_2026_update.md` — Latest assessment addendum and code status.
- `docs/publishing_checklist.md` — Remaining report, figure, notebook and QA tasks.
- `.gitignore` — Exclusion rules for local datasets and files.

The latest final report, local results CSVs and chart image exports are **not yet uploaded**. We will add reviewed artifacts once their final versions are approved and available, without publishing student-identifying or sensitive information.

## Reproducibility

The large source datasets are not included in this GitHub
repository.

The notebook uses local dataset paths and requires access
to the corresponding input files to reproduce the analysis.

**Important:** The presently committed notebook predates the final Step 44 and financial updates. The results addenda preserve the recorded findings, but they are not a claim that the current checked-in notebook can regenerate all newer outputs. Review the [reproducibility guide](docs/reproducibility.md) and [publication checklist](docs/publishing_checklist.md) before attempting independent validation.

The project uses Python, pandas, NumPy, scikit-learn and
SciPy, among other analysis libraries.

## Limitations

- The aircraft recovery analysis is retrospective.
- Forecast errors can substantially affect aircraft readiness.
- Aircraft type and equipment compatibility are not verified.
- Crew, maintenance and full-network constraints are incomplete.
- The optimisation uses a turnaround-shortfall proxy.
- No real-world post-swap airline delay savings are established.
- The experiments do not constitute a live dispatch system.

## Conclusion

The study demonstrates how predictive modelling and
mathematical optimisation can support the analysis of
airline disruption management.

However, the retrospective evaluation reveals that
forecast uncertainty can significantly undermine the
feasibility of seemingly attractive recovery recommendations.

Practical deployment would require improved operational
information, uncertainty-aware decision support,
additional feasibility constraints and human oversight.

## Disclaimer

This repository is intended solely for academic purposes.
It is not an official Delta Air Lines project and does not
represent an operational airline recovery system.
