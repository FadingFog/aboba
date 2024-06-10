import asyncio
import itertools
from typing import Annotated

from fastapi import Depends

from app.models import SomeDataA, SomeDataB
from app.repositories import SomeDataRepository


class SomeDataService:
    def __init__(self, repository: Annotated[SomeDataRepository, Depends()]):
        self._repository = repository

    async def get_data(self):
        results = await asyncio.gather(*[
            self._repository.get_all(SomeDataA),
            self._repository.get_all(SomeDataB),
        ])

        results = list(itertools.chain(*results))
        result = sorted(results, key=lambda i: i.id)
        return result
