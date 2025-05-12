import time
import RPi.GPIO as GPIO
from hx711 import HX711

DT = 5 #Logical GPIO pin 5 for DT (physical pin 29)
SCK = 6 #Logical GPIO pin 6 for DT (physical pin 31)

hx = HX711(dout_pin=DT, pd_sck_pin=SCK) # Initialise the HX711 with the pins needed

GPIO.setmode(GPIO.BCM)

def read_sensor_for_time_with_interval(time: int, interval: int):
    print("TO IMPLEMENT")

def read_sensor():
    weight = hx.get_weight(5)
    print(f"WEIGHT: {weight}")
    return weight

if __name__ == "__main__":
    print(read_sensor())