import os
from functools import partial
from typing import AsyncGenerator, Type

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine

from app.models import BaseA, BaseB, BaseC


def get_binds() -> dict[Type[BaseA | BaseB | BaseC], AsyncEngine]:
    database_uri = os.getenv("DATABASE_URI")
    sources_mapping = {  # Map sources URI per model
        BaseA: database_uri,
        BaseB: database_uri,
        BaseC: database_uri,
    }

    # Create an engine for each model
    binds = {}
    for model, source_uri in sources_mapping.items():
        binds[model] = create_async_engine(
            source_uri,
            pool_size=15,
            max_overflow=15,
            connect_args={
                "timeout": 2,
            },
        )

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
    app.dependency_overrides[async_sessionmaker] = create_session_maker
