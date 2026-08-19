"""
Baseline vs Agent-Controlled Factory Experiment
------------------------------------------------

Compares:

1. Baseline digital twin
   - no predictive-maintenance agent

2. Agent-controlled digital twin
   - predictive failure model
   - preventive maintenance

The same random seed is used for each paired experiment
to make the comparison fair.
"""

import os
import statistics

from twin import MachineTwin
from factory_sim import (
    run_factory_simulation,
    SIM_TIME
)


# -------------------------------------------------
# CONFIGURATION
# -------------------------------------------------

NUMBER_OF_RUNS = 30

OUTPUT_DIR = "data/comparison_runs"


# -------------------------------------------------
# CREATE FRESH DIGITAL TWINS
# -------------------------------------------------

def create_twins():

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

    return (
        twin_1,
        twin_2,
        twin_3
    )


# -------------------------------------------------
# RUN ONE EXPERIMENT
# -------------------------------------------------

def run_experiment(
    seed,
    enable_agent,
    mode
):

    twin_1, twin_2, twin_3 = (
        create_twins()
    )

    events_file = (
        f"{OUTPUT_DIR}/"
        f"{mode}_events_seed_{seed}.csv"
    )

    timeseries_file = (
        f"{OUTPUT_DIR}/"
        f"{mode}_timeseries_seed_{seed}.csv"
    )

    stats = run_factory_simulation(
        twin_1,
        twin_2,
        twin_3,
        random_seed=seed,
        events_file=events_file,
        timeseries_file=timeseries_file,
        enable_agent=enable_agent
    )

    if stats["completion_times"]:

        average_cycle_time = (
            sum(
                stats["completion_times"]
            )
            / len(
                stats["completion_times"]
            )
        )

    else:

        average_cycle_time = 0


    throughput = (
        stats["completed"]
        / SIM_TIME
    )


    total_downtime = (
        stats["downtime"]
        + stats["preventive_downtime"]
    )


    return {
        "seed":
            seed,

        "completed":
            stats["completed"],

        "throughput":
            throughput,

        "cycle_time":
            average_cycle_time,

        "reactive_downtime":
            stats["downtime"],

        "preventive_downtime":
            stats["preventive_downtime"],

        "total_downtime":
            total_downtime,

        "preventive_maintenance":
            stats["preventive_maintenance"],

        "m2_temperature":
            twin_2.temperature,

        "m2_health":
            twin_2.health
    }


# -------------------------------------------------
# MEAN
# -------------------------------------------------

def mean(
    results,
    key
):

    return statistics.mean(
        result[key]
        for result in results
    )


# -------------------------------------------------
# PRINT SUMMARY
# -------------------------------------------------

def print_summary(
    baseline,
    agent
):

    print("\n")
    print("=" * 85)
    print("BASELINE VS AGENT-CONTROLLED DIGITAL TWIN")
    print("=" * 85)

    print(
        f"Number of paired runs : "
        f"{NUMBER_OF_RUNS}"
    )

    print(
        f"Simulation time/run   : "
        f"{SIM_TIME} sec"
    )

    print("\n")
    print(
        f"{'Metric':<30}"
        f"{'Baseline':>15}"
        f"{'Agent':>15}"
        f"{'Difference':>15}"
    )

    print("-" * 75)


    metrics = [
        (
            "Products completed",
            "completed"
        ),
        (
            "Throughput",
            "throughput"
        ),
        (
            "Average cycle time",
            "cycle_time"
        ),
        (
            "Reactive downtime",
            "reactive_downtime"
        ),
        (
            "Preventive downtime",
            "preventive_downtime"
        ),
        (
            "Total downtime",
            "total_downtime"
        ),
        (
            "M2 final temperature",
            "m2_temperature"
        )
    ]


    for label, key in metrics:

        baseline_value = mean(
            baseline,
            key
        )

        agent_value = mean(
            agent,
            key
        )

        difference = (
            agent_value
            - baseline_value
        )

        print(
            f"{label:<30}"
            f"{baseline_value:>15.3f}"
            f"{agent_value:>15.3f}"
            f"{difference:>15.3f}"
        )


    baseline_failures = sum(
        1
        for result in baseline
        if result[
            "reactive_downtime"
        ] > 0
    )

    agent_failures = sum(
        1
        for result in agent
        if result[
            "reactive_downtime"
        ] > 0
    )


    preventive_actions = sum(
        result[
            "preventive_maintenance"
        ]
        for result in agent
    )


    print("\n")
    print("Failure / Maintenance Summary")
    print("-" * 75)

    print(
        f"Baseline runs with reactive failure : "
        f"{baseline_failures}/{NUMBER_OF_RUNS}"
    )

    print(
        f"Agent runs with reactive failure    : "
        f"{agent_failures}/{NUMBER_OF_RUNS}"
    )

    print(
        f"Total preventive interventions      : "
        f"{preventive_actions}"
    )


    # -----------------------------------------
    # PERCENT IMPROVEMENTS
    # -----------------------------------------

    baseline_downtime = mean(
        baseline,
        "reactive_downtime"
    )

    agent_reactive = mean(
        agent,
        "reactive_downtime"
    )


    if baseline_downtime > 0:

        failure_downtime_reduction = (
            (
                baseline_downtime
                - agent_reactive
            )
            / baseline_downtime
            * 100
        )

        print(
            f"Reactive downtime reduction         : "
            f"{failure_downtime_reduction:.2f}%"
        )


    baseline_cycle = mean(
        baseline,
        "cycle_time"
    )

    agent_cycle = mean(
        agent,
        "cycle_time"
    )


    if baseline_cycle > 0:

        cycle_change = (
            (
                agent_cycle
                - baseline_cycle
            )
            / baseline_cycle
            * 100
        )

        print(
            f"Cycle-time change                   : "
            f"{cycle_change:+.2f}%"
        )


    baseline_throughput = mean(
        baseline,
        "throughput"
    )

    agent_throughput = mean(
        agent,
        "throughput"
    )


    if baseline_throughput > 0:

        throughput_change = (
            (
                agent_throughput
                - baseline_throughput
            )
            / baseline_throughput
            * 100
        )

        print(
            f"Throughput change                   : "
            f"{throughput_change:+.2f}%"
        )

    print("=" * 85)


# -------------------------------------------------
# MAIN
# -------------------------------------------------

if __name__ == "__main__":

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    baseline_results = []
    agent_results = []


    for seed in range(
        1,
        NUMBER_OF_RUNS + 1
    ):

        print(
            f"\nRunning paired experiment "
            f"{seed}/{NUMBER_OF_RUNS}"
        )

        # -----------------------------------------
        # BASELINE
        # -----------------------------------------

        print(
            "  Baseline..."
        )

        baseline_result = (
            run_experiment(
                seed=seed,
                enable_agent=False,
                mode="baseline"
            )
        )

        baseline_results.append(
            baseline_result
        )

        # -----------------------------------------
        # AGENT
        # -----------------------------------------

        print(
            "  Agent controlled..."
        )

        agent_result = (
            run_experiment(
                seed=seed,
                enable_agent=True,
                mode="agent"
            )
        )

        agent_results.append(
            agent_result
        )


    print_summary(
        baseline_results,
        agent_results
    )