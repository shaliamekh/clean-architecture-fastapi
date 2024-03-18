from functools import lru_cache
from typing import Annotated
from uuid import UUID

from fastapi import FastAPI, status, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from adapters.repositories.auction_repository.mongodb_repository import (
    MongoAuctionRepository,
)
from domain.enitites.bid import Bid
from domain.value_objects.price import CurrencyOption, Price
from drivers.rest.exception_handlers import exception_container
from ports.repositories.auction_repository import AuctionRepository
from use_cases.submit_bid_use_case import SubmitBidUseCase

app = FastAPI()

exception_container(app)


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


class PriceInput(BaseModel):
    value: float
    currency: CurrencyOption

    def to_entity(self) -> Price:
        return Price(value=self.value, currency=self.currency)


class BidInput(BaseModel):
    bidder_id: UUID
    price: PriceInput

    def to_entity(self, auction_id: UUID) -> Bid:
        return Bid(
            auction_id=auction_id,
            bidder_id=self.bidder_id,
            price=self.price.to_entity(),
        )


@app.post("/auctions/{auction_id}/bids", status_code=status.HTTP_204_NO_CONTENT)
async def submit_bid(
    auction_id: UUID,
    data: BidInput,
    use_case: Annotated[SubmitBidUseCase, Depends(get_submit_bid_use_case)],
) -> None:
    await use_case(data.to_entity(auction_id))
