import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # GPIO pin numbers, not phsical pin numbers

GPIO.setip(17, GPIO.OUT)

try:
    while true:
        GPIO.output(17, GPIO.HIGH)
        time.sleep(1)        
        GPIO.output(17, GPIO.HIGH)
        time.sleep(1)
except KeybaordInterrupt:
    print("Stopped by user")
finally:
    GPIO.cleanup()

