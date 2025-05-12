import time
import lgpio # Tested: RPi.GPIO, pigpio, gpiozero. lgpio will work according to https://forums.raspberrypi.com/viewtopic.php?p=2152007#p2152007
from hx711 import HX711  # Assuming you're using a library for HX711

DT = 5  # Logical GPIO pin 5 for DT (physical pin 29)
SCK = 6  # Logical GPIO pin 6 for SCK (physical pin 31)

chip = lgpio.gpiochip_open(0)  # GPIO chip (0 is typically the first one)
lgpio.gpio_claim_input(chip, DT)  # Claim the data pin
lgpio.gpio_claim_output(chip, SCK)  # Claim the clock pin

# Start hx711
# hx = HX711(dout_pin=DT, pd_sck_pin=SCK)

def read_sensor():
    count = 0
    value = 0
    while count < 24:
        # Generate clock pulse (SCK pin goes HIGH and then LOW)
        lgpio.gpio_write(chip, SCK, 1)  # Set clock HIGH
        time.sleep(0.00001)  # Short delay
        lgpio.gpio_write(chip, SCK, 0)  # Set clock LOW
        time.sleep(0.00001)  # Short delay

        # Read the data bit from DT pin
        if lgpio.gpio_read(chip, DT) == 1:
            value |= 1 << (23 - count)  # Set bit in the correct position

        count += 1
    return value

if __name__ == "__main__":
    print(read_sensor())