"""Airthings API SDK types."""

import time
from dataclasses import dataclass, field
from typing import Optional, cast

from airthings_api_client.models import (
    SensorResponseType0,
    DeviceResponse,
    SensorsResponse,
)
from airthings_api_client.types import Unset


@dataclass
class AirthingsSensor:
    """Representation of Airthings device sensor."""

    sensor_type: str
    value: int | float
    unit: str

    @classmethod
    def from_response(cls, sensor_response: SensorResponseType0 | None | Unset):
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
    def from_response(
        cls, device_response: DeviceResponse, sensors_response: SensorsResponse
    ) -> "AirthingsDevice":
        """Create an AirthingsDevice from a DeviceResponse and a SensorsResponse"""

        mapped = map(AirthingsSensor.from_response, sensors_response.sensors or [])
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
        if self.value is None:
            return False
        if (expires := self._expires) is not None:
            return expires > (int(time.time()) + 20)
        return False
