"""Small deterministic financial-MILP tests (no airline data required)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
import pandas as pd
import pytest
from financial import FinancialScenario, financial_reoptimisation


def toy():
    return pd.DataFrame({
        "Tail A": ["A", "A", "D"],
        "Tail B": ["B", "C", "E"],
        "Predicted Benefit": [20.0, 30.0, 6.0],
    })


def test_default_conservative_is_no_swap():
    summary, selected, scored = financial_reoptimisation(toy())
    row = summary.set_index("Scenario").loc["Conservative"]
    assert row["Selected Swaps"] == 0
    assert row["Modelled Net Value (USD)"] == 0
    assert selected["Conservative"].empty


def test_financial_conflict_and_scenario_objective():
    scenario = FinancialScenario("Toy", 1.0, 100.0, 500.0)
    summary, selected, scored = financial_reoptimisation(toy(), (scenario,))
    # A-B: $1500; A-C: $2500; D-E: $100.
    # A-B and A-C conflict, so choose A-C and D-E.
    assert len(selected["Toy"]) == 2
    assert np.isclose(summary.loc[0, "Modelled Net Value (USD)"], 2600)
    assert len(set(selected["Toy"]["Tail A"]) | set(selected["Toy"]["Tail B"])) == 4
    assert (~summary["Dispatch Authorised"]).all()
    assert (~summary["Actual Savings Verified"]).all()


def test_all_unprofitable_returns_no_swap():
    scenario = FinancialScenario("Loss", .25, 50.0, 500.0)
    frame = toy().assign(**{"Predicted Benefit": [2.0, 3.0, 4.0]})
    summary, selected, _ = financial_reoptimisation(frame, (scenario,))
    assert selected["Loss"].empty
    assert summary.loc[0, "Modelled Net Value (USD)"] == 0


def test_empty_candidates():
    empty = toy().iloc[0:0].copy()
    summary, selected, _ = financial_reoptimisation(empty)
    assert (summary["Selected Swaps"] == 0).all()


@pytest.mark.parametrize("bad", [-1.0, np.nan, np.inf])
def test_invalid_benefit_rejected(bad):
    frame = toy()
    frame.loc[0, "Predicted Benefit"] = bad
    with pytest.raises(ValueError):
        financial_reoptimisation(frame)


def test_invalid_assumption_rejected():
    with pytest.raises(ValueError):
        FinancialScenario("Bad", 0.0, 75.0, 500.0)


def test_same_tail_rejected():
    frame = toy()
    frame.loc[0, "Tail B"] = "A"
    with pytest.raises(ValueError):
        financial_reoptimisation(frame)
