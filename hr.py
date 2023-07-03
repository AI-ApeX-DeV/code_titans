import pygatt
from pygatt.exceptions import BLEError

# Define constants
DEVICE_NAME = "Heart Rate Monitor" # Bluetooth device name

# Create a Bluetooth adapter
adapter = pygatt.GATTToolBackend()

try:
    # Start the Bluetooth adapter
    adapter.start()

    # Scan for Bluetooth devices
    print("Searching for Bluetooth devices...")
    devices = adapter.scan(timeout=10)

    # Find the Bluetooth device by name
    device = next((d for d in devices if d["name"] == DEVICE_NAME), None)
    if device is None:
        print("No device found")
        exit()

    # Connect to the Bluetooth device
    print(f"Connecting to device {device['name']} with address {device['address']}...")
    device_conn = adapter.connect(device['address'])

    # Discover services and characteristics
    device_conn.discover()

    # Get HRV data from a specific characteristic
    hrv_characteristic = device_conn.char_read("00002a37-0000-1000-8000-00805f9b34fb")

    # Convert the data to a float
    hrv = float.from_bytes(hrv_characteristic, byteorder='little')

    # Print the HRV data
    print(f"HRV: {hrv} ms")

finally:
    # Stop the Bluetooth adapter
    adapter.stop()
