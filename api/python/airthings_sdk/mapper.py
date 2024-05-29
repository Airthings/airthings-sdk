"""Module providing an Airthings API SDK."""

import logging
from typing import List, Optional

from httpx import AsyncClient

from airthings_api_client import AuthenticatedClient, Client
from airthings_api_client.api.accounts import get_accounts_ids
from airthings_api_client.api.device import get_devices
from airthings_api_client.api.sensor import get_multiple_sensors
from airthings_api_client.errors import UnexpectedStatus as LibUnexpectedStatus
from airthings_api_client.models import (
    Error,
    GetMultipleSensorsResponse200,
)
from airthings_api_client.models.device_response import DeviceResponse
from airthings_api_client.models.get_multiple_sensors_unit import GetMultipleSensorsUnit
from airthings_api_client.models.sensors_response import SensorsResponse
from airthings_api_client.types import Unset
from airthings_sdk.const import API_URL, AUTH_URL
from airthings_sdk.errors import ApiError, UnexpectedPayloadError, UnexpectedStatusError
from airthings_sdk.types import AirthingsDevice, AirthingsDeviceType, AirthingsToken

logger = logging.getLogger(__name__)


class Airthings:
    """Representation of Airthings API data handler."""

    _client_id: str
    _client_secret: str

    _unit: GetMultipleSensorsUnit
    _access_token: AirthingsToken = AirthingsToken()

    _auth_api_client: Client = Client(
        base_url=AUTH_URL,
        raise_on_unexpected_status=True,
    )
    _api_client: AuthenticatedClient = AuthenticatedClient(
        base_url=API_URL,
        token="invalid_token",  # Should authenticate and update before using
        raise_on_unexpected_status=True,
    )

    devices: dict[str, AirthingsDevice] = {}

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        is_metric: bool,
        web_session: Optional[AsyncClient] = None,
    ):
        """Init Airthings data handler."""
        self._client_id = client_id
        self._client_secret = client_secret
        self._unit = GetMultipleSensorsUnit.METRIC if is_metric else GetMultipleSensorsUnit.IMPERIAL

        if web_session:
            self._auth_api_client.set_async_httpx_client(web_session)
            self._api_client.set_async_httpx_client(web_session)

    def verify_auth(self):
        """Make sure the access token is valid. If not, fetch a new one."""

        if self._access_token.is_valid():
            return

        try:
            auth_response = self._auth_api_client.get_httpx_client().request(
                url=AUTH_URL + "/v1/token",
                method="POST",
                data={
                    "grant_type": "client_credentials",
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                },
            )

            access_token = auth_response.json().get("access_token")
            expires_in = auth_response.json().get("expires_in")

            self._access_token.set_token(access_token=access_token, expires_in=expires_in)
            self._api_client.token = self._access_token.value
        except LibUnexpectedStatus as e:
            raise UnexpectedStatusError(e.status_code, e.content) from e

    async def update_devices(self) -> dict[str, AirthingsDevice]:
        """Update devices and sensors from Airthings API. Return a dict of devices."""
        logger.info("Fetching devices and sensors from Airthings API.")

        self.verify_auth()

        try:
            account_ids = await self._fetch_all_accounts_ids()

            res = {}
            for account_id in account_ids:
                devices = await self._fetch_all_devices(account_id=account_id)

                device_map = {}
                for device in devices:
                    device_map[device.serial_number] = device

                sensors = await self._fetch_all_device_sensors(
                    account_id=account_id,
                    unit=self._unit
                )

                for sensor in sensors:
                    serial_number = sensor.serial_number

                    if isinstance(serial_number, Unset):
                        continue

                    sensor_device = device_map.get(serial_number)
                    if sensor_device is None:
                        logger.debug("%s not found in devices list.", serial_number)
                        continue
                    mapped = AirthingsDevice.from_response(sensor_device, sensor)
                    if mapped.type == AirthingsDeviceType.HUB:
                        logger.debug("Skipping Hub %s.", serial_number)
                        continue
                    res[serial_number] = mapped

            self.devices = res
            logger.info("Fetched %s devices and sensors from Airthings API.", len(res))
            return res
        except LibUnexpectedStatus as e:
            logger.error(
                "Unexpected status code %s received when fetching devices and sensors.",
                e.status_code,
            )
            raise UnexpectedStatusError(e.status_code, e.content) from e

    async def _fetch_all_accounts_ids(self) -> List[str]:
        """Fetch accounts for the given client"""
        response = await get_accounts_ids.asyncio_detailed(client=self._api_client)

        payload = response.parsed

        if payload is None:
            raise UnexpectedPayloadError(response.content)

        return [account.id for account in (payload.accounts or []) if isinstance(account.id, str)]

    async def _fetch_all_devices(self, account_id: str) -> List[DeviceResponse]:
        """Fetch devices for a given account"""
        response = await get_devices.asyncio_detailed(
            account_id=account_id,
            client=self._api_client
        )

        payload = response.parsed

        if payload is None:
            raise UnexpectedPayloadError(response.content)

        return payload.devices or []

    async def _fetch_all_device_sensors(
        self,
        account_id: str,
        unit: GetMultipleSensorsUnit,
        page_number: int = 1,
    ) -> List[SensorsResponse]:
        """Fetch sensors for a given account"""
        response = await get_multiple_sensors.asyncio_detailed(
            account_id=account_id,
            client=self._api_client,
            page_number=page_number,
            unit=unit,
        )

        payload = response.parsed

        if isinstance(payload, Error):
            raise ApiError(payload.message or "Unknown error")

        if payload is None or isinstance(payload, GetMultipleSensorsResponse200) is False:
            raise UnexpectedPayloadError(response.content)

        sensors = payload.results or []

        if payload.has_next is not True:
            return sensors

        return sensors + self._fetch_all_device_sensors(
            account_id=account_id,
            page_number=page_number + 1,
            unit=unit,
        )
