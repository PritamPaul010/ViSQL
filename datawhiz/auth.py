from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Create JWT Access Token
def create_access_token(data: dict):
    """
    Generates a JWT Token using the provided user data
    :param data:
    :return:
    """

    # Copy data to avoid modifying original
    to_encode = data.copy()

    # Define Expiration Time
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Encode the token using SECRET_KEY and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# Decode token
def verify_token(token: str):
    """
    Verifies the JWT token and returns its payload if valid
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        return payload
    except JWTError:
        return None

