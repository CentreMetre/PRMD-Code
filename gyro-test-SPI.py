import spidev
import time

# SPI device on CE0 (GPIO8 / Pin 24)
spi = spidev.SpiDev()
spi.open(0, 0)  # bus 0, device 0 (CE0)
spi.max_speed_hz = 10000000  # 10 MHz
spi.mode = 0b11  # CPOL=1, CPHA=1 per LSM6DSOX datasheet

# Register addresses
WHO_AM_I = 0x0F
CTRL1_XL = 0x10
CTRL2_G = 0x11
OUTX_L_G = 0x22
OUTX_L_XL = 0x28

def write_register(reg, value):
    # MSB = 0 for write
    spi.xfer2([reg & 0x7F, value])

def read_register(reg):
    # MSB = 1 for read, auto-increment for multi-byte
    return spi.xfer2([reg | 0x80, 0x00])[1]

def read_multiple(reg, length):
    # Read multiple bytes from 'reg'
    result = spi.xfer2([reg | 0xC0] + [0x00] * length)
    return result[1:]  # skip first byte (status)

def twos_complement(low, high):
    val = (high << 8) | low
    if val >= 32768:
        val -= 65536
    return val

# Check device ID
if read_register(WHO_AM_I) == 0x6C:
    print("LSM6DSOX detected")
else:
    print("Sensor not detected")
    exit(1)

# Init accelerometer (104Hz, ±2g)
write_register(CTRL1_XL, 0x40)

# Init gyroscope (104Hz, 250 dps)
write_register(CTRL2_G, 0x40)

# Read loop
try:
    while True:
        accel_bytes = read_multiple(OUTX_L_XL, 6)
        gyro_bytes = read_multiple(OUTX_L_G, 6)

        ax = twos_complement(accel_bytes[0], accel_bytes[1])
        ay = twos_complement(accel_bytes[2], accel_bytes[3])
        az = twos_complement(accel_bytes[4], accel_bytes[5])

        gx = twos_complement(gyro_bytes[0], gyro_bytes[1])
        gy = twos_complement(gyro_bytes[2], gyro_bytes[3])
        gz = twos_complement(gyro_bytes[4], gyro_bytes[5])

        print(f"Accel X:{ax}, Y:{ay}, Z:{az} | Gyro X:{gx}, Y:{gy}, Z:{gz}")
        time.sleep(0.1)
except KeyboardInterrupt:
    spi.close()

