import smbus
import time

bus = smbus.SMBus(1)

# Sensor addresses
SENSOR_1_ADDR = 0x6A
SENSOR_2_ADDR = 0x6B

# Control registers to enable sensors (example: 104 Hz, full scale ±2g and ±250 dps)
CTRL1_XL = 0x10  # Accelerometer
CTRL2_G  = 0x11  # Gyroscope

# Register Addresses for Accel and Gyro
ACCEL_LOW_X = 0x28  # Accelerometer X low byte
ACCEL_HIGH_X = 0x29 # Accelerometer X high byte
ACCEL_LOW_Y = 0x2A
ACCEL_HIGH_Y = 0x2B
ACCEL_LOW_Z = 0x2C
ACCEL_HIGH_Z = 0x2D

GYRO_LOW_X = 0x22  # Gyroscope X low byte
GYRO_HIGH_X = 0x23
GYRO_LOW_Y = 0x24
GYRO_HIGH_Y = 0x25
GYRO_LOW_Z = 0x26
GYRO_HIGH_Z = 0x27

def init_sensor(addr):
    try:
        # Attempt to initialize the sensor
        bus.write_byte_data(addr, CTRL1_XL, 0b01000000)  # 104 Hz, ±2g
        bus.write_byte_data(addr, CTRL2_G,  0b01000000)  # 104 Hz, ±250 dps
    except IOError:
        print(f"Error: Could not initialize sensor at address {hex(addr)}")
        return False
    return True

def read_word(addr, reg_low):
    try:
        low = bus.read_byte_data(addr, reg_low)
        high = bus.read_byte_data(addr, reg_low + 1)
        value = (high << 8) | low
        return value - 65536 if value > 32767 else value
    except IOError:
        print(f"Error: Could not read data from address {hex(addr)}")
        return None

def read_accel(addr):
    accel = {}
    accel['x'] = read_word(addr, ACCEL_LOW_X)
    accel['y'] = read_word(addr, ACCEL_LOW_Y)
    accel['z'] = read_word(addr, ACCEL_LOW_Z)
    return accel

def read_gyro(addr):
    gyro = {}
    gyro['x'] = read_word(addr, GYRO_LOW_X)
    gyro['y'] = read_word(addr, GYRO_LOW_Y)
    gyro['z'] = read_word(addr, GYRO_LOW_Z)
    return gyro

# Initialize both sensors
sensor1_initialized = init_sensor(SENSOR_1_ADDR)
sensor2_initialized = init_sensor(SENSOR_2_ADDR)

if not sensor1_initialized or not sensor2_initialized:
    print("One or both sensors failed to initialize. Exiting.")
    exit(1)

# Main loop to read data from both sensors
while True:
    accel1 = read_accel(SENSOR_1_ADDR)
    gyro1 = read_gyro(SENSOR_1_ADDR)
    accel2 = read_accel(SENSOR_2_ADDR)
    gyro2 = read_gyro(SENSOR_2_ADDR)

    # Format the output with padding to align values in the columns
    if accel1 is not None and gyro1 is not None:
        print(f"{accel1['x']:<20}{accel1['y']:<20}{accel1['z']:<20}{gyro1['x']:<20}{gyro1['y']:<20}{gyro1['z']:<20}", end="")
    else:
        print(f"{'Error':<20}{'Error':<20}{'Error':<20}{'Error':<20}{'Error':<20}{'Error':<20}", end="")

    if accel2 is not None and gyro2 is not None:
        print(f"{accel2['x']:<20}{accel2['y']:<20}{accel2['z']:<20}{gyro2['x']:<20}{gyro2['y']:<20}{gyro2['z']:<20}")
    else:
        print(f"{'Error':<20}{'Error':<20}{'Error':<20}{'Error':<20}{'Error':<20}{'Error':<20}")

    time.sleep(1)

