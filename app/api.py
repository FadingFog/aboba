from typing import Annotated

from fastapi import Depends, APIRouter, FastAPI

from app.schemas import SomeData
from app.services import SomeDataService

root_router = APIRouter()


def init_routers(app: FastAPI):
    app.include_router(root_router)


@root_router.get("/", response_model=SomeData)
async def get_some_data(
    some_data_service: Annotated[SomeDataService, Depends()],
):
    return await some_data_service.get_data()
