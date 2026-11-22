from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Customer:
    customer_id: str
    name: str
    tier: str
    region: str
    created_at: datetime


@dataclass(frozen=True, slots=True)
class Order:
    order_id: str
    customer_id: str
    status: str
    amount_cents: int
    created_at: datetime
    updated_at: datetime
