from fastapi import FastAPI
from app.events import router as events_router
from app.audit import router as audit_router

app = FastAPI(title = "Event Message Sender")

# Include routers
app.include_router(events_router)
app.include_router(audit_router)