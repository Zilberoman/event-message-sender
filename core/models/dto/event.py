from pydantic import BaseModel
from typing import Dict
from datetime import datetime

from core.models.event_type import EventType


class Event(BaseModel):
    user_id: str
    event_type: EventType
    event_timestamp: datetime
    properties: Dict = {}
    user_traits: Dict = {}
