import os
from functools import partial
from typing import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, async_scoped_session


def create_session_maker() -> async_sessionmaker[AsyncSession]:
    database_uri = os.getenv("DATABASE_URI")

    engine = create_async_engine(
        database_uri,
        pool_size=15,
        max_overflow=15,
        connect_args={
            "timeout": 5,
        },
    )
    return async_sessionmaker(engine, expire_on_commit=False)


async def new_session(
    scoped_session_maker: async_scoped_session[AsyncSession]
) -> AsyncGenerator[AsyncSession, None]:
    async with scoped_session_maker() as session:
        yield session
        await session.commit()


def init_dependencies(app: FastAPI):
    scoped_session_maker = create_session_maker()
    app.dependency_overrides[AsyncSession] = partial(new_session, scoped_session_maker)
