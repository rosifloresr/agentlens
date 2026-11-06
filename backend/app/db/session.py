from collections.abc import AsyncIterator
from functools import lru_cache
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.config import get_settings

@lru_cache
def get_engine() -> AsyncEngine:
    # pool_pre_ping discards connections Postgres closed while idle, instead
    # of surfacing them as random errors on the next request.
    return create_async_engine(get_settings().database_url, pool_pre_ping=True)

@lru_cache
def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    # expire_on_commit=False: with async, accessing an expired attribute after
    # commit triggers implicit I/O, which raises instead of lazy-loading.
    return async_sessionmaker(get_engine(), expire_on_commit=False)

async def get_session() -> AsyncIterator[AsyncSession]:
    async with get_sessionmaker()() as session:
        yield session
