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

# Read raw 24-bit data from HX711
def read_hx711():
    count = 0
    while lgpio.gpio_read(h, DT_PIN):
        pass
    for _ in range(24):
        lgpio.gpio_write(h, SCK_PIN, 1)
        time.sleep(0.000001)
        count = count << 1
        lgpio.gpio_write(h, SCK_PIN, 0)
        time.sleep(0.000001)
        if lgpio.gpio_read(h, DT_PIN):
            count += 1
    # Extra clock pulse
    lgpio.gpio_write(h, SCK_PIN, 1)
    time.sleep(0.000001)
    lgpio.gpio_write(h, SCK_PIN, 0)
    time.sleep(0.000001)
    # Convert to signed 24-bit int
    if count & 0x800000:
        count |= ~0xffffff
    return count

# Average multiple readings
def average_readings(samples=10, delay=0.05):
    total = 0
    for _ in range(samples):
        total += read_hx711()
        time.sleep(delay)
    return total // samples

# Calibration variables
OFFSET = 0
SCALE = 1.0

# Calibrate using a known weight
def calibrate():
    global OFFSET, SCALE

    input("Place nothing on the scale, then press Enter to tare...")
    OFFSET = average_readings(10)
    print(f"OFFSET (no weight): {OFFSET}")

    input("Place the 500g weight on the scale, then press Enter...")
    raw_with_weight = average_readings(10)
    print(f"Raw with 500g: {raw_with_weight}")

    delta = raw_with_weight - OFFSET
    print(f"Delta raw: {delta}")

    if abs(delta) < 1000:
        print("WARNING: Very small raw difference. Check load cell wiring, mounting, and weight placement.")

    known_weight_grams = 500
    SCALE = delta / known_weight_grams
    print(f"SCALE factor: {SCALE:.6f}")

# Convert to grams
def get_weight():
    raw = average_readings(10)
    adjusted = raw - OFFSET
    weight = adjusted / SCALE

    # Optional sanity check to clamp absurd values
    if abs(weight) > 2000:
        print(f"DEBUG: Unusual weight detected ({weight:.2f}g), skipping...")
        return 0
    return weight

# Main loop
try:
    calibrate()
    print("Reading weight...")
    while True:
        weight = get_weight()
        print(f"Measured Weight: {weight:.2f} grams")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    lgpio.gpiochip_close(h)
