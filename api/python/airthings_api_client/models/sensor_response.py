from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SensorResponse")


@_attrs_define
class SensorResponse:
    """
    Attributes:
        sensor_type (Union[Unset, str]):
        value (Union[Unset, float]):
        unit (Union[Unset, str]):
    """

    sensor_type: Union[Unset, str] = UNSET
    value: Union[Unset, float] = UNSET
    unit: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        sensor_type = self.sensor_type

        value = self.value

        unit = self.unit

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sensor_type is not UNSET:
            field_dict["sensorType"] = sensor_type
        if value is not UNSET:
            field_dict["value"] = value
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sensor_type = d.pop("sensorType", UNSET)

        value = d.pop("value", UNSET)

        unit = d.pop("unit", UNSET)

        sensor_response = cls(
            sensor_type=sensor_type,
            value=value,
            unit=unit,
        )

        sensor_response.additional_properties = d
        return sensor_response

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
