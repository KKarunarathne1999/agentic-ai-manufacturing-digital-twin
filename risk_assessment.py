"""
Factory Risk Assessment
-----------------------

Combines digital-twin operating conditions with
anomaly-detection concepts to classify machine risk.

Risk levels:
- NORMAL
- WARNING
- CRITICAL
- FAILURE

The main focus is Machine 2 because it is currently
the bottleneck and the machine with overheating/failure
behaviour in the simulation.
"""

import csv


CSV_FILE = "data/factory_timeseries.csv"


# -------------------------------------------------
# THRESHOLDS
# -------------------------------------------------

WARNING_TEMP = 40.0
CRITICAL_TEMP = 47.0
FAILURE_TEMP = 50.0

WARNING_HEALTH = 90.0
CRITICAL_HEALTH = 80.0

BUFFER_WARNING = 4
BUFFER_CRITICAL = 5


# -------------------------------------------------
# RISK CLASSIFICATION
# -------------------------------------------------

def assess_risk(row):
    """
    Assess Machine 2 operating risk.

    Returns
    -------
    risk_level : str
        NORMAL, WARNING, CRITICAL, or FAILURE

    reason : str
        Explanation for the assigned risk.
    """

    temperature = float(
        row["m2_temperature"]
    )

    health = float(
        row["m2_health"]
    )

    status = row[
        "m2_status"
    ]

    buffer_1 = int(
        row["buffer_1_level"]
    )

    # -------------------------------------------------
    # FAILURE
    # -------------------------------------------------

    if status in [
        "FAILED",
        "MAINTENANCE"
    ]:

        return (
            "FAILURE",
            f"Machine status is {status}"
        )

    if temperature >= FAILURE_TEMP:

        return (
            "FAILURE",
            f"Temperature reached "
            f"{temperature:.2f} C"
        )

    # -------------------------------------------------
    # CRITICAL
    # -------------------------------------------------

    if temperature >= CRITICAL_TEMP:

        return (
            "CRITICAL",
            f"Temperature is critically high "
            f"({temperature:.2f} C)"
        )

    if health <= CRITICAL_HEALTH:

        return (
            "CRITICAL",
            f"Machine health is critically low "
            f"({health:.2f}%)"
        )

    if buffer_1 >= BUFFER_CRITICAL:

        return (
            "CRITICAL",
            f"Buffer 1 is full "
            f"({buffer_1} products)"
        )

    # -------------------------------------------------
    # WARNING
    # -------------------------------------------------

    if temperature >= WARNING_TEMP:

        return (
            "WARNING",
            f"Temperature is elevated "
            f"({temperature:.2f} C)"
        )

    if health <= WARNING_HEALTH:

        return (
            "WARNING",
            f"Machine health is degrading "
            f"({health:.2f}%)"
        )

    if buffer_1 >= BUFFER_WARNING:

        return (
            "WARNING",
            f"Buffer 1 congestion detected "
            f"({buffer_1} products)"
        )

    # -------------------------------------------------
    # NORMAL
    # -------------------------------------------------

    return (
        "NORMAL",
        "Machine operating within expected limits"
    )


# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

def load_data(filename):
    """
    Load time-series observations.
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
# ANALYSE DATA
# -------------------------------------------------

def analyse_risk(rows):
    """
    Assess every time-series observation.
    """

    results = []

    for row in rows:

        risk_level, reason = assess_risk(
            row
        )

        results.append({
            "timestamp":
                float(row["timestamp"]),

            "risk":
                risk_level,

            "reason":
                reason,

            "temperature":
                float(
                    row["m2_temperature"]
                ),

            "health":
                float(
                    row["m2_health"]
                ),

            "status":
                row["m2_status"],

            "buffer_1":
                int(
                    row["buffer_1_level"]
                )
        })

    return results


# -------------------------------------------------
# SUMMARY
# -------------------------------------------------

def print_summary(results):
    """
    Print risk counts and important events.
    """

    counts = {
        "NORMAL": 0,
        "WARNING": 0,
        "CRITICAL": 0,
        "FAILURE": 0
    }

    for result in results:

        counts[
            result["risk"]
        ] += 1

    print("\n")
    print("=" * 75)
    print("DIGITAL TWIN RISK ASSESSMENT")
    print("=" * 75)

    print(
        f"NORMAL observations   : "
        f"{counts['NORMAL']}"
    )

    print(
        f"WARNING observations  : "
        f"{counts['WARNING']}"
    )

    print(
        f"CRITICAL observations : "
        f"{counts['CRITICAL']}"
    )

    print(
        f"FAILURE observations  : "
        f"{counts['FAILURE']}"
    )

    print("\n")
    print("IMPORTANT RISK EVENTS")
    print("-" * 75)

    previous_risk = None

    for result in results:

        # Only print when the risk level changes.
        # This avoids printing the same warning
        # every simulated second.

        if (
            result["risk"]
            != previous_risk
        ):

            print(
                f"{result['timestamp']:>7.2f} sec | "
                f"{result['risk']:<8} | "
                f"M2 Temp = "
                f"{result['temperature']:.2f} C | "
                f"Health = "
                f"{result['health']:.2f}% | "
                f"B1 = "
                f"{result['buffer_1']} | "
                f"{result['reason']}"
            )

            previous_risk = result[
                "risk"
            ]

    print("=" * 75)


# -------------------------------------------------
# MAIN
# -------------------------------------------------

if __name__ == "__main__":

    rows = load_data(
        CSV_FILE
    )

    results = analyse_risk(
        rows
    )

    print_summary(
        results
    )