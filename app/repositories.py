from typing import TypeVar, Annotated, Type

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from core.stub import Stub

Model = TypeVar("Model", bound=Type[DeclarativeBase])


class SomeDataRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(Stub(AsyncSession))]):
        self._session = session

    async def get_all(self, model: Model) -> list[Model]:
        query = select(model)

        result = await self._session.scalars(query)
        objects = result.all()
        return objects
