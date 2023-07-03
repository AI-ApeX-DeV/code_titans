# a function to retrieve and print the heart rate taken from a watch connected through blutooth to my computer


import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService
# from adafruit_ble.services.standard.heart_rate import HeartRateService
from adafruit_ble.services.standard import BatteryService
# from adafruit_ble.services.standard import ScanResponse
from adafruit_ble.uuid import VendorUUID
from adafruit_ble.services import Service
from adafruit_ble.characteristics import Characteristic
from adafruit_ble.characteristics import ComplexCharacteristic

# The heart rate service UUID


SERVICE_UUID = VendorUUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
# The characteristic UUID to read the heart rate from
CHARACTERISTIC_UUID = VendorUUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")


class BleDevice:
    def __init__(self):
        self._ble = BLERadio()
        self._connection = None

    def connect(self, device_address):
        # Scan for advertising devices
        for adv in self._ble.start_scan(ProvideServicesAdvertisement):
            # Check if the device name matches the given name
            if adv.complete_name == device_address:
                # Stop scanning
                self._ble.stop_scan()
                # Connect to the GATT server of the device
                self._connection = self._ble.connect(adv)
                # Get the GATT service and characteristic of the heart rate monitor
                return self._connection

    def find_service(self, uuid):
        for service in self._connection:
            if service.uuid == uuid:
                return service

    def find_characteristic(self, uuid):
        for service in self._connection:
            for characteristic in service:
                if characteristic.uuid == uuid:
                    return characteristic


def heart_rate():
    # Create a BLE device with the ble_device library
    ble_device = BleDevice()

    # Connect to the GATT server of the watch
    ble_device.connect("B4:5A:67:6E:6C:3B")

    # Get the GATT service and characteristic of the heart rate monitor
    service = ble_device.find_service(SERVICE_UUID)
    characteristic = service.find_characteristic(CHARACTERISTIC_UUID)

    # Read the characteristic value (heart rate) repeatedly
    while True:
        value = characteristic.read_value()
        print(value)
        time.sleep(1)


if __name__ == "__main__":
    heart_rate()
