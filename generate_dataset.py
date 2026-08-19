"""
Generate Multiple Factory Simulations
-------------------------------------

Runs the digital-twin manufacturing simulation many times
using different random seeds.

Each run creates a different operating trajectory.

The generated time-series files will later be combined
into a machine-learning dataset.
"""

import csv
import os

from twin import MachineTwin
from factory_sim import run_factory_simulation


NUMBER_OF_RUNS = 30

OUTPUT_DIR = "data/simulation_runs"

COMBINED_FILE = "data/combined_factory_timeseries.csv"


def create_twins():
    """
    Create fresh twins for every simulation run.
    """

    twin_1 = MachineTwin(
        machine_id="M1",
        name="Machine 1"
    )

    twin_2 = MachineTwin(
        machine_id="M2",
        name="Machine 2"
    )

    twin_3 = MachineTwin(
        machine_id="M3",
        name="Machine 3"
    )

    return twin_1, twin_2, twin_3


def run_simulations():
    """
    Run multiple factory simulations.
    """

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    for run_id in range(
        1,
        NUMBER_OF_RUNS + 1
    ):

        print(
            f"Running simulation "
            f"{run_id}/{NUMBER_OF_RUNS}"
        )

        twin_1, twin_2, twin_3 = (
            create_twins()
        )

        timeseries_file = (
            f"{OUTPUT_DIR}/"
            f"timeseries_run_{run_id}.csv"
        )

        events_file = (
            f"{OUTPUT_DIR}/"
            f"events_run_{run_id}.csv"
        )

        run_factory_simulation(
            twin_1,
            twin_2,
            twin_3,
            random_seed=run_id,
            timeseries_file=timeseries_file,
            events_file=events_file
        )


def combine_timeseries_files():
    """
    Combine all time-series runs into one CSV file.
    """

    first_file = True

    with open(
        COMBINED_FILE,
        "w",
        newline=""
    ) as output_file:

        writer = None

        for run_id in range(
            1,
            NUMBER_OF_RUNS + 1
        ):

            filename = (
                f"{OUTPUT_DIR}/"
                f"timeseries_run_{run_id}.csv"
            )

            with open(
                filename,
                "r",
                newline=""
            ) as input_file:

                reader = csv.DictReader(
                    input_file
                )

                if first_file:

                    fieldnames = [
                        "run_id"
                    ] + reader.fieldnames

                    writer = csv.DictWriter(
                        output_file,
                        fieldnames=fieldnames
                    )

                    writer.writeheader()

                    first_file = False

                for row in reader:

                    row_with_run = {
                        "run_id": run_id,
                        **row
                    }

                    writer.writerow(
                        row_with_run
                    )


if __name__ == "__main__":

    run_simulations()

    combine_timeseries_files()

    print("\nDataset generation complete.")

    print(
        f"Combined dataset: "
        f"{COMBINED_FILE}"
    )