## database.py
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./blog.db"

# connection string for SQLite database
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# a session local class that will be used to create database sessions, autocommit and autoflush are set to False to have more control over transactions
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# base class for all our models to inherit from
class Base(DeclarativeBase):
    pass


# dependency to get a database session
async def get_db():
    async with AsyncSessionLocal() as session:
        # Yields a database session and ensures it's closed after use
        yield session