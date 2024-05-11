from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from dotenv import load_dotenv

import os

load_dotenv()

engine: AsyncEngine = create_async_engine(os.getenv("DATABASE_URL"))
"""
AsyncEngine: A SQLAlchemy AsyncEngine instance.
This engine is configured to connect to the database specified by the DATABASE_URL environment variable.
"""

Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)
"""
AsyncSession: A SQLAlchemy sessionmaker instance configured for asynchronous sessions.
This sessionmaker is bound to the AsyncEngine instance and configured with specific session options:
- autocommit: False to prevent automatic commits.
- autoflush: False to prevent automatic session flushes.
- expire_on_commit: False to prevent session expiration on commit.
"""
