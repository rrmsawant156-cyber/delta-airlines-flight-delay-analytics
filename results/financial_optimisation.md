# Financially informed aircraft-swap optimisation

**Status:** Scenario analysis of the 16 January 2024 Atlanta (ATL) academic case study. Monetary values are **ordinary US dollars**, not thousands or millions. None are verified realised Delta savings.

## From operational proxy to an economic decision

The original binary MILP selects mutually exclusive aircraft exchanges to maximise the predicted reduction in combined turnaround-readiness shortfall. The financial version maximises the sum of positive assumed net contributions, while retaining aircraft exclusivity and allowing **zero exchanges**.

For candidate swap `i` under assumed scenario `s`:

```text
modelled_net_benefit(i,s)
  = predicted_combined_shortfall_reduction_minutes(i)
    × assumed_conversion_fraction(s)
    × assumed_USD_per_avoided_delay_minute(s)
    − assumed_USD_per_swap(s)
```

Shortfall reduction is **not itself measured avoided departure delay**; the conversion factor is explicitly assumed.

| Scenario | Proxy-to-delay conversion | Assumed marginal delay value | Assumed incremental swap cost | Positive net requires predicted shortfall reduction above |
|---|---:|---:|---:|---:|
| Conservative | 25% | $50/min | $500/swap | 40.00 min |
| Base | 50% | $75/min | $500/swap | 13.33 min |
| Optimistic | 100% | $100/min | $500/swap | 5.00 min |

The break-even thresholds follow the model equation and assume no additional costs or interactions beyond those represented. Strictly positive net requires **more than** the threshold.

## Matched scenario results

The original shortfall-only MILP selected **8 swaps** from **19 candidate exchanges**, for a **predicted** 81.82-minute reduction against a 232.78-minute **forecast** shortfall baseline (35.15% of that proxy). The same original portfolio is valued under each financial scenario for a fair objective comparison.

| Scenario | Original MILP swaps | Original net (USD) | Financial MILP swaps | Financial net (USD) | Improvement in modelled objective (USD) |
|---|---:|---:|---:|---:|---:|
| Conservative | 8 | -2,977.28 | 0 | 0.00 | +2,977.28 |
| Base | 8 | -931.83 | 2 | +480.90 | +1,412.73 |
| Optimistic | 8 | +4,181.79 | 7 | +4,513.94 | +332.15 |

The economically preferable **modelled** choice can be not to intervene. The positive figures are conditional on assumed parameters; they are **not observed airline cost savings**.

## Retrospective feasibility diagnostics

- Of 19 forecast-generated candidates, **11 passed** and **8 failed** a *limited* hindsight scheduling screen.
- Of the **two base financial selections**, **one passed**.
- Of the **seven optimistic financial selections**, **three passed** (not five).
- When optimisation was **repeated with retrospective passing-candidate restrictions**, the base case selected **one swap**, with assumed net value **+$117.64**, and the optimistic case selected **five swaps**, with assumed net value **+$2,490.05**.
- **None of the 11 historically passing candidates** showed positive observed improvement in the tested turnaround-shortfall proxy.

The five-swap hindsight-reoptimised optimistic solution must **not** be described as five of the original seven financial choices passing the screen.

Hindsight checks use information that may not be known at the time of a real swap decision, and alternative aircraft assignments were never actually operated. This analysis establishes neither actual counterfactual departure delays nor realised economic benefits.

## BTS accounting benchmark and assumed coefficients

The supporting financial source is BTS Air Carrier Financial Schedule P-5.2, filtered to Delta domestic 2024 records. The project reported approximately **$7,108.34 per airborne hour**, or **$118.47 per airborne minute**, as an **average accounting expense benchmark**. BTS financial fields use their documented reporting scales, which must be checked when independently reproducing the calculation.

**This benchmark is not the marginal cost of one minute of ground delay, and is not the actual cost of exchanging two scheduled aircraft assignments.** The $50/$75/$100-per-minute coefficients and $500-per-swap charge are *illustrative*, not measured from the BTS table. Do not confuse the P-5.2 `INTERCHG_CHARG` accounting category with this operational swap charge.

## What is required before claiming savings?

Validated decision-time forecasts; empirically measured marginal delay and exchange costs; aircraft-type compatibility; crew, gate and maintenance feasibility; both-aircraft downstream scheduling effects; a prospective, multi-day, human-reviewed trial; and an appropriate no-intervention comparator.

**Conclusion:** A cost-aware decision-support *proof of concept*, not an airline savings claim.
