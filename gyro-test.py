import time
import smbus2
import env
import utils.prmd_json as pjson
import json
import sensor_enum

I2C_BUS = smbus2.SMBus(1)  # The I2C bus

# The sensor addresses
SENSOR_UPPER = 0x6A  # The upper part of the limb, e.g. upper arm in arm test
SENSOR_LOWER = 0x6B  # The lower part of the limb, e.g. lower arm in arm test.
# DO (or D0) has to be high power to be this address: Connect to 3Vo

"""
VARIABLE MEANINGS
ACCEL   - Accelerometer data
GYRO    - Gyro data
LOW     - Lower half (low byte) of data
HIGH    - High half (high byte) of data
X, Y, Z - Axes
Example:
ACCEL_LOW_X
This is accelerometer data, the low byte of said data, for the X axis 
"""

# Data output addresses
ACCEL_LOW_X = 0x28
ACCEL_HIGH_X = 0x29
ACCEL_LOW_Y = 0x2A
ACCEL_HIGH_Y = 0x2B
ACCEL_LOW_Z = 0x2C
ACCEL_HIGH_Z = 0x2D

GYRO_LOW_X = 0x22
GYRO_HIGH_X = 0x23
GYRO_LOW_Y = 0x24
GYRO_HIGH_Y = 0x25
GYRO_LOW_Z = 0x26
GYRO_HIGH_Z = 0x27

CTRL_ACCEL = 0x10
ACCEL_CONFIG = 0x40

CTRL_GYRO = 0x11
GYRO_CONFIG = 0x42


def read_register(sensor_address, register):
    return I2C_BUS.read_byte_data(sensor_address, register)


def write_register(sensor_address, register, value):
    """
    Write a value to a register of a sensor using smbus2
    :param sensor_address: The sensor to write to
    :param register: The register to write to
    :param value: The value to write
    """
    I2C_BUS.write_byte_data(sensor_address, register, value)


def read_sensor_axis(sensor_address, register_low, register_high):
    """
    Args:
        sensor_address: The address of the sensor to read, upper or lower
        register_low: the low address of the register to read
        register_high: the high address of the register to read

    Returns: the signed value

    """
    high = read_register(sensor_address, register_high)
    low = read_register(sensor_address, register_low)
    value = (high << 8) | low
    if value > 32767:
        value -= 65536  # Convert to signed value
    return value


def initial_config():

    """

    Returns:Nothing

    """
    write_register(SENSOR_UPPER, CTRL_ACCEL, ACCEL_CONFIG)
    time.sleep(0.1)
    write_register(SENSOR_LOWER, CTRL_ACCEL, ACCEL_CONFIG)
    time.sleep(0.1)
    write_register(SENSOR_UPPER, CTRL_GYRO, GYRO_CONFIG)
    time.sleep(0.1)
    write_register(SENSOR_LOWER, CTRL_GYRO, GYRO_CONFIG)
    time.sleep(0.1)
    print("Config Complete:")
    print(f"""
    UPPER ACCEL: {read_register(SENSOR_UPPER, CTRL_ACCEL)}
    LOWER ACCEL: {read_register(SENSOR_LOWER, CTRL_ACCEL)}
    UPPER GYRO: {read_register(SENSOR_UPPER, CTRL_GYRO)}
    LOWER GYRO: {read_register(SENSOR_LOWER, CTRL_GYRO)}
    """)

def read_sensors_for_time_with_interval(seconds, interval):
    """

    Reads the sensors and writes the data to the

    Args:
        seconds:The time in seconds to read
        interval:The time between readings in seconds (can be < 1)

    Returns: The readings as a list

    """
    start = time.time()
    end = start + seconds
    current_time = time.time()

    print("start:" + str(start))
    print("end:" + str(end))
    print("current:" + str(current_time))

    readings = {}

    while time.time() < end:


        print("time.time in loop: " + str(time.time()))
        # Read accelerometer data from SENSOR_UPPER
        UPPER_ACCEL_X = read_sensor_axis(SENSOR_UPPER, ACCEL_LOW_X, ACCEL_HIGH_X)
        UPPER_ACCEL_Y = read_sensor_axis(SENSOR_UPPER, ACCEL_LOW_Y, ACCEL_HIGH_Y)
        UPPER_ACCEL_Z = read_sensor_axis(SENSOR_UPPER, ACCEL_LOW_Z, ACCEL_HIGH_Z)

        # Read accelerometer data from SENSOR_LOWER
        LOWER_ACCEL_X = read_sensor_axis(SENSOR_LOWER, ACCEL_LOW_X, ACCEL_HIGH_X)
        LOWER_ACCEL_Y = read_sensor_axis(SENSOR_LOWER, ACCEL_LOW_Y, ACCEL_HIGH_Y)
        LOWER_ACCEL_Z = read_sensor_axis(SENSOR_LOWER, ACCEL_LOW_Z, ACCEL_HIGH_Z)

        # Read gyroscope data from SENSOR_UPPER
        UPPER_GYRO_X = read_sensor_axis(SENSOR_UPPER, GYRO_LOW_X, GYRO_HIGH_X)
        UPPER_GYRO_Y = read_sensor_axis(SENSOR_UPPER, GYRO_LOW_Y, GYRO_HIGH_Y)
        UPPER_GYRO_Z = read_sensor_axis(SENSOR_UPPER, GYRO_LOW_Z, GYRO_HIGH_Z)

        # Read gyroscope data from SENSOR_LOWER
        LOWER_GYRO_X = read_sensor_axis(SENSOR_LOWER, GYRO_LOW_X, GYRO_HIGH_X)
        LOWER_GYRO_Y = read_sensor_axis(SENSOR_LOWER, GYRO_LOW_Y, GYRO_HIGH_Y)
        LOWER_GYRO_Z = read_sensor_axis(SENSOR_LOWER, GYRO_LOW_Z, GYRO_HIGH_Z)

        current_time = time.time()

        new_reading = {} # reset reading

        new_reading = {
            "lower_accel_x": LOWER_ACCEL_X,
            "lower_accel_y": LOWER_ACCEL_Y,
            "lower_accel_z": LOWER_ACCEL_Z,
            "upper_accel_x": UPPER_ACCEL_X,
            "upper_accel_y": UPPER_ACCEL_Y,
            "upper_accel_z": UPPER_ACCEL_Z,
            "lower_gyro_x": LOWER_GYRO_X,
            "lower_gyro_y": LOWER_GYRO_Y,
            "lower_gyro_z": LOWER_GYRO_Z,
            "upper_gyro_x": UPPER_GYRO_X,
            "upper_gyro_y": UPPER_GYRO_Y,
            "upper_gyro_z": UPPER_GYRO_Z
        }

        readings[current_time] = new_reading

        print(readings[current_time])



        print("Sleeping for ", interval)
        time.sleep(interval)

    return readings


def read_sensors_for_time(seconds):
    return read_sensors_for_time_with_interval(seconds, 0)


def get_calibration_data():
    calibration_data = read_sensors_for_time(0.5)


if __name__ == '__main__':
    session_start = time.time()
    initial_config()
    get_calibration_data()
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("GATHERED CALIBRATION DATA")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    readings = read_sensors_for_time_with_interval(1, 0.25)
    print("Done reading")

    readings["sensor_type"] = sensor_enum.SensorType.GYRO_ACCEL.value
    file_name = str(session_start)
    pjson.write_to_json_file(readings, file_name, "/home/pi/prmd/data/sessions")

    print("Done writing to file")



