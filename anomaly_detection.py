"""
Factory Anomaly Detection
-------------------------

Reads digital-twin time-series data and identifies
abnormal operating conditions.

Initial detection rules:
- high temperature
- degraded health
- full upstream buffer
- machine failure state
"""

import csv


CSV_FILE = "data/factory_timeseries.csv"

WARNING_TEMP = 40.0
CRITICAL_TEMP = 50.0

WARNING_HEALTH = 85.0

BUFFER_WARNING_LEVEL = 5


def load_data(filename):
    """
    Load factory time-series data.
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


def detect_anomalies(rows):
    """
    Detect abnormal factory conditions.
    """

    anomalies = []

    for row in rows:

        timestamp = float(
            row["timestamp"]
        )

        # -----------------------------------------
        # MACHINE 1
        # -----------------------------------------

        m1_temp = float(
            row["m1_temperature"]
        )

        m1_health = float(
            row["m1_health"]
        )

        if m1_temp >= CRITICAL_TEMP:

            anomalies.append({
                "timestamp": timestamp,
                "machine": "M1",
                "type": "CRITICAL_TEMPERATURE",
                "value": m1_temp
            })

        elif m1_temp >= WARNING_TEMP:

            anomalies.append({
                "timestamp": timestamp,
                "machine": "M1",
                "type": "HIGH_TEMPERATURE",
                "value": m1_temp
            })

        if m1_health <= WARNING_HEALTH:

            anomalies.append({
                "timestamp": timestamp,
                "machine": "M1",
                "type": "LOW_HEALTH",
                "value": m1_health
            })

        # -----------------------------------------
        # MACHINE 2
        # -----------------------------------------

        m2_temp = float(
            row["m2_temperature"]
        )

        m2_health = float(
            row["m2_health"]
        )

        m2_status = row[
            "m2_status"
        ]

        if m2_temp >= CRITICAL_TEMP:

            anomalies.append({
                "timestamp": timestamp,
                "machine": "M2",
                "type": "CRITICAL_TEMPERATURE",
                "value": m2_temp
            })

        elif m2_temp >= WARNING_TEMP:

            anomalies.append({
                "timestamp": timestamp,
                "machine": "M2",
                "type": "HIGH_TEMPERATURE",
                "value": m2_temp
            })

        if m2_health <= WARNING_HEALTH:

            anomalies.append({
                "timestamp": timestamp,
                "machine": "M2",
                "type": "LOW_HEALTH",
                "value": m2_health
            })

        if m2_status == "FAILED":

            anomalies.append({
                "timestamp": timestamp,
                "machine": "M2",
                "type": "MACHINE_FAILURE",
                "value": m2_status
            })

        # -----------------------------------------
        # MACHINE 3
        # -----------------------------------------

        m3_temp = float(
            row["m3_temperature"]
        )

        m3_health = float(
            row["m3_health"]
        )

        if m3_temp >= CRITICAL_TEMP:

            anomalies.append({
                "timestamp": timestamp,
                "machine": "M3",
                "type": "CRITICAL_TEMPERATURE",
                "value": m3_temp
            })

        elif m3_temp >= WARNING_TEMP:

            anomalies.append({
                "timestamp": timestamp,
                "machine": "M3",
                "type": "HIGH_TEMPERATURE",
                "value": m3_temp
            })

        if m3_health <= WARNING_HEALTH:

            anomalies.append({
                "timestamp": timestamp,
                "machine": "M3",
                "type": "LOW_HEALTH",
                "value": m3_health
            })

        # -----------------------------------------
        # BUFFER CONGESTION
        # -----------------------------------------

        buffer_1 = int(
            row["buffer_1_level"]
        )

        if buffer_1 >= BUFFER_WARNING_LEVEL:

            anomalies.append({
                "timestamp": timestamp,
                "machine": "FACTORY",
                "type": "BUFFER_1_FULL",
                "value": buffer_1
            })

    return anomalies


def print_summary(anomalies):
    """
    Print detected anomalies.
    """

    print("\n" + "=" * 65)
    print("FACTORY ANOMALY DETECTION")
    print("=" * 65)

    print(
        f"Total anomalies detected: "
        f"{len(anomalies)}"
    )

    print("-" * 65)

    for anomaly in anomalies:

        print(
            f"{anomaly['timestamp']:>7.2f} sec | "
            f"{anomaly['machine']:<8} | "
            f"{anomaly['type']:<25} | "
            f"{anomaly['value']}"
        )

    print("=" * 65)


if __name__ == "__main__":

    data = load_data(
        CSV_FILE
    )

    anomalies = detect_anomalies(
        data
    )

    print_summary(
        anomalies
    )