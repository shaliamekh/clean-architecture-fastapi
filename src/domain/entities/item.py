from uuid import UUID, uuid4
from dataclasses import dataclass, field


@dataclass
class Item:
    name: str
    description: str
    id: UUID = field(default_factory=uuid4)
