from datetime import date, datetime
from typing import Any
from uuid import UUID

from adapters.exceptions import DatabaseError
from domain.enitites.auction import Auction
from domain.enitites.bid import Bid
from domain.enitites.item import Item
from domain.value_objects.price import Price
from ports.repositories.auction_repository import AuctionRepository
from motor.motor_asyncio import AsyncIOMotorClient
from bson import Binary


class MongoAuctionRepository(AuctionRepository):
    def __init__(self, client: AsyncIOMotorClient):  # type: ignore
        self.collection = client.auctions.auction  # type: ignore

    async def get(self, **filters: Any) -> Auction | None:
        filters = self.__get_filters(filters)
        try:
            document = await self.collection.find_one(filters)
            return self.__to_auction_entity(document) if document else None
        except Exception as e:
            raise DatabaseError(e)

    async def add_bid(self, bid: Bid) -> bool:
        try:
            r = await self.collection.update_one(
                {"_id": Binary.from_uuid(bid.auction_id)},
                {"$push": {"bids": self.__bid_to_doc(bid)}},
            )
            return bool(r.modified_count)
        except Exception as e:
            raise DatabaseError(e)

    async def add(self, auction: Auction) -> None:
        try:
            auction_doc = self.__auction_to_doc(auction)
            await self.collection.insert_one(auction_doc)
        except Exception as e:
            raise DatabaseError(e)

    @staticmethod
    def __get_filters(filters_args: dict[str, Any]) -> dict[str, Any]:
        filters = {}
        if f := filters_args.get("id"):
            filters["_id"] = Binary.from_uuid(f)
        return filters

    def __auction_to_doc(self, auction: Auction) -> dict[str, Any]:
        return {
            "_id": Binary.from_uuid(auction.id),
            "item": {
                "_id": Binary.from_uuid(auction.item.id),
                "name": auction.item.name,
                "description": auction.item.description,
            },
            "seller_id": Binary.from_uuid(auction.seller_id),
            "start_date": auction.start_date.isoformat(),
            "end_date": auction.end_date.isoformat(),
            "start_price": {
                "value": auction.start_price.value,
                "currency": auction.start_price.currency,
            },
            "bids": [self.__bid_to_doc(bid) for bid in auction.bids],
        }

    @staticmethod
    def __bid_to_doc(bid: Bid) -> dict[str, Any]:
        return {
            "bidder_id": Binary.from_uuid(bid.bidder_id),
            "price": {"value": bid.price.value, "currency": bid.price.currency},
            "auction_id": Binary.from_uuid(bid.auction_id),
            "_id": Binary.from_uuid(bid.id),
            "created_at": bid.created_at.isoformat(),
        }

    def __to_auction_entity(self, obj: dict[str, Any]) -> Auction:
        return Auction(
            id=UUID(bytes=obj["_id"]),
            item=Item(
                id=UUID(bytes=obj["item"]["_id"]),
                name=obj["item"]["name"],
                description=obj["item"]["description"],
            ),
            seller_id=UUID(bytes=obj["seller_id"]),
            start_date=date.fromisoformat(obj["start_date"]),
            end_date=date.fromisoformat(obj["end_date"]),
            start_price=Price(
                value=obj["start_price"]["value"],
                currency=obj["start_price"]["currency"],
            ),
            bids=[self.__to_bid_entity(bid) for bid in obj["bids"]],
        )

    @staticmethod
    def __to_bid_entity(bid: dict[str, Any]) -> Bid:
        return Bid(
            bidder_id=UUID(bytes=bid["bidder_id"]),
            price=Price(
                value=bid["price"]["value"],
                currency=bid["price"]["currency"],
            ),
            auction_id=UUID(bytes=bid["auction_id"]),
            id=UUID(bytes=bid["_id"]),
            created_at=datetime.fromisoformat(bid["created_at"]),
        )
