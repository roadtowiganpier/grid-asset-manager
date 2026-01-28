from fastapi import FastAPI

from database import engine
from models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BESS Grid Manager API")


@app.get("/")
def read_root():
    return {"message": "BESS Grid Manager API", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}