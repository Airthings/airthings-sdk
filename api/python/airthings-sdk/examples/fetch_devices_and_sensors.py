"""Example of fetching devices and sensors from Airthings API."""

import asyncio
import logging
import sys

from airthings_sdk import Airthings

logging.basicConfig(level=logging.INFO)


async def main():
    """Run the example and print devices with their sensors."""
    if len(sys.argv) <= 2:
        logging.error("Please add client id and client secret as parameters.")
        logging.info("Usage:")
        logging.info("python fetch_devices_and_sensors.py <client_id> <client_secret>")
        sys.exit(1)
    client_id = sys.argv[1]
    client_secret = sys.argv[2]

    airthings = Airthings(
        client_id=client_id,
        client_secret=client_secret,
        is_metric=True,
    )

    devices = await airthings.update_data()
    for device in devices.values():
        print(f"Device: {device.name} ({device.serial_number}), {device.type.name}")
        print("  Sensors:")
        if not device.sensors:
            print("    No sensors available.")
            continue
        for sensor in device.sensors:
            print(f"    {sensor.sensor_type}: {sensor.value} {sensor.unit}")
        print()


if __name__ == "__main__":
    asyncio.run(main())
