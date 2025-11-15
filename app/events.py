from fastapi import APIRouter

from core.dao.events_dao import store_event, get_user_events
from core.dao.helpers.deduplication import has_sent_template_today, has_sent_template_ever
from core.dao.send_logs_dao import store_send_log, get_user_sends
from core.models.dto.event import Event
from core.models.dto.responses.ingest_event_response import IngestEventResponse
from core.rules.engine import rule_engine

router = APIRouter()

@router.post("/events", response_model= IngestEventResponse)
async def ingest_event(event: Event):
    store_event(event)

    decisions = rule_engine.apply_rules(event, get_user_events = get_user_events,
                                        get_user_sends = get_user_sends,
                                        has_sent_template_today = has_sent_template_today,
                                        has_sent_template_ever = has_sent_template_ever)

    for decision in decisions:
        if decision.should_send:
            store_send_log(decision.to_send_log())
        else:
            store_send_log(decision.to_suppression_log())

    return IngestEventResponse(status = "ok", decisions = [decision.reason for decision in decisions])
