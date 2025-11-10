from sqlalchemy import Column, Integer, String
from sqlalchemy import Enum as SQLAlchemyEnum
from enum import Enum

from .db import Base

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable= False)
    role = Column(SQLAlchemyEnum(RoleEnum), nullable= False, default=RoleEnum.user)

