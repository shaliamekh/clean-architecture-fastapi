from datetime import date, timedelta
from uuid import UUID, uuid4

from domain.entities.auction import Auction
from domain.entities.bid import Bid
from domain.entities.item import Item
from domain.value_objects.price import CurrencyOption, Price


def create_bid(
    auction_id: UUID | None = None,
    price_value: float = 100.0,
    price_currency: CurrencyOption = CurrencyOption.euro,
) -> Bid:
    return Bid(
        bidder_id=uuid4(),
        price=Price(value=price_value, currency=price_currency),
        auction_id=auction_id if auction_id else uuid4(),
    )


def create_auction(
    bids: list[Bid] | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    start_price_value: int = 10,
) -> Auction:
    return Auction(
        item=Item(name="Test item", description="Test item description"),
        seller_id=uuid4(),
        start_date=start_date if start_date else date.today() - timedelta(days=7),
        end_date=end_date if end_date else date.today() + timedelta(days=7),
        start_price=Price(value=start_price_value, currency=CurrencyOption.euro),
        bids=bids if bids else [],
    )
