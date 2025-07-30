from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sensors_response import SensorsResponse


T = TypeVar("T", bound="GetMultipleSensorsResponse200")


@_attrs_define
class GetMultipleSensorsResponse200:
    """
    Attributes:
        results (Union[Unset, list['SensorsResponse']]):
        has_next (Union[Unset, bool]): True if next pages can be fetched, false otherwise.
        total_pages (Union[Unset, int]):
    """

    results: Union[Unset, list["SensorsResponse"]] = UNSET
    has_next: Union[Unset, bool] = UNSET
    total_pages: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        results: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for results_item_data in self.results:
                results_item = results_item_data.to_dict()
                results.append(results_item)

        has_next = self.has_next

        total_pages = self.total_pages

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if results is not UNSET:
            field_dict["results"] = results
        if has_next is not UNSET:
            field_dict["hasNext"] = has_next
        if total_pages is not UNSET:
            field_dict["totalPages"] = total_pages

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sensors_response import SensorsResponse

        d = dict(src_dict)
        results = []
        _results = d.pop("results", UNSET)
        for results_item_data in _results or []:
            results_item = SensorsResponse.from_dict(results_item_data)

            results.append(results_item)

        has_next = d.pop("hasNext", UNSET)

        total_pages = d.pop("totalPages", UNSET)

        get_multiple_sensors_response_200 = cls(
            results=results,
            has_next=has_next,
            total_pages=total_pages,
        )

        get_multiple_sensors_response_200.additional_properties = d
        return get_multiple_sensors_response_200

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
