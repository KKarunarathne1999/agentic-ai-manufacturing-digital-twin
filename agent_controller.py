"""
Agentic Factory Controller
--------------------------

Connects:

Digital Twin
    +
Predictive Maintenance Model
    +
Decision Agent

The controller monitors Machine 2 and can trigger
preventive maintenance before a predicted failure.
"""

import pickle

from decision_agent import ManufacturingAgent


MODEL_FILE = "models/predictive_maintenance.pkl"


class AgentController:

    def __init__(self):

        with open(
            MODEL_FILE,
            "rb"
        ) as file:

            self.model = pickle.load(
                file
            )

        self.agent = ManufacturingAgent(
            maintenance_probability=0.80,
            warning_probability=0.50
        )

        self.preventive_maintenance_count = 0


    def build_features(
        self,
        twin_1,
        twin_2,
        twin_3,
        buffer_1,
        buffer_2
    ):
        """
        Build features in exactly the same order
        used during predictive-maintenance training.
        """

        return [[
            twin_1.temperature,
            twin_1.health,

            twin_2.temperature,
            twin_2.health,

            twin_3.temperature,
            twin_3.health,

            len(buffer_1.items),
            len(buffer_2.items),

            1 if twin_2.status == "RUNNING" else 0,
            1 if twin_2.status == "IDLE" else 0,
        ]]


    def get_failure_probability(
        self,
        twin_1,
        twin_2,
        twin_3,
        buffer_1,
        buffer_2
    ):
        """
        Predict probability of Machine 2 failing soon.
        """

        features = self.build_features(
            twin_1,
            twin_2,
            twin_3,
            buffer_1,
            buffer_2
        )

        probability = (
            self.model.predict_proba(
                features
            )[0][1]
        )

        return float(
            probability
        )


    def decide(
        self,
        twin_1,
        twin_2,
        twin_3,
        buffer_1,
        buffer_2
    ):
        """
        Generate agent decision.
        """

        failure_probability = (
            self.get_failure_probability(
                twin_1,
                twin_2,
                twin_3,
                buffer_1,
                buffer_2
            )
        )

        if twin_2.temperature >= 47:

            risk_level = "CRITICAL"

        elif twin_2.temperature >= 40:

            risk_level = "WARNING"

        else:

            risk_level = "NORMAL"

        decision = self.agent.decide(
            risk_level=risk_level,
            failure_probability=failure_probability,
            machine_status=twin_2.status
        )

        return (
            failure_probability,
            decision
        )