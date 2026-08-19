"""
Digital Twin Model
------------------

Represents the live digital state of a manufacturing machine.

Each MachineTwin tracks:
- machine status
- current product
- products processed
- busy time
- utilisation
- temperature
- health
- failure state
- maintenance state
"""


class MachineTwin:
    """
    Digital representation of one manufacturing machine.
    """

    def __init__(
        self,
        machine_id,
        name
    ):
        self.machine_id = machine_id
        self.name = name

        # Operational state
        self.status = "IDLE"
        self.current_product = None

        # Production information
        self.products_processed = 0
        self.busy_time = 0.0

        # Machine condition
        self.temperature = 25.0
        self.health = 100.0

        # Last digital-twin update time
        self.last_update = 0.0


    # -------------------------------------------------
    # PROCESSING
    # -------------------------------------------------

    def start_processing(
        self,
        product_id,
        current_time
    ):
        """
        Machine begins processing a product.
        """

        self.status = "RUNNING"
        self.current_product = product_id
        self.last_update = current_time


    def finish_processing(
        self,
        product_id,
        processing_time,
        current_time
    ):
        """
        Machine completes processing.
        """

        self.status = "IDLE"
        self.current_product = None

        self.products_processed += 1
        self.busy_time += processing_time

        self.last_update = current_time


    # -------------------------------------------------
    # TEMPERATURE
    # -------------------------------------------------

    def increase_temperature(
        self,
        amount
    ):
        """
        Increase machine temperature.
        """

        self.temperature += amount


    def cool_down(
        self,
        amount
    ):
        """
        Cool machine while idle.

        Temperature cannot drop below
        ambient temperature of 25 C.
        """

        self.temperature -= amount

        if self.temperature < 25.0:
            self.temperature = 25.0


    # -------------------------------------------------
    # HEALTH
    # -------------------------------------------------

    def degrade_health(
        self,
        amount
    ):
        """
        Reduce machine health.
        """

        self.health -= amount

        if self.health < 0:
            self.health = 0.0


    # -------------------------------------------------
    # FAILURE
    # -------------------------------------------------

    def fail(
        self,
        current_time
    ):
        """
        Mark machine as failed.
        """

        self.status = "FAILED"
        self.current_product = None
        self.last_update = current_time


    # -------------------------------------------------
    # MAINTENANCE
    # -------------------------------------------------

    def start_maintenance(
        self,
        current_time
    ):
        """
        Put machine into maintenance state.
        """

        self.status = "MAINTENANCE"
        self.current_product = None
        self.last_update = current_time


    def complete_maintenance(
        self,
        current_time
    ):
        """
        Complete maintenance and partially
        restore machine condition.
        """

        self.status = "IDLE"
        self.current_product = None

        # Restore machine temperature
        self.temperature = 30.0

        # Recover machine health
        self.health = min(
            100.0,
            self.health + 20.0
        )

        self.last_update = current_time


    # -------------------------------------------------
    # UTILISATION
    # -------------------------------------------------

    def utilisation(
        self,
        simulation_time
    ):
        """
        Calculate utilisation percentage.
        """

        if simulation_time <= 0:
            return 0.0

        return (
            self.busy_time
            / simulation_time
            * 100
        )


    # -------------------------------------------------
    # TEMPERATURE CONDITION
    # -------------------------------------------------

    def get_temperature_status(self):
        """
        Convert temperature into an
        operational condition.
        """

        if self.temperature >= 50:
            return "CRITICAL"

        if self.temperature >= 40:
            return "WARNING"

        return "NORMAL"


    # -------------------------------------------------
    # HEALTH CONDITION
    # -------------------------------------------------

    def get_health_status(self):
        """
        Convert health percentage into
        an operational condition.
        """

        if self.health <= 70:
            return "CRITICAL"

        if self.health <= 85:
            return "WARNING"

        return "HEALTHY"


    # -------------------------------------------------
    # DIGITAL TWIN STATE
    # -------------------------------------------------

    def get_state(
        self,
        simulation_time
    ):
        """
        Return complete current twin state.
        """

        return {
            "machine_id":
                self.machine_id,

            "name":
                self.name,

            "status":
                self.status,

            "current_product":
                self.current_product,

            "products_processed":
                self.products_processed,

            "temperature":
                round(
                    self.temperature,
                    2
                ),

            "temperature_status":
                self.get_temperature_status(),

            "health":
                round(
                    self.health,
                    2
                ),

            "health_status":
                self.get_health_status(),

            "utilisation":
                round(
                    self.utilisation(
                        simulation_time
                    ),
                    2
                ),

            "last_update":
                round(
                    self.last_update,
                    2
                )
        }


    # -------------------------------------------------
    # DISPLAY
    # -------------------------------------------------

    def __str__(self):
        return (
            f"{self.name} "
            f"[status={self.status}, "
            f"temperature={self.temperature:.2f} C, "
            f"health={self.health:.2f}%, "
            f"processed={self.products_processed}]"
        )