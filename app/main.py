from dotenv import load_dotenv
from fastapi import FastAPI

from app.api import init_routers
from core.dependencies import init_dependencies
from core.logging import get_logger


def create_app() -> FastAPI:
    _app = FastAPI()
    load_dotenv()
    get_logger()
    init_dependencies(_app)
    init_routers(_app)

    return _app


app = create_app()
