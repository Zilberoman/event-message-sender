from typing import List

from pydantic import BaseModel

from core.models.event import Event
from core.models.send_log import SendLog


class AuditResponse(BaseModel):
    events: List[Event]
    sends: List[SendLog]