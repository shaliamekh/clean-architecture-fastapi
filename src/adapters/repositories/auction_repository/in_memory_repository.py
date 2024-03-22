from typing import Any

from domain.enitites.auction import Auction
from domain.enitites.bid import Bid
from ports.repositories.auction_repository import AuctionRepository


class InMemoryAuctionRepository(AuctionRepository):
    auctions: list[Auction] = []

    async def get(self, **filters: Any) -> Auction | None:
        for auction in self.auctions:
            if (f := filters.get("id")) and f == auction.id:
                return auction
        return None

    async def add_bid(self, bid: Bid) -> bool:
        for auction in self.auctions:
            if auction.id == bid.auction_id:
                auction.bids.append(bid)
                return True
        return False
