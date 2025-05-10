import time
import smbus2

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
    :return:
    """
    I2C_BUS.write_byte_data(sensor_address, register, value)


def initial_config():
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



if __name__ == '__main__':
    initial_config()
    while True:
        # Read accelerometer data from SENSOR_UPPER
        UPPER_ACCEL_LOW_X = read_register(SENSOR_UPPER, ACCEL_LOW_X)
        UPPER_ACCEL_HIGH_X = read_register(SENSOR_UPPER, ACCEL_HIGH_X)
        UPPER_ACCEL_X = (UPPER_ACCEL_HIGH_X << 8) | UPPER_ACCEL_LOW_X

        UPPER_ACCEL_LOW_Y = read_register(SENSOR_UPPER, ACCEL_LOW_Y)
        UPPER_ACCEL_HIGH_Y = read_register(SENSOR_UPPER, ACCEL_HIGH_Y)
        UPPER_ACCEL_Y = (UPPER_ACCEL_HIGH_Y << 8) | UPPER_ACCEL_LOW_Y

        UPPER_ACCEL_LOW_Z = read_register(SENSOR_UPPER, ACCEL_LOW_Z)
        UPPER_ACCEL_HIGH_Z = read_register(SENSOR_UPPER, ACCEL_HIGH_Z)
        UPPER_ACCEL_Z = (UPPER_ACCEL_HIGH_Z << 8) | UPPER_ACCEL_LOW_Z

        # Read accelerometer data from SENSOR_LOWER
        LOWER_ACCEL_LOW_X = read_register(SENSOR_LOWER, ACCEL_LOW_X)
        LOWER_ACCEL_HIGH_X = read_register(SENSOR_LOWER, ACCEL_HIGH_X)
        LOWER_ACCEL_X = (LOWER_ACCEL_HIGH_X << 8) | LOWER_ACCEL_LOW_X

        LOWER_ACCEL_LOW_Y = read_register(SENSOR_LOWER, ACCEL_LOW_Y)
        LOWER_ACCEL_HIGH_Y = read_register(SENSOR_LOWER, ACCEL_HIGH_Y)
        LOWER_ACCEL_Y = (LOWER_ACCEL_HIGH_Y << 8) | LOWER_ACCEL_LOW_Y

        LOWER_ACCEL_LOW_Z = read_register(SENSOR_LOWER, ACCEL_LOW_Z)
        LOWER_ACCEL_HIGH_Z = read_register(SENSOR_LOWER, ACCEL_HIGH_Z)
        LOWER_ACCEL_Z = (LOWER_ACCEL_HIGH_Z << 8) | LOWER_ACCEL_LOW_Z

        # Read gyroscope data from SENSOR_UPPER
        UPPER_GYRO_LOW_X = read_register(SENSOR_UPPER, GYRO_LOW_X)
        UPPER_GYRO_HIGH_X = read_register(SENSOR_UPPER, GYRO_HIGH_X)
        UPPER_GYRO_X = (UPPER_GYRO_HIGH_X << 8) | UPPER_GYRO_LOW_X

        UPPER_GYRO_LOW_Y = read_register(SENSOR_UPPER, GYRO_LOW_Y)
        UPPER_GYRO_HIGH_Y = read_register(SENSOR_UPPER, GYRO_HIGH_Y)
        UPPER_GYRO_Y = (UPPER_GYRO_HIGH_Y << 8) | UPPER_GYRO_LOW_Y

        UPPER_GYRO_LOW_Z = read_register(SENSOR_UPPER, GYRO_LOW_Z)
        UPPER_GYRO_HIGH_Z = read_register(SENSOR_UPPER, GYRO_HIGH_Z)
        UPPER_GYRO_Z = (UPPER_GYRO_HIGH_Z << 8) | UPPER_GYRO_LOW_Z

        # Read gyroscope data from SENSOR_LOWER
        LOWER_GYRO_LOW_X = read_register(SENSOR_LOWER, GYRO_LOW_X)
        LOWER_GYRO_HIGH_X = read_register(SENSOR_LOWER, GYRO_HIGH_X)
        LOWER_GYRO_X = (LOWER_GYRO_HIGH_X << 8) | LOWER_GYRO_LOW_X

        LOWER_GYRO_LOW_Y = read_register(SENSOR_LOWER, GYRO_LOW_Y)
        LOWER_GYRO_HIGH_Y = read_register(SENSOR_LOWER, GYRO_HIGH_Y)
        LOWER_GYRO_Y = (LOWER_GYRO_HIGH_Y << 8) | LOWER_GYRO_LOW_Y

        LOWER_GYRO_LOW_Z = read_register(SENSOR_LOWER, GYRO_LOW_Z)
        LOWER_GYRO_HIGH_Z = read_register(SENSOR_LOWER, GYRO_HIGH_Z)
        LOWER_GYRO_Z = (LOWER_GYRO_HIGH_Z << 8) | LOWER_GYRO_LOW_Z

        print("SENSOR_UPPER ACCELEROMETER:")
        print(f"  X: {UPPER_ACCEL_X}, Y: {UPPER_ACCEL_Y}, Z: {UPPER_ACCEL_Z}")
        print("SENSOR_UPPER GYROSCOPE:")
        print(f"  X: {UPPER_GYRO_X}, Y: {UPPER_GYRO_Y}, Z: {UPPER_GYRO_Z}")

        print("\nSENSOR_LOWER ACCELEROMETER:")
        print(f"  X: {LOWER_ACCEL_X}, Y: {LOWER_ACCEL_Y}, Z: {LOWER_ACCEL_Z}")
        print("SENSOR_LOWER GYROSCOPE:")
        print(f"  X: {LOWER_GYRO_X}, Y: {LOWER_GYRO_Y}, Z: {LOWER_GYRO_Z}")
