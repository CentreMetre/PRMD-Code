import json
import sensor_enum

"""
Used to convert a session of data into a json file for uploading to the cloud.
"""


def write_to_json_file(readings, file_name):
    """

    Args:
        file_name:
        readings: The reading data

    Returns:

    """
    with open(file_name, 'w') as f:
        json.dump(readings, f, indent=4)
