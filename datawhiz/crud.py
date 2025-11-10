from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from . import models,schemas
from .auth.hashing import hash_password, verify_password
from .auth.dependencies import get_current_user


#Create
async def create_user(db: AsyncSession, user: schemas.UserCreate):
    result = await db.execute(select(models.User).where(models.User.email == user.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail= "Email is already registered!")


    new_user = models.User(name= user.name, email= user.email, password = hash_password(user.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# Read Single
async def get_user(db:AsyncSession, user_id: int):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalar_one_or_none()

# Read All Users
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()

# Update - Change username or email
async def update_user(db: AsyncSession, user_id: int, user: schemas.UserBase):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    existing_user = result.scalar_one_or_none()

    if existing_user is None:
        return None

    existing_user.name = user.name
    existing_user.email = user.email

    await db.commit()
    await db.refresh(existing_user)
    return existing_user

# Update - Change password
async def update_user_password(db: AsyncSession, user_id: int, current_password: str, new_password: str):
    print('update_user_password called')
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    existing_user = result.scalar_one_or_none()

    if existing_user is None:
        return None

    if not verify_password(current_password, existing_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password Does Not Match!")

    existing_user.password = hash_password(new_password)
    await db.commit()
    await db.refresh(existing_user)
    return existing_user





# Delete
async def delete_user(db:AsyncSession, user_id: int):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    existing_user = result.scalar_one_or_none()

    if existing_user is None:
        return None

    await db.delete(existing_user)
    await db.commit()
    return existing_user

