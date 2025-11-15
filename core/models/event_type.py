from enum import Enum

class EventType(Enum):
    SIGNUP_COMPLETED = "signup_completed"
    LINK_BANK_SUCCESS = "link_bank_success"
    PAYMENT_INITIATED = "payment_initiated"
    PAYMENT_FAILED = "payment_failed"
