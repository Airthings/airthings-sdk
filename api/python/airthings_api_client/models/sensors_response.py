from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sensor_response import SensorResponse


T = TypeVar("T", bound="SensorsResponse")


@_attrs_define
class SensorsResponse:
    """
    Attributes:
        serial_number (Union[Unset, str]):
        sensors (Union[Unset, list[Union['SensorResponse', None]]]):
        recorded (Union[None, Unset, str]):
        battery_percentage (Union[None, Unset, int]):
    """

    serial_number: Union[Unset, str] = UNSET
    sensors: Union[Unset, list[Union["SensorResponse", None]]] = UNSET
    recorded: Union[None, Unset, str] = UNSET
    battery_percentage: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.sensor_response import SensorResponse

        serial_number = self.serial_number

        sensors: Union[Unset, list[Union[None, dict[str, Any]]]] = UNSET
        if not isinstance(self.sensors, Unset):
            sensors = []
            for sensors_item_data in self.sensors:
                sensors_item: Union[None, dict[str, Any]]
                if isinstance(sensors_item_data, SensorResponse):
                    sensors_item = sensors_item_data.to_dict()
                else:
                    sensors_item = sensors_item_data
                sensors.append(sensors_item)

        recorded: Union[None, Unset, str]
        if isinstance(self.recorded, Unset):
            recorded = UNSET
        else:
            recorded = self.recorded

        battery_percentage: Union[None, Unset, int]
        if isinstance(self.battery_percentage, Unset):
            battery_percentage = UNSET
        else:
            battery_percentage = self.battery_percentage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if serial_number is not UNSET:
            field_dict["serialNumber"] = serial_number
        if sensors is not UNSET:
            field_dict["sensors"] = sensors
        if recorded is not UNSET:
            field_dict["recorded"] = recorded
        if battery_percentage is not UNSET:
            field_dict["batteryPercentage"] = battery_percentage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sensor_response import SensorResponse

        d = dict(src_dict)
        serial_number = d.pop("serialNumber", UNSET)

        sensors = []
        _sensors = d.pop("sensors", UNSET)
        for sensors_item_data in _sensors or []:

            def _parse_sensors_item(data: object) -> Union["SensorResponse", None]:
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_sensor_response_type_0 = SensorResponse.from_dict(data)

                    return componentsschemas_sensor_response_type_0
                except:  # noqa: E722
                    pass
                return cast(Union["SensorResponse", None], data)

            sensors_item = _parse_sensors_item(sensors_item_data)

            sensors.append(sensors_item)

        def _parse_recorded(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        recorded = _parse_recorded(d.pop("recorded", UNSET))

        def _parse_battery_percentage(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        battery_percentage = _parse_battery_percentage(d.pop("batteryPercentage", UNSET))

        sensors_response = cls(
            serial_number=serial_number,
            sensors=sensors,
            recorded=recorded,
            battery_percentage=battery_percentage,
        )

        sensors_response.additional_properties = d
        return sensors_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
