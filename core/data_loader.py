import json
import logging
import utils.file_io as fr
from config import config


class DataLoader:
    """
    DataLoader class for loading and preprocessing data.

    This class is responsible for loading data from a specified path,
    preprocessing it, and separating it into IMU and strain gauge data.
    The data is expected to be in JSON format, with each line being a JSON object.
    The JSON objects should contain a "sensor_type" field that indicates
    whether the data is from an IMU or a strain gauge.

    Attributes:
        data_path (str): The path to the data file.
        imu_data (list): List to store IMU data.
        strain_data (list): List to store strain gauge data.
    """

    def __init__(self, data_path: str = config.DEFAULT_DATA_PATH):
        """
        Initialise the DataLoader with the specified data path.

        Args:
            data_path (str): The path to the data file.
        """
        self.data_path = data_path
        self.imu_data = []
        self.strain_data = []

    def load_data(self):
        """
        Load data from the specified path and preprocess it.

        This function reads the data from the file, which is expected to be
        in JSON format. It then processes the data to separate IMU and strain
        gauge data. The data is expected to be a string with each line being
        a JSON object. Each JSON object should contain a "sensor_type" field
        that indicates whether the data is from an IMU or a strain gauge.

        Raises:
            Exception: If there is an error loading the data.
        """
        try:
            logging.debug(f"Loading data from: {self.data_path}")
            data = fr.read_file_json(self.data_path)
            self.preprocess_data(data)
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            raise Exception(f"Error loading data: {e}") from e

    def preprocess_data(self, data: list) -> None:
        """
        Preprocess the loaded data to extract relevant information.

        Args:
            data (str): The raw data as a string.
        """
        logging.debug(f"Preprocessing {len(data)} data lines")
        for entry in data:
            logging.debug(f"Processing entry: {entry}")
            if entry["sensor_type"] == "gyro_accel":
                self.imu_data.append(entry)
            elif entry["sensor_type"] == "strain_gauge":
                self.strain_data.append(entry)

        # sort the data by timestamp
        self.imu_data.sort(key=lambda x: x["timestamp"])
        self.strain_data.sort(key=lambda x: x["timestamp"])
        logging.debug(
            f"IMU data count: {len(self.imu_data)}, Strain data count: {len(self.strain_data)}"
        )

    def get_imu_data(self):
        """
        Get the IMU data.

        Returns:
            list: The IMU data.
        """
        return self.imu_data

    def get_strain_data(self):
        """
        Get the strain data.

        Returns:
            list: The strain data.
        """
        return self.strain_data
