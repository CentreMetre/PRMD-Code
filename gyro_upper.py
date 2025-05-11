import smbus
import time

I2C_ADDR = 0x6A  # Upper sensor
bus = smbus.SMBus(1)  # i2c bus 1

# register addresses
WHO_AM_I = 0x0F
CTRL1_XL = 0x10
CTRL2_G = 0x11
OUTX_L_G = 0x22  # gryo low byte
OUTX_L_A = 0x28  # accelerator low bye

WHO_AM_I = 0x0F
CTRL1_XL = 0x10
CTRL2_G = 0x11
OUTY_L_G = 0x24
OUTZ_L_G = 0x26
OUTY_L_A = 0x2A
OUTZ_L_A = 0x2C


# check if sensor is detected
if bus.read_byte_data(I2C_ADDR, WHO_AM_I) == 0x6C:
    print("LSM6DSOX detected")

# config accelerometer (104Hz, +/-4g)
bus.write_byte_data(I2C_ADDR, CTRL1_XL, 0x40)  # 0x40 used for most sensitivity

# config gyroscope (104Hz, 250dps)
bus.write_byte_data(I2C_ADDR, CTRL2_G, 0x42)  # 0x42 used for most sensitivity


def read_data(register):
    # read 2 bytes of data from the given register
    low = bus.read_byte_data(I2C_ADDR, register)
    high = bus.read_byte_data(I2C_ADDR, register + 1)
    value = (high << 8) | low
    if value > 32767:
        value -= 65536  # Convert to signed value
    return value


calibration_readings = {
    'accel': {'X': [], 'Y': [], 'Z': []},
    'gyro': {'X': [], 'Y': [], 'Z': []}
}

# while True:
#     # Accelerometer readings
#     accel_x = read_data(OUTX_L_A)
#     accel_y = read_data(OUTY_L_A)
#     accel_z = read_data(OUTZ_L_A)
#
#     # Gyroscope readings
#     gyro_x = read_data(OUTX_L_G)
#     gyro_y = read_data(OUTY_L_G)
#     gyro_z = read_data(OUTZ_L_G)
#
#     print(f"Accel X: {accel_x}, Y: {accel_y}, Z: {accel_z}")
#     print(f"Gyro  X: {gyro_x}, Y: {gyro_y}, Z: {gyro_z}")
#     print()
#     time.sleep(0.1)


def calibrate_final_data(data):
    accel_bias_X_mean = calculate_mean(calibration_readings['accel']['X'])
    accel_bias_Y_mean = calculate_mean(calibration_readings['accel']['Y'])
    accel_bias_Z_mean = calculate_mean(calibration_readings['accel']['Z'])

    gyro_bias_X_mean = calculate_mean(calibration_readings['gyro']['X'])
    gyro_bias_Y_mean = calculate_mean(calibration_readings['gyro']['Y'])
    gyro_bias_Z_mean = calculate_mean(calibration_readings['gyro']['Z'])


def get_calibration_data():
    calibration_readings = read_sensors_for_time(2)


def read_sensors_for_time(seconds):
    start = time.time()
    end = start + seconds

    readings = {
        'accel': {'X': [], 'Y': [], 'Z': []},
        'gyro': {'X': [], 'Y': [], 'Z': []}
    }

    while True:
        # Accelerometer readings
        accel_x = read_data(OUTX_L_A)
        readings['accel']['X'].append(accel_x)

        accel_y = read_data(OUTY_L_A)
        readings['accel']['Y'].append(accel_y)

        accel_z = read_data(OUTZ_L_A)
        readings['accel']['Z'].append(accel_z)

        # Gyroscope readings
        gyro_x = read_data(OUTX_L_G)
        readings['gyro']['X'].append(gyro_x)

        gyro_y = read_data(OUTY_L_G)
        readings['gyro']['Y'].append(gyro_y)

        gyro_z = read_data(OUTZ_L_G)
        readings['gyro']['Z'].append(gyro_z)

        print(f"Accel X: {accel_x}, Y: {accel_y}, Z: {accel_z}")
        print(f"Gyro  X: {gyro_x}, Y: {gyro_y}, Z: {gyro_z}")

        if time.time() >= end:
            return readings


def calculate_mean(list):
    length = 0
    total_sum = 0
    for i in range(len(list)):
        length = + 1
        total_sum = total_sum + list[i]
