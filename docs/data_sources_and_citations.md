# Data sources, attribution, and reporting units

## Project attribution

**Adelaide University — Business Analytics academic project (2026).** The source project began under the legacy University of Adelaide during the 2025 transition period. Adelaide University commenced operations in January 2026 following the merger of the University of Adelaide and the University of South Australia. The precise degree/course title and submitted institutional attribution should follow the student's current enrolment and assessment brief.

This is an **independent student academic project**, not research commissioned, endorsed, sponsored or operationally deployed by Adelaide University, Delta Air Lines or the U.S. Department of Transportation.

## Authoritative public input data

1. **U.S. Department of Transportation, Bureau of Transportation Statistics (BTS).** *Reporting Carrier On-Time Performance (1987–present)*, monthly domestic flight-level records. Used for the project’s Delta Air Lines (carrier code DL) 2023–2025 historical flight records, delays, cancellations, diversions, tails and aircraft-rotation analysis.
   - Table information: https://www.transtats.bts.gov/TableInfo.asp?QO_fu146_anzr=b0-gvzr&gnoyr_VQ=FGJ
   - Field definitions: https://www.transtats.bts.gov/Fields.asp?gnoyr_VQ=FGJ
2. **BTS.** *Air Carrier Financial — Schedule P-5.2: Aircraft Operating Expenses and Related Statistics*, quarterly aircraft financial records. Used for the contextual **2024 Delta domestic average airborne operating-expense benchmark**, not observed swap charges or marginal delay costs.
   - Table information: https://www.transtats.bts.gov/TableInfo.asp?QO_fu146_anzr=Nv4+Pn44vr4+Sv0n0pvny&gnoyr_VQ=FMK
   - Selection/download page: https://www.transtats.bts.gov/DL_SelectFields.aspx?QO_fu146_anzr=Nv4+Pn44vr4+Sv0n0pvny&gnoyr_VQ=FMK
3. **Adelaide University (institutional naming).** Official announcement of its January 2026 commencement: https://adelaide.edu.au/about/news/2026/a-bold-new-future-for-australian-higher-education-begins-today/

## Project data and calculated results

- Raw Delta historical population in local work: **3,020,512 flight observations, 2023–2025**.
- Filtered recovery-model dataset: **2,078,304** eligible records; it is **not** a complete record of every flight.
- Sequential-delay study (2024): **696,776** consecutive-aircraft observations, described in [results/sequential_delay_2024.md](../results/sequential_delay_2024.md).
- Cost-aware optimisation scenarios: modelled financial outputs described in [results/financial_optimisation.md](../results/financial_optimisation.md).
- Financial source: the locally supplied BTS Schedule P-5.2 export `T_F41SCHEDULE_P52(1).csv` was used during the research. The CSV is not currently included in the repository.

## Monetary and measurement distinctions

The academic analysis reported about **USD 118.47 per airborne minute** as an **average 2024 Delta domestic aircraft operating-expense benchmark** from P-5.2. Verify filtering and reporting scale before independent reproduction. This is neither the marginal cost of a minute of **ground delay** nor the incremental cost of swapping scheduled aircraft assignments.

The model instead **assumes** USD 50, 75, and 100 per avoidable delay minute, a 25%, 50%, and 100% proxy-to-delay conversion, and a fixed USD 500 per swap. All modelled net values are **ordinary US dollars** and are **hypothetical**. Do not multiply them by 1,000 or describe them as measured savings.

The P-5.2 `INTERCHG_CHARG` item describes aircraft interchange accounting; it is **not** the operational swap charge used by the model.

## Reuse and reproducibility

Follow the agency's download and applicable reuse conditions. The repository intentionally does not redistribute the large original BTS exports. Provide instructions, source tables, chosen fields, date/carrier filters, code version, data processing, and output checks when finalising the notebook.
