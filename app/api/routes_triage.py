from fastapi import APIRouter

from app.agents.triage import triage_issue
from app.domain.schemas import TriageRequest, TriageResult

router = APIRouter(prefix="/triage", tags=["triage"])


@router.post("", response_model=TriageResult)
def create_triage(request: TriageRequest) -> TriageResult:
    return triage_issue(request)
