from fastapi.testclient import TestClient

from app.agents.triage import triage_issue
from app.domain.schemas import IssueCategory, Priority, TriageRequest
from app.main import app

client = TestClient(app)


def test_damaged_product_is_high_priority() -> None:
    result = triage_issue(TriageRequest(message="My product arrived damaged"))
    assert result.category == IssueCategory.DAMAGED_PRODUCT
    assert result.priority == Priority.HIGH
    assert result.requires_human is False


def test_urgent_safety_issue_requires_human() -> None:
    result = triage_issue(TriageRequest(message="This is a safety issue, I may take legal action"))
    assert result.priority == Priority.URGENT
    assert result.requires_human is True


def test_triage_endpoint_returns_structured_result() -> None:
    response = client.post(
        "/api/v1/triage",
        json={"message": "I want a refund for my order", "order_id": "ORD-100"},
    )
    assert response.status_code == 200
    assert response.json()["category"] == "refund_request"
    assert response.json()["order_id"] == "ORD-100"
