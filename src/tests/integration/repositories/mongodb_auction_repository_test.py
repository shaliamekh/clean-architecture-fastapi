from uuid import uuid4

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from adapters.repositories.auction_repository.mongodb_repository import (
    MongoAuctionRepository,
)
from tests.utils import create_auction, create_bid


@pytest.fixture
async def auction_repository(client: AsyncIOMotorClient):  # type: ignore
    repo = MongoAuctionRepository(client)
    yield repo
    await repo.collection.drop()


async def test_get_by_id_success(auction_repository: MongoAuctionRepository):
    auction = create_auction()
    await auction_repository.add(auction)
    assert await auction_repository.get(id=auction.id) == auction


async def test_get_by_id_not_found(auction_repository: MongoAuctionRepository):
    assert await auction_repository.get(id=uuid4()) is None


async def test_add_bid_success(auction_repository: MongoAuctionRepository):
    auction = create_auction()
    await auction_repository.add(auction)
    bid = create_bid(auction_id=auction.id)
    assert await auction_repository.add_bid(bid) is True


async def test_add_bid_auction_not_found(auction_repository: MongoAuctionRepository):
    bid = create_bid(auction_id=uuid4())
    assert await auction_repository.add_bid(bid) is False
