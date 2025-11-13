from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy import Enum as SQLAlchemyEnum
from enum import Enum
import uuid

from .db import Base

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default= lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)
    email = Column(String, index=True, nullable= False)
    password = Column(String, nullable= False)
    role = Column(SQLAlchemyEnum(RoleEnum), nullable= False, default=RoleEnum.user)
    is_deleted = Column(Boolean, nullable= False, default= False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

