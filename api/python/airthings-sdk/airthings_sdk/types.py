"""Airthings API SDK types."""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, cast

from airthings_api_client.models import (
    DeviceResponse,
    SensorResponse,
    SensorsResponse,
)
from airthings_api_client.types import Unset


class AirthingsDeviceType(str, Enum):
    """Airthings device types."""

    VIEW_PLUS = "VIEW_PLUS"
    VIEW_RADON = "VIEW_RADON"
    VIEW_POLLUTION = "VIEW_POLLUTION"
    WAVE = "WAVE"
    WAVE_PLUS = "WAVE_PLUS"
    WAVE_MINI = "WAVE_MINI"
    WAVE_RADON = "WAVE_GEN2"
    HUB = "HUB"
    AP_1 = "AP_1"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def from_raw_value(cls, value: str) -> "AirthingsDeviceType":
        """Get device type from raw value."""
        for device_type in cls:
            if device_type.value == value:
                device_type.raw_value = value
                return device_type
        unknown_device = AirthingsDeviceType.UNKNOWN
        unknown_device.raw_value = value
        return unknown_device

    @property
    def product_name(self) -> str:
        if self == AirthingsDeviceType.VIEW_PLUS:
            return "View Plus"
        if self == AirthingsDeviceType.VIEW_RADON:
            return "View Radon"
        if self == AirthingsDeviceType.VIEW_POLLUTION:
            return "View Pollution"
        if self == AirthingsDeviceType.WAVE:
            return "Wave Gen 1"
        if self == AirthingsDeviceType.WAVE_PLUS:
            return "Wave Plus"
        if self == AirthingsDeviceType.WAVE_MINI:
            return "Wave Mini"
        if self == AirthingsDeviceType.WAVE_RADON:
            return "Wave Radon"
        if self == AirthingsDeviceType.HUB:
            return "Hub"
        if self == AirthingsDeviceType.AP_1:
            return "Renew"
        return "Unknown"


@dataclass
class AirthingsSensor:
    """Representation of Airthings device sensor."""

    sensor_type: str
    value: int | float
    unit: str

    @classmethod
    def from_response(cls, sensor_response: SensorResponse | None | Unset):
        """Create an AirthingsSensor from a SensorResponse"""

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
    type: AirthingsDeviceType
    name: str
    home: Optional[str]
    recorded: Optional[str]
    sensors: list[AirthingsSensor] = field(default_factory=list)

    @classmethod
    def from_response(
        cls,
        device_response: DeviceResponse,
        sensors_response: SensorsResponse,
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
            type=AirthingsDeviceType.from_raw_value(cast(str, device_response.type_)),
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
