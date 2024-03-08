"""Module providing an Airthings API SDK."""

import logging
import time
from dataclasses import dataclass, field
from typing import List, Optional, cast

from httpx import AsyncClient, TimeoutException

from airthings_api_client import Client, AuthenticatedClient
from airthings_api_client.api.accounts import get_accounts_ids
from airthings_api_client.api.device import get_devices
from airthings_api_client.api.sensor import get_multiple_sensors
from airthings_api_client.errors import UnexpectedStatus
from airthings_api_client.models import Error, SensorResponseType0
from airthings_api_client.models.device_response import DeviceResponse
from airthings_api_client.models.get_multiple_sensors_unit import GetMultipleSensorsUnit
from airthings_api_client.models.sensors_response import SensorsResponse
from airthings_api_client.types import Unset, UNSET

AUTH_URL = "https://accounts-api.airthings.com"
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
        cls, sensor_response: SensorResponseType0 | None | Unset
    ):
        """Create an AirthingsSensor from a SensorResponseType0"""

        if sensor_response is None or isinstance(sensor_response, Unset):
            return None

        return cls(
            sensor_type=cast(str, sensor_response.sensor_type),
            value=cast(float | int, sensor_response.value),
            unit=cast(str, sensor_response.unit),
        )


@dataclass
class AirthingsDevice:
    """Representation of an Airthings device"""

    serial_number: str
    type: str
    name: str
    home: Optional[str]
    recorded: Optional[str]
    sensors: list[AirthingsSensor] = field(default_factory=list)

    @classmethod
    def init_from_device_response(
        cls, device_response: DeviceResponse, sensors_response: SensorsResponse
    ) -> "AirthingsDevice":
        """Create an AirthingsDevice from a DeviceResponse and a SensorsResponse"""

        mapped = map(
            AirthingsSensor.init_from_sensor_response, sensors_response.sensors or []
        )
        filtered = list(filter(lambda sensor: sensor is not None, mapped))

        if sensors_response.battery_percentage is not None:
            filtered.append(
                AirthingsSensor(
                    sensor_type="battery",
                    value=cast(int, sensors_response.battery_percentage),
                    unit="%",
                )
            )
        return cls(
            serial_number=cast(str, device_response.serial_number),
            name=cast(str, device_response.name),
            type=cast(str, device_response.type),
            home=cast(str | None, device_response.home),
            recorded=cast(str | None, sensors_response.recorded),
            sensors=filtered,
        )


class AirthingsToken:
    """Representation of an Airthings API token."""

    value: Optional[str] = None
    _expires: Optional[int] = None

    def set_token(self, access_token: str, expires_in: int):
        """Set the token and its expiration time."""
        self.value = access_token
        self._expires = expires_in + int(time.time())

    def is_valid(self) -> bool:
        """Check if the token is valid."""
        return (
            self.value is not None
            and self._expires is not None
            and self._expires > (int(time.time()) + 20)
        )

    def as_header(self) -> dict[str, str]:
        """Return the token as a header."""
        return {"Authorization": f"Bearer {self.value}"}


