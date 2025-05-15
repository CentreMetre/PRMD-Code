
import settings
from communication.client import get_iot_hub_client
from communication.upload import run_upload

import user_io

def main():
    print("In main")
    user_io.user_flow()
    connection_string = settings.IOT_CONNECTION_STRING
    client = get_iot_hub_client(connection_string)
    run_upload(client)

    # TODO: hook up the upload schedule, all the other code for communication is in place
    # Not sure how to implement this yet, but I think it should be a separate thread
    # or a separate process that checks if we're connected to the internet
    # and if so, it should run the upload function every 5 minutes.

