from typing import Generator

from sqlalchemy import create_engine

# from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
#                                     create_async_engine)
from sqlalchemy.orm import Session, sessionmaker

from src.settings.db_settings import settings

# Async version
# engine = create_async_engine(url=settings.ASYNC_DATABASE_URL, echo=True)
# SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sync version
engine = create_engine(url=settings.SYNC_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# async def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
