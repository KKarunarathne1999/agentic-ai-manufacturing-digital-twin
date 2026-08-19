"""
Isolation Forest Evaluation
---------------------------

Training:
    Runs 1-24
    NORMAL observations only

Testing:
    Runs 25-30
    NORMAL + ANOMALY observations

Ground-truth labels:
    0 = NORMAL
    1 = ANOMALY

Isolation Forest output:
    1  = normal
    -1 = anomaly
"""

import csv

from sklearn.ensemble import IsolationForest
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

WARNING_TEMPERATURE = 40.0
WARNING_HEALTH = 85.0
BUFFER_CAPACITY = 5


# -------------------------------------------------
# CREATE GROUND-TRUTH LABEL
# -------------------------------------------------

def create_ground_truth(row):
    """
    Returns:
        0 = NORMAL
        1 = ANOMALY
    """

    m2_temperature = float(
        row["m2_temperature"]
    )

    m2_health = float(
        row["m2_health"]
    )

    m2_status = row[
        "m2_status"
    ]

    buffer_1 = int(
        row["buffer_1_level"]
    )

    # High temperature
    if m2_temperature >= WARNING_TEMPERATURE:
        return 1

    # Poor machine health
    if m2_health <= WARNING_HEALTH:
        return 1

    # Buffer congestion
    if buffer_1 >= BUFFER_CAPACITY:
        return 1

    # Failure / maintenance
    if m2_status in [
        "FAILED",
        "MAINTENANCE"
    ]:
        return 1

    return 0


# -------------------------------------------------
# EXTRACT FEATURES
# -------------------------------------------------

def extract_features(row):
    """
    Numerical features used by Isolation Forest.
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
    ]


# -------------------------------------------------
# LOAD DATASET
# -------------------------------------------------

def load_dataset(filename):
    """
    Training:
        runs 1-24
        ONLY normal observations

    Testing:
        runs 25-30
        normal + anomaly observations
    """

    train_features = []

    test_rows = []
    test_features = []
    test_labels = []

    total_training_rows = 0
    excluded_training_anomalies = 0

    with open(
        filename,
        mode="r",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            run_id = int(
                row["run_id"]
            )

            features = extract_features(
                row
            )

            label = create_ground_truth(
                row
            )

            # -----------------------------------------
            # TRAINING RUNS
            # -----------------------------------------

            if run_id <= TRAIN_RUN_MAX:

                total_training_rows += 1

                # VERY IMPORTANT:
                # Train ONLY on normal observations
                if label == 0:

                    train_features.append(
                        features
                    )

                else:

                    excluded_training_anomalies += 1

            # -----------------------------------------
            # TESTING RUNS
            # -----------------------------------------

            else:

                test_rows.append(
                    row
                )

                test_features.append(
                    features
                )

                test_labels.append(
                    label
                )

    return (
        train_features,
        test_rows,
        test_features,
        test_labels,
        total_training_rows,
        excluded_training_anomalies,
    )


# -------------------------------------------------
# TRAIN MODEL
# -------------------------------------------------

def train_model(train_features):
    """
    Train Isolation Forest using only
    healthy factory observations.
    """

    model = IsolationForest(
        n_estimators=300,
        contamination=0.05,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(
        train_features
    )

    return model


# -------------------------------------------------
# PREDICT
# -------------------------------------------------

def predict(model, test_features):
    """
    Isolation Forest returns:

        1  = normal
        -1 = anomaly

    Convert to:

        0 = normal
        1 = anomaly
    """

    raw_predictions = model.predict(
        test_features
    )

    scores = model.decision_function(
        test_features
    )

    predictions = [
        1 if prediction == -1 else 0
        for prediction in raw_predictions
    ]

    return predictions, scores


# -------------------------------------------------
# CLASS DISTRIBUTION
# -------------------------------------------------

def print_ground_truth_distribution(
    test_labels
):
    """
    Show normal/anomaly distribution.
    """

    total = len(
        test_labels
    )

    anomaly_count = sum(
        test_labels
    )

    normal_count = (
        total
        - anomaly_count
    )

    print("\nGround Truth Distribution")
    print("-" * 60)

    if total == 0:
        print("No test observations found.")
        return

    print(
        f"Normal observations  : "
        f"{normal_count} "
        f"({normal_count / total * 100:.2f}%)"
    )

    print(
        f"Anomaly observations : "
        f"{anomaly_count} "
        f"({anomaly_count / total * 100:.2f}%)"
    )


# -------------------------------------------------
# EVALUATION
# -------------------------------------------------

def evaluate(
    labels,
    predictions
):
    """
    Calculate evaluation metrics.
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
    print("=" * 70)
    print("ISOLATION FOREST EVALUATION")
    print("=" * 70)

    print(
        f"Accuracy  : {accuracy:.4f}"
    )

    print(
        f"Precision : {precision:.4f}"
    )

    print(
        f"Recall    : {recall:.4f}"
    )

    print(
        f"F1-score  : {f1:.4f}"
    )

    print("\nConfusion Matrix")
    print("-" * 70)

    print(matrix)

    print("\nMatrix format:")

    print(
        "[[True Normal, False Alarm],"
    )

    print(
        " [Missed Anomaly, Detected Anomaly]]"
    )

    print("\nClassification Report")
    print("-" * 70)

    print(
        classification_report(
            labels,
            predictions,
            labels=[0, 1],
            target_names=[
                "NORMAL",
                "ANOMALY",
            ],
            zero_division=0,
        )
    )


