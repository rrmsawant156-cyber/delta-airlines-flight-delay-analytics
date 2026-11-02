# Publication and reproduction checklist

## Documentation stage (current)

- [x] Preserve existing notebook and `src/` prototype; do not overwrite unfinished work.
- [x] Add separately labelled 2024 sequential-delay results and financial scenarios.
- [x] Make assumptions, units, break-even thresholds and absence of realised savings explicit.
- [x] Document the current gap between updated results and repository-executable code.
- [ ] Add the *final reviewed* assessment report (PDF preferred) under `reports/`; check author names, grades/comments, student identifiers and other private information before publishing.
- [ ] Add the approved 10-minute stakeholder presentation under `presentations/`.
- [ ] Copy approved generated outputs from the local `delta_final_assessment_results` directory into suitable `results/` and `figures/` folders. Note: the repository currently ignores `*.csv`, so either adjust `.gitignore` carefully for curated small results or commit reviewed CSVs explicitly.
- [ ] Verify that the original 2024 Step 44 figure matches the result table.
- [ ] Decide whether the repository should remain private. It is **currently private**.

## Notebook cleanup stage (after user finalises code)

- [ ] Remove unnecessary cells and outputs *without changing logic*.
- [ ] Verify all notebook dependencies and local path configuration.
- [ ] Run from a clean kernel with documented input files and random seeds.
- [ ] Regenerate and compare descriptive, predictive, optimisation, finance, and Step 44 outputs.
- [ ] Reconcile exact report figures with fresh execution.
- [ ] Verify final notebook and CLI scripts agree where they overlap. The CLI prototype must not be represented as implementing all analyses automatically unless demonstrated.
- [ ] Document run time, machine/software environment, and accessible official BTS input sources.
- [ ] Replace `notebooks/BUSI6029_Assessment2_Delta.ipynb` only after these tests.

## Suggested safe data policy

Do not publish full raw/engineered flight CSVs, large joblib artefacts, credentials, student IDs, private email addresses, or sensitive internal records. Use URLs to official datasets where permissible; document download and preparation steps. Avoid placing a local Mac filesystem path into executable examples without an explicit configuration variable.

## Acceptance

This checklist should be completed before claiming **fully reproducible end-to-end results**.
