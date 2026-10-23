
"""
Delta Air Lines — Operational Safety Review
BUSI6029 Business Analytics Project

Applies a fail-closed review gate to mathematical
aircraft swap candidates.

This module does NOT independently validate airline
operational requirements or issue dispatch approval.
"""

import pandas as pd


REQUIRED_APPROVAL_CHECKS = [
    "EQUIPMENT_COMPATIBLE",
    "CREW_FEASIBLE",
    "MAINTENANCE_CLEARED",
    "ADDITIONAL_COMMITMENTS_CLEARED",
    "GATE_AND_AIRPORT_FEASIBLE",
    "DECISION_TIME_DATA_VERIFIED",
]


def assess_swap_operational_readiness(
    selected_swaps,
    approval_evidence=None,
):
    """
    Assess operational review status for
    mathematically selected aircraft exchanges.

    Parameters
    ----------
    selected_swaps : pandas.DataFrame
        Swap candidates containing Tail A and Tail B.

    approval_evidence : pandas.DataFrame or None
        Optional independently obtained review evidence.

        Required fields:
        - Tail A
        - Tail B
        - All six REQUIRED_APPROVAL_CHECKS

        Check values must be True, False or missing.

    Returns
    -------
    pandas.DataFrame
        Selected candidates plus approval checks,
        REVIEW_STATUS, REVIEW_REASON and
        OPERATIONALLY_AUTHORISED.

    Statuses:
        REJECT:
            At least one check explicitly failed.

        REVIEW_REQUIRED:
            At least one check is missing or unverified.

        CHECKS_REPORTED_PASSED:
            All submitted checks report True.
            This is NOT dispatch authorisation.
    """

    if not isinstance(selected_swaps, pd.DataFrame):
        raise TypeError(
            "selected_swaps must be a DataFrame."
        )

    required_identity = ["Tail A", "Tail B"]

    missing_identity = [
        col for col in required_identity
        if col not in selected_swaps.columns
    ]

    if missing_identity:
        raise ValueError(
            f"Missing aircraft identifiers: {missing_identity}"
        )

    result = selected_swaps.copy()

    if result.empty:
        for col in REQUIRED_APPROVAL_CHECKS:
            result[col] = pd.Series(dtype="boolean")

        result["REVIEW_STATUS"] = pd.Series(
            dtype="object"
        )

        result["REVIEW_REASON"] = pd.Series(
            dtype="object"
        )

        result["OPERATIONALLY_AUTHORISED"] = pd.Series(
            dtype="bool"
        )

        return result

    if result[required_identity].isna().any().any():
        raise ValueError(
            "Selected swaps contain missing aircraft IDs."
        )

    for col in required_identity:
        result[col] = (
            result[col]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        if result[col].eq("").any():
            raise ValueError(
                f"{col} cannot be blank."
            )

    if approval_evidence is None:

        for col in REQUIRED_APPROVAL_CHECKS:
            result[col] = pd.NA

    else:

        if not isinstance(
            approval_evidence, pd.DataFrame
        ):
            raise TypeError(
                "approval_evidence must be a DataFrame."
            )

        required_evidence = (
            required_identity
            + REQUIRED_APPROVAL_CHECKS
        )

        missing = [
            col for col in required_evidence
            if col not in approval_evidence.columns
        ]

        if missing:
            raise ValueError(
                f"Missing approval fields: {missing}"
            )

        evidence = approval_evidence[
            required_evidence
        ].copy()

        for col in required_identity:
            if evidence[col].isna().any():
                raise ValueError(
                    f"{col} contains missing identifiers."
                )

            evidence[col] = (
                evidence[col]
                .astype(str)
                .str.strip()
                .str.upper()
            )

            if evidence[col].eq("").any():
                raise ValueError(
                    f"{col} cannot be blank."
                )

        if evidence.duplicated(
            required_identity
        ).any():
            raise ValueError(
                "Duplicate aircraft-pair approval evidence."
            )

        # Strictly allow True, False, or missing values.
        # Do not silently convert strings such as
        # 'True' or numeric values into approvals.
        for col in REQUIRED_APPROVAL_CHECKS:

            valid = evidence[col].map(
                lambda value: (
                    pd.isna(value)
                    or isinstance(value, bool)
                )
            )

            if not valid.all():
                raise ValueError(
                    f"{col} must contain True, "
                    "False, or missing."
                )

        result = result.merge(
            evidence,
            on=required_identity,
            how="left",
            validate="many_to_one",
        )

    def evaluate_row(row):

        failed = [
            col
            for col in REQUIRED_APPROVAL_CHECKS
            if (
                pd.notna(row[col])
                and row[col] == False
            )
        ]

        unknown = [
            col
            for col in REQUIRED_APPROVAL_CHECKS
            if pd.isna(row[col])
        ]

        if failed:
            return pd.Series({
                "REVIEW_STATUS": "REJECT",
                "REVIEW_REASON": (
                    "Failed checks: "
                    + ", ".join(failed)
                ),
            })

        if unknown:
            return pd.Series({
                "REVIEW_STATUS": "REVIEW_REQUIRED",
                "REVIEW_REASON": (
                    "Unverified: "
                    + ", ".join(unknown)
                ),
            })

        return pd.Series({
            "REVIEW_STATUS": "CHECKS_REPORTED_PASSED",
            "REVIEW_REASON": (
                "All supplied checks report passed. "
                "Independent verification and human "
                "dispatch authorisation are still required."
            ),
        })

    evaluations = result.apply(
        evaluate_row,
        axis=1,
    )

    result = pd.concat(
        [result, evaluations],
        axis=1,
    )

    # This prototype never authorises a swap.
    result["OPERATIONALLY_AUTHORISED"] = False

    return result


def summarise_safety_review(reviewed_swaps):
    """
    Summarise operational review outcomes.

    Returns counts of selected mathematical
    candidates by review status.
    """

    if not isinstance(reviewed_swaps, pd.DataFrame):
        raise TypeError(
            "reviewed_swaps must be a DataFrame."
        )

    if "REVIEW_STATUS" not in reviewed_swaps.columns:
        raise ValueError(
            "REVIEW_STATUS column is required."
        )

    counts = (
        reviewed_swaps["REVIEW_STATUS"]
        .value_counts()
        .to_dict()
    )

    return {
        "total_candidates": len(reviewed_swaps),
        "rejected": int(counts.get("REJECT", 0)),
        "review_required": int(
            counts.get("REVIEW_REQUIRED", 0)
        ),
        "checks_reported_passed": int(
            counts.get("CHECKS_REPORTED_PASSED", 0)
        ),
        "operationally_authorised": 0,
    }
