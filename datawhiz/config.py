from pydantic import BaseModel
from dotenv import load_dotenv
import os

#Loads all variables from .env into Python’s environment so os.getenv() can read them.
load_dotenv()

#Read variables from the environment
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))