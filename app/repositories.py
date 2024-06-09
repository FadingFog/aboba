from typing import TypeVar, Annotated, Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


class SomeDataRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(AsyncSession)]):
        self._session = session
