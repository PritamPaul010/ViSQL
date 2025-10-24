# datawhiz/main.py

from fastapi import FastAPI
from datawhiz.db import engine, Base

app = FastAPI(title="DataWhiz")

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "DataWhiz backend is running successfully 🚀"}
