import json
from azure.iot.device import IoTHubDeviceClient

# unused until we have live data


def send_telemetry_data(client: IoTHubDeviceClient, data: dict) -> None:
    """
    Sends telemetry data to Azure IoT Hub.

    This function formats the provided telemetry data as JSON and sends it to the Azure IoT Hub using
    the provided IoTHubDeviceClient instance. It handles any exceptions that may occur during the
    sending process and raises appropriate errors. The function ensures that the telemetry data is in a
    format that can be serialised to JSON. If the data is not serializable, a TypeError will be raised.

    Args:
        client (IoTHubDeviceClient): The IoTHubDeviceClient instance to send data.
        data (str): The telemetry data to send.

    Raises:
        TypeError: If the data is not serializable to JSON.
        Exception: If there is an error while sending the telemetry data.

    Returns:
        None
    """
    try:
        json_data = json.dumps(data)
        client.send_message(json_data)
    except TypeError as e:
        raise TypeError("Telemetry data must be a JSON-serializable object.") from e
    except Exception as e:
        raise Exception(
            "An error occurred while sending telemetry data to Azure IoT Hub."
        ) from e
