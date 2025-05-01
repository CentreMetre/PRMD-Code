import smbus
import time

# I2C bus (typically 1 on Raspberry Pi)
bus = smbus.SMBus(1)

# I2C addresses for the two sensors
address_sensor_1 = 0x6A
address_sensor_2 = 0x6B

# Read WHO_AM_I register (0x0F) from both sensors
def read_who_am_i(address):
    try:
        who_am_i = bus.read_byte_data(address, 0x0F)
        print(f"WHO_AM_I at address {hex(address)}: {who_am_i}")
    except Exception as e:
        print(f"Error with address {hex(address)}: {e}")

# Read from both sensors
read_who_am_i(address_sensor_1)
read_who_am_i(address_sensor_2)

