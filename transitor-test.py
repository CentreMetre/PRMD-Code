import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM (Broadcom chip-specific pin numbers)
GPIO.setmode(GPIO.BCM)

# Set GPIO 17 as an output pin
GPIO.setup(17, GPIO.OUT)

# Blink an LED connected to GPIO 17
for _ in range(5):
    GPIO.output(17, GPIO.HIGH)  # Turn LED on
    time.sleep(1)  # Wait for 1 second
    GPIO.output(17, GPIO.LOW)   # Turn LED off
    time.sleep(1)  # Wait for 1 second

# Clean up GPIO settings
GPIO.cleanup()

