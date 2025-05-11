class Session:
    """
    Represents a session of data collection from a specific sensor.

    Each session is identified by a unique session ID and contains data points collected from the sensor.
    The session also includes the type of sensor from which the data was collected.
    The data points are stored as a list of dictionaries, where each dictionary contains a timestamp and the corresponding data.

    Attributes:
        session_id (str): The unique identifier for the session.
        sensor_type (str): The type of sensor from which the data was collected.
        data_points (list[dict]): A list of dictionaries containing the timestamp and data collected during the session.
    """

    def __init__(self, session_id: str, sensor_type: str, data_points: list[dict]):
        self.session_id = session_id
        self.sensor_type = sensor_type
        self.data_points = data_points

    @classmethod
    def from_json(cls, json_data: dict) -> "Session":
        """
        Create a Session instance from JSON data.

        This method extracts the session ID, sensor type, and data points from the provided JSON data.
        It assumes that the JSON data contains a key "sensor_type" and a list of data points.
        The session ID is extracted from the JSON data, and if not present, defaults to "unknown".

        Args:
            json_data (dict): The JSON data containing session information.

        Returns:
            Session: An instance of the Session class initialized with the provided JSON data.
        """
        sensor_type = json_data.get("sensor_type", "unknown")

        data_points = []

        for timestamp, data in json_data.items():
            if timestamp != "sensor_type":
                data_points.append({"timestamp": timestamp, "data": data})

        return cls(
            session_id=json_data.get("session_id", "unknown"),
            sensor_type=sensor_type,
            data_points=data_points,
        )

    def get_session_id(self) -> str:
        """
        Get the session ID.

        Returns:
            str: The session ID.
        """
        return self.session_id

    def get_all_datapoints(self) -> list:
        """
        Get all data points in the session.

        Returns:
            list: A list of all data points in the session.
        """
        return self.data_points
