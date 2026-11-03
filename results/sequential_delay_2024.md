# 2024 consecutive-aircraft delay association — Step 44

**Status:** Reported historical descriptive analysis; not a causal estimate.  
**Source:** Delta 2023–2025 prepared recovery dataset, 2024 subset; Step 44 executed in the working Jupyter notebook.  
**Population:** 696,776 operated, eligible consecutive-flight observations with a verified same-aircraft same-day predecessor and airport continuity.

## Comparison

| Previous aircraft arrival status | Flights | Mean previous arrival delay (min) | Mean next departure delay (min) | Mean next arrival delay (min) | Next departure delayed 15+ min | Next arrival delayed 15+ min |
|---|---:|---:|---:|---:|---:|---:|
| Previous flight 15+ minutes late | 102,083 | 57.05 | 48.97 | 43.19 | 69.46% | 59.60% |
| Previous flight under 15 minutes late | 594,693 | -10.66 | 1.43 | -5.05 | 8.62% | 10.00% |

The next-departure delay incidence is **60.84 percentage points**, approximately **8.1 times**, higher in the first group. This is an observational comparison: weather, airport congestion, and schedule structure may affect both flights. It does **not** prove that the predecessor delay caused the next departure delay or that an aircraft swap would prevent it.

These groups are **both sequential flights**. They are *not* a comparison between independently operated flights and aircraft rotations. Here, “individual” or “direct” should not be used to imply unlinked flights.

## Reproduction logic

1. Read the prepared recovery CSV.
2. Filter year to 2024 and keep operated flights with non-null current arrival/departure and previous arrival delay.
3. Require `SAME_DAY_SEQUENCE`, `LOCATION_CONTINUOUS`, an aircraft tail number, and nonnegative scheduled ground time.
4. Group the next flight by `PREV_ARR_DELAY >= 15`.
5. Report group counts, mean **signed** delays, and incidence of `DEP_DELAY >= 15` and `ARR_DELAY >= 15`.

Expected output: `10_sequential_delay_comparison.csv`, `figure_44a_next_departure_delay.png` and `figure_44b_delay_minutes_comparison.png` in the local results folder. These generated artifacts are **not yet committed here**; see `docs/publishing_checklist.md`.

Negative averages indicate flights operating earlier than scheduled, not data errors.

## Interpretation

The evidence motivates accounting for consecutive aircraft rotations in operational recovery decisions. It is not direct evidence that the proposed MILP aircraft exchanges would improve next-flight departure performance.
