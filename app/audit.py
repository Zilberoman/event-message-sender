from fastapi import APIRouter

from core.dao.events_dao import get_user_events
from core.dao.send_logs_dao import get_user_sends
from core.models.dto.responses.audit_response import AuditResponse

router = APIRouter()

@router.get("/audit/{user_id}", response_model = AuditResponse)
async def audit_user(user_id: str):
    return AuditResponse(events = [e.dict() for e in get_user_events(user_id)],
                         sends = [s.dict() for s in get_user_sends(user_id)])
