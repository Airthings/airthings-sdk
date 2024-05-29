from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.accounts_response import AccountsResponse
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/accounts",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[AccountsResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AccountsResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AccountsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[AccountsResponse]:
    """List all accounts the current user is member of

     Lists all accounts the current user is member of. The data returned by this endpoint changes when a
    user is added or removed from business accounts. It is safe to assume that the accountId remains
    constant for Consumer users. The accountId returned by this endpoint is used to fetch the devices
    and sensors from the other endpoints.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountsResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[AccountsResponse]:
    """List all accounts the current user is member of

     Lists all accounts the current user is member of. The data returned by this endpoint changes when a
    user is added or removed from business accounts. It is safe to assume that the accountId remains
    constant for Consumer users. The accountId returned by this endpoint is used to fetch the devices
    and sensors from the other endpoints.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountsResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[AccountsResponse]:
    """List all accounts the current user is member of

     Lists all accounts the current user is member of. The data returned by this endpoint changes when a
    user is added or removed from business accounts. It is safe to assume that the accountId remains
    constant for Consumer users. The accountId returned by this endpoint is used to fetch the devices
    and sensors from the other endpoints.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountsResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[AccountsResponse]:
    """List all accounts the current user is member of

     Lists all accounts the current user is member of. The data returned by this endpoint changes when a
    user is added or removed from business accounts. It is safe to assume that the accountId remains
    constant for Consumer users. The accountId returned by this endpoint is used to fetch the devices
    and sensors from the other endpoints.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
