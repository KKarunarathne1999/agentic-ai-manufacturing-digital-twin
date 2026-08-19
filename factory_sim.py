"""
Manufacturing Factory Simulation
--------------------------------

Three-machine production line:

    Machine 1 -> Buffer 1 -> Machine 2 -> Buffer 2 -> Machine 3

Includes:
- finite buffers
- variable processing times
- temperature and health degradation
- cooling
- reactive failure maintenance
- preventive agent maintenance
- event logging
- time-series logging
- predictive-maintenance-driven control
"""

import random

import simpy

from logger import FactoryLogger
from timeseries_logger import TimeSeriesLogger
from agent_controller import AgentController


# -------------------------------------------------
# CONFIGURATION
# -------------------------------------------------

M1_TIME = 5
M2_TIME = 7
M3_TIME = 4

PROCESSING_VARIATION = 0.15

ARRIVAL_INTERVAL = 6
BUFFER_CAPACITY = 5

SIM_TIME = 180

FAILURE_TEMPERATURE = 50.0
REPAIR_TIME = 15

PREVENTIVE_MAINTENANCE_TIME = 10


# -------------------------------------------------
# PROCESSING-TIME VARIABILITY
# -------------------------------------------------

def get_processing_time(base_time):

    minimum = base_time * (
        1 - PROCESSING_VARIATION
    )

    maximum = base_time * (
        1 + PROCESSING_VARIATION
    )

    return random.uniform(
        minimum,
        maximum
    )


# -------------------------------------------------
# MACHINE 1
# -------------------------------------------------

def machine_1_process(
    env,
    machine_1,
    buffer_1,
    buffer_2,
    product_id,
    stats,
    twin_1,
    logger
):

    with machine_1.request() as request:

        yield request

        twin_1.start_processing(
            product_id=product_id,
            current_time=env.now
        )

        logger.log_event(
            timestamp=env.now,
            twin=twin_1,
            event="PROCESS_START",
            product_id=product_id,
            buffer_1_level=len(buffer_1.items),
            buffer_2_level=len(buffer_2.items)
        )

        print(
            f"{env.now:>7.2f} sec | "
            f"Machine 1 starts Product {product_id}"
        )

        processing_time = (
            get_processing_time(M1_TIME)
        )

        yield env.timeout(
            processing_time
        )

        twin_1.finish_processing(
            product_id=product_id,
            processing_time=processing_time,
            current_time=env.now
        )

        twin_1.increase_temperature(
            1.2
        )

        twin_1.degrade_health(
            0.15
        )

        logger.log_event(
            timestamp=env.now,
            twin=twin_1,
            event="PROCESS_FINISH",
            product_id=product_id,
            buffer_1_level=len(buffer_1.items),
            buffer_2_level=len(buffer_2.items)
        )

        print(
            f"{env.now:>7.2f} sec | "
            f"Machine 1 finishes Product {product_id} "
            f"| Processing = {processing_time:.2f} sec "
            f"| Temp = {twin_1.temperature:.2f} C"
        )

    yield buffer_1.put(
        product_id
    )

    logger.log_event(
        timestamp=env.now,
        twin=twin_1,
        event="BUFFER_1_PUT",
        product_id=product_id,
        buffer_1_level=len(buffer_1.items),
        buffer_2_level=len(buffer_2.items)
    )


# -------------------------------------------------
# MACHINE 2
# -------------------------------------------------

