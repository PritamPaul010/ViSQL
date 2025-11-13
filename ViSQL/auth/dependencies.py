from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncConnection # yields AsyncSession

from ViSQL.auth.jwt_handler import verify_token
from ViSQL.db import get_db
from ViSQL.schemas import UserBase
from .. import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login-form")

async def get_current_user(
        token: str = Depends(oauth2_scheme), # 1) Extract token string from "Authorization: Bearer ..."
        db: AsyncConnection = Depends(get_db) # 2) Provide an async DB session (closed automatically)
):
    # 3) Verify token signature and expiry; extract identity (email/sub)
    email = verify_token(token)

    if not email:
        # verify_access_token could return None; better to raise here
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Invalid Token")

    # 4) Query the database for the user
    result = await db.execute(select(models.User).where((models.User.email == email) & (models.User.is_deleted == False)))
    user = result.scalars().first()

    # 5) If user not found, raise 404 (or 401 depending on semantics)
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= 'User Not Found!')

    # 6) Return user object. This becomes the value injected into route functions.
    return user



async def get_current_admin(current_user = Depends(get_current_user)):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Administrative privileges required!")
    return current_user