"""Module providing an Airthings API SDK."""

import logging
import time
from typing import Optional

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
from airthings_sdk.const import API_URL, AUTH_URL, CACHE_TIMEOUT
from airthings_sdk.errors import ApiError, UnexpectedPayloadError, UnexpectedStatusError
from airthings_sdk.types import AirthingsDevice, AirthingsToken

logger = logging.getLogger(__name__)


class Airthings:
    """Representation of Airthings API data handler."""

    _client_id: str
    _client_secret: str

    _unit: GetMultipleSensorsUnit
    _access_token: AirthingsToken = AirthingsToken()

    _accounts: list[str] = []
    _cache_timestamp: Optional[int] = None

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

    def authenticate(self):
        """Make sure the access token is valid. If not, fetch a new one."""

        if self._access_token.is_valid():
            logger.info("Access token is valid, no need to refresh.")
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

            self._access_token.set_token(
                access_token=access_token,
                expires_in=expires_in,
            )
            self._api_client.token = self._access_token.value
            logger.info("Authenticated successfully ")
        except LibUnexpectedStatus as e:
            raise UnexpectedStatusError(e.status_code, e.content) from e

    async def _update_devices_cache(self):
        """Update the devices cache."""
        self._cache_timestamp = int(time.time())
        devices: list[DeviceResponse] = []
        for account in self._accounts:
            devices.extend(await self._fetch_all_devices(account_id=account))
            logger.info("Fetched %s devices from account %s.", len(devices), account)
        self.devices = {
            device.serial_number: AirthingsDevice.from_response(device)
            for device in devices
        }
        logger.info("Updated devices cache with %s devices.", len(self.devices))

    async def update_data(self, invalidate_cache: bool = False) -> dict[str, AirthingsDevice]:
        """Update devices and sensors from Airthings API. Return a dict of devices."""
        logger.info("Fetching devices and sensors from Airthings API.")

        should_refresh = (
            invalidate_cache or
            not self.devices or
            self._accounts_fetched_at is None or
            self._accounts_fetched_at + CACHE_TIMEOUT < int(time.time())
        )

        fetched_devices = False

        try:
            if should_refresh:
                self._accounts = await self._fetch_all_accounts_ids()
                self._accounts_fetched_at = int(time.time())
                logger.info("Fetched %s accounts", len(self._accounts))

                await self._update_devices_cache()
                fetched_devices = True

            sensor_responses = []

            for account_id in self._accounts:
                # Fetch sensors for each account
                sensor_responses.extend(
                    await self._fetch_all_device_sensors(
                        account_id=account_id,
                        unit=self._unit,
                    )
                )

            for sensor_response in sensor_responses:
                device_serial = sensor_response.serial_number
                if not isinstance(device_serial, str):
                    logger.info("Invalid serial number: %s", device_serial)
                    continue
                elif device_serial not in self.devices:
                    if not fetched_devices:
                        await self._update_devices_cache()
                        fetched_devices = True
                        break

            for device in self.devices.values():
                sensors_response = next(
                    (s for s in sensor_responses if s.serial_number == device.serial_number),
                    None,
                )
                if sensors_response:
                    device.update_sensors(sensors_response)
            return self.devices
        except LibUnexpectedStatus as e:
            logger.error(
                "Unexpected status code %s received when fetching devices and sensors",
                e.status_code,
            )
            raise UnexpectedStatusError(e.status_code, e.content) from e

    async def _fetch_all_accounts_ids(self) -> list[str]:
        """Fetch accounts for the given client"""

        self.authenticate()

        response = await get_accounts_ids.asyncio_detailed(client=self._api_client)
        payload = response.parsed

        if payload is None:
            raise UnexpectedPayloadError(response.content)

        return [account.id for account in (payload.accounts or []) if isinstance(account.id, str)]

    async def _fetch_all_devices(self, account_id: str) -> list[DeviceResponse]:
        """Fetch devices for a given account"""

        self.authenticate()

        response = await get_devices.asyncio_detailed(
            account_id=account_id,
            client=self._api_client,
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
    ) -> list[SensorsResponse]:
        """Fetch sensors for a given account"""

        try:
            response = await get_multiple_sensors.asyncio_detailed(
                account_id=account_id,
                client=self._api_client,
                page_number=page_number,
                unit=unit,
            )
        except LibUnexpectedStatus as e:
            raise UnexpectedStatusError(e.status_code, e.content) from e

        payload = response.parsed

        if isinstance(payload, Error):
            raise ApiError(payload.message or "Unknown error")

        if payload is None or not isinstance(payload, GetMultipleSensorsResponse200):
            raise UnexpectedPayloadError(response.content)

        sensors = payload.results or []

        if payload.has_next is not True:
            return sensors

        return sensors + await self._fetch_all_device_sensors(
            account_id=account_id,
            page_number=page_number + 1,
            unit=unit,
        )