def machine_2_worker(
    env,
    machine_2,
    buffer_1,
    buffer_2,
    stats,
    twin_2,
    logger
):

    while True:

        product_id = yield buffer_1.get()

        logger.log_event(
            timestamp=env.now,
            twin=twin_2,
            event="BUFFER_1_GET",
            product_id=product_id,
            buffer_1_level=len(buffer_1.items),
            buffer_2_level=len(buffer_2.items)
        )

        # -----------------------------------------
        # REACTIVE FAILURE
        # -----------------------------------------

        if (
            twin_2.temperature
            >= FAILURE_TEMPERATURE
        ):

            twin_2.fail(
                env.now
            )

            logger.log_event(
                timestamp=env.now,
                twin=twin_2,
                event="FAILURE",
                product_id=product_id,
                buffer_1_level=len(buffer_1.items),
                buffer_2_level=len(buffer_2.items)
            )

            print(
                f"{env.now:>7.2f} sec | "
                f"Machine 2 FAILED "
                f"| Temp = {twin_2.temperature:.2f} C"
            )

            # Maintenance physically occupies M2
            with machine_2.request() as maintenance_request:

                yield maintenance_request

                twin_2.start_maintenance(
                    env.now
                )

                logger.log_event(
                    timestamp=env.now,
                    twin=twin_2,
                    event="MAINTENANCE_START",
                    product_id=product_id,
                    buffer_1_level=len(buffer_1.items),
                    buffer_2_level=len(buffer_2.items)
                )

                stats["downtime"] += (
                    REPAIR_TIME
                )

                print(
                    f"{env.now:>7.2f} sec | "
                    f"Machine 2 reactive maintenance started"
                )

                yield env.timeout(
                    REPAIR_TIME
                )

                twin_2.complete_maintenance(
                    env.now
                )

                logger.log_event(
                    timestamp=env.now,
                    twin=twin_2,
                    event="MAINTENANCE_COMPLETE",
                    product_id=product_id,
                    buffer_1_level=len(buffer_1.items),
                    buffer_2_level=len(buffer_2.items)
                )

                print(
                    f"{env.now:>7.2f} sec | "
                    f"Machine 2 reactive maintenance completed"
                )

        # -----------------------------------------
        # NORMAL PROCESSING
        # -----------------------------------------

        with machine_2.request() as request:

            yield request

            twin_2.start_processing(
                product_id=product_id,
                current_time=env.now
            )

            logger.log_event(
                timestamp=env.now,
                twin=twin_2,
                event="PROCESS_START",
                product_id=product_id,
                buffer_1_level=len(buffer_1.items),
                buffer_2_level=len(buffer_2.items)
            )

            print(
                f"{env.now:>7.2f} sec | "
                f"Machine 2 starts Product {product_id}"
            )

            processing_time = (
                get_processing_time(M2_TIME)
            )

            yield env.timeout(
                processing_time
            )

            twin_2.finish_processing(
                product_id=product_id,
                processing_time=processing_time,
                current_time=env.now
            )

            twin_2.increase_temperature(
                1.8
            )

            twin_2.degrade_health(
                0.25
            )

            logger.log_event(
                timestamp=env.now,
                twin=twin_2,
                event="PROCESS_FINISH",
                product_id=product_id,
                buffer_1_level=len(buffer_1.items),
                buffer_2_level=len(buffer_2.items)
            )

            print(
                f"{env.now:>7.2f} sec | "
                f"Machine 2 finishes Product {product_id} "
                f"| Processing = {processing_time:.2f} sec "
                f"| Temp = {twin_2.temperature:.2f} C"
            )

        yield buffer_2.put(
            product_id
        )

        logger.log_event(
            timestamp=env.now,
            twin=twin_2,
            event="BUFFER_2_PUT",
            product_id=product_id,
            buffer_1_level=len(buffer_1.items),
            buffer_2_level=len(buffer_2.items)
        )


# -------------------------------------------------
# MACHINE 3
# -------------------------------------------------

