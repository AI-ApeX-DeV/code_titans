# Import libraries
import bluetooth
import serial

# Define constants
PORT = 1 # Bluetooth port number
BAUDRATE = 9600 # Serial baud rate
TIMEOUT = 10 # Serial timeout (in seconds)
DEVICE_NAME = "Blood Pressure Cuff" # Bluetooth device name

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
    # Send a command to the device to start measurement
    print("Starting measurement...")
    port.write(b"S")

    # Read the response from the device
    response = port.readline().decode()

    # Check if the response is valid
    if response.startswith("BP:"):
        # Parse the response to get the systolic and diastolic blood pressure values
        systolic, diastolic = map(int, response[3:].split("/"))
        print(f"Systolic: {systolic} mmHg, Diastolic: {diastolic} mmHg")
    else:
        print("Invalid response")

    # Wait for a key press for 1 second
    key = input("Press 'q' to quit or any other key to continue: ")

    # Break the loop if 'q' key is pressed
    if key == 'q':
        break

# Close the serial port
port.close()
