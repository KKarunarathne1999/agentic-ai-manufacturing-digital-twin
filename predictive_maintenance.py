"""
Predictive Maintenance Model
----------------------------

Predict whether Machine 2 will enter a failure or maintenance
state within the next prediction window.

Training runs:
    1-24

Testing runs:
    25-30

Target:
    0 = no failure soon
    1 = failure within next 15 simulated seconds
"""

import csv
import pickle
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)


# -------------------------------------------------
# CONFIGURATION
# -------------------------------------------------

CSV_FILE = "data/combined_factory_timeseries.csv"

TRAIN_RUN_MAX = 24

PREDICTION_WINDOW = 15


# -------------------------------------------------
# LOAD RAW DATA
# -------------------------------------------------

def load_rows(filename):
    """
    Load the combined time-series dataset.
    """

    rows = []

    with open(
        filename,
        mode="r",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            rows.append(row)

    return rows


# -------------------------------------------------
# GROUP BY SIMULATION RUN
# -------------------------------------------------

def group_by_run(rows):
    """
    Group observations by run_id.
    """

    runs = {}

    for row in rows:

        run_id = int(row["run_id"])

        if run_id not in runs:
            runs[run_id] = []

        runs[run_id].append(row)

    return runs


# -------------------------------------------------
# FUTURE FAILURE LABEL
# -------------------------------------------------

def create_failure_labels(run_rows):
    """
    Create target labels.

    For each timestamp, check whether Machine 2
    will enter FAILED or MAINTENANCE within the
    next PREDICTION_WINDOW seconds.

    Returns:
        list of 0/1 labels
    """

    labels = []

    for i, row in enumerate(run_rows):

        current_time = float(
            row["timestamp"]
        )

        future_limit = (
            current_time
            + PREDICTION_WINDOW
        )

        failure_soon = 0

        for future_row in run_rows[
            i + 1:
        ]:

            future_time = float(
                future_row["timestamp"]
            )

            if future_time > future_limit:
                break

            future_status = future_row[
                "m2_status"
            ]

            if future_status in [
                "FAILED",
                "MAINTENANCE",
            ]:
                failure_soon = 1
                break

        labels.append(
            failure_soon
        )

    return labels


# -------------------------------------------------
# FEATURE EXTRACTION
# -------------------------------------------------

def extract_features(row):
    """
    Features representing current factory condition.
    """

    return [
        float(row["m1_temperature"]),
        float(row["m1_health"]),

        float(row["m2_temperature"]),
        float(row["m2_health"]),

        float(row["m3_temperature"]),
        float(row["m3_health"]),

        float(row["buffer_1_level"]),
        float(row["buffer_2_level"]),

        1 if row["m2_status"] == "RUNNING" else 0,
        1 if row["m2_status"] == "IDLE" else 0,
    ]


# -------------------------------------------------
# BUILD ML DATASET
# -------------------------------------------------

def build_dataset(runs):
    """
    Create training and testing feature matrices.
    """

    train_features = []
    train_labels = []

    test_features = []
    test_labels = []

    test_rows = []

    for run_id, run_rows in runs.items():

        labels = create_failure_labels(
            run_rows
        )

        for row, label in zip(
            run_rows,
            labels
        ):

            features = extract_features(
                row
            )

            if run_id <= TRAIN_RUN_MAX:

                train_features.append(
                    features
                )

                train_labels.append(
                    label
                )

            else:

                test_features.append(
                    features
                )

                test_labels.append(
                    label
                )

                test_rows.append(
                    row
                )

    return (
        train_features,
        train_labels,
        test_features,
        test_labels,
        test_rows,
    )


# -------------------------------------------------
# TRAIN MODEL
# -------------------------------------------------

def train_model(
    train_features,
    train_labels
):
    """
    Train Random Forest classifier.
    """

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    model.fit(
        train_features,
        train_labels
    )

    return model


# -------------------------------------------------
# EVALUATION
# -------------------------------------------------

def evaluate(
    labels,
    predictions
):
    """
    Evaluate predictive-maintenance performance.
    """

    accuracy = accuracy_score(
        labels,
        predictions
    )

    precision = precision_score(
        labels,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        labels,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        labels,
        predictions,
        zero_division=0
    )

    matrix = confusion_matrix(
        labels,
        predictions,
        labels=[0, 1]
    )

    print("\n")
    print("=" * 75)
    print("PREDICTIVE MAINTENANCE EVALUATION")
    print("=" * 75)

    print(
        f"Prediction window : "
        f"{PREDICTION_WINDOW} sec"
    )

    print(
        f"Accuracy          : "
        f"{accuracy:.4f}"
    )

    print(
        f"Precision         : "
        f"{precision:.4f}"
    )

    print(
        f"Recall            : "
        f"{recall:.4f}"
    )

    print(
        f"F1-score          : "
        f"{f1:.4f}"
    )

    print("\nConfusion Matrix")
    print("-" * 75)

    print(matrix)

    print("\nMatrix format:")

    print(
        "[[No Failure correctly predicted, False Warning],"
    )

    print(
        " [Missed Future Failure, Correct Failure Prediction]]"
    )

    print("\nClassification Report")
    print("-" * 75)

    print(
        classification_report(
            labels,
            predictions,
            labels=[0, 1],
            target_names=[
                "NO FAILURE SOON",
                "FAILURE SOON",
            ],
            zero_division=0,
        )
    )


# -------------------------------------------------
# SHOW PREDICTIONS
# -------------------------------------------------

def show_examples(
    model,
    test_rows,
    test_features,
    test_labels,
    limit=30
):
    """
    Show failure-probability examples.
    """

    probabilities = model.predict_proba(
        test_features
    )[:, 1]

    predictions = model.predict(
        test_features
    )

    print("\n")
    print("=" * 105)
    print("SAMPLE FAILURE PREDICTIONS")
    print("=" * 105)

    shown = 0

    for (
        row,
        true_label,
        prediction,
        probability,
    ) in zip(
        test_rows,
        test_labels,
        predictions,
        probabilities,
    ):

        if (
            true_label == 1
            or prediction == 1
        ):

            print(
                f"Run {int(row['run_id']):>2} | "
                f"{float(row['timestamp']):>7.2f} sec | "
                f"True = {true_label} | "
                f"Pred = {prediction} | "
                f"Failure probability = "
                f"{probability:.3f} | "
                f"M2 Temp = "
                f"{float(row['m2_temperature']):.2f} C | "
                f"M2 Health = "
                f"{float(row['m2_health']):.2f}% | "
                f"B1 = {row['buffer_1_level']} | "
                f"Status = {row['m2_status']}"
            )

            shown += 1

            if shown >= limit:
                break


# -------------------------------------------------
# MAIN
# -------------------------------------------------

if __name__ == "__main__":

    import os

    import pickle

    # -----------------------------------------

    # LOAD DATA

    # -----------------------------------------

    rows = load_rows(

        CSV_FILE

    )

    runs = group_by_run(

        rows

    )

    (

        train_features,

        train_labels,

        test_features,

        test_labels,

        test_rows,

    ) = build_dataset(

        runs

    )

    # -----------------------------------------

    # CONFIGURATION SUMMARY

    # -----------------------------------------

    print("\n")

    print("=" * 75)

    print("PREDICTIVE MAINTENANCE CONFIGURATION")

    print("=" * 75)

    print(

        f"Training observations : "

        f"{len(train_features)}"

    )

    print(

        f"Testing observations  : "

        f"{len(test_features)}"

    )

    print(

        f"Training failure-soon : "

        f"{sum(train_labels)}"

    )

    print(

        f"Testing failure-soon  : "

        f"{sum(test_labels)}"

    )

    print(

        f"Prediction window     : "

        f"{PREDICTION_WINDOW} sec"

    )

    # -----------------------------------------

    # SAFETY CHECKS

    # -----------------------------------------

    if len(train_features) == 0:

        raise RuntimeError(

            "No training observations found."

        )

    if len(test_features) == 0:

        raise RuntimeError(

            "No testing observations found."

        )

    # -----------------------------------------

    # TRAIN MODEL

    # -----------------------------------------

    model = train_model(

        train_features,

        train_labels

    )

    print(

        "\nPredictive maintenance "

        "model trained successfully."

    )

    # -----------------------------------------

    # SAVE MODEL

    # -----------------------------------------

    os.makedirs(

        "models",

        exist_ok=True

    )

    model_path = (

        "models/predictive_maintenance.pkl"

    )

    with open(

        model_path,

        "wb"

    ) as file:

        pickle.dump(

            model,

            file

        )

    print(

        f"Model saved to: {model_path}"

    )

    # -----------------------------------------

    # PREDICT TEST DATA

    # -----------------------------------------

    predictions = model.predict(

        test_features

    )

    # -----------------------------------------

    # EVALUATE MODEL

    # -----------------------------------------

    evaluate(

        test_labels,

        predictions

    )

    # -----------------------------------------

    # SHOW EXAMPLE PREDICTIONS

    # -----------------------------------------

    show_examples(

        model,

        test_rows,

        test_features,

        test_labels

    )