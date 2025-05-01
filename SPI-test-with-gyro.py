import spidev
import time

# Create an SPI object
spi = spidev.SpiDev()

# Open SPI bus (0 is the default bus, 0 is the chip select)
spi.open(0, 0)

# Set SPI speed (in Hz), mode (0 or 3), and bit length
spi.max_speed_hz = 50000  # Change this as needed
spi.mode = 3  # SPI mode (0 to 3, depending on your device)
spi.bits_per_word = 8  # 8 bits per word, most common

try:
    while True:
        # Read data from SPI (example: reading 3 bytes)
        data = spi.readbytes(3)

        # Print the received data
        print("Received Data:", data)
        time.sleep(0.1)
except KeyboardInterrupt:
    spi.close()
