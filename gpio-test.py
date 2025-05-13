import lgpio
import time

# Define GPIO pins (BCM numbering)
DT_PIN = 5     # HX711 DOUT
SCK_PIN = 27    # HX711 SCK

# Open GPIO chip
h = lgpio.gpiochip_open(0)

# Set pin directions
lgpio.gpio_claim_input(h, DT_PIN)
lgpio.gpio_claim_output(h, SCK_PIN)

def read_hx711():
    count = 0

    # Wait until DT goes low
    while lgpio.gpio_read(h, DT_PIN):
        pass

    # Read 24 bits
    for _ in range(24):
        lgpio.gpio_write(h, SCK_PIN, 1)
        time.sleep(0.000001)
        count = count << 1
        lgpio.gpio_write(h, SCK_PIN, 0)
        time.sleep(0.000001)
        if lgpio.gpio_read(h, DT_PIN):
            count += 1

    # One extra clock to set gain
    lgpio.gpio_write(h, SCK_PIN, 1)
    time.sleep(0.000001)
    lgpio.gpio_write(h, SCK_PIN, 0)
    time.sleep(0.000001)

    # Convert to signed int
    if count & 0x800000:
        count |= ~0xffffff

    return count

# Calibration variables
OFFSET = 0         # This will be set as tare value
SCALE = 1          # This will be updated during calibration

def get_weight_grams():
    raw = read_hx711()
    adjusted = raw - OFFSET
    grams = adjusted / SCALE
    return grams

def calibrate():
    global OFFSET, SCALE

    input("Make sure the scale is empty, then press Enter to tare...")
