import json
import os

import sensor_enum

"""
Used to convert a session of data into a json file for uploading to the cloud.
"""


def write_to_json_file(readings, file_name, dir_path):
    """

    Args:
        dir_path:
        file_name:
        readings: The reading data

    Returns:

    """

    full_path = os.path.join(dir_path, file_name + ".json")

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    print(full_path)

    with open(full_path, 'w') as f:
        json.dump(readings, f, indent=4)
