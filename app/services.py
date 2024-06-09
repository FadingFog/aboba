from typing import Annotated

from fastapi import Depends

from app.repositories import SomeDataRepository


class SomeDataService:
    def __init__(self, repository: Annotated[SomeDataRepository, Depends()]):
        self._repository = repository

    async def get_data(self):

