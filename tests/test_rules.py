import pytest
from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_signup_welcome_email():
    # Загружаем тестовое событие из json
    with open("tests/data/signup_event.json") as f:
        event = json.load(f)

    response = client.post("/events", json=event)
    assert response.status_code == 200
    decisions = response.json()["decisions"]
    assert any("signup completed" in d for d in decisions)

def test_insufficient_funds_email_once_per_day():
    with open("tests/data/payment_failed_event.json") as f:
        event = json.load(f)

    # Первый вызов – должно отправиться
    response1 = client.post("/events", json=event)
    decisions1 = response1.json()["decisions"]
    assert any("insufficient funds" in d.lower() for d in decisions1)

    # Второй вызов того же события того же дня – должно подавиться
    response2 = client.post("/events", json=event)
    decisions2 = response2.json()["decisions"]
    assert any("skipped: already sent today" in d.lower() for d in decisions2)
