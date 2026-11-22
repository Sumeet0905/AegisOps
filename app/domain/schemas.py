from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class IssueCategory(StrEnum):
    DAMAGED_PRODUCT = "damaged_product"
    WRONG_ITEM = "wrong_item"
    MISSING_ITEM = "missing_item"
    LATE_DELIVERY = "late_delivery"
    REFUND_REQUEST = "refund_request"
    OTHER = "other"


class Priority(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class TriageRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    message: str = Field(min_length=3, max_length=5000)
    order_id: str | None = Field(default=None, min_length=1, max_length=64)
    customer_id: str | None = Field(default=None, min_length=1, max_length=64)
    channel: str = Field(default="web", min_length=1, max_length=32)


class TriageResult(BaseModel):
    category: IssueCategory
    priority: Priority
    sentiment: str
    requires_human: bool
    order_id: str | None = None
    customer_id: str | None = None
    rationale: str
