"""
import smbus

bus = smbus.SMBus(1)

# Address of the 2 sensors
SENSOR_1_ADDR = 0x6A
SENSOR_2_ADDR = 0x6B

# Control registers to enable sensors (example: 104 Hz, full scale ±2g and ±250 dps)
CTRL1_ACCEL = 0x10  # Accelerometer
CTRL2_GYRO = 0x11  # Gyroscope

# Register Addresses
## Gyro
### X
GYRO_LOW_X = 0x22  # Gyroscope X low byte
GYRO_HIGH_X = 0x23 # Gyro x high byte
### Y
GYRO_LOW_Y = 0x24
GYRO_HIGH_Y = 0x25
### Z
GYRO_LOW_Z = 0x26
GYRO_HIGH_Z = 0x27

## Accelerometer
### X
ACCEL_LOW_X = 0x28  # ACCEL X low byte
ACCEL_HIGH_X = 0x29 # ACCEL x high byte
### Y
ACCEL_LOW_Y = 0x2A
ACCEL_HIGH_Y = 0x2B
### Z
ACCEL_LOW_Z = 0x2C
ACCEL_HIGH_Z = 0x2D

def init_sensor(addr):
    bus.write_byte_data(addr, CTRL1_ACCEL, 0b01000000)  # 104 Hz, ±2g
    bus.write_byte_data(addr, CTRL2_GYRO, 0b01000000)  # 104 Hz, ±250 dps

def read_word(addr, reg_low):
    low = bus.read_byte_data(addr, reg_low)
    high = bus.read_byte_data(addr, reg_low + 1)
    value = (high << 8) | low
    return value - 65536 if value > 32767 else value

def read_accel(addr):
    return {
        'x': read_word(addr, 0x28),
        'y': read_word(addr, 0x2A),
        'z': read_word(addr, 0x2C),
    }
"""

import smbus

bus = smbus.SMBus(1)

SENSOR_1_ADDR = 0x6A
SENSOR_2_ADDR = 0x6B

# Control registers to enable sensors (example: 104 Hz, full scale ±2g and ±250 dps)
CTRL1_XL = 0x10  # Accelerometer
CTRL2_G  = 0x11  # Gyroscope

def init_sensor(addr):
    bus.write_byte_data(addr, CTRL1_XL, 0b01000000)  # 104 Hz, ±2g
    bus.write_byte_data(addr, CTRL2_G,  0b01000000)  # 104 Hz, ±250 dps

def read_word(addr, reg_low):
    low = bus.read_byte_data(addr, reg_low)
    high = bus.read_byte_data(addr, reg_low + 1)
    value = (high << 8) | low
    return value - 65536 if value > 32767 else value

def read_accel(addr):
    return {
        'x': read_word(addr, 0x28),
        'y': read_word(addr, 0x2A),
        'z': read_word(addr, 0x2C),
    }

def read_gyro(addr):
    return {
        'x': read_word(addr, 0x22),
        'y': read_word(addr, 0x24),
        'z': read_word(addr, 0x26),
    }

# Initialise both sensors
init_sensor(SENSOR_1_ADDR)
init_sensor(SENSOR_2_ADDR)

# Read and print data
accel1 = read_accel(SENSOR_1_ADDR)
gyro1  = read_gyro(SENSOR_1_ADDR)
accel2 = read_accel(SENSOR_2_ADDR)
gyro2  = read_gyro(SENSOR_2_ADDR)

print("Sensor 1 Accel:", accel1)
print("Sensor 1 Gyro :", gyro1)
print("Sensor 2 Accel:", accel2)
print("Sensor 2 Gyro :", gyro2)

