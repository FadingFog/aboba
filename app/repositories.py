from typing import TypeVar, Annotated, Type

from fastapi import Depends
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from core.logging import logger
from core.stub import Stub

Model = TypeVar("Model", bound=DeclarativeBase)
ModelClass = Type[Model]


class SomeDataRepository:
    """Interface for interacting with database."""

    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(Stub(AsyncSession))],
        session_maker: Annotated[async_sessionmaker, Depends(Stub(async_sessionmaker))],
    ):
        self._session = session
        # Session maker is required when accessing more than one database at a time
        # https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-faq-threadsafe
        self._session_maker = session_maker

    async def get_all_by_model(self, model: ModelClass) -> tuple[Model]:
        """Get data from appropriate source based on passed model"""
        try:
            async with self._session_maker() as session:
                query = select(model)

                result = await session.scalars(query)
                objects = result.all()
        except Exception:
            logger.info(f"Error on getting data of {model} model")
            objects = tuple()

        return objects

    async def get_all_by_model_raw(self, model: ModelClass) -> tuple[Model]:
        """Get data from appropriate source based on passed model using raw SQL"""
        try:
            async with self._session_maker() as session:
                query = text(f"SELECT * FROM {model.__tablename__}")

                result = await session.execute(
                    statement=query,
                    bind_arguments={"mapper": model}  # Passed argument to get_bind(), so it can use the correct bind
                )
                objects = result.all()
        except Exception:
            logger.info(f"Error on getting data of {model} model")
            objects = tuple()

        return objects

    async def create(self, obj: Model) -> Model:
        """Save object to database"""
        # Since I don't know (for now) how to handle ID duplication in multiple tables/sources
        # it will be handled externally (like in tests with initial_id)
        self._session.add(obj)
        # Commit instead of flush because of different sessions in create() & get_all_by_model_raw() methods
        await self._session.commit()
        return obj
