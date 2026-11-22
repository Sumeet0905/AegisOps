from app.domain.schemas import IssueCategory, Priority, TriageRequest, TriageResult

_CATEGORY_TERMS: tuple[tuple[IssueCategory, tuple[str, ...]], ...] = (
    (IssueCategory.DAMAGED_PRODUCT, ("damaged", "broken", "cracked", "defective")),
    (IssueCategory.WRONG_ITEM, ("wrong item", "incorrect item", "not what i ordered")),
    (IssueCategory.MISSING_ITEM, ("missing", "not received", "item absent")),
    (IssueCategory.LATE_DELIVERY, ("late", "delayed", "delivery hasn't", "not delivered")),
    (IssueCategory.REFUND_REQUEST, ("refund", "money back", "return my money")),
)

_URGENT_TERMS = ("fraud", "charged twice", "unauthorized", "legal action", "safety")
_NEGATIVE_TERMS = ("angry", "upset", "terrible", "disappointed", "unacceptable")


def triage_issue(request: TriageRequest) -> TriageResult:
    """Classify a support message using transparent rules, without model-side actions."""
    message = request.message.casefold()
    category = IssueCategory.OTHER
    for candidate, terms in _CATEGORY_TERMS:
        if any(term in message for term in terms):
            category = candidate
            break

    urgent = any(term in message for term in _URGENT_TERMS)
    negative = any(term in message for term in _NEGATIVE_TERMS)
    priority = Priority.URGENT if urgent else (
        Priority.HIGH if negative or category in {
            IssueCategory.DAMAGED_PRODUCT, IssueCategory.WRONG_ITEM
        } else Priority.NORMAL
    )
    return TriageResult(
        category=category,
        priority=priority,
        sentiment="negative" if negative else "neutral",
        requires_human=urgent,
        order_id=request.order_id,
        customer_id=request.customer_id,
        rationale=(
            "Matched transparent keyword rules; no external action was performed."
        ),
    )
