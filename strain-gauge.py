import time
import pigpio
from hx711 import HX711  # Assuming you're using a library for HX711

DT = 5  # Logical GPIO pin 5 for DT (physical pin 29)
SCK = 6  # Logical GPIO pin 6 for SCK (physical pin 31)

pi = pigpio.pi('localhost', 8888)

if not pi.connected:
    print("Pi not connected")
    exit()

# Start hx711
hx = HX711(dout_pin=DT, pd_sck_pin=SCK)

def read_sensor():
    weight = hx.get_weight(5)  # Get 5 readings
    print(f"WEIGHT: {weight}")
    return weight

if __name__ == "__main__":
    print(read_sensor())