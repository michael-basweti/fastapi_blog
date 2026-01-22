## database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# connection string for SQLite database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # needed for SQLite only because sqlite is not designed for multi-threaded applications hence we need to set check_same_thread to False
    connect_args={"check_same_thread": False},
)

# a session local class that will be used to create database sessions, autocommit and autoflush are set to False to have more control over transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for all our models to inherit from
class Base(DeclarativeBase):
    pass


# dependency to get a database session
def get_db():
    with SessionLocal() as db:
        # Yields a database session and ensures it's closed after use
        yield db