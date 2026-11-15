import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://taskmanager:taskmanager@localhost:5432/taskmanager",
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session]:
    """Give one SQLAlchemy session to a request, then close it.

    FastAPI caches this dependency for the request, so every repository
    built during that request shares the same session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
