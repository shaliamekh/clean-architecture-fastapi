from domain.enitites.bid import Bid
from ports.repositories.auction_repository import AuctionRepository
from use_cases.exceptions import (
    AuctionNotActiveError,
    LowBidError,
    AuctionNotFoundError,
)


class SubmitBidUseCase:
    def __init__(self, auction_repository: AuctionRepository):
        self._auction_repository = auction_repository

    async def __call__(self, bid: Bid) -> None:
        auction = await self._auction_repository.get(id=bid.auction_id)
        if not auction:
            raise AuctionNotFoundError(bid.auction_id)
        if not auction.is_active:
            raise AuctionNotActiveError(auction.id)
        if bid.price.value <= auction.minimal_bid_price.value:
            raise LowBidError(auction.minimal_bid_price)
        await self._auction_repository.add_bid(bid)
