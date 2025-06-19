from fastapi import FastAPI, Request
from sqlmodel import Field, SQLModel, create_engine, Session, select, Column
from sqlalchemy import JSON
from typing import List
from datetime import datetime, timezone
import uuid
import asyncio

# Initialize FastAPI app
app = FastAPI()

# Use SQLite for persistent storage
DATABASE_URL = "sqlite:///./webhooks.db"
engine = create_engine(DATABASE_URL, echo=True)

# Define the Webhook model using SQLModel (ORM)
class Webhook(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)  # Unique webhook ID

    # Use timezone-aware datetime (UTC)
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    status: str = "unprocessed"  # Either 'unprocessed' or 'processed'

    # Store JSON payload with proper JSON column type
    payload: dict = Field(sa_column=Column(JSON))

# Create DB tables at startup
@app.on_event("startup")
def init_db():
    SQLModel.metadata.create_all(engine)

# POST endpoint to receive a webhook
@app.post("/webhook")
async def receive_webhook(req: Request):
    payload = await req.json()
    webhook = Webhook(payload=payload)

    with Session(engine) as session:
        session.add(webhook)
        session.commit()
        session.refresh(webhook)  # Ensures the ID is available
        webhook_id = webhook.id   # Capture ID before session closes

    # Now pass the captured ID to background task
    asyncio.create_task(process_webhook(webhook_id))

    return {"message": "Webhook received", "id": webhook_id}

# Background task to simulate 5-second processing delay
async def process_webhook(webhook_id: str):
    try:
        await asyncio.sleep(5)  # Simulate processing delay

        with Session(engine) as session:
            # Retrieve the webhook from DB
            webhook = session.exec(select(Webhook).where(Webhook.id == webhook_id)).first()
            if webhook:
                webhook.status = "processed"  # Mark as processed
                session.add(webhook)
                session.commit()
    except Exception as e:
        print(f"Error processing {webhook_id}: {e}") 

# GET endpoint to return list of received webhooks
@app.get("/webhooks")
def list_webhooks() -> List[Webhook]:
    with Session(engine) as session:
        # Fetch webhooks in reverse chronological order (latest first)
        webhooks = session.exec(select(Webhook).order_by(Webhook.received_at.desc())).all()
    return webhooks

@app.get("/health")
def health_check():
    return {"ok": True}
