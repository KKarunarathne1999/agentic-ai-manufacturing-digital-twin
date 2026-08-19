"""
Factory Event Analysis
----------------------

Basic validation and summary of the structured
event log created by the digital twin simulation.
"""

import csv
from collections import Counter, defaultdict


CSV_FILE = "data/factory_events.csv"


def load_events(filename):
    """
    Load the CSV file into memory.
    """

    events = []

    with open(
        filename,
        mode="r",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            events.append(row)

    return events


def analyse_events(events):
    """
    Produce basic statistics from the factory event log.
    """

    print("\n" + "=" * 55)
    print("FACTORY EVENT DATA ANALYSIS")
    print("=" * 55)

    print(
        f"Total logged events : {len(events)}"
    )

    # -------------------------------------------------
    # EVENT COUNTS
    # -------------------------------------------------

    event_counts = Counter(
        event["event"]
        for event in events
    )

    print("\nEvent Counts")
    print("-" * 55)

    for event_name, count in event_counts.items():

        print(
            f"{event_name:<25}: {count}"
        )

    # -------------------------------------------------
    # MACHINE EVENT COUNTS
    # -------------------------------------------------

    machine_counts = Counter(
        event["machine_id"]
        for event in events
    )

    print("\nEvents by Machine")
    print("-" * 55)

    for machine, count in machine_counts.items():

        print(
            f"{machine:<25}: {count}"
        )

    # -------------------------------------------------
    # TEMPERATURE ANALYSIS
    # -------------------------------------------------

    temperatures = defaultdict(list)

    for event in events:

        machine_id = event["machine_id"]

        temperature = float(
            event["temperature"]
        )

        temperatures[
            machine_id
        ].append(
            temperature
        )

    print("\nTemperature Summary")
    print("-" * 55)

    for machine, values in temperatures.items():

        average_temp = (
            sum(values)
            / len(values)
        )

        maximum_temp = max(
            values
        )

        minimum_temp = min(
            values
        )

        print(
            f"{machine} | "
            f"Min = {minimum_temp:.2f} C | "
            f"Avg = {average_temp:.2f} C | "
            f"Max = {maximum_temp:.2f} C"
        )

    # -------------------------------------------------
    # HEALTH ANALYSIS
    # -------------------------------------------------

    health_values = defaultdict(list)

    for event in events:

        machine_id = event[
            "machine_id"
        ]

        health = float(
            event["health"]
        )

        health_values[
            machine_id
        ].append(
            health
        )

    print("\nMachine Health Summary")
    print("-" * 55)

    for machine, values in health_values.items():

        print(
            f"{machine} | "
            f"Final/Minimum health = "
            f"{min(values):.2f}%"
        )

    # -------------------------------------------------
    # BUFFER ANALYSIS
    # -------------------------------------------------

    buffer_1_values = []
    buffer_2_values = []

    for event in events:

        if event["buffer_1_level"]:

            buffer_1_values.append(
                int(
                    event["buffer_1_level"]
                )
            )

        if event["buffer_2_level"]:

            buffer_2_values.append(
                int(
                    event["buffer_2_level"]
                )
            )

    print("\nBuffer Summary")
    print("-" * 55)

    if buffer_1_values:

        print(
            f"Buffer 1 maximum level : "
            f"{max(buffer_1_values)}"
        )

    if buffer_2_values:

        print(
            f"Buffer 2 maximum level : "
            f"{max(buffer_2_values)}"
        )

    # -------------------------------------------------
    # FAILURE EVENTS
    # -------------------------------------------------

    failures = [
        event
        for event in events
        if event["event"] == "FAILURE"
    ]

    print("\nFailure Summary")
    print("-" * 55)

    print(
        f"Total failures : {len(failures)}"
    )

    for failure in failures:

        print(
            f"Time = {failure['timestamp']} sec | "
            f"Machine = {failure['machine_id']} | "
            f"Temperature = "
            f"{failure['temperature']} C"
        )

    print("\n" + "=" * 55)


if __name__ == "__main__":

    events = load_events(
        CSV_FILE
    )

    analyse_events(
        events
    )