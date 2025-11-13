from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base, with_loader_criteria
from sqlalchemy import event

# from .models import User

# SQLite database URL
DATABASE_URL = "sqlite+aiosqlite:///./ViSQL.db"

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

# Automatic Filtering for Soft-deleted Rows
# @event.listens_for(AsyncSession, 'do_orm_execute')
# def _add_filtering_deleted(execute_state):
#     """Automatically exclude rows where is_deleted = True"""
#     # if execute_state.is_select and not execute_state.execution_options.get("include_deleted", False):
#     #     # Apply Global Filters to the model that have `is_deleted` column




# Dependency for FastAPI routes
async def get_db():
    db = async_session_local()
    try:
        yield db
    finally:
        await db.close()
