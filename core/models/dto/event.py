from pydantic import BaseModel
from typing import Dict
from datetime import datetime

class Event(BaseModel):
    user_id: str
    event_type: str
    event_timestamp: datetime
    properties: Dict = {}
    user_traits: Dict = {}
