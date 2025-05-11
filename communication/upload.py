import datetime
import os
import json
from models.session import Session
from settings import SESSION_DIR
from azure.iot.device import IoTHubDeviceClient
from utils.file_io import read_file


def upload_all_sessions(client: IoTHubDeviceClient) -> None:
    """
    Uploads all session files from the session directory to Azure IoT Hub.

    This function iterates through all JSON files in the session directory,
    loads their contents, and sends each item as a separate message using the IoTHubDeviceClient.

    Args:
        client (IoTHubDeviceClient): The connected IoT Hub client.

    Raises:
        Exception: If there is an error while uploading session files to Azure IoT Hub.
    """
    for filename in os.listdir(SESSION_DIR):
        if not filename.endswith(".json"):
            continue  # skip non-json files

        try:
            file_path = os.path.join(SESSION_DIR, filename)
            raw_data = read_file(file_path)
            session = Session.from_json(json.loads(raw_data))

            for dp in session.get_all_datapoints():
                message = {
                    "timestamp": convert_unix_to_iso(dp["timestamp"]),
                    "data": dp["data"],
                }
                client.send_message(message)

            os.remove(file_path)  # remove the file after upload

        except Exception as e:
            raise Exception(
                f"An error occurred while uploading session file {filename} to Azure IoT Hub."
            ) from e


def run_upload(client: IoTHubDeviceClient) -> None:
    """
    Main function to run the upload process.

    This function connects to the IoT Hub client and calls the upload_all_sessions function
    to upload all session files. It handles any exceptions that may occur during the process.

    Args:
        client (IoTHubDeviceClient): The IoT Hub client to use for uploading session files.

    Raises:
        Exception: If there is an error while uploading session files to Azure IoT Hub.
    """
    try:
        client.connect()
        upload_all_sessions(client)

    except Exception as e:
        raise Exception(
            "An error occurred while uploading session files to Azure IoT Hub."
        ) from e

    finally:
        client.disconnect()


def convert_unix_to_iso(unix_timestamp: int) -> str:
    """
    Converts a Unix timestamp to ISO 8601 format.

    Args:
        unix_timestamp (int): The Unix timestamp to convert.

    Returns:
        str: The ISO 8601 formatted date string.
    """
    return datetime.datetime.fromtimestamp(unix_timestamp).isoformat()
