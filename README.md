# Payload Data Logger

Python-based airborne data logging system developed for the Georgia Tech High Altitude Balloon Payload Challenge.

This project was designed for integration with an Orange Pi Zero 2W, onboard accelerometer, and CO₂ sensors to support autonomous data collection during flight operations.

## Features

- Accelerometer-based launch detection
- Real-time CO₂ sensor data collection
- Pressure compensation for atmospheric variation
- Integrated sensor management and logging pipeline
- SD card CSV data logging
- I2C and GPIO-based hardware communication

## Hardware Used

- Orange Pi Zero 2W
- MPU6050 accelerometer
- CO₂ sensors (PWM output)
- SD card storage module

## Included Scripts

### `FINALPayload.py`
Main integrated payload program responsible for:
- Launch detection using accelerometer thresholds
- Reading CO₂ sensor values
- Coordinating sensor timing
- Logging flight data to SD card

### `AccelDataCollect.py`
Standalone accelerometer testing and logging utility used during sensor integration and debugging.

### `PressureCompensation.py`
Post-processing utility that aligns pressure and CO₂ data and applies atmospheric pressure compensation to improve measurement accuracy.

## Technologies

- Python
- Linux
- I2C communication
- GPIO/PWM signal processing
- CSV data logging
- Sensor integration
