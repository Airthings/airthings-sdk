"""Airthings API SDK types."""

import logging
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

_LOGGER = logging.getLogger(__name__)


class AirthingsDeviceType(str, Enum):
    """Airthings device types."""

    AP_1 = "AP_1"
    CORENTIUM_HOME_2 = "RAVEN_RADON"
    HUB = "HUB"
    VIEW_PLUS = "VIEW_PLUS"
    VIEW_POLLUTION = "VIEW_POLLUTION"
    VIEW_RADON = "VIEW_RADON"
    WAVE = "WAVE"
    WAVE_ENHANCE = "WAVE_ENHANCE"
    WAVE_MINI = "WAVE_MINI"
    WAVE_PLUS = "WAVE_PLUS"
    WAVE_RADON = "WAVE_GEN2"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def from_raw_value(cls, value: str) -> "AirthingsDeviceType":
        """Get device type from raw value."""
        for device_type in cls:
            if device_type.value == value:
                return device_type
        _LOGGER.debug("Unknown device type: %s", value)
        return AirthingsDeviceType.UNKNOWN

    @property
    def product_name(self) -> str:
        """Return a display product name for this device type."""
        return {
            AirthingsDeviceType.AP_1: "Renew",
            AirthingsDeviceType.CORENTIUM_HOME_2: "Corentium Home 2",
            AirthingsDeviceType.HUB: "Hub",
            AirthingsDeviceType.VIEW_PLUS: "View Plus",
            AirthingsDeviceType.VIEW_POLLUTION: "View Pollution",
            AirthingsDeviceType.VIEW_RADON: "View Radon",
            AirthingsDeviceType.WAVE: "Wave Gen 1",
            AirthingsDeviceType.WAVE_ENHANCE: "Wave Enhance",
            AirthingsDeviceType.WAVE_MINI: "Wave Mini",
            AirthingsDeviceType.WAVE_PLUS: "Wave Plus",
            AirthingsDeviceType.WAVE_RADON: "Wave Radon",
        }.get(self, "Unknown")


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
    ) -> "AirthingsDevice":
        """Create an AirthingsDevice from a DeviceResponse and a SensorsResponse"""

        return cls(
            serial_number=cast(str, device_response.serial_number),
            name=cast(str, device_response.name),
            type=AirthingsDeviceType.from_raw_value(cast(str, device_response.type_)),
            home=cast(str | None, device_response.home),
            recorded=None,
            sensors=[],
        )

    def update_sensors(
        self,
        sensors_response: SensorsResponse,
    ) -> None:
        """Update the sensors of the device from a SensorsResponse"""
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

        self.sensors = filtered
        self.recorded = cast(str | None, sensors_response.recorded)


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
