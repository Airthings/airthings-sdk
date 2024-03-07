from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DeviceResponse")


@_attrs_define
class DeviceResponse:
    """
    Attributes:
        serial_number (Union[Unset, str]):
        home (Union[None, Unset, str]):
        name (Union[Unset, str]):
        type (Union[Unset, str]):
        sensors (Union[Unset, List[str]]):
    """

    serial_number: Union[Unset, str] = UNSET
    home: Union[None, Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    sensors: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        serial_number = self.serial_number

        home: Union[None, Unset, str]
        if isinstance(self.home, Unset):
            home = UNSET
        else:
            home = self.home

        name = self.name

        type = self.type

        sensors: Union[Unset, List[str]] = UNSET
        if not isinstance(self.sensors, Unset):
            sensors = self.sensors

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if serial_number is not UNSET:
            field_dict["serialNumber"] = serial_number
        if home is not UNSET:
            field_dict["home"] = home
        if name is not UNSET:
            field_dict["name"] = name
        if type is not UNSET:
            field_dict["type"] = type
        if sensors is not UNSET:
            field_dict["sensors"] = sensors

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        serial_number = d.pop("serialNumber", UNSET)

        def _parse_home(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        home = _parse_home(d.pop("home", UNSET))

        name = d.pop("name", UNSET)

        type = d.pop("type", UNSET)

        sensors = cast(List[str], d.pop("sensors", UNSET))

        device_response = cls(
            serial_number=serial_number,
            home=home,
            name=name,
            type=type,
            sensors=sensors,
        )

        device_response.additional_properties = d
        return device_response

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