class Airthings:
    """Representation of Airthings API data handler."""

    _client_id: str
    _client_secret: str
    _unit: GetMultipleSensorsUnit
    _access_token: AirthingsToken
    devices: List[AirthingsDevice]

    _auth_api_client: Client
    _api_client: AuthenticatedClient

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        is_metric: bool,
        websession: Optional[AsyncClient] = None,
    ):
        """Init Airthings data handler."""
        self._client_id = client_id
        self._client_secret = client_secret
        self._unit = (
            GetMultipleSensorsUnit.METRIC
            if is_metric
            else GetMultipleSensorsUnit.IMPERIAL
        )
        self._access_token = AirthingsToken()
        self._devices: dict[str, AirthingsDevice] = {}

        self._auth_api_client = Client(base_url=AUTH_URL)
        self._api_client = AuthenticatedClient(
            base_url=API_URL, token="invalid_token"  # Should authenticate before using
        )
        if websession:
            self._auth_api_client.set_async_httpx_client(websession)
            self._api_client.set_async_httpx_client(websession)

    def verify_auth(self):
        """Make sure the access token is valid. If not, fetch a new one."""

        if self._access_token.is_valid():
            return

        auth_response = self._auth_api_client.get_httpx_client().request(
            url=AUTH_URL + "/v1/token",
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
            self._api_client.token = self._access_token.value
        else:
            raise ValueError("No access token found")

    def update_devices(self) -> dict[str, AirthingsDevice]:
        """Update devices and sensors from Airthings API. Return a dict of devices."""
        self.verify_auth()

        account_ids = self._fetch_all_accounts_ids()

        res = {}
        logging.info("Accounts found: %s", len(account_ids))
        for account_id in account_ids:
            logging.info("Account: %s", account_id)

            devices = self._fetch_all_devices(account_id=account_id)

            logging.info("%s devices found in account %s", len(devices), account_id)
            logging.info("Devices: %s", devices)

            sensors = self._fetch_all_device_sensors(
                account_id=account_id, unit=self._unit
            )
            if not sensors:
                logging.error("No sensors found in account %s", account_id)
                break
            logging.info("%s sensors found in account %s", len(sensors), account_id)
            logging.info("Sensors: %s,", sensors)
            logging.info("Pages: %s", sensors)

            for device in devices:
                for sensor in sensors:
                    if device.serial_number != sensor.serial_number:
                        continue
                    res[cast(str, device.serial_number)] = (
                        AirthingsDevice.init_from_device_response(device, sensor)
                    )

        logger.info("Mapped devices: %s", res)
        return res

    def _fetch_all_accounts_ids(self) -> List[str]:
        """Fetch accounts for the given client"""
        try:
            response = get_accounts_ids.sync_detailed(client=self._api_client).parsed

            if response is None:
                return []
            return [
                account.id
                for account in (response.accounts or [])
                if isinstance(account.id, str)
            ]
        except UnexpectedStatus as e:
            logging.error("Unexpected status while fetching accounts: %s", e)
            return []
        except TimeoutException as e:
            logging.error("Timeout while fetching accounts: %s", e)
            return []
        except Exception as e:  # pylint: disable=broad-except
            logging.error("Error while fetching accounts: %s", e)
            return []

    def _fetch_all_devices(self, account_id: str) -> List[DeviceResponse]:
        """Fetch devices for a given account"""
        try:
            sensors_response = get_devices.sync_detailed(
                account_id=account_id, client=self._api_client
            ).parsed

            if sensors_response is None or isinstance(sensors_response, Unset):
                return []

            return sensors_response.devices or []
        except UnexpectedStatus as e:
            logging.error("Unexpected status while fetching devices: %s", e)
            return []
        except TimeoutException as e:
            logging.error("Timeout while fetching devices: %s", e)
            return []

    def _fetch_all_device_sensors(
        self,
        account_id: str,
        page_number: int = 1,
        unit: Optional[GetMultipleSensorsUnit] = None,
    ) -> List[SensorsResponse]:
        """Fetch sensors for a given account"""
        try:
            sensors_response = get_multiple_sensors.sync_detailed(
                account_id=account_id,
                client=self._api_client,
                page_number=page_number,
                unit=unit or UNSET,
            ).parsed

            if sensors_response is None or isinstance(sensors_response, Error):
                return []

            device_sensors = sensors_response.results or []

            if sensors_response.has_next is False:
                return device_sensors

            return (
                self._fetch_all_device_sensors(
                    account_id=account_id,
                    page_number=page_number + 1,
                    unit=unit,
                )
                + device_sensors
            )
        except UnexpectedStatus as e:
            logging.error("Unexpected status while fetching sensors: %s", e)
            return []
        except TimeoutException as e:
            logging.error("Timeout while fetching sensors: %s", e)
            return []
