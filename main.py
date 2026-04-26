from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import engine, SessionLocal
from models import Base, Battery
from llm_service import ask_bess_question_stream

Base.metadata.create_all(bind=engine)
app = FastAPI(title="BESS Grid Manager API")

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "BESS Grid Manager API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/batteries")
def get_batteries(db: Session = Depends(get_db)):
    batteries = db.query(Battery).all()
    return [
        {
            "id": b.id,
            "name": b.name,
            "capacity_kwh": b.capacity_kwh,
            "max_charge_rate_kw": b.max_charge_rate_kw,
            "is_active": b.is_active
         }
            for b in batteries
        ]

@app.post("/llm/ask")
def ask_llm(question: str):
    return StreamingResponse(
        ask_bess_question_stream(question),
        media_type="text/plain"
    )

@app.get("/batteries/summary")
def get_battery_summary(db: Session = Depends(get_db)):
    rows = db.query(
        Battery.is_active,
        func.count(Battery.id),
        func.sum(Battery.capacity_kwh),
        func.sum(Battery.max_discharge_rate_kw)
    ).group_by(Battery.is_active).all()

    return [
        {
            "is_active": row[0],
            "battery_count": row[1],
            "total_capacity_kwh": row[2],
            "total_max_discharge_rate_kw": row[3]
        }
        for row in rows
    ]