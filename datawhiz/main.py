# datawhiz/main.py

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from . import models, schemas, crud
from .auth import auth
from .auth.dependencies import get_current_user
from .db import engine, Base, get_db
from .models import RoleEnum

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

@app.post("/users/create", response_model= schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await crud.create_user(db, user)
    return new_user

@app.get("/users/all", response_model= list[schemas.User])
async def read_users(skip: int= 0, limit: int = 10, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    print('Current User: ', current_user)
    print('Current User Role: ', current_user.role)
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "You do not have the permission required to see all users!")
    users = await crud.get_users(db, skip, limit)
    return users

@app.get("/users/me/info", response_model= schemas.User)
async def read_user(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    db_user = await crud.get_user(db, user_id = current_user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f'User with user id ({current_user.id}) Not Found!')
    return db_user

@app.put("/users/me/update", response_model= schemas.User)
async def update_user(user: schemas.UserBase, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    updated_user = await crud.update_user(db, current_user.id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail=f'User with user id ({current_user.id}) Not Found!')
    return updated_user

@app.put("/users/me/update-cred", response_model= schemas.MessageResponse)
async def update_user_password(req: schemas.PasswordUpdateRequest, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    print(f'update_user_password api called for user id: {current_user.id}')
    updated_user = await crud.update_user_password(db, current_user.id, req.current_password, req.new_password)
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User Not found!")
    return {"message": "Password Reset Successfully!"}

@app.delete("/users/me")
async def delete_user(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    deleted_user = await crud.delete_user(db, current_user.id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail= f'User with user id ({current_user.id}) Not Found!')
    return {"message": f'User with user id ({current_user.id}) Deleted Successfully!'}


@app.post("/login", response_model=schemas.TokenResponse)
async def login_json(login_data: schemas.LoginRequest, db: AsyncSession = Depends(get_db)):
    token = await auth.authenticate_user(login_data.email, login_data.password, db)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/login-form", response_model=schemas.TokenResponse)
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    print(f'login_form api called for user name: {form_data.username} and password: {form_data.password}')
    token = await auth.authenticate_user(form_data.username, form_data.password, db)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/auth/forget-password")
async def forget_password(email: str, db: AsyncSession = Depends(get_db)):
    print(f'forget_password api called for email id: {email}')
    reset_token = await auth.forgot_password(db, email)
    if reset_token is None:
        raise HTTPException(status_code=500, detail=f'Failed to Created Password Reset Token!')
    return {"reset_token": reset_token, "message": "Password reset token generated successfully!"}



@app.post("/auth/reset-password", response_model= schemas.MessageResponse)
async def reset_password(reset_token: str, new_password: str, db: AsyncSession = Depends(get_db)):
    print(f'reset_password api called!')
    message = await auth.reset_password(db, reset_token, new_password)
    return message



@app.get("/me")
def get_profile(current_user= Depends(get_current_user)):
    return {"message": f"Welcome Back, {current_user.name}!"}




