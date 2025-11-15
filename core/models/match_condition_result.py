from typing import NamedTuple, Optional

class MatchConditionResult(NamedTuple):
    is_success: bool
    should_create_decision: Optional[bool] = False
    reason: Optional[str] = ""