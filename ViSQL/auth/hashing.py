from passlib.context import CryptContext

# Define bcrypt hashing context
pwd_context = CryptContext(schemes=["argon2"], deprecated = "auto")

# Function to hash plain pwd
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password,hashed_password)


