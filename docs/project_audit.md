
# Methodology and Model Audit

## BUSI6029 — Individual Project Audit Framework

**Project:** Delta Air Lines Flight Delay Analytics  
**Audit category:** Methodology and Model Audit  
**Status:** Preliminary evidence checklist

## 1. Audit Objective

To systematically assess the methodological
validity, model assumptions, evaluation strategy,
reproducibility, and responsible interpretation
of the project's predictive and prescriptive
analytics components.

The audit aims to identify strengths,
limitations and opportunities for improvement.

## 2. Audit Scope

The proposed audit covers:

- Predictive model design.
- Training and validation procedures.
- Feature selection and availability.
- Prescriptive optimisation assumptions.
- Objective functions and constraints.
- Sensitivity analysis.
- Forecast-assisted optimisation.
- Reproducibility and documentation.

## 3. Audit Criteria

Each criterion should be assessed using:

- Pass
- Partial
- Fail
- Not assessed

The auditor should record supporting evidence
and recommended corrective actions.

## 4. Audit Checklist

### A. Business Problem and Method Selection

Question:
Is the analytical problem clearly defined?

Evidence to inspect:
Project objectives, methodology, notebook introduction.

Question:
Are regression and integer programming
appropriate for the stated analytical goals?

Evidence to inspect:
Model development and optimisation formulation.

### B. Data and Feature Methodology

Question:
Are the datasets and transformations documented?

Evidence to inspect:
Data dictionary and Jupyter preprocessing cells.

Question:
Could any predictive features introduce
information unavailable at decision time?

Evidence to inspect:
Feature definitions and temporal availability.

### C. Model Validation

Question:
Is the predictive evaluation separated by time?

Evidence to inspect:
2023 training, 2024 validation, and 2025 holdout.

Question:
Was the final holdout preserved from model tuning?

Evidence to inspect:
Modelling sequence and evaluation code.

Question:
Are MAE, RMSE and R-squared reported accurately?

Evidence to inspect:
Saved prediction results and summary tables.

### D. Optimisation Methodology

Question:
Is the objective function explicitly defined?

Evidence to inspect:
ILP code and formulation.

Question:
Are decision variables and aircraft conflict
constraints implemented consistently?

Evidence to inspect:
Candidate screening and integer programme.

Question:
Are operational constraints and exclusions
clearly documented?

Evidence to inspect:
Turnaround, next-flight and feasibility audits.

### E. Forecast Integration

Question:
Were forecast-only candidate decisions separated
from historical outcome evaluation?

Evidence to inspect:
Steps 3AK–3AN.

Question:
Are forecast feasibility and observed feasibility
clearly distinguished?

Evidence to inspect:
Selected-exchange evaluation tables.

### F. Sensitivity and Robustness

Question:
Were major scheduling assumptions tested?

Evidence to inspect:
Turnaround and safety-margin sensitivity results.

Question:
Are findings interpreted cautiously when
forecasts produce infeasible exchanges?

Evidence to inspect:
Sensitivity analysis and model limitations.

### G. Reproducibility

Question:
Are library versions documented?

Evidence to inspect:
requirements.txt.

Question:
Are datasets and derived features described?

Evidence to inspect:
docs/data_dictionary.md.

Question:
Can another user rerun the notebook using
the available documentation?

Evidence to inspect:
docs/reproducibility.md and a clean execution test.

## 5. Preliminary Evidence Summary

The project provides evidence of:

- Chronological predictive model evaluation.
- Recorded 2025 holdout metrics.
- Defined candidate-swap optimisation.
- Aircraft conflict constraints.
- Historical feasibility checks.
- Multiple operational sensitivity scenarios.
- Forecast-driven candidate generation.
- Documented forecast uncertainty and limitations.

These items still require independent verification
before being marked as formally audited.

## 6. Known Limitations Requiring Review

The following issues warrant specific attention:

- Full reproducibility has not been verified
  on a clean independent environment.
- Recovery features may create decision-time
  availability concerns.
- The optimisation does not fully represent
  equipment, crew and maintenance constraints.
- Forecast-driven candidates were evaluated
  retrospectively, not through a live deployment.
- The recovery sample was constructed using
  retrospective data-quality and schedule filters.

## 7. Audit Findings Template

For each finding, record:

Finding ID:
Audit criterion:
Status:
Supporting evidence:
Implication:
Corrective action:
Priority:
Responsible person:
Target completion date:

Do not label an audit item as fully passed
unless supporting evidence has been checked.

## 8. Suggested Improvement Actions

1. Validate notebook execution from a clean kernel.
2. Make local dataset configuration portable.
3. Document the exact preprocessing sequence.
4. Verify all model features against information
   available at the relevant decision point.
5. Extend the optimisation feasibility model.
6. Separate predicted objective values from
   historical proxy evaluation.
7. Maintain version-controlled audit evidence.

## 9. Reflection Prompts

- Which methodological decision was strongest?
- Which assumption created the greatest risk?
- How did the model change during the project?
- What could have been validated earlier?
- What would I do differently in a future
  Business Analytics project?

## 10. Audit Conclusion

The project has developed a detailed predictive
and prescriptive analytical framework.

However, a complete methodology audit requires
verification of implementation, reproducibility,
assumptions, and interpretation.

Any final Assessment 3 reflection should report
the actual evidence examined, findings identified,
and improvements proposed by the individual auditor.
