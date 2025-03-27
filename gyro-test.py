import smbus
import time

I2C_ADDR = 0x6A
bus = smbus.SMBus(1) # i2c bus 1

#register addresses
WHO_AM_I = 0x0F
CRTL_XL = 0x10
CTRL2_G = 0x11
OUTX_L_G = 0x22 #gryo low byte
OUTX_L_A = 0x28 #accelerator low bye

#check if sensor is detected
if bus.read_byte_date(I2C_ADDR, WHO_AM_I) == 0x6C:
    print("LSM6DSOX detected")

#confidue accelerometer (104Hz, +/-4g)
bus.write_byte_data(I2C_ADDR, CTRL1_XL, 0x50)

#config gyroscope (104Hz, 250dps)
bus.write_byte_data(I2C_ADDR, CRTL2_G, 0x50)

def read_data(register):
    #read 2 bytes of data from he given register
    low = bus.read_byte_data(I2C_ADDR, register)
    high = bus.read_byte_data(I2C_ADDR, register + 1)
    value = (high << 8) | low
    if value > 32767:
        value -= 65536  # Convert to signed value
    return value

while True:
    accel_x = read_data(OUTX_L_A)
    gyro_x = read_data(OUTX_L_G)

    print(f"Accel X: {accel_x}, Gyro X: {gyro_x}")
    time.sleep(1)