def machine_3_worker(
    env,
    machine_3,
    buffer_1,
    buffer_2,
    stats,
    twin_3,
    logger
):

    while True:

        product_id = yield buffer_2.get()

        logger.log_event(
            timestamp=env.now,
            twin=twin_3,
            event="BUFFER_2_GET",
            product_id=product_id,
            buffer_1_level=len(buffer_1.items),
            buffer_2_level=len(buffer_2.items)
        )

        with machine_3.request() as request:

            yield request

            twin_3.start_processing(
                product_id=product_id,
                current_time=env.now
            )

            logger.log_event(
                timestamp=env.now,
                twin=twin_3,
                event="PROCESS_START",
                product_id=product_id,
                buffer_1_level=len(buffer_1.items),
                buffer_2_level=len(buffer_2.items)
            )

            print(
                f"{env.now:>7.2f} sec | "
                f"Machine 3 starts Product {product_id}"
            )

            processing_time = (
                get_processing_time(M3_TIME)
            )

            yield env.timeout(
                processing_time
            )

            twin_3.finish_processing(
                product_id=product_id,
                processing_time=processing_time,
                current_time=env.now
            )

            twin_3.increase_temperature(
                1.0
            )

            twin_3.degrade_health(
                0.10
            )

            logger.log_event(
                timestamp=env.now,
                twin=twin_3,
                event="PROCESS_FINISH",
                product_id=product_id,
                buffer_1_level=len(buffer_1.items),
                buffer_2_level=len(buffer_2.items)
            )

            print(
                f"{env.now:>7.2f} sec | "
                f"Machine 3 finishes Product {product_id}"
            )

        stats["completed"] += 1

        cycle_time = (
            env.now
            - stats["arrival_times"][product_id]
        )

        stats["completion_times"].append(
            cycle_time
        )

        logger.log_event(
            timestamp=env.now,
            twin=twin_3,
            event="PRODUCT_COMPLETED",
            product_id=product_id,
            buffer_1_level=len(buffer_1.items),
            buffer_2_level=len(buffer_2.items)
        )

        print(
            f"{env.now:>7.2f} sec | "
            f"Product {product_id} COMPLETED "
            f"| Cycle time = {cycle_time:.2f} sec"
        )


# -------------------------------------------------
# PRODUCT GENERATOR
# -------------------------------------------------

def product_generator(
    env,
    machine_1,
    buffer_1,
    buffer_2,
    stats,
    twin_1,
    logger
):

    product_id = 1

    while True:

        stats["arrival_times"][
            product_id
        ] = env.now

        print(
            f"{env.now:>7.2f} sec | "
            f"Product {product_id} enters factory"
        )

        logger.log_event(
            timestamp=env.now,
            twin=twin_1,
            event="PRODUCT_ARRIVAL",
            product_id=product_id,
            buffer_1_level=len(buffer_1.items),
            buffer_2_level=len(buffer_2.items)
        )

        env.process(
            machine_1_process(
                env,
                machine_1,
                buffer_1,
                buffer_2,
                product_id,
                stats,
                twin_1,
                logger
            )
        )

        product_id += 1

        yield env.timeout(
            ARRIVAL_INTERVAL
        )


# -------------------------------------------------
# COOLING
# -------------------------------------------------

def cooling_process(
    env,
    twin,
    cooling_rate=0.5
):

    while True:

        yield env.timeout(1)

        if twin.status == "IDLE":

            twin.cool_down(
                cooling_rate
            )


# -------------------------------------------------
# TIME-SERIES MONITOR
# -------------------------------------------------

def factory_monitor(
    env,
    twin_1,
    twin_2,
    twin_3,
    buffer_1,
    buffer_2,
    stats,
    timeseries_logger
):

    while True:

        timeseries_logger.log_state(
            timestamp=env.now,
            twin_1=twin_1,
            twin_2=twin_2,
            twin_3=twin_3,
            buffer_1=buffer_1,
            buffer_2=buffer_2,
            completed_products=stats["completed"]
        )

        yield env.timeout(1)


# -------------------------------------------------
# AGENT CONTROL
# -------------------------------------------------

