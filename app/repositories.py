from typing import TypeVar, Annotated, Type

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from core.logging import logger
from core.stub import Stub

Model = TypeVar("Model", bound=Type[DeclarativeBase])


class SomeDataRepository:
    """
    Interface for interacting with database.
    """
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(Stub(AsyncSession))],
        session_maker: Annotated[async_sessionmaker, Depends(Stub(async_sessionmaker))],
    ):
        self._session = session
        self._session_maker = session_maker
        # Session maker is required when accessing more than one database at a time
        # https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-faq-threadsafe

    async def get_all_by_model(self, model: Model) -> tuple[Model]:
        try:
            async with self._session_maker() as session:
                query = select(model)

                result = await session.scalars(query)
                objects = result.all()
        except Exception:
            logger.info(f"Error on getting data of {model} model")
            objects = tuple()

        return objects
