"""
Agentic Decision Engine
-----------------------

Converts digital-twin state, risk level, and predictive
maintenance probability into recommended factory actions.

Actions:
    CONTINUE
    MONITOR
    REDUCE_LOAD
    SCHEDULE_MAINTENANCE
    EMERGENCY_MAINTENANCE
"""


class ManufacturingAgent:
    """
    Simple rule-based manufacturing decision agent.
    """

    def __init__(
        self,
        maintenance_probability=0.80,
        warning_probability=0.50
    ):
        self.maintenance_probability = (
            maintenance_probability
        )

        self.warning_probability = (
            warning_probability
        )


    def decide(
        self,
        risk_level,
        failure_probability,
        machine_status
    ):
        """
        Select an operational action.

        Parameters
        ----------
        risk_level : str
            NORMAL, WARNING, CRITICAL or FAILURE

        failure_probability : float
            Probability that the machine will fail soon.

        machine_status : str
            Current digital-twin machine status.

        Returns
        -------
        dict
            Action, priority and explanation.
        """

        # -------------------------------------------------
        # MACHINE ALREADY FAILED / UNDER MAINTENANCE
        # -------------------------------------------------

        if machine_status in [
            "FAILED",
            "MAINTENANCE"
        ]:
            return {
                "action": "EMERGENCY_MAINTENANCE",
                "priority": "CRITICAL",
                "reason": (
                    f"Machine status is {machine_status}."
                )
            }

        # -------------------------------------------------
        # HIGH PREDICTED FAILURE PROBABILITY
        # -------------------------------------------------

        if (
            failure_probability
            >= self.maintenance_probability
        ):
            return {
                "action": "SCHEDULE_MAINTENANCE",
                "priority": "HIGH",
                "reason": (
                    "Predictive-maintenance model estimates "
                    f"{failure_probability:.1%} probability "
                    "of failure soon."
                )
            }

        # -------------------------------------------------
        # CRITICAL OPERATING CONDITION
        # -------------------------------------------------

        if risk_level == "CRITICAL":
            return {
                "action": "REDUCE_LOAD",
                "priority": "HIGH",
                "reason": (
                    "Machine is operating in a critical condition."
                )
            }

        # -------------------------------------------------
        # WARNING CONDITION
        # -------------------------------------------------

        if (
            risk_level == "WARNING"
            or failure_probability
            >= self.warning_probability
        ):
            return {
                "action": "MONITOR",
                "priority": "MEDIUM",
                "reason": (
                    "Machine condition requires increased monitoring."
                )
            }

        # -------------------------------------------------
        # NORMAL OPERATION
        # -------------------------------------------------

        return {
            "action": "CONTINUE",
            "priority": "LOW",
            "reason": (
                "Machine operating normally."
            )
        }


    def should_trigger_preventive_maintenance(
        self,
        failure_probability,
        machine_status
    ):
        """
        Return True when preventive maintenance should
        be triggered automatically.
        """

        if machine_status != "RUNNING":
            return False

        return (
            failure_probability
            >= self.maintenance_probability
        )


# -------------------------------------------------
# SIMPLE TEST
# -------------------------------------------------

if __name__ == "__main__":

    agent = ManufacturingAgent()

    tests = [
        ("NORMAL", 0.10, "RUNNING"),
        ("WARNING", 0.55, "RUNNING"),
        ("CRITICAL", 0.70, "RUNNING"),
        ("CRITICAL", 0.91, "RUNNING"),
        ("FAILURE", 1.00, "FAILED"),
    ]

    print("\n" + "=" * 70)
    print("AGENT DECISION TEST")
    print("=" * 70)

    for (
        risk,
        probability,
        status
    ) in tests:

        decision = agent.decide(
            risk_level=risk,
            failure_probability=probability,
            machine_status=status
        )

        print(
            f"\nRisk        : {risk}"
        )

        print(
            f"Failure Prob: {probability:.1%}"
        )

        print(
            f"Status      : {status}"
        )

        print(
            f"Action      : {decision['action']}"
        )

        print(
            f"Priority    : {decision['priority']}"
        )

        print(
            f"Reason      : {decision['reason']}"
        )