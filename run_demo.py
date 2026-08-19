"""
Main demo for the Agentic AI-Powered Digital Twin project.

This file connects:

1. Factory simulation
2. Machine digital twins
3. Predictive-maintenance-driven agent actions
"""

from twin import MachineTwin
from factory_sim import (
    run_factory_simulation,
    SIM_TIME
)


# -------------------------------------------------
# CREATE DIGITAL TWINS
# -------------------------------------------------

machine_1_twin = MachineTwin(
    machine_id="M1",
    name="Machine 1"
)

machine_2_twin = MachineTwin(
    machine_id="M2",
    name="Machine 2"
)

machine_3_twin = MachineTwin(
    machine_id="M3",
    name="Machine 3"
)


# -------------------------------------------------
# RUN FACTORY SIMULATION
# -------------------------------------------------

stats = run_factory_simulation(
    machine_1_twin,
    machine_2_twin,
    machine_3_twin
)


# -------------------------------------------------
# CALCULATE FACTORY METRICS
# -------------------------------------------------

if stats["completion_times"]:

    average_cycle_time = (
        sum(stats["completion_times"])
        / len(stats["completion_times"])
    )

else:

    average_cycle_time = 0


throughput = (
    stats["completed"]
    / SIM_TIME
)


# -------------------------------------------------
# PRINT FACTORY RESULTS
# -------------------------------------------------

print("\n")
print("=" * 55)
print("FACTORY RESULTS")
print("=" * 55)

print(
    f"Products completed      : "
    f"{stats['completed']}"
)

print(
    f"Throughput              : "
    f"{throughput:.3f} products/sec"
)

print(
    f"Average cycle time      : "
    f"{average_cycle_time:.2f} sec"
)

print(
    f"Reactive downtime       : "
    f"{stats['downtime']} sec"
)

print(
    f"Preventive maintenance  : "
    f"{stats['preventive_maintenance']}"
)

print(
    f"Preventive downtime     : "
    f"{stats['preventive_downtime']} sec"
)

total_downtime = (
    stats["downtime"]
    + stats["preventive_downtime"]
)

print(
    f"Total downtime          : "
    f"{total_downtime} sec"
)


# -------------------------------------------------
# PRINT DIGITAL TWIN STATES
# -------------------------------------------------

print("\n")
print("=" * 55)
print("DIGITAL TWIN STATES")
print("=" * 55)


for twin in [
    machine_1_twin,
    machine_2_twin,
    machine_3_twin
]:

    state = twin.get_state(
        simulation_time=SIM_TIME
    )

    print("\n")

    for key, value in state.items():

        print(
            f"{key:<20}: {value}"
        )


# -------------------------------------------------
# DIGITAL TWIN ALERTS
# -------------------------------------------------

print("\n")
print("=" * 55)
print("DIGITAL TWIN ALERTS")
print("=" * 55)


twins = [
    machine_1_twin,
    machine_2_twin,
    machine_3_twin
]


alerts_found = False


for twin in twins:

    temperature_status = (
        twin.get_temperature_status()
    )

    health_status = (
        twin.get_health_status()
    )

    # -----------------------------------------
    # TEMPERATURE ALERTS
    # -----------------------------------------

    if temperature_status == "WARNING":

        print(
            f"WARNING: {twin.name} temperature is high "
            f"({twin.temperature:.2f} C)"
        )

        alerts_found = True


    elif temperature_status == "CRITICAL":

        print(
            f"CRITICAL: {twin.name} temperature is "
            f"{twin.temperature:.2f} C"
        )

        alerts_found = True


    # -----------------------------------------
    # HEALTH ALERTS
    # -----------------------------------------

    if health_status == "WARNING":

        print(
            f"WARNING: {twin.name} health has dropped to "
            f"{twin.health:.2f}%"
        )

        alerts_found = True


    elif health_status == "CRITICAL":

        print(
            f"CRITICAL: {twin.name} health has dropped to "
            f"{twin.health:.2f}%"
        )

        alerts_found = True


if not alerts_found:

    print(
        "No machine alerts detected."
    )


# -------------------------------------------------
# AGENT SUMMARY
# -------------------------------------------------

print("\n")
print("=" * 55)
print("AGENTIC MAINTENANCE SUMMARY")
print("=" * 55)

if stats["preventive_maintenance"] > 0:

    print(
        f"The agent triggered "
        f"{stats['preventive_maintenance']} "
        f"preventive maintenance intervention(s)."
    )

    print(
        f"Planned preventive downtime : "
        f"{stats['preventive_downtime']} sec"
    )

else:

    print(
        "The agent did not trigger preventive maintenance."
    )


if stats["downtime"] > 0:

    print(
        f"Reactive failure downtime    : "
        f"{stats['downtime']} sec"
    )

else:

    print(
        "No reactive Machine 2 failure downtime occurred."
    )


print(
    f"Total Machine 2 downtime     : "
    f"{total_downtime} sec"
)

print("=" * 55)