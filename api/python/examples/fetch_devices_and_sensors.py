import sys
from airthings_sdk import Airthings

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print("Please add client id and client secret as parameters.")
        print("Usage:")
        print("python fetch_devices_and_sensors.py <client_id> <client_secret>")
        exit(1)
    client_id = sys.argv[1]
    client_secret = sys.argv[2]

    airthings = Airthings(
        client_id=client_id,
        client_secret=client_secret,
        is_metric=True,
    )

    devices = airthings.update_devices()
    print(devices)
