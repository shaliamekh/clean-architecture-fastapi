import uuid
from typing import Any

import pytest
from fastapi import status

from domain.value_objects.price import Price, CurrencyOption
from drivers.rest.dependencies import get_submit_bid_use_case
from drivers.rest.main import app

from httpx import AsyncClient

from use_cases.exceptions import (
    AuctionNotFoundError,
    AuctionNotActiveError,
    LowBidError,
)
from adapters.exceptions import ExternalError

auction_id = uuid.uuid4()
payload = {
    "bidder_id": str(uuid.uuid4()),
    "price": {"value": 90, "currency": "EUR"},
}
url = f"/auctions/{str(auction_id)}/bids"


@pytest.mark.parametrize(
    "exception, status_code",
    (
        (AuctionNotFoundError(auction_id), status.HTTP_404_NOT_FOUND),
        (AuctionNotActiveError(auction_id), status.HTTP_422_UNPROCESSABLE_ENTITY),
        (
            LowBidError(Price(value=10, currency=CurrencyOption.euro)),
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
    ),
)
async def test_submit_bid_auction_with_exceptions(
    async_client: AsyncClient, exception: Exception, status_code: int
):
    class MockUseCase:
        async def __call__(self, *args: Any, **kwargs: Any) -> None:
            raise exception

    app.dependency_overrides[get_submit_bid_use_case] = MockUseCase
    response = await async_client.post(url, json=payload)
    assert response.status_code == status_code
    assert response.json() == {"message": str(exception)}


async def test_submit_bid_auction_not_found(async_client: AsyncClient):
    exception = ExternalError

    class MockUseCase:
        async def __call__(self, *args: Any, **kwargs: Any) -> None:
            raise exception

    app.dependency_overrides[get_submit_bid_use_case] = MockUseCase
    response = await async_client.post(url, json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"message": "Something went wrong. Please try again"}


async def test_submit_bid_success(async_client: AsyncClient):
    class MockUseCase:
        async def __call__(self, *args: Any, **kwargs: Any) -> None:
            pass

    app.dependency_overrides[get_submit_bid_use_case] = MockUseCase
    response = await async_client.post(url, json=payload)
    assert response.status_code == status.HTTP_204_NO_CONTENT
