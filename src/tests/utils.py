from datetime import date, timedelta
from uuid import UUID, uuid4

from domain.enitites.auction import Auction
from domain.enitites.bid import Bid
from domain.enitites.item import Item
from domain.value_objects.price import Price, CurrencyOption


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
        start_date=date.today() - timedelta(days=7) if not start_date else start_date,
        end_date=date.today() + timedelta(days=7) if not end_date else end_date,
        start_price=Price(value=start_price_value, currency=CurrencyOption.euro),
        bids=bids if bids else [],
    )
