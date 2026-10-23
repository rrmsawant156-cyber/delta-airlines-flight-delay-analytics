
"""
Delta Air Lines — Aircraft Recovery Optimisation
BUSI6029 Business Analytics Project

Academic predictive–prescriptive decision-support prototype.

This module:
1. Generates candidate reciprocal aircraft block exchanges.
2. Screens forecast readiness and scheduling margins.
3. Selects non-conflicting exchanges using SciPy MILP.
4. Returns NO_SWAP when no positive-benefit candidates exist.

IMPORTANT:
The modelled benefit is a turnaround-shortfall proxy,
NOT verified flight-delay savings.

Input blocks must already be constructed and validated.
Aircraft equipment, crew, maintenance, gate and complete
network feasibility are NOT independently verified here.
"""

from itertools import combinations

import numpy as np
import pandas as pd

from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix


REQUIRED_BLOCK_COLUMNS = [
    "BLOCK_ID",
    "TAIL_NUM",
    "DEST",
    "BLOCK_START_MIN",
    "BLOCK_END_MIN",
    "FOLLOWING_DEP_MIN",
    "REMOTE_GROUND_MIN",
    "PRED_READY_MIN",
]

CANDIDATE_COLUMNS = [
    "Block A Index",
    "Block B Index",
    "Tail A",
    "Tail B",
    "Route A",
    "Route B",
    "Predicted Original Shortfall",
    "Predicted Swapped Shortfall",
    "Predicted Benefit",
    "Minimum Forecast Scheduling Margin",
]


def _check_parameter(value, name, strictly_positive=False):
    if isinstance(value, (bool, str)):
        raise ValueError(f"{name} must be numeric.")

    try:
        value = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric.") from exc

    if not np.isfinite(value):
        raise ValueError(f"{name} must be finite.")

    if strictly_positive and value <= 0:
        raise ValueError(f"{name} must be positive.")

    if not strictly_positive and value < 0:
        raise ValueError(f"{name} cannot be negative.")

    return value


