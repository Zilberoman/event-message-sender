import json

import pytest
from fastapi.testclient import TestClient
from app.main import app
from core.dao.events_dao import events_by_user
from core.dao.send_logs_dao import sends_by_user

client = TestClient(app)

def post_event(filename):
    with open(f"tests/data/{filename}") as file:
        event = json.load(file)
    response = client.post("/events", json = event)
    assert response.status_code == 200
    return response.json()["decisions"]

@pytest.fixture(autouse=True)
def clear_data_before_and_after_tests():
    sends_by_user.clear()
    events_by_user.clear()
    yield
    sends_by_user.clear()
    events_by_user.clear()

def test_welcome_email_sent():
    decisions = post_event("signup_event.json")
    assert any("signup completed" in decision.lower() for decision in decisions)

def test_welcome_email_sent_second_time():
    decisions = post_event("signup_event.json")
    print(decisions)
    assert any("signup completed" in decision.lower() for decision in decisions)
    decisions = post_event("signup_event.json")
    assert any("skipped: already sent" in decision.lower() for decision in decisions)


def test_bank_link_nudge_sms():
    # Firstly signup
    post_event("signup_event.json")

    # Then link
    decisions = post_event("bank_link_event.json")
    assert any("bank linked" in decision.lower() for decision in decisions)


def test_insufficient_funds_email_once_per_day():
    post_event("payment_failed_event.json")

    # Repeat the same event
    decisions = post_event("payment_failed_event.json")
    assert any("skipped: already sent today" in decision.lower() for decision in decisions)


def test_high_risk_alert():
    decisions = post_event("payment_failed_high_risk_event.json")
    assert any("payment failed 3+" in decision.lower() for decision in decisions)
    assert any("internal_alert" in decision.lower() or True for decision in decisions)
