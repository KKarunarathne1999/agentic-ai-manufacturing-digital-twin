"""
Digital Twin Time-Series Logger
-------------------------------

Records the state of the complete factory at
regular simulated time intervals.
"""

import csv
import os


class TimeSeriesLogger:

    def __init__(
        self,
        filename="data/factory_timeseries.csv"
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

            "m1_status",
            "m1_temperature",
            "m1_health",

            "m2_status",
            "m2_temperature",
            "m2_health",

            "m3_status",
            "m3_temperature",
            "m3_health",

            "buffer_1_level",
            "buffer_2_level",

            "completed_products"
        ]

        with open(
            self.filename,
            "w",
            newline=""
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=self.fieldnames
            )

            writer.writeheader()


    def log_state(
        self,
        timestamp,
        twin_1,
        twin_2,
        twin_3,
        buffer_1,
        buffer_2,
        completed_products
    ):

        row = {
            "timestamp": round(timestamp, 2),

            "m1_status": twin_1.status,
            "m1_temperature": round(
                twin_1.temperature, 2
            ),
            "m1_health": round(
                twin_1.health, 2
            ),

            "m2_status": twin_2.status,
            "m2_temperature": round(
                twin_2.temperature, 2
            ),
            "m2_health": round(
                twin_2.health, 2
            ),

            "m3_status": twin_3.status,
            "m3_temperature": round(
                twin_3.temperature, 2
            ),
            "m3_health": round(
                twin_3.health, 2
            ),

            "buffer_1_level": len(
                buffer_1.items
            ),

            "buffer_2_level": len(
                buffer_2.items
            ),

            "completed_products":
                completed_products
        }

        with open(
            self.filename,
            "a",
            newline=""
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=self.fieldnames
            )

            writer.writerow(row)