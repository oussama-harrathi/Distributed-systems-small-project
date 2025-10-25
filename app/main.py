from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
import time
from .db import Base, engine, get_db
from .models import Item

app = FastAPI(title="Mini Kube App")

# Simple retry loop to ensure DB is ready before creating tables
def wait_for_db(max_attempts: int = 30, delay_seconds: float = 1.0):
    last_err = None
    for _ in range(max_attempts):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except Exception as e:
            last_err = e
            time.sleep(delay_seconds)
    raise RuntimeError(f"Database never became ready: {last_err}")

# Run once at import time for demo simplicity
wait_for_db()
Base.metadata.create_all(bind=engine)

class ItemIn(BaseModel):
    name: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/items")
def create_item(payload: ItemIn, db: Session = Depends(get_db)):
    item = Item(name=payload.name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "name": item.name}

@app.get("/items")
def list_items(db: Session = Depends(get_db)):
    items = db.query(Item).order_by(Item.id).all()
    return [{"id": i.id, "name": i.name} for i in items]
