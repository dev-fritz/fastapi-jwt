import asyncio
from src.models import *
from src.core.deps import Base
from src.core.database import engine


async def create_tables() -> None:
    print("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    async def main():
        await create_tables()
        await engine.dispose()

    asyncio.run(main())
