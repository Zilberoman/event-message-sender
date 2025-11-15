from pydantic import BaseModel
from datetime import datetime

class SendLog(BaseModel):
    user_id: str
    template_name: str
    channel: str
    timestamp: datetime
    reason: str
    suppressed: bool = False
