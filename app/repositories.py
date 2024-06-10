from typing import TypeVar, Annotated, Type

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from core.stub import Stub

Model = TypeVar("Model", bound=Type[DeclarativeBase])


class SomeDataRepository:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(Stub(AsyncSession))],
        session_maker: Annotated[async_sessionmaker, Depends(Stub(async_sessionmaker))],
    ):
        self._session = session
        self._session_maker = session_maker

    async def get_all(self, model: Model) -> list[Model]:
        async with self._session_maker() as session:
            query = select(model)

            result = await session.scalars(query)
            objects = result.all()
        return objects
