from typing import Annotated

from fastapi import Depends

from app.main import app
from app.services import SomeDataService


@app.get("/")
async def get_some_data(
    some_data_service: Annotated[SomeDataService, Depends()],
):
    return await some_data_service.get_data()
