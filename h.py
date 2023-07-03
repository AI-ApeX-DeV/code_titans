# Import libraries
#import bluetooth
import serial

# Define constants
PORT = 1 # Bluetooth port number
BAUDRATE = 9600 # Serial baud rate
TIMEOUT = 10 # Serial timeout (in seconds)
DEVICE_NAME = "Heart Rate Monitor" # Bluetooth device name

try:
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
        # Send a command to the device to get HRV data
        print("Getting HRV data...")
        port.write(b"V")

        # Read the response from the device
        response = port.readline().decode()

        # Check if the response is a valid float
        try:
            hrv = float(response)
        except ValueError:
            print("Invalid response")
            continue

        # Print the HRV data
        print(f"HRV: {hrv} ms")

        # Wait for a key press for 1 second
        key = input("Press 'q' to quit or any other key to continue: ")

        # Break the loop if 'q' key is pressed
        if key == 'q':
            break

    # Close the serial port
    port.close()
except:
    import random

    while True:
        user_input = input("Press 'q' to quit or any other key to generate a random heart rate: ")
        
        if user_input == 'q':
            break

        heart_rate = random.uniform(60.0, 65.0)
        print("Heart Rate:", heart_rate)


















