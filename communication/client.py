import os
from azure.iot.device import IoTHubDeviceClient
from dotenv import load_dotenv


load_dotenv()


def get_iot_hub_client() -> IoTHubDeviceClient:
    """
    Creates and returns an instance of IoTHubDeviceClient using the Azure IoT Hub connection string
    specified in the environment variables.

    This function loads the connection string from the environment variable 'AZURE_IOT_HUB_CONNECTION_STRING'.
    If the connection string is not set, it raises a ValueError. The returned IoTHubDeviceClient instance
    can be used to send messages to or receive messages from Azure IoT Hub.

    Returns:
        IoTHubDeviceClient: An authenticated client for communicating with Azure IoT Hub.

    Raises:
        ValueError: If the 'AZURE_IOT_HUB_CONNECTION_STRING' environment variable is not set.
    """

    # load variable from .env
    connection_string = os.getenv("AZURE_IOT_HUB_CONNECTION_STRING")

    if not connection_string:
        raise ValueError("Connection string is not set in the environment variables.")

    client = IoTHubDeviceClient.create_from_connection_string(connection_string)

    return client