# -------------------------------------------------
# SAMPLE RESULTS
# -------------------------------------------------

def show_examples(
    rows,
    labels,
    predictions,
    scores,
    limit=30
):
    """
    Display anomaly-related predictions.
    """

    print("\n")
    print("=" * 105)
    print("SAMPLE ANOMALY PREDICTIONS")
    print("=" * 105)

    shown = 0

    for (
        row,
        true_label,
        predicted_label,
        score,
    ) in zip(
        rows,
        labels,
        predictions,
        scores,
    ):

        if (
            true_label == 1
            or predicted_label == 1
        ):

            print(
                f"Run {int(row['run_id']):>2} | "
                f"{float(row['timestamp']):>7.2f} sec | "
                f"True = {true_label} | "
                f"Pred = {predicted_label} | "
                f"Score = {score:.4f} | "
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

    (
        train_features,
        test_rows,
        test_features,
        test_labels,
        total_training_rows,
        excluded_training_anomalies,
    ) = load_dataset(
        CSV_FILE
    )

    print("\n")
    print("=" * 70)
    print("ML ANOMALY DETECTION CONFIGURATION")
    print("=" * 70)

    print(
        f"Total rows from runs 1-24     : "
        f"{total_training_rows}"
    )

    print(
        f"Excluded anomalous train rows : "
        f"{excluded_training_anomalies}"
    )

    print(
        f"Normal training observations  : "
        f"{len(train_features)}"
    )

    print(
        f"Testing observations          : "
        f"{len(test_features)}"
    )

    print(
        "Training mode                 : "
        "NORMAL ONLY"
    )

    print(
        "Training runs                 : "
        "1-24"
    )

    print(
        "Testing runs                  : "
        "25-30"
    )

    print(
        "Isolation Forest contamination: "
        "5%"
    )

    print_ground_truth_distribution(
        test_labels
    )

    # -----------------------------------------
    # SAFETY CHECKS
    # -----------------------------------------

    if len(train_features) == 0:

        raise RuntimeError(
            "No normal training observations found."
        )

    if len(test_features) == 0:

        raise RuntimeError(
            "No testing observations found."
        )

    # -----------------------------------------
    # TRAIN
    # -----------------------------------------

    model = train_model(
        train_features
    )

    # -----------------------------------------
    # PREDICT
    # -----------------------------------------

    predictions, scores = predict(
        model,
        test_features
    )

    # -----------------------------------------
    # EVALUATE
    # -----------------------------------------

    evaluate(
        test_labels,
        predictions
    )

    # -----------------------------------------
    # EXAMPLES
    # -----------------------------------------

    show_examples(
        test_rows,
        test_labels,
        predictions,
        scores
    )