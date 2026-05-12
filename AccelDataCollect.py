import time
import csv
from smbus2 import SMBus

# Constants
ACC_ADDRESS = 0x68
LOG_FILE = '/mnt/sdcard/accel_log.csv'  # Change path if needed

# Initialize accelerometer (wake it up)
def initialize_accelerometer():
    bus = SMBus(1)
    bus.write_byte_data(ACC_ADDRESS, 0x6B, 0)  # Wake up device
    return bus

# Read acceleration (16-bit signed values)
def read_acceleration(bus):
    def read_word(register):
        high = bus.read_byte_data(ACC_ADDRESS, register)
        low = bus.read_byte_data(ACC_ADDRESS, register + 1)
        value = (high << 8) | low
        return value - 65536 if value >= 0x8000 else value

    try:
        x = read_word(0x3B)
        y = read_word(0x3D)
        z = read_word(0x3F)
        return (x, y, z)
    except:
        return (None, None, None)

# Main loop
try:
    bus = initialize_accelerometer()
    print("Accelerometer initialized. Logging to file...")

    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Accel_X', 'Accel_Y', 'Accel_Z'])

        while True:
            x, y, z = read_acceleration(bus)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            writer.writerow([timestamp, x, y, z])
            file.flush()
            print(f"[{timestamp}] X={x}, Y={y}, Z={z}")
            time.sleep(0.25)

except KeyboardInterrupt:
    print("\nLogging stopped by user.")
finally:
    try:
        bus.close()
    except:
        pass
