from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from domain.value_objects.price import Price


@dataclass
class Bid:
    bidder_id: UUID
    price: Price
    auction_id: UUID
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
