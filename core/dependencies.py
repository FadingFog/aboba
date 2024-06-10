import os
from functools import partial
from typing import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.models import BaseA, BaseB


def get_binds():
    database_uri = os.getenv("DATABASE_URI")

    engine_1 = create_async_engine(
        database_uri,
        pool_size=15,
        max_overflow=15,
        connect_args={
            "timeout": 2,
        },
    )
    engine_2 = create_async_engine(
        database_uri,
        pool_size=15,
        max_overflow=15,
        connect_args={
            "timeout": 2,
        },
    )
    binds = {
        BaseA: engine_1,
        BaseB: engine_2,
    }
    return binds


def create_session_maker() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        binds=get_binds(),
        expire_on_commit=False
    )


async def new_session(
    session_maker: async_sessionmaker[AsyncSession]
) -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session
        await session.commit()


def init_dependencies(app: FastAPI):
    session_maker = create_session_maker()
    app.dependency_overrides[AsyncSession] = partial(new_session, session_maker)
