"""Airthings API data handler."""

import logging
import time
from dataclasses import dataclass, field
from typing import List, Optional

from httpx import AsyncClient, TimeoutException

from airthings_api_client import Client, AuthenticatedClient
from airthings_api_client.api.accounts import get_accounts_ids
from airthings_api_client.api.device import get_devices
from airthings_api_client.api.sensor import get_multiple_sensors
from airthings_api_client.errors import UnexpectedStatus
from airthings_api_client.models import Error, AccountResponse
from airthings_api_client.models.device_response import DeviceResponse
from airthings_api_client.models.get_multiple_sensors_unit import GetMultipleSensorsUnit
from airthings_api_client.models.sensor_response_type_0 import SensorResponseType0
from airthings_api_client.models.sensors_response import SensorsResponse

AUTH_URL = "https://accounts-api.airthings.com/v1/token"
API_URL = "https://consumer-api.airthings.com"

logger = logging.getLogger(__name__)

@dataclass
class AirthingsSensor:
    """Representation of Airthings device sensor."""

    sensor_type: str
    value: int | float
    unit: str

    @classmethod
    def init_from_sensor_response(
        cls, sensor_response: SensorResponseType0
    ) -> "AirthingsSensor":
        """Create an AirthingsSensor from a SensorResponseType0"""
        return cls(
            sensor_type=sensor_response.sensor_type,
            value=sensor_response.value,
            unit=sensor_response.unit,
        )


@dataclass
class AirthingsDevice:
    """Representation of an Airthings device"""

    serial_number: str
    name: str
    home: str
    type: str
    recorded: Optional[str]
    sensors: list[AirthingsSensor] = field(default_factory=list)

    @classmethod
    def init_from_device_response(
        cls, device_response: DeviceResponse, sensors_response: SensorsResponse
    ) -> "AirthingsDevice":
        """Create an AirthingsDevice from a DeviceResponse and a SensorsResponse"""
        sensors = [
            AirthingsSensor.init_from_sensor_response(sensor)
            for sensor in sensors_response.sensors
        ]
        sensors.append(
            AirthingsSensor(
                sensor_type="battery",
                value=sensors_response.battery_percentage,
                unit="%",
            )
        )
        return cls(
            serial_number=device_response.serial_number,
            name=device_response.name,
            home=device_response.home,
            type=device_response.type,
            recorded=sensors_response.recorded,
            sensors=sensors,
        )


class AirthingsToken:
    """Representation of an Airthings API token."""

    value: Optional[str]
    _expires: Optional[int]

    def __init__(self):
        self.value = None
        self._expires = None

    def set_token(self, access_token: str, expires_in: int):
        """Set the token and its expiration time."""
        self.value = access_token
        self._expires = expires_in + int(time.time())

    def is_valid(self) -> bool:
        """Check if the token is valid."""
        return self.value and self._expires and self._expires > (int(time.time()) + 20)

    def as_header(self) -> dict[str, str]:
        """Return the token as a header."""
        return {"Authorization": f"Bearer {self.value}"}


