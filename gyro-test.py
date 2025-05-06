import time
import board
import busio
import adafruit_lsm6dsox

# Create the shared I2C bus (for /dev/i2c-1 on Raspberry Pi)
i2c = busio.I2C(board.SCL, board.SDA)

# Initialise the two sensors at different I2C addresses
sensor1 = adafruit_lsm6dsox.LSM6DSOX(i2c, address=0x6A)  # SDO = GND or unconnected
#sensor2 = adafruit_lsm6dsox.LSM6DSOX(i2c, address=0x6B)  # SDO = VCC

# Read and print data from both sensors
while True:
    accel1 = sensor1.acceleration
    gyro1 = sensor1.gyro
    temp1 = sensor1.temperature

#    accel2 = sensor2.acceleration
#    gyro2 = sensor2.gyro
#    temp2 = sensor2.temperature

    print("=== Sensor 1 (0x6A) ===")
    print(f"Accel: X={accel1[0]:.2f}, Y={accel1[1]:.2f}, Z={accel1[2]:.2f} m/s²")
    print(f"Gyro:  X={gyro1[0]:.2f}, Y={gyro1[1]:.2f}, Z={gyro1[2]:.2f} dps")
    print(f"Temp:  {temp1:.2f} °C")

#    print("\n=== Sensor 2 (0x6B) ===")
#    print(f"Accel: X={accel2[0]:.2f}, Y={accel2[1]:.2f}, Z={accel2[2]:.2f} m/s²")
#    print(f"Gyro:  X={gyro2[0]:.2f}, Y={gyro2[1]:.2f}, Z={gyro2[2]:.2f} dps")
#    print(f"Temp:  {temp2:.2f} °C\n")
#
    time.sleep(0.5)

