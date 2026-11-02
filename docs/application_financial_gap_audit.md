# Standalone application audit — financial integration gap

**Review date:** 2 November 2026  
**Code reviewed:** `src/app.py`, `src/recovery.py`, `src/safety.py`, `src/prediction.py`, plus repository usage documentation.  
**Method:** GitHub source-level inspection only. This is **not** a successful end-to-end runtime test, nor an independent replication of the later Jupyter financial results.

## Current code behaviour — evidenced by inspection

- `src/app.py` exposes three CLI modes: `predict`, `recover`, `integrated`.
- `recover` and `integrated` call `recommend_aircraft_swaps` from `src/recovery.py`.
- `src/recovery.py` constructs candidate aircraft block exchanges and passes the `Predicted Benefit` (turnaround shortfall proxy) directly as the objective to SciPy `milp`.
- The current CLI summaries report eligible blocks, candidate swaps, selected swaps, forecast baseline, and **predicted proxy improvement**.
- The safety module applies an operational review gate. Its flags do **not** establish full dispatch safety or operational authorisation.

## Financial capabilities missing from the committed standalone app

1. No financial-mode CLI option or scenario configuration for `alpha`, marginal delay-minute cost, and incremental swap cost.
2. No objective coefficients based on `Predicted Benefit × alpha × delay_cost − swap_cost`.
3. No output comparing original shortfall-only selection with a separately reoptimised cost-aware portfolio.
4. No exported scenario-specific net values, break-even thresholds, or assumptions audit file.
5. No reproducible tests proving that a cost-aware optimiser chooses zero swaps when all net contributions are negative.
6. No independent runtime verification of parity with the final notebook results (0 / 2 / 7 swaps and scenario outputs) for the ATL research case.
7. No actual real-time information integration, calibrated marginal financial costs, or full aircraft/crew/network constraint checking.

## Implication

**The updated financial analysis is available as documented research results, not as an implemented feature of the current standalone application.** The app must not be described as a proven, financially integrated operational decision-support tool.

## Proposed extension without disrupting the working app

Add a **separate, opt-in financial mode** after the final notebook is cleaned and its result tables are independently reproduced.

Input: the same eligible candidate set produced by the original forecast-time screening, with each candidate's combined predicted shortfall improvement. Validate that these values are finite and nonnegative.

Optimisation: use the existing binary aircraft exclusivity matrix with scenario-specific net coefficients; candidates with no positive net contribution should not be selected. Allow zero swaps. Reject invalid negative cost and conversion inputs.

Output: original 8-swap benchmark valued under each financial scenario; financially reoptimised portfolio and individual selected candidate values; assumptions and units; scenario objective differences; review-required statuses; separate retrospective diagnostic pass counts.

**Do not use retrospective feasibility data to select live recommendations.** Hindsight screening belongs in diagnostic evaluation only.

## Minimum acceptance tests

| Test | Expected behaviour |
|---|---|
| Zero or negative net benefit across every candidate | Financial mode returns no swaps and $0 modelled net |
| Two candidates share an aircraft | No portfolio may contain both |
| Base ATL 2024 input | Exactly 2 financially selected swaps and +$480.90 modelled net **if inputs and conventions match the original notebook** |
| Conservative ATL case | 0 swaps and $0 |
| Optimistic ATL case | 7 swaps and +$4,513.94 modelled net |
| Input units | Monetary coefficients in USD, shortfall in minutes |
| Invalid inputs | Explicit error, not silent coercion |
| Original vs financial objective comparison | Value the original eight swaps using the **same** financial assumptions |
| Operational safeguards | Every proposed swap remains REVIEW REQUIRED; never auto-authorise |
| Decision-time integrity | No historical future information used for live selection |
| Provenance | Record dataset version, parameter values, and model version in outputs |
| Claims | Prohibit describing these hypothetical values as verified realised savings |

## Release status

**Not ready to claim financial-app parity.** The cleaned notebook, input fixtures, local execution environment and tests are still needed. The present audit is source inspection and a concrete acceptance plan.
