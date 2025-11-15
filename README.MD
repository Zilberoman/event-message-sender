# Event Message Sender

A small Python service to process user events and decide which message to send.

---

## Features
- Accepts inbound events via REST endpoint `/events`
- Applies configurable rules to decide on messages:
    - `WELCOME_EMAIL` (after signup)
    - `BANK_LINK_NUDGE_SMS` (if bank linked within 24h)
    - `INSUFFICIENT_FUNDS_EMAIL` (only once per user per day)
    - `HIGH_RISK_ALERT` (internal alert if 3+ failed payments)
- Deduplication of messages
- Audit/debug endpoint `/audit/<user_id>` to see why a message was sent or suppressed
- In-memory storage (easy to swap for SQLite or another DB)

---

## How to run

```bash
./run_server.sh
```
Server runs at http://localhost:8000

Endpoints:

POST /events — send a user event

GET /audit/<user_id> — audit a user

You could find test http requests in requests folder

DAO layer can be extended to SQLite, Postgres, or another database

#TODO: make validations for example "once per day" or "once" configurable in yaml file 
(for example take reason from there) OR make enum with condition function and response function 


## TESTS
How to run:
```bash
    pip install -r requirements.txt
    pytest tests/
```

