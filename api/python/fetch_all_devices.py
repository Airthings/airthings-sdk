import logging
import sys
import time
from dataclasses import dataclass, field
from typing import List, Optional

import coloredlogs
from httpx import AsyncClient, Response, TimeoutException, request

from airthings_for_consumer_api_client import AuthenticatedClient
from airthings_for_consumer_api_client.api.accounts import get_accounts_ids
from airthings_for_consumer_api_client.api.device import get_devices
from airthings_for_consumer_api_client.api.sensor import get_multiple_sensors
from airthings_for_consumer_api_client.client import Client
from airthings_for_consumer_api_client.errors import UnexpectedStatus
from airthings_for_consumer_api_client.models.device_response import DeviceResponse
from airthings_for_consumer_api_client.models.get_multiple_sensors_unit import GetMultipleSensorsUnit
from airthings_for_consumer_api_client.models.sensor_response_type_0 import SensorResponseType0
from airthings_for_consumer_api_client.models.sensors_response import SensorsResponse
from const import AUTH_URL

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG")


class RateLimitError(Exception):
    """Rate limit exceeded"""

    def __init__(self, status_code: int, content: bytes):
        self.status_code = status_code
        self.content = content

        super().__init__(f"Rate limit exceeded: {status_code} {content}")


class User:
    def __init__(
        self,
        domain: str,
        sn: str,
        client_id: str,
        client_secret: str,
        unit: GetMultipleSensorsUnit = GetMultipleSensorsUnit.METRIC,
    ):
        self.domain = domain
        self.sn = sn
        self.client_id = client_id
        self.client_secret = client_secret
        self.unit = unit

        self.access_token: Optional[str] = None
        self.expires: Optional[int] = None

    def __str__(self):
        return f"User(user_group={self.user_group})"

    def authenticate(self):
        try:
            auth_response: Response = request(
                method="POST",
                url=AUTH_URL,
                data={
                    "grant_type": "client_credentials",
                    "client_id": user.client_id,
                    "client_secret": user.client_secret,
                },
            )
            if access_token := auth_response.json()["access_token"]:
                self.access_token = access_token
            else:
                raise ValueError("No access token found")

            if expires := auth_response.json()["expires_in"]:
                self.expires = int(time.time()) + expires
            else:
                raise ValueError("No expires_in found")

            logger.info("Authenticated: %s", self.access_token)

        except Exception as e:
            logging.error("Error while authenticating: %s", e)
            return None


@dataclass
class Sensor:
    sensor_type: str
    value: int | float
    unit: str

    @classmethod
    def init_from_sensor_response(cls, sensor_response: SensorResponseType0) -> "Sensor":
        return cls(
            sensor_type=sensor_response.sensor_type,
            value=sensor_response.value,
            unit=sensor_response.unit,
        )


@dataclass
class Device:
    serial_number: str
    name: str
    home: str
    type: str
    recorded: Optional[str]
    battery_level: Optional[int] = None
    sensors: list[Sensor] = field(default_factory=list)

    @classmethod
    def init_from_device_response(
        cls,
        device_response: DeviceResponse,
        sensors_response: SensorsResponse
    ) -> "Device":
        return cls(
            serial_number=device_response.serial_number,
            name=device_response.name,
            home=device_response.home,
            type=device_response.type,
            recorded=sensors_response.recorded,
            battery_level=sensors_response.battery_percentage,
            sensors=[Sensor.init_from_sensor_response(sensor) for sensor in sensors_response.sensors],
        )


class Airthings:
    _access_token: Optional[str] = None
    _client_id: str
    _client_secret: str
    _websession: AsyncClient
    devices: List[Device]

    def __init__(self, client_id, client_secret, websession):
        """Init Airthings data handler."""
        self._client_id = client_id
        self._client_secret = client_secret
        self._websession = websession
        self._access_token = None
        self._devices = {}

    def fetch_data(self):
        user = User(
            domain="https://accounts-api.airthings.com",
            sn="sn",
            client_id=self._client_id,
            client_secret=self._client_secret,
        )

        try:
            user.authenticate()
        except Exception as e:
            logging.error("Error while authenticating: %s", e)
            exit(1)

        with AuthenticatedClient(
            base_url=user.domain,
            timeout=10,
            verify_ssl=False,
            token=user.access_token,
        ) as client:
            client.set_httpx_client(AsyncClient())
            logging.debug("Client setup complete")

            if accounts := self.fetch_accounts():
                logging.info("Accounts found: %s", len(accounts.accounts))
                for account in accounts.accounts:
                    logging.info("Account: %s", account)

                    if devices := self.fetch_devices(account_id=account.id):
                        logging.info(
                            "%s devices found in account %s",
                            len(devices.devices), account.id
                        )
                        logging.info("Devices: %s", devices)

                    while True:
                        all_sensors: List[SensorsResponse] = []
                        if sensors := self.fetch_sensors(
                            account_id=account.id, unit=user.unit
                        ):
                            logging.info(
                                "%s sensors found in account %s",
                                len(sensors.results), account.id
                            )
                            logging.info("Sensors: %s,", sensors.results)
                            all_sensors.extend(sensors.results)
                            logging.info("Pages: %s", sensors.total_pages)
                            if not sensors.has_next:
                                break

                    mapped_devices: List[DeviceResponse] = []

                    # Add devices and sensors
                    for device in devices.devices:
                        for sensor in sensors.results:
                            if device.serial_number == sensor.serial_number:
                                mapped_devices.append(
                                    Device.init_from_device_response(device, sensor)
                                )

                    logger.info("Mapped devices: %s", mapped_devices)

    def fetch_accounts():
        try:
            accounts_response = get_accounts_ids.sync_detailed(
                client=client,
            )
            if accounts := accounts_response.parsed:
                return accounts
            return None
        except UnexpectedStatus as e:
            logging.error("Unexpected status while fetching accounts: %s", e)
            return None
        except TimeoutException as e:
            logging.error("Timeout while fetching accounts: %s", e)
            return None

    def fetch_devices(account_id: str) -> Optional[List[DeviceResponse]]:
        try:
            sensors_response = get_devices.sync_detailed(
                account_id=account_id,
                client=client,
            )
            logger.info("Device headers: %s", sensors_response.headers)
            if sensors := sensors_response.parsed:
                return sensors
            return None
        except UnexpectedStatus as e:
            logging.error("Unexpected status while fetching devices: %s", e)
            return None
        except TimeoutException as e:
            logging.error("Timeout while fetching devices: %s", e)
            return None

    def fetch_sensors(
        self,
        account_id: str,
        page_number: int = 1,
        unit: Optional[GetMultipleSensorsUnit] = None,
    ) -> Optional[List[SensorsResponse]]:
        try:
            sensors_response = get_multiple_sensors.sync_detailed(
                account_id=account_id,
                client=client,
                page_number=page_number,
                unit=unit,
            )

            sensors_response.parsed.results

            if sensors := sensors_response.parsed:
                if sensors.has_next:
                    return self.fetch_sensors(
                        account_id=account_id,
                        page_number=page_number + 1,
                        unit=unit
                    )
                return sensors
            return None
        except UnexpectedStatus as e:
            logging.error("Unexpected status while fetching sensors: %s", e)
            return None
        except TimeoutException as e:
            logging.error("Timeout while fetching sensors: %s", e)
            return None


if __name__ == "__main__":
    Airthings(
        client_id="client_id",
        client_secret="client_secret",
        websession=AsyncClient(),
    ).fetch_data()
