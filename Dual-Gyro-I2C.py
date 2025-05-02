import smbus
import time

bus = smbus.SMBus(1)

SENSOR_1_ADDR = 0x6A
SENSOR_2_ADDR = 0x6B

CTRL1_XL = 0x10  # Accelerometer control
CTRL2_G  = 0x11  # Gyroscope control

# Register addresses
ACCEL_REGS = {'x': 0x28, 'y': 0x2A, 'z': 0x2C}
GYRO_REGS  = {'x': 0x22, 'y': 0x24, 'z': 0x26}

def init_sensor(addr):
    try:
        bus.write_byte_data(addr, CTRL1_XL, 0b01000000)
        bus.write_byte_data(addr, CTRL2_G,  0b01000000)
        return True
    except IOError:
        print(f"Error: Could not initialise sensor at address {hex(addr)}")
        return False

def read_word(addr, reg_low):
    try:
        low = bus.read_byte_data(addr, reg_low)
        high = bus.read_byte_data(addr, reg_low + 1)
        value = (high << 8) | low
        return value - 65536 if value > 32767 else value
    except IOError:
        return None

def read_axes(addr, regs):
    return {axis: read_word(addr, reg) for axis, reg in regs.items()}

# Initialise sensors
if not init_sensor(SENSOR_1_ADDR) or not init_sensor(SENSOR_2_ADDR):
    exit("One or both sensors failed to initialise.")

# Loop to read and print
def readout():
    while True:
            try:
            a1 = read_axes(SENSOR_1_ADDR, ACCEL_REGS)
            g1 = read_axes(SENSOR_1_ADDR, GYRO_REGS)
            a2 = read_axes(SENSOR_2_ADDR, ACCEL_REGS)
            g2 = read_axes(SENSOR_2_ADDR, GYRO_REGS)

            def fmt(label, val):
                return f"{label}:{val:>6}" if val is not None else f"{label}: ERR"

            output = " | ".join([
                fmt("A1x", a1['x']), fmt("A1y", a1['y']), fmt("A1z", a1['z']),
                fmt("G1x", g1['x']), fmt("G1y", g1['y']), fmt("G1z", g1['z']),
                fmt("A2x", a2['x']), fmt("A2y", a2['y']), fmt("A2z", a2['z']),
                fmt("G2x", g2['x']), fmt("G2y", g2['y']), fmt("G2z", g2['z']),
            ])

            print(output)
            time.sleep(1)
        except IOError:
            init_senor(addr)
            readout()



