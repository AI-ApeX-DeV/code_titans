# Import libraries
import bluetooth
import serial
import json

# Define constants
PORT = 1 # Bluetooth port number
BAUDRATE = 9600 # Serial baud rate
TIMEOUT = 10 # Serial timeout (in seconds)
DEVICE_NAME = "Fitness Tracker" # Bluetooth device name

# Find the Bluetooth address of the device
print("Searching for Bluetooth devices...")
devices = bluetooth.discover_devices(lookup_names=True)
for addr, name in devices:
    if name == DEVICE_NAME:
        print(f"Found device {name} with address {addr}")
        device_addr = addr
        break
else:
    print("No device found")
    exit()

# Create a serial port object to communicate with the device
print("Connecting to serial port...")
port = serial.Serial(f"COM{PORT}", baudrate=BAUDRATE, timeout=TIMEOUT)

# Loop until 'q' key is pressed
while True:
    # Send a command to the device to get sleep data
    print("Getting sleep data...")
    port.write(b"G")

    # Read the response from the device
    response = port.readline().decode()

    # Check if the response is valid JSON
    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        print("Invalid response")
        continue

    # Parse the JSON data to get the sleep stages and durations
    sleep_stages = data["sleep_stages"] # List of sleep stages (0: awake, 1: light, 2: deep, 3: REM)
    sleep_durations = data["sleep_durations"] # List of sleep durations (in minutes) for each stage
    total_sleep = sum(sleep_durations) # Total sleep duration (in minutes)

    # Print the sleep data
    print(f"Total sleep: {total_sleep} minutes")
    print(f"Awake: {sleep_durations[0]} minutes")
    print(f"Light: {sleep_durations[1]} minutes")
    print(f"Deep: {sleep_durations[2]} minutes")
    print(f"REM: {sleep_durations[3]} minutes")

    # Wait for a key press for 1 second
    key = input("Press 'q' to quit or any other key to continue: ")

    # Break the loop if 'q' key is pressed
    if key == 'q':
        break

# Close the serial port
port.close()
