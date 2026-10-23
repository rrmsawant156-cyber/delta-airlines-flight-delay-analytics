
# ==========================================================
# DELTA AIR LINES — FLIGHT DELAY PREDICTION MODULE
# BUSI6029 Business Analytics Project
#
# Reusable schedule-only Random Forest predictions.
# No historical training data required at inference.
# ==========================================================

from pathlib import Path

import joblib
import numpy as np
import pandas as pd


REQUIRED_FEATURES = [
    "MONTH",
    "DAY_OF_WEEK",
    "IS_WEEKEND",
    "CRS_DEP_HOUR",
    "CRS_ARR_HOUR",
    "CRS_ELAPSED_TIME",
    "DISTANCE",
    "ORIGIN",
    "DEST",
]

NUMERIC_FEATURES = REQUIRED_FEATURES[:7]
AIRPORT_FEATURES = ["ORIGIN", "DEST"]


def load_prediction_model(model_path):
    """
    Load a previously fitted scikit-learn pipeline.

    SECURITY:
    Only load model files created by you or obtained
    from a fully trusted source. Joblib loading can
    execute code embedded in malicious files.
    """
    path = Path(model_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Trained model not found: {path}"
        )

    model = joblib.load(path)

    if not callable(getattr(model, "predict", None)):
        raise TypeError(
            "Loaded object does not support prediction."
        )

    actual_features = list(
        getattr(model, "feature_names_in_", [])
    )

    if actual_features != REQUIRED_FEATURES:
        raise ValueError(
            "Loaded model feature schema does not match "
            "the schedule-only prediction module."
        )

    return model


def predict_flight_delays(flights, model):
    """
    Predict non-negative arrival delays in minutes.

    Parameters
    ----------
    flights : pandas.DataFrame
        Input table with the nine scheduled-flight
        features. Additional columns are preserved.

    model : fitted scikit-learn pipeline
        Schedule-only Random Forest.

    Returns
    -------
    pandas.DataFrame
        Input records plus PREDICTED_ARR_DELAY_MIN.
    """

    if not isinstance(flights, pd.DataFrame):
        raise TypeError("flights must be a DataFrame.")

    if flights.empty:
        raise ValueError("Input flight table is empty.")

    missing = [
        col for col in REQUIRED_FEATURES
        if col not in flights.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    X = flights[REQUIRED_FEATURES].copy()

    for col in NUMERIC_FEATURES:
        X[col] = pd.to_numeric(
            X[col], errors="raise"
        )

    if X[NUMERIC_FEATURES].isna().any().any():
        raise ValueError(
            "Numeric prediction features contain "
            "missing values."
        )

    ranges = {
        "MONTH": (1, 12),
        "DAY_OF_WEEK": (1, 7),
        "IS_WEEKEND": (0, 1),
        "CRS_DEP_HOUR": (0, 23),
        "CRS_ARR_HOUR": (0, 23),
        "CRS_ELAPSED_TIME": (1, None),
        "DISTANCE": (1, None),
    }

    for col, (minimum, maximum) in ranges.items():
        values = X[col].to_numpy(dtype=float)

        if not np.isfinite(values).all():
            raise ValueError(
                f"{col} contains non-finite values."
            )

        if (values < minimum).any():
            raise ValueError(
                f"{col} contains invalid values."
            )

        if maximum is not None:
            if (values > maximum).any():
                raise ValueError(
                    f"{col} contains invalid values."
                )

    for col in AIRPORT_FEATURES:
        if X[col].isna().any():
            raise ValueError(
                f"{col} contains missing airport codes."
            )

        X[col] = (
            X[col].astype(str)
            .str.strip()
            .str.upper()
        )

        if not X[col].str.fullmatch(
            r"[A-Z]{3}"
        ).all():
            raise ValueError(
                f"{col} must contain three-letter "
                "airport codes."
            )

    predictions = np.asarray(
        model.predict(X), dtype=float
    )

    if not np.isfinite(predictions).all():
        raise ValueError(
            "Model produced non-finite predictions."
        )

    results = flights.copy()

    results["PREDICTED_ARR_DELAY_MIN"] = np.round(
        np.maximum(predictions, 0.0),
        2
    )

    return results


def predict_csv(input_path, model_path, output_path):
    """
    Load an external CSV, predict arrival delays,
    and save the results to another CSV.
    """

    flights = pd.read_csv(input_path)

    model = load_prediction_model(model_path)

    predictions = predict_flight_delays(
        flights, model
    )

    output = Path(output_path)
    output.parent.mkdir(
        parents=True, exist_ok=True
    )

    predictions.to_csv(
        output, index=False
    )

    return predictions
