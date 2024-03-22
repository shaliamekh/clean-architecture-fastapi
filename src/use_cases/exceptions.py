from uuid import UUID

from domain.value_objects.price import Price


class AuctionNotFoundError(Exception):
    def __init__(self, auction_id: UUID):
        self.auction_id = auction_id

    def __str__(self) -> str:
        return f"Auction not found: {self.auction_id}"


class AuctionNotActiveError(Exception):
    def __init__(self, auction_id: UUID):
        self.auction_id = auction_id

    def __str__(self) -> str:
        return f"Auction is not active: {self.auction_id}"


class LowBidError(Exception):
    def __init__(self, min_price: Price):
        self.min_price = min_price

    def __str__(self) -> str:
        return f"New bids for the auction should be higher than {self.min_price.value} {self.min_price.currency}"
