from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database URL
DATABASE_URL = "sqlite+aiosqlite:///./datawhiz.db"

# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create session factory
async_session_local = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI routes
async def get_db():
    db = async_session_local()
    try:
        yield db
    finally:
        await db.close()
