"""
Factory Event Logger
--------------------

Stores structured manufacturing events in CSV format.

The logged data will later support:
- anomaly detection
- predictive maintenance
- dashboards
- machine learning
- Agentic AI
"""

import csv
import os


class FactoryLogger:

    def __init__(
        self,
        filename="data/factory_events.csv"
    ):
        self.filename = filename

        directory = os.path.dirname(filename)

        if directory:
            os.makedirs(
                directory,
                exist_ok=True
            )

        self.fieldnames = [
            "timestamp",
            "machine_id",
            "machine_name",
            "event",
            "status",
            "temperature",
            "health",
            "product_id",
            "buffer_1_level",
            "buffer_2_level"
        ]

        with open(
            self.filename,
            mode="w",
            newline=""
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=self.fieldnames
            )

            writer.writeheader()


    def log_event(
        self,
        timestamp,
        twin,
        event,
        product_id=None,
        buffer_1_level=None,
        buffer_2_level=None
    ):
        """
        Write one digital-twin event to the CSV file.
        """

        row = {
            "timestamp": round(timestamp, 2),

            "machine_id":
                twin.machine_id,

            "machine_name":
                twin.name,

            "event":
                event,

            "status":
                twin.status,

            "temperature":
                round(
                    twin.temperature,
                    2
                ),

            "health":
                round(
                    twin.health,
                    2
                ),

            "product_id":
                product_id,

            "buffer_1_level":
                buffer_1_level,

            "buffer_2_level":
                buffer_2_level
        }

        with open(
            self.filename,
            mode="a",
            newline=""
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=self.fieldnames
            )

            writer.writerow(row)