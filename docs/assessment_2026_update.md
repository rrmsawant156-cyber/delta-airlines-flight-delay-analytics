# Assessment 2 update — November 2026

This document describes new analyses added to the academic project after the earlier repository snapshot. The existing `notebooks/BUSI6029_Assessment2_Delta.ipynb` and `src/` scripts have **not** been replaced or revalidated by this documentation update.

## New results

- **Step 44:** Direct comparison of consecutive aircraft operations by previous-flight arrival status; 696,776 valid 2024 observations. See [sequential results](../results/sequential_delay_2024.md).
- **Financial extension:** Cost-aware MILP with conservative, base and optimistic assumptions and an explicit no-swap option. See [financial results](../results/financial_optimisation.md).
- **Retrospective checks:** Separate the original portfolio's pass rates from hindsight-constrained reoptimisation; no verified realised saving is claimed.
- **Source financial benchmark:** BTS Schedule P-5.2 Delta 2024 accounting information is used only as contextual average expense, not as a marginal delay cost.

## Known integration gap

The original checked-in notebook and the standalone `src/` application may **not yet contain** the final Step 44 and cost-aware implementation. Do not assume an independent `git clone` reproduces every result documented here. The updated **cleaned notebook** is planned as a separate change once the full code has been reviewed, executed from a clean kernel, and cross-checked against the final report.

The current README and prior documentation may describe earlier experiments. For latest numerical claims, prefer the new result notes above and reconcile against the final cleaned notebook before calling the repository end-to-end reproducible.

## Current source of truth and ethics

The newest user-reviewed assessment report and original notebook executions provide the figures recorded in the result notes. This repository is not affiliated with Delta Air Lines. It contains an exploratory academic model, not safety-validated aircraft dispatch software. Neither predicted turnaround-shortfall reduction nor hypothetical net value is demonstrated realised airline benefit.
