import time

import gyro_accel
import strain_gauge
import settings
from communication.client import get_iot_hub_client
from communication.upload import run_upload
import os
from utils import file_io

def main():
    connection_string = settings.IOT_CONNECTION_STRING
    client = get_iot_hub_client(connection_string)
    run_upload(client)

    # TODO: hook up the upload schedule, all the other code for communication is in place
    # Not sure how to implement this yet, but I think it should be a separate thread
    # or a separate process that checks if we're connected to the internet
    # and if so, it should run the upload function every 5 minutes.

gyro_accel_measured = False
strain_gauge_measured = False

def ask_sensor_type():
    is_answer_valid = False
    choice = -1

    valid_answers = [0]

    print("Please choose a sensor type:")
    if gyro_accel_measured == False:
        print("[1] Gyroscope & Accelerometer")
        valid_answers.append(1)
    if strain_gauge_measured == False:
        print("[2] Strain Gauge")
        valid_answers.append(2)
    print("[0] Exit")

    while not input_valid(valid_answers, choice):
        choice = int(input())
        if input_valid(valid_answers, choice):
            break
        print(f"Input of {choice} is not valid. Try again.")


    return choice

def input_valid(valid_inputs, choice):
    if choice not in valid_inputs:
        return False
    return True



if __name__ == "__main__":
    choice = -1
    session_start = time.time()
    gyro_accel_data = {}
    strain_gauge_data = {}
    while True:
        while gyro_accel_measured == False or strain_gauge_measured == False:
            choice = ask_sensor_type()
        if choice == 0:
            break
        if choice == 1:
            gyro_accel.run_session()
            gyro_accel_measured = True
        if choice == 2:
            strain_gauge_data = strain_gauge.run_session()
            strain_gauge_measured = True

    final_readings = {}
    # final_readings["session_start"] = session_start
    if gyro_accel_data:
        final_readings["gyro_accel"] = strain_gauge_data
    if strain_gauge_data:
        final_readings["strain_gauge"] = strain_gauge_data

    if not final_readings:
        print("No data gathered or written.")
        exit()

    file_name = f"{session_start}.json"
    path_to_write = os.path.join(os.getcwd(), settings.SESSION_DIR, file_name)
    file_io.write_to_json_file(path_to_write, final_readings)

