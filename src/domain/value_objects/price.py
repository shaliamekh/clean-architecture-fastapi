from dataclasses import dataclass
from enum import StrEnum


class CurrencyOption(StrEnum):
    euro = "EUR"
    dollar = "USD"


@dataclass(frozen=True)
class Price:
    value: float
    currency: CurrencyOption
