from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base
from typing import Generator
from src.core.database import Session

Base = declarative_base()


async def get_session() -> Generator:
    """
    Asynchronous context manager for database sessions.

    This function creates a new database session and yields it for use within an asynchronous context. After the context is exited, the session is automatically closed.

    :return: A generator that yields an AsyncSession object.
    """
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()
