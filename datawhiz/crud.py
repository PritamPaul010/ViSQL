from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models,schemas


#Create
async def create_user(db: AsyncSession, user: schemas.UserCreate):
    new_user = models.User(name= user.name, email= user.email)
    db.add(new_user)
    await db.commit()
    await db.refresh()
    return new_user

# Read Single
async def get_user(db:AsyncSession, user_id: int):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalar_one_or_none()

# Read All Users
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.User).skip(skip).limit(limit))
    return result.scalars.all()

# Update - Change username or email
async def update_user(db: AsyncSession, user_id: int, user: schemas.UserCreate):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    existing_user = result.scalar_one_or_none()

    if existing_user is None:
        return None

    existing_user.name = user.name
    existing_user.email = user.email

    await db.commit()
    await db.refresh(existing_user)
    return existing_user

# Delete
async def delete_user(db:AsyncSession, user_id: int):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    existing_user = result

    if existing_user is None:
        return None

    await db.delete()
    await db.commit()
    return existing_user

