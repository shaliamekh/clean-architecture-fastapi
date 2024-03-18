from uuid import UUID

from pydantic import BaseModel

from domain.enitites.bid import Bid
from domain.value_objects.price import CurrencyOption, Price


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
