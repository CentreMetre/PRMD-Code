import json
import sensor_enum

"""
Used to convert a session of data into a json file for uploading to the cloud.
"""


def convert_reading_list_to_json(readings, sensor_type: sensor_enum):
    """

    Args:
        readings: The reading data
        sensor_type: The type of sensor used, as a sensor_enum

    Returns:

    """
    readings["sensor_type"] = sensor_type.value
    json_readings = json.dumps(readings, indent=4)
    return json_readings
