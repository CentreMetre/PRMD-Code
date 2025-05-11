from dotenv import load_dotenv
from communication.client import get_iot_hub_client
from communication.upload import run_upload
import os


def main():
    load_dotenv()
    connection_string = os.getenv("IOT_CONNECTION_STRING")
    client = get_iot_hub_client(connection_string)
    run_upload(client=client)


if __name__ == "__main__":
    main()
