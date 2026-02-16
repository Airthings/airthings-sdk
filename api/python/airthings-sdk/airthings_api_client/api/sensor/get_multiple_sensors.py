from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_multiple_sensors_response_200 import GetMultipleSensorsResponse200
from ...models.get_multiple_sensors_unit import GetMultipleSensorsUnit
from ...types import UNSET, Response, Unset


def _get_kwargs(
    account_id: str,
    *,
    sn: Union[Unset, list[str]] = UNSET,
    page_number: Union[Unset, int] = 1,
    unit: Union[Unset, GetMultipleSensorsUnit] = GetMultipleSensorsUnit.METRIC,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_sn: Union[Unset, list[str]] = UNSET
    if not isinstance(sn, Unset):
        json_sn = sn

    params["sn"] = json_sn

    params["pageNumber"] = page_number

    json_unit: Union[Unset, str] = UNSET
    if not isinstance(unit, Unset):
        json_unit = unit.value

    params["unit"] = json_unit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/accounts/{account_id}/sensors",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, GetMultipleSensorsResponse200]]:
    if response.status_code == 200:
        response_200 = GetMultipleSensorsResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, GetMultipleSensorsResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    account_id: str,
    *,
    client: AuthenticatedClient,
    sn: Union[Unset, list[str]] = UNSET,
    page_number: Union[Unset, int] = 1,
    unit: Union[Unset, GetMultipleSensorsUnit] = GetMultipleSensorsUnit.METRIC,
) -> Response[Union[Error, GetMultipleSensorsResponse200]]:
    """Get sensors for a set of devices

     Get sensors for a set of devices. The response will contain the latest sensor values for the
    devices.
    The sensor values are updated depending on the device types sampling rate.
    It is recommended to poll the API at a regular interval to get the latest sensor values.
    The response will be paginated with a maximum of 50 records per page.

    Args:
        account_id (str):
        sn (Union[Unset, list[str]]):
        page_number (Union[Unset, int]):  Default: 1.
        unit (Union[Unset, GetMultipleSensorsUnit]):  Default: GetMultipleSensorsUnit.METRIC.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetMultipleSensorsResponse200]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        sn=sn,
        page_number=page_number,
        unit=unit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    account_id: str,
    *,
    client: AuthenticatedClient,
    sn: Union[Unset, list[str]] = UNSET,
    page_number: Union[Unset, int] = 1,
    unit: Union[Unset, GetMultipleSensorsUnit] = GetMultipleSensorsUnit.METRIC,
) -> Optional[Union[Error, GetMultipleSensorsResponse200]]:
    """Get sensors for a set of devices

     Get sensors for a set of devices. The response will contain the latest sensor values for the
    devices.
    The sensor values are updated depending on the device types sampling rate.
    It is recommended to poll the API at a regular interval to get the latest sensor values.
    The response will be paginated with a maximum of 50 records per page.

    Args:
        account_id (str):
        sn (Union[Unset, list[str]]):
        page_number (Union[Unset, int]):  Default: 1.
        unit (Union[Unset, GetMultipleSensorsUnit]):  Default: GetMultipleSensorsUnit.METRIC.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetMultipleSensorsResponse200]
    """

    return sync_detailed(
        account_id=account_id,
        client=client,
        sn=sn,
        page_number=page_number,
        unit=unit,
    ).parsed


async def asyncio_detailed(
    account_id: str,
    *,
    client: AuthenticatedClient,
    sn: Union[Unset, list[str]] = UNSET,
    page_number: Union[Unset, int] = 1,
    unit: Union[Unset, GetMultipleSensorsUnit] = GetMultipleSensorsUnit.METRIC,
) -> Response[Union[Error, GetMultipleSensorsResponse200]]:
    """Get sensors for a set of devices

     Get sensors for a set of devices. The response will contain the latest sensor values for the
    devices.
    The sensor values are updated depending on the device types sampling rate.
    It is recommended to poll the API at a regular interval to get the latest sensor values.
    The response will be paginated with a maximum of 50 records per page.

    Args:
        account_id (str):
        sn (Union[Unset, list[str]]):
        page_number (Union[Unset, int]):  Default: 1.
        unit (Union[Unset, GetMultipleSensorsUnit]):  Default: GetMultipleSensorsUnit.METRIC.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetMultipleSensorsResponse200]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        sn=sn,
        page_number=page_number,
        unit=unit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    account_id: str,
    *,
    client: AuthenticatedClient,
    sn: Union[Unset, list[str]] = UNSET,
    page_number: Union[Unset, int] = 1,
    unit: Union[Unset, GetMultipleSensorsUnit] = GetMultipleSensorsUnit.METRIC,
) -> Optional[Union[Error, GetMultipleSensorsResponse200]]:
    """Get sensors for a set of devices

     Get sensors for a set of devices. The response will contain the latest sensor values for the
    devices.
    The sensor values are updated depending on the device types sampling rate.
    It is recommended to poll the API at a regular interval to get the latest sensor values.
    The response will be paginated with a maximum of 50 records per page.

    Args:
        account_id (str):
        sn (Union[Unset, list[str]]):
        page_number (Union[Unset, int]):  Default: 1.
        unit (Union[Unset, GetMultipleSensorsUnit]):  Default: GetMultipleSensorsUnit.METRIC.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetMultipleSensorsResponse200]
    """

    return (
        await asyncio_detailed(
            account_id=account_id,
            client=client,
            sn=sn,
            page_number=page_number,
            unit=unit,
        )
    ).parsed
