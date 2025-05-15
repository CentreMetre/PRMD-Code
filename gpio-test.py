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

