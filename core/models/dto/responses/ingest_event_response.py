from typing import List

from pydantic import BaseModel

class IngestEventResponse(BaseModel):
    status: str
    decisions: List[str]