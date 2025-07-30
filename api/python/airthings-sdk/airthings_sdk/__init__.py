"""A client library for accessing Airthings for Consumer API"""

from .errors import ApiError, UnexpectedPayloadError, UnexpectedStatusError
from .mapper import Airthings
from .types import AirthingsDevice, AirthingsDeviceType, AirthingsSensor

__all__ = (
    "Airthings",
    "AirthingsDevice",
    "AirthingsDeviceType",
    "AirthingsSensor",
    "ApiError",
    "UnexpectedPayloadError",
    "UnexpectedStatusError",
)
