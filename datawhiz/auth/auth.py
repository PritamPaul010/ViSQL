from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordBearer
from ..models import User
from .hashing import verify_password
from .jwt_handler import create_access_token

async def authenticate_user(email: str, password: str, db: AsyncSession):
    # Get User from DB
        result = await db.execute(select(User).where(User.email == email))
        print('result: ', result)
        user = result.scalars().first()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Invalid Email- User Doesn't Exist!" )

        if not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Invalid Password!")

        token = create_access_token(data={'sub': user.email})
        return token
    # except Exception as e:
    #     print(f'authenticate_user error: {e}')
    #     raise HTTPException(status_code=500, detail= "Internal Server Error: Failed to Authenticate User!")


