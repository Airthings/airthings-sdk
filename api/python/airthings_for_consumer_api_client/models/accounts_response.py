from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_response import AccountResponse


T = TypeVar("T", bound="AccountsResponse")


@_attrs_define
class AccountsResponse:
    """
    Attributes:
        accounts (Union[Unset, List['AccountResponse']]):
    """

    accounts: Union[Unset, List["AccountResponse"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        accounts: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.accounts, Unset):
            accounts = []
            for accounts_item_data in self.accounts:
                accounts_item = accounts_item_data.to_dict()
                accounts.append(accounts_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if accounts is not UNSET:
            field_dict["accounts"] = accounts

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.account_response import AccountResponse

        d = src_dict.copy()
        accounts = []
        _accounts = d.pop("accounts", UNSET)
        for accounts_item_data in _accounts or []:
            accounts_item = AccountResponse.from_dict(accounts_item_data)

            accounts.append(accounts_item)

        accounts_response = cls(
            accounts=accounts,
        )

        accounts_response.additional_properties = d
        return accounts_response

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