def agent_monitor_process(
    env,
    controller,
    machine_2,
    twin_1,
    twin_2,
    twin_3,
    buffer_1,
    buffer_2,
    stats,
    logger
):

    while True:

        yield env.timeout(1)

        # Do not issue a new intervention
        # if maintenance/failure is already active.
        if twin_2.status in [
            "FAILED",
            "MAINTENANCE"
        ]:
            continue

        (
            failure_probability,
            decision
        ) = controller.decide(
            twin_1,
            twin_2,
            twin_3,
            buffer_1,
            buffer_2
        )

        if (
            decision["action"]
            != "SCHEDULE_MAINTENANCE"
        ):
            continue

        print(
            f"{env.now:>7.2f} sec | "
            f"AGENT ALERT | "
            f"Failure probability = "
            f"{failure_probability:.1%}"
        )

        # Request M2 itself.
        # If M2 is currently processing, this waits safely
        # until that product finishes.
        with machine_2.request() as maintenance_request:

            yield maintenance_request

            # Re-check after waiting for the machine.
            if twin_2.status in [
                "FAILED",
                "MAINTENANCE"
            ]:
                continue

            stats[
                "preventive_maintenance"
            ] += 1

            controller.preventive_maintenance_count += 1

            twin_2.start_maintenance(
                env.now
            )

            logger.log_event(
                timestamp=env.now,
                twin=twin_2,
                event="PREVENTIVE_MAINTENANCE_START",
                product_id=None,
                buffer_1_level=len(buffer_1.items),
                buffer_2_level=len(buffer_2.items)
            )

            print(
                f"{env.now:>7.2f} sec | "
                f"AGENT ACTION | "
                f"Preventive maintenance started"
            )

            stats[
                "preventive_downtime"
            ] += (
                PREVENTIVE_MAINTENANCE_TIME
            )

            yield env.timeout(
                PREVENTIVE_MAINTENANCE_TIME
            )

            twin_2.complete_maintenance(
                env.now
            )

            logger.log_event(
                timestamp=env.now,
                twin=twin_2,
                event="PREVENTIVE_MAINTENANCE_COMPLETE",
                product_id=None,
                buffer_1_level=len(buffer_1.items),
                buffer_2_level=len(buffer_2.items)
            )

            print(
                f"{env.now:>7.2f} sec | "
                f"AGENT ACTION | "
                f"Preventive maintenance completed"
            )


# -------------------------------------------------
# MAIN SIMULATION
# -------------------------------------------------

def run_factory_simulation(
    twin_1,
    twin_2,
    twin_3,
    random_seed=42,
    timeseries_file="data/factory_timeseries.csv",
    events_file="data/factory_events.csv",
    enable_agent=True

):

    random.seed(
        random_seed
    )

    env = simpy.Environment()

    controller = AgentController()

    logger = FactoryLogger(
        filename=events_file
    )

    timeseries_logger = TimeSeriesLogger(
        filename=timeseries_file
    )

    # Machines
    machine_1 = simpy.Resource(
        env,
        capacity=1
    )

    machine_2 = simpy.Resource(
        env,
        capacity=1
    )

    machine_3 = simpy.Resource(
        env,
        capacity=1
    )

    # Buffers
    buffer_1 = simpy.Store(
        env,
        capacity=BUFFER_CAPACITY
    )

    buffer_2 = simpy.Store(
        env,
        capacity=BUFFER_CAPACITY
    )

    stats = {
        "completed": 0,
        "arrival_times": {},
        "completion_times": [],
        "downtime": 0,
        "preventive_maintenance": 0,
        "preventive_downtime": 0
    }

    # Factory processes
    env.process(
        product_generator(
            env,
            machine_1,
            buffer_1,
            buffer_2,
            stats,
            twin_1,
            logger
        )
    )

    env.process(
        machine_2_worker(
            env,
            machine_2,
            buffer_1,
            buffer_2,
            stats,
            twin_2,
            logger
        )
    )

    env.process(
        machine_3_worker(
            env,
            machine_3,
            buffer_1,
            buffer_2,
            stats,
            twin_3,
            logger
        )
    )

    # Monitoring
    env.process(
        factory_monitor(
            env,
            twin_1,
            twin_2,
            twin_3,
            buffer_1,
            buffer_2,
            stats,
            timeseries_logger
        )
    )

    # Cooling
    env.process(
        cooling_process(
            env,
            twin_1
        )
    )

    env.process(
        cooling_process(
            env,
            twin_2
        )
    )

    env.process(
        cooling_process(
            env,
            twin_3
        )
    )

    # Agent
    if enable_agent:
        env.process(
            agent_monitor_process(
                env,
                controller,
                machine_2,
                twin_1,
                twin_2,
                twin_3,
                buffer_1,
                buffer_2,
                stats,
                logger
            )
        )

    env.run(
        until=SIM_TIME
    )

    stats["buffer_1_level"] = (
        len(buffer_1.items)
    )

    stats["buffer_2_level"] = (
        len(buffer_2.items)
    )

    return stats