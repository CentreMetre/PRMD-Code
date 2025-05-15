
import settings
from communication.client import get_iot_hub_client
from communication.upload import run_upload

from utils import user_io, server


def main():
    print("In main")
    user_io.user_flow()
    server.upload_data()

if __name__ == "__main__":
    main()