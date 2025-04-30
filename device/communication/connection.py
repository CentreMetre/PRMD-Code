from azure.iot.device import IoTHubDeviceClient
import time
import logging

CONNECTION_STRING = "HostName=ica-hub.azure-devices.net;DeviceId=myPi;SharedAccessKey=fGZ9gCilX6Hy+aNuoeopiyWFfAUnAw4vqMZZbLAz+lI="


# Set up logging
logging.basicConfig(level=logging.INFO)

def main():
    try:
        # Create the device client from the connection string
        device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

        # The device client will connect automatically on creation
        logging.info("Device client connected.")
        
        while True:
            message = "gyro_X=55 gyro_Y=55 gyro_Z=66 accelerometer=77"
            try:
                logging.info(f"Sending message: {message}")
                device_client.send_message(message)
                logging.info("Message sent successfully.")
            except Exception as e:
                logging.error(f"Error sending message: {e}")
            
            # Sleep for 5 seconds before sending the next message
            time.sleep(5)
    except Exception as e:
        logging.error(f"Failed to initialize device client: {e}")

if __name__ == "__main__":
    main()
