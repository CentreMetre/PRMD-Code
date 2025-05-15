import time
import lgpio # Tested: RPi.GPIO, pigpio, gpiozero. lgpio will work according to https://forums.raspberrypi.com/viewtopic.php?p=2152007#p2152007

DT = 5  # Logical GPIO pin 5 for DT (physical pin 29)
SCK = 6  # Logical GPIO pin 6 for SCK (physical pin 31)

chip = lgpio.gpiochip_open(0)  # GPIO chip (0 is typically the first one)
lgpio.gpio_claim_input(chip, DT)  # Claim the data pin
lgpio.gpio_claim_output(chip, SCK)  # Claim the clock pin

# Start hx711
# hx = HX711(dout_pin=DT, pd_sck_pin=SCK)

def read_sensor_for_time(seconds):
    readings = {}
    print(f"The sensor will read for {seconds} seconds")
    input("Press enter to start")
    end_time = time.time() + seconds

    while time.time() < end_time:
        # Wait until DT goes LOW indicating data is ready
        while lgpio.gpio_read(chip, DT):
            pass

        count = 0
        value = 0

        # Read 24 bits from HX711
        for _ in range(24):
            lgpio.gpio_write(chip, SCK, 1)
            time.sleep(0.00001)
            value = value << 1
            lgpio.gpio_write(chip, SCK, 0)
            time.sleep(0.00001)
            if lgpio.gpio_read(chip, DT):
                value += 1

        # One extra clock to set gain for next read
        lgpio.gpio_write(chip, SCK, 1)
        time.sleep(0.00001)
        lgpio.gpio_write(chip, SCK, 0)
        time.sleep(0.00001)

        # Convert to signed 24-bit value
        if value & 0x800000:
            value |= ~0xFFFFFF  # Extend sign for negative numbers

        # Add reading with timestamp key
        timestamp = time.time()
        readings[timestamp] = value

    print("Readings in read function")
    print(readings)
    return readings


def run_session():
    readings = read_sensor_for_time(5)


if __name__ == "__main__":
    run_session()
