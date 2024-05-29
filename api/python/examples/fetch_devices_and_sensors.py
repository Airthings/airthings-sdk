"""Example of fetching devices and sensors from Airthings API."""

import asyncio
import sys

from airthings_sdk import Airthings


async def main():
    if len(sys.argv) <= 2:
        print("Please add client id and client secret as parameters.")
        print("Usage:")
        print("python fetch_devices_and_sensors.py <client_id> <client_secret>")
        sys.exit(1)
    client_id = sys.argv[1]
    client_secret = sys.argv[2]

    airthings = Airthings(
        client_id=client_id,
        client_secret=client_secret,
        is_metric=True
    )

    devices = await airthings.update_devices()
    print(devices)

if __name__ == "__main__":
    asyncio.run(main())