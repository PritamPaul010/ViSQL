from datetime import datetime, timedelta, UTC, timezone
from fastapi import HTTPException, status
from jose import JWTError, jwt

from ViSQL.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, RESET_TOKEN_EXPIRE_MINUTES


# Create JWT Access Token
def create_token(data: dict, type: str = 'access'):
    """
    Generates a JWT Token using the provided user data
    :param data:
    :return:
    """

    # Copy data to avoid modifying original
    try:
        to_encode = data.copy()

        token_expire_minutes = RESET_TOKEN_EXPIRE_MINUTES if type == 'reset' else ACCESS_TOKEN_EXPIRE_MINUTES

        # Define Expiration Time
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})

        # Encode the token using SECRET_KEY and algorithm
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print(f'create_token error for type - {type}: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error: Failed to Create Access Token!")


# Decode token
def verify_token(token: str):
    """
    Verifies the JWT token and returns its payload if valid
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail= "Invalid token: user not found!"
            )

        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= "Token has expired!"
            )

        return email

    except JWTError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid or expired token!"
        )
