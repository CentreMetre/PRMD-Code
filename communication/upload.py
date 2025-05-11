import os
import json
from communication.client import get_iot_hub_client
from azure.iot.device import IoTHubDeviceClient
from utils.file_io import read_file

SESSIONS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "sessions"
)


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
    for filename in os.listdir(SESSIONS_DIR):
        file_path = os.path.join(SESSIONS_DIR, filename)

        if not filename.endswith(".json"):
            continue  # skip non-json files

        try:
            session_data = read_file(file_path)

            for entry in session_data:
                message = json.dumps(entry)
                client.send_message(message)

            os.remove(file_path)  # remove the file after upload

        except Exception as e:
            raise Exception(
                f"An error occurred while uploading session file {filename} to Azure IoT Hub."
            ) from e


def run_upload() -> None:
    """
    Main function to run the upload process.

    This function creates an IoTHubDeviceClient instance, connects to Azure IoT Hub,
    and uploads all session files from the session directory. It handles any exceptions
    that may occur during the process and ensures proper cleanup of resources.

    Raises:
        Exception: If there is an error while uploading session files to Azure IoT Hub.
    """
    try:
        client = get_iot_hub_client()
        client.connect()

        upload_all_sessions(client)

    except Exception as e:
        raise Exception(
            "An error occurred while uploading session files to Azure IoT Hub."
        ) from e

    finally:
        client.disconnect()
