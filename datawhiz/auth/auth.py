from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordBearer
from ..models import User
from .hashing import verify_password, hash_password
from .jwt_handler import create_token, verify_token


async def authenticate_user(email: str, password: str, db: AsyncSession):
    # Get User from DB
        result = await db.execute(select(User).where(User.email == email))
        print('result: ', result)
        user = result.scalars().first()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Invalid Email- User Doesn't Exist!" )

        if not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Invalid Password!")

        token = create_token(data={'sub': user.email}, type = 'access') # Access Token Created
        return token
    # except Exception as e:
    #     print(f'authenticate_user error: {e}')
    #     raise HTTPException(status_code=500, detail= "Internal Server Error: Failed to Authenticate User!")


# Forgot Password
async def forgot_password(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    existing_user = result.scalar_one_or_none()

    if existing_user is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"No user exist with email id: {email}")

    reset_token = create_token(data= {"sub": email}, type= 'reset')

    return reset_token

async def reset_password(db: AsyncSession, reset_token: str, new_password: str):
    email = verify_token(reset_token)
    if email is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No email found in Reset Token!")

    result = await db.execute(select(User).where(User.email == email))
    existing_user = result.scalar_one_or_none()

    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No user exist with email id: {email}")

    existing_user.password = hash_password(new_password)
    await db.commit()
    await db.refresh(existing_user)

    return {"message": "Password Reset Successfully!"}





