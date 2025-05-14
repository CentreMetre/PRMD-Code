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
SCALE = 1          # This will be set to 1 for relative readings

# Average function to get stable readings
def average_readings(num_samples):
    total = 0
    for _ in range(num_samples):
        total += read_hx711()
        time.sleep(0.1)  # Small delay to avoid too many quick reads
    return total // num_samples





# Calibrate the scale using a known weight (e.g., 500g)
def calibrate():
    global OFFSET, SCALE

    # Step 1: Tare the scale (set the offset)
    input("Place nothing on the scale, then press Enter to tare...")
    OFFSET = average_readings(10)  # Average of 10 readings for stability
    print(f"Tare set: {OFFSET}")

    # Step 2: Place the 500ml bottle of water (500g)
    input("Place the 500ml bottle of water (500g) on the scale, then press Enter...")
    raw_with_water = average_readings(10)  # Get the average raw value with the bottle of water on the scale

    # Step 3: Calculate the scale factor
    known_weight_grams = 500  # 500ml bottle of water = 500g
    SCALE = (raw_with_water - OFFSET) / known_weight_grams  # Calculate scale factor
    print(f"Calibration complete. SCALE factor: {SCALE:.6f}")

# Get the weight based on the current scale factor







def get_weight():
    raw = average_readings(10)  # Apply averaging for stable weight readings
    adjusted = raw - OFFSET
    weight = adjusted / SCALE  # Convert raw value to weight (grams)





    return weight

# Main function to run
try:
    calibrate()

    while True:
        # Measure weight and apply averaging
        weight = get_weight()
        print(f"Measured Weight: {weight:.2f} grams")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    lgpio.gpiochip_close(h)