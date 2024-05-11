from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base

from typing import Generator

from src.core.database import Session

Base = declarative_base()


async def get_session() -> Generator:
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()
