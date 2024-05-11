from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from dotenv import load_dotenv

import os

load_dotenv()

engine: AsyncEngine = create_async_engine(os.getenv("DATABASE_URL"))
Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)
