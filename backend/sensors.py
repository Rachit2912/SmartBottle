import serial
import time
import pandas as pd
import math

# Replace 'COM3' with your Arduino's port name (e.g., 'COM3' for Windows or '/dev/ttyACM0' for Linux/Mac)
arduino_port = 'COM5'
baud_rate = 9600  # Must match the Arduino baud rate

# Radius of the water bottle in centimeters
bottle_radius = 3.5  # Adjust according to your bottle's radius

# CSV file to store the data
data_file = 'water_level_data.csv'

def calculate_volume(height_cm, radius_cm):
    """Calculate volume based on height and radius."""
    return math.pi * (radius_cm ** 2) * height_cm

try:
    # Initialize serial connection
    ser = serial.Serial(arduino_port, baud_rate)
    time.sleep(2)  # Wait for the connection to initialize

    # Check if CSV file exists; if not, create it with headers
    try:
        pd.read_csv(data_file)
    except FileNotFoundError:
        pd.DataFrame(columns=['Timestamp', 'Height_cm', 'Volume_ml']).to_csv(data_file, index=False)

    print("Reading water level data from Arduino...")
    while True:
        # Read the water level data
        if ser.in_waiting > 0:
            height = ser.readline().decode('utf-8').strip()
            try:
                height = float(height)  # Convert height to a float
                volume_ml = calculate_volume(height, bottle_radius) * 10  # Convert to mL (1 cm^3 = 1 mL)

                # Log the data
                print(f"Water Level: {height} cm, Volume: {volume_ml:.2f} mL")

                # Append data to CSV
                new_data = pd.DataFrame({
                    'Timestamp': [time.strftime('%Y-%m-%d %H:%M:%S')],
                    'Height_cm': [height],
                    'Volume_ml': [volume_ml]
                })
                new_data.to_csv(data_file, mode='a', header=False, index=False)

            except ValueError:
                print("Invalid data received, skipping this reading.")

except serial.SerialException:
    print("Error: Could not open the serial port. Check the port name and connection.")
except KeyboardInterrupt:
    print("\nExiting program.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
