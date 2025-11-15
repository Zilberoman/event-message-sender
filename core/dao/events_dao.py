from collections import defaultdict

from core.models.dto.event import Event

events_by_user = defaultdict(list)

def store_event(event: Event):
    events_by_user[event.user_id].append(event)

def get_user_events(user_id):
    return events_by_user[user_id]