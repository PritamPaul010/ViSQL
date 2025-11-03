# datawhiz/main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from . import models, schemas, crud
from .auth import auth
from .db import engine, Base, get_db

app = FastAPI(title="DataWhiz")

#Create Tables on Startup (Runs once)
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "DataWhiz backend is running successfully 🚀"}

@app.get('/health')
async def check_health():
    return {"status": "ok"}

## User CRUD Endpoints

@app.post("/users/", response_model= schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await crud.create_user(db, user)
    return new_user

@app.get("/users/", response_model= list[schemas.User])
async def read_users(skip: int= 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    users = await crud.get_users(db, skip, limit)
    return users

@app.get("/users/{user_id}", response_model= schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id = user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f'User with user id ({user_id}) Not Found!')
    return db_user

@app.put("/users/{user_id}", response_model= schemas.User)
async def update_user(user_id: int, user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    updated_user = await crud.update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail=f'User with user id ({user_id}) Not Found!')
    return updated_user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    deleted_user = await crud.delete_user(db, user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail= f'User with user id ({user_id}) Not Found!')
    return {'message': f'User with user id ({user_id}) Deleted Successfully!'}


@app.post("/login", response_model=schemas.TokenResponse)
async def login_user(login_data: schemas.LoginRequest, db: AsyncSession = Depends(get_db)):
    token = await auth.authenticate_user(login_data.email, login_data.password, db)
    return {'access_token': token, "token_type": 'bearer'}



