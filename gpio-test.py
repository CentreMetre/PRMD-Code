import lgpio
import time

# Define GPIO pins (BCM numbering)
DT_PIN = 5     # HX711 DOUT
SCK_PIN = 6    # HX711 SCK

# Open GPIO chip
h = lgpio.gpiochip_open(0)

# Set pin directions
lgpio.gpio_claim_input(h, DT_PIN)
lgpio.gpio_claim_output(h, SCK_PIN)

# Read HX711 data
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
    lgpio.gpio_write(h, SCK_PIN, 1)
    time.sleep(0.000001)
    lgpio.gpio_write(h, SCK_PIN, 0)
    time.sleep(0.000001)
    if count & 0x800000:
        count |= ~0xffffff
    return count

# Fixed scale factor for plausible output (tweak as needed)
SCALE = 80.0
OFFSET = 0

# Average function to smooth noise
def average_readings(num_samples):
    total = 0
    for _ in range(num_samples):
        total += read_hx711()
        time.sleep(0.1)
    return total // num_samples

# Tare only
def tare():
    global OFFSET
    input("Place NOTHING on the scale, then press Enter to tare...")
    OFFSET = average_readings(10)
    print(f"Tare set: {OFFSET}")

# Get weight using simulated scale
def get_weight():
    raw = average_readings(10)
    print("\n Raw:", raw)
    adjusted = raw - OFFSET
    weight = adjusted / SCALE
    return weight

# Main
try:
    tare()
    while True:
        weight = get_weight()
        print(f"Measured Weight: {weight:.2f} grams")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    lgpio.gpiochip_close(h)
