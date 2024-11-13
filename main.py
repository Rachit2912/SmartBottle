#1. taking input from sensor : 
import serial
import time
import pandas as pd 
# Replace 'COM3' with your Arduino's port name (e.g., 'COM3' for Windows or '/dev/ttyACM0' for Linux/Mac)
arduino_port = 'COM5'
baud_rate = 9600  # Must match the Arduino baud rate

try:
    # Initialize serial connection
    ser = serial.Serial(arduino_port, baud_rate)
    time.sleep(2)  # Wait for the connection to initialize

    print("Reading water level data from Arduino...")
    while True:
        # Read the water level data
        if ser.in_waiting > 0:
            water_level = ser.readline().decode('utf-8').strip()
            print(f"Water Level: {water_level}")

except serial.SerialException:
    print("Error: Could not open the serial port. Check the port name and connection.")
except KeyboardInterrupt:
    print("\nExiting program.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()


#2. store the data : 






# data visualization : 

