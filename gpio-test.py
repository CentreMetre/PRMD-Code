import lgpio
import time

DT_PIN = 5  # Data pin DOUT
SCK_PIN = 27  # clock pin PD_SCK

# open gpio chip
h = lgpio.gpiochip_open(0)

# set pin directions
lgpio.gpio_claim_input(h, DT_PIN)
lgpio.gpio_claim_output(h, SCK_PIN)

def read_hx711():
    count = 0

    # Wait until DT goes low
    while lgpio.gpio_read(h, DT_PIN):
        pass

    # Read 24 bits of data
    for _ in range(24):
        lgpio.gpio_write(h, SCK_PIN, 1)
        time.sleep(0.000001)  # 1 µs
        count = count << 1
        lgpio.gpio_write(h, SCK_PIN, 0)
        time.sleep(0.000001)
        if lgpio.gpio_read(h, DT_PIN):
            count += 1

    # Set gain (1 more clock pulse)
    lgpio.gpio_write(h, SCK_PIN, 1)
    time.sleep(0.000001)
    lgpio.gpio_write(h, SCK_PIN, 0)
    time.sleep(0.000001)

    # Convert to signed int
    if count & 0x800000:
        count |= ~0xffffff  # Two's complement for 24-bit signed value

    return count

try:
    while True:
        val = read_hx711()
        print(f'Reading: {val}')
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    lgpio.gpiochip_close(h)