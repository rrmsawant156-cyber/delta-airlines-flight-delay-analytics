"""Financial aircraft-recovery scenarios for academic decision support.

This module reoptimises EXISTING screened candidates under hypothetical cost
assumptions. It does not verify operational feasibility or actual savings.
"""

from dataclasses import dataclass
import numpy as np
import pandas as pd
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix


@dataclass(frozen=True)
class FinancialScenario:
    name: str
    conversion: float
    delay_cost_usd_per_min: float
    swap_cost_usd: float

    def __post_init__(self):
        for name, value in [
            ("conversion", self.conversion),
            ("delay_cost_usd_per_min", self.delay_cost_usd_per_min),
            ("swap_cost_usd", self.swap_cost_usd),
        ]:
            if isinstance(value, bool) or not np.isfinite(float(value)):
                raise ValueError(f"{name} must be finite and numeric")
        if not 0 < self.conversion <= 1:
            raise ValueError("conversion must be in (0,1]")
        if self.delay_cost_usd_per_min <= 0 or self.swap_cost_usd < 0:
            raise ValueError("delay cost must be positive and swap cost nonnegative")


DEFAULT_SCENARIOS = (
    FinancialScenario("Conservative", .25, 50.0, 500.0),
    FinancialScenario("Base", .50, 75.0, 500.0),
    FinancialScenario("Optimistic", 1.0, 100.0, 500.0),
)

REQUIRED = ("Tail A", "Tail B", "Predicted Benefit")


def financial_reoptimisation(candidates, scenarios=DEFAULT_SCENARIOS):
    """Compare no-action and cost-aware MILP choices using screened candidates.

    Selected swaps remain mathematical candidates requiring independent dispatch
    review. Input candidates must have been screened at the actual decision time.

    Returns (scenario_summary_df, selected_by_scenario, scored_candidates).
    """
    if not isinstance(candidates, pd.DataFrame):
        raise TypeError("candidates must be a pandas DataFrame")
    missing = set(REQUIRED).difference(candidates.columns)
    if missing:
        raise ValueError(f"Missing financial input columns: {sorted(missing)}")

    frame = candidates.copy().reset_index(drop=True)
    frame["Predicted Benefit"] = pd.to_numeric(frame["Predicted Benefit"], errors="raise")
    if not np.isfinite(frame["Predicted Benefit"].to_numpy(float)).all():
        raise ValueError("Predicted Benefit must be finite")
    if (frame["Predicted Benefit"] < 0).any():
        raise ValueError("Predicted Benefit must be nonnegative")
    if frame[list(REQUIRED)].isna().any().any():
        raise ValueError("Missing tail or benefit")
    for col in ("Tail A", "Tail B"):
        frame[col] = frame[col].astype(str).str.strip().str.upper()
        if frame[col].eq("").any():
            raise ValueError(f"Blank tail in {col}")
    if frame["Tail A"].eq(frame["Tail B"]).any():
        raise ValueError("Swap must use two different aircraft")

    aircraft = sorted(set(frame["Tail A"]) | set(frame["Tail B"]))
    membership = lil_matrix((len(aircraft), len(frame)), dtype=float)
    index = {tail: i for i, tail in enumerate(aircraft)}
    for j, r in frame.iterrows():
        membership[index[r["Tail A"]], j] = 1
        membership[index[r["Tail B"]], j] = 1
    mat = membership.tocsr()

    summary = []
    selected_by_scenario = {}
    for scenario in scenarios:
        if not isinstance(scenario, FinancialScenario):
            raise TypeError("Expected FinancialScenario instance")
        net_col = f"{scenario.name} Net Benefit ($)"
        frame[net_col] = (
            frame["Predicted Benefit"]
            * scenario.conversion
            * scenario.delay_cost_usd_per_min
            - scenario.swap_cost_usd
        )
        net = frame[net_col].to_numpy(dtype=float)
        if len(frame) == 0 or not (net > 1e-9).any():
            chosen = frame.iloc[0:0].copy()
        else:
            result = milp(
                c=-net,
                integrality=np.ones(len(frame), dtype=int),
                bounds=Bounds(np.zeros(len(frame)), np.ones(len(frame))),
                constraints=LinearConstraint(
                    mat, lb=np.zeros(len(aircraft)), ub=np.ones(len(aircraft))
                ),
                options={"mip_rel_gap": 0.0},
            )
            if result.status != 0 or result.x is None:
                raise RuntimeError(f"{scenario.name}: MILP optimum not confirmed: {result.message}")
            chosen = frame.loc[result.x > .5].copy()
        if len(chosen):
            flags = pd.concat([chosen["Tail A"], chosen["Tail B"]], ignore_index=True)
            if not flags.is_unique:
                raise AssertionError("Conflicting aircraft selected")
        modelled_net = float(chosen[net_col].sum())
        if modelled_net < -1e-7:
            raise AssertionError("Financial objective worse than no action")
        chosen["Operational Authorisation"] = "REVIEW_REQUIRED"
        chosen["Realised Savings"] = "NOT_ESTABLISHED"
        selected_by_scenario[scenario.name] = chosen
        summary.append({
            "Scenario": scenario.name,
            "Conversion Assumption": scenario.conversion,
            "Assumed USD per Avoided Delay Minute": scenario.delay_cost_usd_per_min,
            "Assumed USD per Swap": scenario.swap_cost_usd,
            "Break-even Predicted Shortfall (min)": (
                scenario.swap_cost_usd
                / (scenario.conversion * scenario.delay_cost_usd_per_min)
            ),
            "Selected Swaps": len(chosen),
            "Predicted Shortfall Benefit (min)": float(chosen["Predicted Benefit"].sum()),
            "Modelled Net Value (USD)": modelled_net,
            "Actual Savings Verified": False,
            "Dispatch Authorised": False,
        })
    return pd.DataFrame(summary), selected_by_scenario, frame
