[![Airthings][logo]](https://www.airthings.com)

# Airthings API SDK for Python

API SDK for Airthings consumer products.

## Getting Started

Prerequisites:

- [Python](https://www.python.org/downloads/) with version 3.11 that is required by Home Assistant ([docs](https://developers.home-assistant.io/docs/development_environment?_highlight=python&_highlight=versi#manual-environment) or [reference](https://github.com/home-assistant/architecture/blob/master/adr/0002-minimum-supported-python-version.md))
- [Poetry](https://python-poetry.org/docs/#installation)

Then run following steps:

```shell
poetry install # Install dependencies
./generate_client.sh # Generate REST API client code
python3 examples//fetch_devices_and_sensors.py CLIENT_ID CLIENT_SECRET # Run example to make sure all works
```


[logo]: https://upload.wikimedia.org/wikipedia/commons/d/d1/Airthings_logo.svg