def generate_forecast_swap_candidates(
    blocks,
    extra_margin=10,
    departure_window=120,
    atl_turnaround=45,
    remote_turnaround=45,
):
    """
    Generate mathematically screened reciprocal swaps.

    All time variables must share one continuous timeline
    measured in minutes.

    This reproduces the core mathematical screening
    approach from the project's original Step 3AL.

    The function does not use observed arrival delays.
    """

    if not isinstance(blocks, pd.DataFrame):
        raise TypeError("blocks must be a pandas DataFrame.")

    missing = [
        col for col in REQUIRED_BLOCK_COLUMNS
        if col not in blocks.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required block columns: {missing}"
        )

    extra_margin = _check_parameter(
        extra_margin, "extra_margin"
    )

    departure_window = _check_parameter(
        departure_window, "departure_window"
    )

    atl_turnaround = _check_parameter(
        atl_turnaround, "atl_turnaround"
    )

    remote_turnaround = _check_parameter(
        remote_turnaround, "remote_turnaround"
    )

    population = blocks[
        REQUIRED_BLOCK_COLUMNS
    ].copy()

    if population.empty:
        raise ValueError(
            "The aircraft recovery input is empty."
        )

    if population.isna().any().any():
        raise ValueError(
            "Required recovery fields contain missing values."
        )

    if population["BLOCK_ID"].duplicated().any():
        raise ValueError(
            "BLOCK_ID values must be unique."
        )

    for col in ["TAIL_NUM", "DEST"]:
        population[col] = (
            population[col]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        if population[col].eq("").any():
            raise ValueError(
                f"{col} contains a blank value."
            )

    numeric_columns = [
        "BLOCK_START_MIN",
        "BLOCK_END_MIN",
        "FOLLOWING_DEP_MIN",
        "REMOTE_GROUND_MIN",
        "PRED_READY_MIN",
    ]

    for col in numeric_columns:
        population[col] = pd.to_numeric(
            population[col],
            errors="raise",
        )

        values = population[
            col
        ].to_numpy(dtype=float)

        if not np.isfinite(values).all():
            raise ValueError(
                f"{col} contains non-finite values."
            )

    if (
        population["BLOCK_END_MIN"]
        <= population["BLOCK_START_MIN"]
    ).any():
        raise ValueError(
            "Every block must end after it starts."
        )

    if (
        population["FOLLOWING_DEP_MIN"]
        <= population["BLOCK_END_MIN"]
    ).any():
        raise ValueError(
            "Following departure must be after block return."
        )

    if (population["REMOTE_GROUND_MIN"] < 0).any():
        raise ValueError(
            "REMOTE_GROUND_MIN cannot be negative."
        )

    population = (
        population.sort_values("BLOCK_ID")
        .reset_index(drop=True)
    )

    population["PRED_BASE_SHORTFALL"] = np.maximum(
        population["PRED_READY_MIN"]
        - population["BLOCK_START_MIN"],
        0.0,
    )

    predicted_baseline = float(
        population["PRED_BASE_SHORTFALL"].sum()
    )

    screening_counts = {
        "Distinct-tail pairs within departure window": 0,
        "Both forecasted swap starts meet safety margin": 0,
        "Next-flight and remote buffers also pass": 0,
        "Positive forecasted shortfall benefit": 0,
    }

    records = []

    for i, j in combinations(
        range(len(population)), 2
    ):
        a = population.iloc[i]
        b = population.iloc[j]

        if a["TAIL_NUM"] == b["TAIL_NUM"]:
            continue

        departure_difference = abs(
            a["BLOCK_START_MIN"]
            - b["BLOCK_START_MIN"]
        )

        if departure_difference > departure_window:
            continue

        screening_counts[
            "Distinct-tail pairs within departure window"
        ] += 1

        # Tail A takes Block B.
        start_margin_a = (
            b["BLOCK_START_MIN"]
            - a["PRED_READY_MIN"]
        )

        # Tail B takes Block A.
        start_margin_b = (
            a["BLOCK_START_MIN"]
            - b["PRED_READY_MIN"]
        )

        if min(
            start_margin_a,
            start_margin_b,
        ) < extra_margin:
            continue

        screening_counts[
            "Both forecasted swap starts meet safety margin"
        ] += 1

        # Check the next recorded ATL commitments.
        next_margin_a = (
            a["FOLLOWING_DEP_MIN"]
            - b["BLOCK_END_MIN"]
            - atl_turnaround
        )

        next_margin_b = (
            b["FOLLOWING_DEP_MIN"]
            - a["BLOCK_END_MIN"]
            - atl_turnaround
        )

        # Outstation turnaround margins.
        remote_margin_a = (
            b["REMOTE_GROUND_MIN"]
            - remote_turnaround
        )

        remote_margin_b = (
            a["REMOTE_GROUND_MIN"]
            - remote_turnaround
        )

        margins = [
            start_margin_a,
            start_margin_b,
            next_margin_a,
            next_margin_b,
            remote_margin_a,
            remote_margin_b,
        ]

        if min(margins) < extra_margin:
            continue

        screening_counts[
            "Next-flight and remote buffers also pass"
        ] += 1

        predicted_before = float(
            a["PRED_BASE_SHORTFALL"]
            + b["PRED_BASE_SHORTFALL"]
        )

        predicted_after = float(
            max(-start_margin_a, 0.0)
            + max(-start_margin_b, 0.0)
        )

        predicted_benefit = (
            predicted_before - predicted_after
        )

        if predicted_benefit <= 1e-8:
            continue

        screening_counts[
            "Positive forecasted shortfall benefit"
        ] += 1

        records.append({
            "Block A Index": a["BLOCK_ID"],
            "Block B Index": b["BLOCK_ID"],
            "Tail A": a["TAIL_NUM"],
            "Tail B": b["TAIL_NUM"],
            "Route A": f"ATL-{a['DEST']}-ATL",
            "Route B": f"ATL-{b['DEST']}-ATL",
            "Predicted Original Shortfall": predicted_before,
            "Predicted Swapped Shortfall": predicted_after,
            "Predicted Benefit": predicted_benefit,
            "Minimum Forecast Scheduling Margin": float(
                min(margins)
            ),
        })

    candidate_df = pd.DataFrame(
        records,
        columns=CANDIDATE_COLUMNS,
    )

    screening_summary = pd.DataFrame(
        list(screening_counts.items()),
        columns=["Screening Stage", "Pairs"],
    )

    return {
        "candidate_df": candidate_df,
        "screening_summary": screening_summary,
        "predicted_baseline_min": predicted_baseline,
        "eligible_blocks": len(population),
    }


def optimise_aircraft_swaps(
    candidate_df,
    time_limit=60,
):
    """
    Select non-conflicting swaps by maximising
    total predicted shortfall reduction.

    Each aircraft can participate in at most one swap.
    """

    if not isinstance(candidate_df, pd.DataFrame):
        raise TypeError(
            "candidate_df must be a DataFrame."
        )

    required = [
        "Tail A",
        "Tail B",
        "Predicted Benefit",
    ]

    missing = [
        col for col in required
        if col not in candidate_df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing candidate fields: {missing}"
        )

    time_limit = _check_parameter(
        time_limit,
        "time_limit",
        strictly_positive=True,
    )

    candidates = candidate_df.copy()

    if candidates[required].isna().any().any():
        raise ValueError(
            "Candidate aircraft or benefit values are missing."
        )

    candidates["Predicted Benefit"] = pd.to_numeric(
        candidates["Predicted Benefit"],
        errors="raise",
    )

    benefits_all = candidates[
        "Predicted Benefit"
    ].to_numpy(dtype=float)

    if not np.isfinite(benefits_all).all():
        raise ValueError(
            "All candidate benefits must be finite."
        )

    for col in ["Tail A", "Tail B"]:
        candidates[col] = (
            candidates[col].astype(str)
            .str.strip()
            .str.upper()
        )

        if candidates[col].eq("").any():
            raise ValueError(
                f"{col} cannot be blank."
            )

    if (
        candidates["Tail A"]
        == candidates["Tail B"]
    ).any():
        raise ValueError(
            "An aircraft cannot be swapped with itself."
        )

    candidates = (
        candidates.loc[
            candidates["Predicted Benefit"] > 1e-8
        ]
        .reset_index(drop=True)
    )

    if candidates.empty:
        return {
            "status": "NO_SWAP",
            "solver_message": "No positive-benefit candidates.",
            "candidate_count": 0,
            "selected_count": 0,
            "predicted_benefit_min": 0.0,
            "selected_swaps": candidates,
        }

    aircraft = sorted(
        set(candidates["Tail A"])
        | set(candidates["Tail B"])
    )

    aircraft_index = {
        tail: index
        for index, tail in enumerate(aircraft)
    }

    n_candidates = len(candidates)

    conflicts = lil_matrix(
        (len(aircraft), n_candidates),
        dtype=float,
    )

    for k, swap in candidates.iterrows():
        conflicts[
            aircraft_index[swap["Tail A"]], k
        ] = 1

        conflicts[
            aircraft_index[swap["Tail B"]], k
        ] = 1

    benefits = candidates[
        "Predicted Benefit"
    ].to_numpy(dtype=float)

    result = milp(
        c=-benefits,
        integrality=np.ones(
            n_candidates, dtype=int
        ),
        bounds=Bounds(
            np.zeros(n_candidates),
            np.ones(n_candidates),
        ),
        constraints=LinearConstraint(
            conflicts.tocsr(),
            lb=np.zeros(len(aircraft)),
            ub=np.ones(len(aircraft)),
        ),
        options={
            "time_limit": time_limit,
            "mip_rel_gap": 0.0,
        },
    )

    if result.status != 0 or result.x is None:
        raise RuntimeError(
            "MILP optimum not confirmed: "
            + str(result.message)
        )

    selected = (
        candidates.loc[result.x > 0.5]
        .copy()
        .sort_values(
            "Predicted Benefit",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    used_aircraft = (
        selected["Tail A"].tolist()
        + selected["Tail B"].tolist()
    )

    if len(used_aircraft) != len(set(used_aircraft)):
        raise AssertionError(
            "Selected swaps reuse an aircraft."
        )

    return {
        "status": "OPTIMAL",
        "solver_message": str(result.message),
        "candidate_count": n_candidates,
        "selected_count": len(selected),
        "predicted_benefit_min": float(
            selected["Predicted Benefit"].sum()
        ),
        "selected_swaps": selected,
    }


def recommend_aircraft_swaps(
    blocks,
    extra_margin=10,
    departure_window=120,
    atl_turnaround=45,
    remote_turnaround=45,
):
    """
    Run candidate generation and MILP optimisation.

    Input:
        Forecast-ready aircraft rotation block DataFrame.

    Output:
        A dictionary containing summary statistics,
        candidates, screening stages and selected swaps.

    No operational dispatch authorisation is implied.
    """

    screening = generate_forecast_swap_candidates(
        blocks=blocks,
        extra_margin=extra_margin,
        departure_window=departure_window,
        atl_turnaround=atl_turnaround,
        remote_turnaround=remote_turnaround,
    )

    solution = optimise_aircraft_swaps(
        screening["candidate_df"]
    )

    baseline = float(
        screening["predicted_baseline_min"]
    )

    benefit = float(
        solution["predicted_benefit_min"]
    )

    if benefit < -1e-8:
        raise ValueError(
            "Predicted benefit cannot be negative."
        )

    if benefit > baseline + 1e-6:
        raise ValueError(
            "Predicted benefit exceeds baseline shortfall."
        )

    improvement_pct = (
        100.0 * benefit / baseline
        if baseline > 0
        else 0.0
    )

    return {
        "status": solution["status"],
        "eligible_blocks": screening["eligible_blocks"],
        "candidate_count": solution["candidate_count"],
        "selected_count": solution["selected_count"],
        "predicted_baseline_min": baseline,
        "predicted_benefit_min": benefit,
        "predicted_remaining_shortfall_min": (
            baseline - benefit
        ),
        "predicted_improvement_pct": improvement_pct,
        "screening_summary": screening["screening_summary"],
        "candidate_df": screening["candidate_df"],
        "selected_swaps": solution["selected_swaps"],
    }
