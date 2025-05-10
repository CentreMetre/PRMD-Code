import json

"""
Used to convert a session of data into a json file for uploading to the cloud.
"""

def convert_reading_list_to_json(reading):
    json_readings = json.dumps(reading, indent=4)
    return json_readings
