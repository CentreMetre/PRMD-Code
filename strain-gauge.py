import RPi.GPIO as GPIO
from hx711 import HX711
import time

GPIO.setmode(GPIO.BCM)

DT_PIN = 40 #gpio 21 https://pinout.xyz/pinout/5v_power
SCK_PIN = 11 #gpio 17

hx = HX711(DT_PIN, SCK_PIN)

hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(1)

hx.reset()
hx.tare()

print("Scale is ready. Place and object to measure weight")

try:
    while True:
        weight = hs.get_weight(5)
        print(f"Weight: {weight:.2f} grams")

        hx.power_down()
        hx.power_up()
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting")
finally:
    GPIO.cleanup()
