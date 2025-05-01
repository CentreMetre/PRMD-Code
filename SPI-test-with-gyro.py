import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Device 0 (CE0)
spi.max_speed_hz = 50000

def read_data():
    data = spi.xfer2([0x01, 0x80, 0x00])  # Example SPI transfer (modify according to your sensor)
    return data

try:
    while True:
        print(read_data())
        time.sleep(1)

finally:
    spi.close()
