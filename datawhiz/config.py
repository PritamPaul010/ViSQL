from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv
import os


dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
#Loads all variables from .env into Python’s environment so os.getenv() can read them.
load_dotenv(dotenv_path)

#Read variables from the environment
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
RESET_TOKEN_EXPIRE_MINUTES = int(os.getenv("RESET_TOKEN_EXPIRE_MINUTES", 5))