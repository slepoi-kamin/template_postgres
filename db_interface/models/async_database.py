import contextlib

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from db_interface.conf import PG_PASS, PG_USER, host
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

async_engine = create_async_engine(f'postgresql+asyncpg://{PG_USER}:{PG_PASS}@{host}', echo=True)
Base = declarative_base()
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def init_models():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# async def get_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session

