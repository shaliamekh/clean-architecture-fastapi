from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from adapters.repositories.auction_repository.mongodb_repository import (
    MongoAuctionRepository,
)
from ports.repositories.auction_repository import AuctionRepository
from use_cases.submit_bid_use_case import SubmitBidUseCase


@lru_cache
def get_mongo_client() -> AsyncIOMotorClient:  # type: ignore
    return AsyncIOMotorClient("mongodb://localhost:27017")


def get_auction_repository(
    mongo_client: Annotated[AsyncIOMotorClient, Depends(get_mongo_client)],  # type: ignore
) -> AuctionRepository:
    return MongoAuctionRepository(mongo_client)


def get_submit_bid_use_case(
    auction_repository: Annotated[AuctionRepository, Depends(get_auction_repository)],
) -> SubmitBidUseCase:
    return SubmitBidUseCase(auction_repository)
