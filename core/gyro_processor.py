import datetime
import logging
from typing import Dict

from config import config


class GyroProcessor:
    def __init__(self):
        self.lower_angle = 0.0
        self.upper_angle = 0.0
        self.last_timestamp = None

        self.angles = []

    def process_data(self, gyro_data: list[Dict]) -> None:
        for data in gyro_data:
            timestamp = datetime.fromisoformat(data["timestamp"])
            dt = self._get_delta_time(timestamp)

            if dt is not None:
                self.angle_upper += data["upper_gyro_z"] * dt * config.GYRO_SCALE
                self.angle_lower += data["lower_gyro_z"] * dt * config.GYRO_SCALE

                logging.debug(
                    f"Upper angle: {self.angle_upper}, Lower angle: {self.angle_lower}, dt: {dt}s"
                )

                self.angles.append(
                    {
                        "timestamp": timestamp,
                        "angle_upper": self.angle_upper,
                        "angle_lower": self.angle_lower,
                    }
                )

            self.last_timestamp = timestamp

    def _get_delta_time(self, current_timestamp: datetime) -> float:
        """
        Calculate the time difference between the current timestamp and the last
        timestamp.

        Args:
            current_timestamp (datetime): The current timestamp.
        Returns:
            float: The time difference in seconds.
        """

        if self.last_timestamp is None:
            return None

        delta_time = (current_timestamp - self.last_timestamp).total_seconds()
        return delta_time

    def get_angles(self):
        """
        Get the angles from the IMU data.

        Returns:
            list: A list of angles.
        """
        return self.angles
