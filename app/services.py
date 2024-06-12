import asyncio
import itertools
from typing import Annotated

from fastapi import Depends

from app.models import SomeDataA, SomeDataB, SomeDataC
from app.repositories import SomeDataRepository, Model


class SomeDataService:
    """
    Layer between API routers and repository layer.
    Implements business logic, perform validations & etc.
    """

    def __init__(self, repository: Annotated[SomeDataRepository, Depends()]):
        self._repository = repository

    async def get_all_data(self) -> list[Model]:
        """Get data from every source, sort it and return it in a list."""
        results = await asyncio.gather(*[
            self._repository.get_all_by_model(SomeDataA),
            self._repository.get_all_by_model(SomeDataB),
            self._repository.get_all_by_model(SomeDataC),
        ])

        results = list(itertools.chain(*results))
        result = sorted(results, key=lambda i: i.id)
        return result
