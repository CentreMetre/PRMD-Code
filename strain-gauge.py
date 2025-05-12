import time
import lgpio # Tested: RPi.GPIO, pigpio, gpiozero. lgpio will work according to https://forums.raspberrypi.com/viewtopic.php?p=2152007#p2152007
from hx711 import HX711  # Assuming you're using a library for HX711

DT = 5  # Logical GPIO pin 5 for DT (physical pin 29)
SCK = 6  # Logical GPIO pin 6 for SCK (physical pin 31)

chip = lgpio.gpiochip_open(0)  # GPIO chip (0 is typically the first one)
lgpio.gpio_claim_input(chip, DT)  # Claim the data pin
lgpio.gpio_claim_output(chip, SCK)  # Claim the clock pin

# Start hx711
hx = HX711(dout_pin=DT, pd_sck_pin=SCK)

def read_sensor():
    def read_weight():
        try:
            print("Reading weight...")
            weight = hx._read(20)  # Get the average of 20 readings
            print(f"Weight: {weight} grams")
        except Exception as e:
            print(f"Error reading data: {e}")

if __name__ == "__main__":
    print(read_sensor())