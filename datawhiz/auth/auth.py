from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import User
from .hashing import verify_password
from .jwt_handler import create_access_token

async def authenticate_user(email: str, password: str, db: AsyncSession):
    # Get User from DB
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Invalid Email- User Doesn't Exist!" )

    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Invalid Password!")

    token = create_access_token(data={'sub': user.email})

    return token
