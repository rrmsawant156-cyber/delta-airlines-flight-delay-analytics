
"""
Delta Air Lines — Standalone Analytics Application
BUSI6029 Business Analytics Project

Modes:
  predict     Predict delays from a flight CSV.
  recover     Optimise an existing recovery-block CSV.
  integrated  Forecast incoming aircraft readiness and
              optimise recovery using two input CSVs.

All results are for academic decision support.
No aircraft exchange is operationally authorised.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from prediction import load_prediction_model, predict_flight_delays
from recovery import recommend_aircraft_swaps
from safety import (
    assess_swap_operational_readiness,
    summarise_safety_review,
)


TURNAROUND_MIN = 45

RECOVERY_COLUMNS = [
    "BLOCK_ID",
    "TAIL_NUM",
    "DEST",
    "BLOCK_START_MIN",
    "BLOCK_END_MIN",
    "FOLLOWING_DEP_MIN",
    "REMOTE_GROUND_MIN",
    "PRED_READY_MIN",
]


def load_csv(path):
    path = Path(path)

    if not path.is_file():
        raise FileNotFoundError(f"CSV file not found: {path}")

    return pd.read_csv(path)


def save_csv(frame, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    return path


def run_prediction(input_path, model_path, output_dir):
    """Run schedule-only flight delay prediction."""

    flights = load_csv(input_path)
    model = load_prediction_model(model_path)

    results = predict_flight_delays(flights, model)

    output = save_csv(
        results,
        Path(output_dir) / "predicted_flight_delays.csv",
    )

    print("\nFLIGHT DELAY PREDICTION")
    print("Input flights:", len(flights))
    print("Predictions generated:", len(results))
    print("Results:", output)

    return results


def calculate_readiness(incoming, model):
    """
    Calculate predicted aircraft readiness from
    scheduled incoming arrival and model predictions.

    INCOMING_SCHED_ARR_MIN must share the same
    continuous minute timeline as recovery blocks.
    """

    required = ["BLOCK_ID", "INCOMING_SCHED_ARR_MIN"]

    missing = [c for c in required if c not in incoming.columns]

    if missing:
        raise ValueError(
            f"Missing incoming flight fields: {missing}"
        )

    if incoming["BLOCK_ID"].isna().any():
        raise ValueError("Incoming BLOCK_ID cannot be missing.")

    if incoming["BLOCK_ID"].duplicated().any():
        raise ValueError("Incoming BLOCK_ID must be unique.")

    scheduled_arrival = pd.to_numeric(
        incoming["INCOMING_SCHED_ARR_MIN"],
        errors="raise",
    ).to_numpy(dtype=float)

    if not np.isfinite(scheduled_arrival).all():
        raise ValueError(
            "Incoming scheduled arrival contains invalid values."
        )

    results = predict_flight_delays(incoming, model)

    results["PRED_READY_MIN"] = (
        scheduled_arrival
        + results["PREDICTED_ARR_DELAY_MIN"].to_numpy(dtype=float)
        + TURNAROUND_MIN
    )

    return results


def prepare_integrated_blocks(blocks, incoming, model):
    """
    Connect incoming flight predictions to rotation
    blocks using their unique BLOCK_ID.

    Never use previously supplied readiness values
    in integrated mode.
    """

    if "BLOCK_ID" not in blocks.columns:
        raise ValueError("Blocks CSV requires BLOCK_ID.")

    if blocks["BLOCK_ID"].isna().any():
        raise ValueError("Block IDs cannot be missing.")

    if blocks["BLOCK_ID"].duplicated().any():
        raise ValueError("Block IDs must be unique.")

    readiness = calculate_readiness(incoming, model)

    blocks = blocks.drop(
        columns=["PRED_READY_MIN", "PREDICTED_ARR_DELAY_MIN"],
        errors="ignore",
    ).copy()

    merged = blocks.merge(
        readiness[
            [
                "BLOCK_ID",
                "PREDICTED_ARR_DELAY_MIN",
                "PRED_READY_MIN",
            ]
        ],
        on="BLOCK_ID",
        how="left",
        validate="one_to_one",
        indicator=True,
    )

    if not merged["_merge"].eq("both").all():
        raise ValueError(
            "One or more blocks have no matching incoming forecast."
        )

    if len(blocks) != len(incoming):
        raise ValueError(
            "Integrated mode requires exactly one incoming "
            "flight for each recovery block."
        )

    merged = merged.drop(columns=["_merge"])

    # Ensure the recovery engine's eight fields exist.
    missing = [
        col for col in RECOVERY_COLUMNS
        if col not in merged.columns
    ]

    if missing:
        raise ValueError(
            f"Integrated recovery input missing: {missing}"
        )

    return merged, readiness


def run_recovery(blocks, output_dir):
    """
    Run forecast-based mathematical optimisation and
    apply the operational review safeguard.
    """

    result = recommend_aircraft_swaps(
        blocks=blocks,
        extra_margin=10,
        departure_window=120,
        atl_turnaround=45,
        remote_turnaround=45,
    )

    reviewed = assess_swap_operational_readiness(
        result["selected_swaps"]
    )

    reviewed = reviewed.copy()

    reviewed["RECOMMENDATION_TYPE"] = (
        "MATHEMATICAL_CANDIDATE_ONLY"
    )

    reviewed["BENEFIT_INTERPRETATION"] = (
        "Forecast-based turnaround-shortfall proxy; "
        "not realised flight-delay savings"
    )

    safety_summary = summarise_safety_review(reviewed)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    save_csv(
        reviewed,
        output_dir / "reviewed_aircraft_swaps.csv",
    )

    save_csv(
        result["candidate_df"],
        output_dir / "screened_swap_candidates.csv",
    )

    save_csv(
        result["screening_summary"],
        output_dir / "swap_screening_summary.csv",
    )

    summary = {
        "status": result["status"],
        "eligible_blocks": int(result["eligible_blocks"]),
        "candidate_swaps": int(result["candidate_count"]),
        "selected_swaps": int(result["selected_count"]),
        "predicted_baseline_min": float(
            result["predicted_baseline_min"]
        ),
        "predicted_benefit_min": float(
            result["predicted_benefit_min"]
        ),
        "predicted_remaining_shortfall_min": float(
            result["predicted_remaining_shortfall_min"]
        ),
        "predicted_improvement_pct": float(
            result["predicted_improvement_pct"]
        ),
        "operational_review": safety_summary,
        "disclaimer": (
            "Academic mathematical decision support only. "
            "No swap is operationally authorised."
        ),
    }

    summary_path = output_dir / "recovery_summary.json"

    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    print("\nAIRCRAFT RECOVERY OPTIMISATION")
    print("Status:", summary["status"])
    print("Eligible blocks:", summary["eligible_blocks"])
    print("Candidates:", summary["candidate_swaps"])
    print("Selected mathematical swaps:", summary["selected_swaps"])
    print(
        "Predicted shortfall reduction:",
        round(summary["predicted_benefit_min"], 2),
        "minutes",
    )
    print("Operational authorisation: NONE")
    print("Results directory:", output_dir)

    if result["selected_count"] == 0:
        print("Decision: NO BENEFICIAL SWAP IDENTIFIED")
    else:
        print("Decision: CANDIDATES REQUIRE OPERATIONAL REVIEW")

    return summary


def main():
    parser = argparse.ArgumentParser(
        description="Delta Air Lines analytics prototype"
    )

    subparsers = parser.add_subparsers(
        dest="mode",
        required=True,
    )

    predict_parser = subparsers.add_parser("predict")
    predict_parser.add_argument("--flights", required=True)
    predict_parser.add_argument("--model", required=True)
    predict_parser.add_argument("--output-dir", required=True)

    recover_parser = subparsers.add_parser("recover")
    recover_parser.add_argument("--blocks", required=True)
    recover_parser.add_argument("--output-dir", required=True)

    integrated_parser = subparsers.add_parser("integrated")
    integrated_parser.add_argument("--incoming", required=True)
    integrated_parser.add_argument("--blocks", required=True)
    integrated_parser.add_argument("--model", required=True)
    integrated_parser.add_argument("--output-dir", required=True)

    args = parser.parse_args()

    if args.mode == "predict":
        run_prediction(
            args.flights,
            args.model,
            args.output_dir,
        )

    elif args.mode == "recover":
        blocks = load_csv(args.blocks)
        run_recovery(blocks, args.output_dir)

    elif args.mode == "integrated":
        blocks = load_csv(args.blocks)
        incoming = load_csv(args.incoming)
        model = load_prediction_model(args.model)

        prepared_blocks, readiness = prepare_integrated_blocks(
            blocks,
            incoming,
            model,
        )

        output_dir = Path(args.output_dir)

        save_csv(
            readiness,
            output_dir / "incoming_readiness_predictions.csv",
        )

        save_csv(
            prepared_blocks,
            output_dir / "forecast_ready_blocks.csv",
        )

        run_recovery(prepared_blocks, output_dir)


if __name__ == "__main__":
    main()
