import OPi.GPIO as GPIO
import time
from smbus2 import SMBus
import csv

# Pin configurations
sensor1Pin = 7 
sensor2Pin = 16  
accmeterAddress = 0x68  # I2C address for accelerometer

# Initializes GPIO which is used for the CO2 sensors
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor1Pin, GPIO.IN)
GPIO.setup(sensor2Pin, GPIO.IN)

# Initializes accelerometer which uses SMBus
def initializeAccmeter():
    bus = SMBus(1)
    bus.write_byte_data(accmeterAddress, 0x6B, 0)  # Wake up the sensor
    return bus

# Reads acceleration
def readAcceleration(bus):
    try:
        accel_x = bus.read_byte_data(accmeterAddress, 0x3B) << 8 | bus.read_byte_data(accmeterAddress, 0x3C)
        accel_y = bus.read_byte_data(accmeterAddress, 0x3D) << 8 | bus.read_byte_data(accmeterAddress, 0x3E)
        accel_z = bus.read_byte_data(accmeterAddress, 0x3F) << 8 | bus.read_byte_data(accmeterAddress, 0x40)
        return accel_x, accel_y, accel_z
    except IOError as e:
        print("I2C communication error while reading acceleration data:", e)
        return [0, 0, 0]  # Default values in case of an error

# Reads CO2 concentration using PWM
def readCo2Concentration(sensorPin):
    try:
        GPIO.wait_for_edge(sensorPin, GPIO.RISING, timeout=5000)  # Timeout set to 5000 ms (5 seconds)
        startTime = time.time()

        GPIO.wait_for_edge(sensorPin, GPIO.FALLING, timeout=5000)
        highDuration = time.time() - startTime  # Duration of high pulse

        cycleDuration = 0.001 # 1ms cycle duration from sensor documentation
        
        # Convert high duration to CO2 concentration based on the datasheet
        co2Concentration = (highDuration / cycleDuration) * 2000
        return co2Concentration
    except RuntimeError:
        print(f"Timeout occurred while waiting for PWM signal on pin {sensorPin}")
        return None

# Logs data to SD card
def log_data_to_sd(timestamp, co2_level_sensor1, co2_level_sensor2):
    with open('/mnt/sdcard/data_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, co2_level_sensor1, co2_level_sensor2])
        file.flush()  # Ensure data is written immediately

# Main function
def main():
    # Initialize components
    bus = initializeAccmeter()

    print("System initialized. Waiting for launch...")

    try:
        co2_level_sensor1 = None
        co2_level_sensor2 = None

        while True: # Loop waiting for launch
            accelData = readAcceleration(bus) # Read acceleration data

            if max(accelData) > 16000:  # Launch threshold based on accelerometer sensitivity
                print("Launch detected. Starting data collection...")

                sensor1NextRead = time.time()
                sensor2NextRead = time.time() + 15
                break

            time.sleep(0.1)

        # Data collection loop
        while True:
            currentTime = time.time()

            # Read from sensor 1 every 30 seconds
            if currentTime >= sensor1NextRead:
                co2_level_sensor1 = readCo2Concentration(sensor1Pin)
                sensor1NextRead = currentTime + 30

            # Read from sensor 2 every 30 seconds
            if currentTime >= sensor2NextRead:
                co2_level_sensor2 = readCo2Concentration(sensor2Pin)
                sensor2NextRead = currentTime + 30

            # Log data only when both sensors have data
            if co2_level_sensor1 is not None and co2_level_sensor2 is not None:
                timestamp = time.time()
                log_data_to_sd(timestamp, co2_level_sensor1, co2_level_sensor2)

                print(f"Logged data: Time={timestamp}, Sensor1_CO2={co2_level_sensor1}, Sensor2_CO2={co2_level_sensor2}")

                # Reset the sensor data after logging
                co2_level_sensor1 = None
                co2_level_sensor2 = None

            time.sleep(0.1) # Short delay to avoid busy-waiting

    except KeyboardInterrupt:
        print("Finished collecting data.")

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()