class Airthings:
    """Representation of Airthings API data handler."""

    _access_token: Optional[str] = None
    _client_id: str
    _client_secret: str
    _unit: GetMultipleSensorsUnit
    _access_token: AirthingsToken
    devices: List[AirthingsDevice]

    _authApiClient: Client
    _apiClient: AuthenticatedClient

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        is_metric: bool,
        websession: Optional[AsyncClient] = None,
    ) -> "Airthings":
        """Init Airthings data handler."""
        self._client_id = client_id
        self._client_secret = client_secret
        self._unit = (
            GetMultipleSensorsUnit.METRIC
            if is_metric
            else GetMultipleSensorsUnit.IMPERIAL
        )
        self._access_token = AirthingsToken()
        self._devices = {}

        self._authClient = Client(base_url="https://accounts-api.airthings.com")
        self._apiClient = AuthenticatedClient(
            base_url=API_URL, token="invalid_token"  # Should authenticate before using
        )
        if websession:
            self._authClient.set_async_httpx_client(websession)
            self._apiClient.set_async_httpx_client(websession)

    def _verify_auth(self):
        """Authenticate to Airthings API and set the access token and updates internal api clients."""

        if self._access_token.is_valid():
            return

        auth_response = self._authClient.get_httpx_client().request(
            url=AUTH_URL,
            method="POST",
            data={
                "grant_type": "client_credentials",
                "client_id": self._client_id,
                "client_secret": self._client_secret,
            },
        )

        if access_token := auth_response.json().get("access_token"):
            self._access_token.set_token(
                access_token=access_token,
                expires_in=int(auth_response.json()["expires_in"]),
            )
            print(self._access_token.value)
            self._apiClient.token = self._access_token.value
        else:
            raise ValueError("No access token found")

    def update_devices(self) -> Optional[dict[str, AirthingsDevice]]:
        """Update devices and sensors from Airthings API. Return a dict of devices."""
        self._verify_auth()

        accounts = self.fetch_all_accounts()

        if not accounts:
            logging.error("No accounts found")
            return None

        res = {}
        logging.info("Accounts found: %s", len(accounts))
        for account in accounts:
            logging.info("Account: %s", account)

            devices = self.fetch_all_devices(account_id=account.id)

            logging.info("%s devices found in account %s", len(devices), account.id)
            logging.info("Devices: %s", devices)

            sensors = self.fetch_all_device_sensors(
                account_id=account.id, unit=self._unit
            )
            if not sensors:
                logging.error("No sensors found in account %s", account.id)
                break
            logging.info("%s sensors found in account %s", len(sensors), account.id)
            logging.info("Sensors: %s,", sensors)
            logging.info("Pages: %s", sensors)

            for device in devices:
                for sensor in sensors:
                    if device.serial_number == sensor.serial_number:
                        res[device.serial_number] = (
                            AirthingsDevice.init_from_device_response(device, sensor)
                        )

        logger.info("Mapped devices: %s", res)
        return res

    def fetch_all_accounts(self) -> List[AccountResponse]:
        """Fetch accounts for the given client"""
        try:
            accounts_response = get_accounts_ids.sync_detailed(client=self._apiClient)
            if accounts := accounts_response.parsed:
                return accounts.accounts
            return []
        except UnexpectedStatus as e:
            logging.error("Unexpected status while fetching accounts: %s", e)
            return []
        except TimeoutException as e:
            logging.error("Timeout while fetching accounts: %s", e)
            return []
        except Exception as e:  # pylint: disable=broad-except
            logging.error("Error while fetching accounts: %s", e)
            return []

    def fetch_all_devices(self, account_id: str) -> List[DeviceResponse]:
        """Fetch devices for a given account"""
        try:
            sensors_response = get_devices.sync_detailed(
                account_id=account_id,
                client=self._apiClient,
            )
            logger.info("Device headers: %s", sensors_response.headers)
            return sensors_response.parsed.devices
        except UnexpectedStatus as e:
            logging.error("Unexpected status while fetching devices: %s", e)
            return []
        except TimeoutException as e:
            logging.error("Timeout while fetching devices: %s", e)
            return []

    def fetch_all_device_sensors(
        self,
        account_id: str,
        page_number: int = 1,
        unit: Optional[GetMultipleSensorsUnit] = None,
    ) -> List[SensorsResponse]:
        """Fetch sensors for a given account"""
        try:
            sensors_response = get_multiple_sensors.sync_detailed(
                account_id=account_id,
                client=self._apiClient,
                page_number=page_number,
                unit=unit,
            ).parsed

            if sensors_response is Error or sensors_response is None:
                return []

            device_sensors = sensors_response.results

            if sensors_response.has_next is False:
                return device_sensors

            return device_sensors + self.fetch_all_device_sensors(
                account_id=account_id,
                page_number=page_number + 1,
                unit=unit,
            )
        except UnexpectedStatus as e:
            logging.error("Unexpected status while fetching sensors: %s", e)
            return []
        except TimeoutException as e:
            logging.error("Timeout while fetching sensors: %s", e)
            return []
