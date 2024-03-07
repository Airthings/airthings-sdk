from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sensor_response_type_0 import SensorResponseType0


T = TypeVar("T", bound="SensorsResponse")


@_attrs_define
class SensorsResponse:
    """
    Attributes:
        serial_number (Union[Unset, str]):
        sensors (Union[Unset, List[Union['SensorResponseType0', None]]]):
        recorded (Union[None, Unset, str]):
        battery_percentage (Union[None, Unset, int]):
    """

    serial_number: Union[Unset, str] = UNSET
    sensors: Union[Unset, List[Union["SensorResponseType0", None]]] = UNSET
    recorded: Union[None, Unset, str] = UNSET
    battery_percentage: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.sensor_response_type_0 import SensorResponseType0

        serial_number = self.serial_number

        sensors: Union[Unset, List[Union[Dict[str, Any], None]]] = UNSET
        if not isinstance(self.sensors, Unset):
            sensors = []
            for sensors_item_data in self.sensors:
                sensors_item: Union[Dict[str, Any], None]
                if isinstance(sensors_item_data, SensorResponseType0):
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

        field_dict: Dict[str, Any] = {}
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
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.sensor_response_type_0 import SensorResponseType0

        d = src_dict.copy()
        serial_number = d.pop("serialNumber", UNSET)

        sensors = []
        _sensors = d.pop("sensors", UNSET)
        for sensors_item_data in _sensors or []:

            def _parse_sensors_item(data: object) -> Union["SensorResponseType0", None]:
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_sensor_response_type_0 = SensorResponseType0.from_dict(data)

                    return componentsschemas_sensor_response_type_0
                except:  # noqa: E722
                    pass
                return cast(Union["SensorResponseType0", None], data)

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
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
