from dotenv import load_dotenv
from fastapi import FastAPI

from core.dependencies import init_dependencies


def create_app() -> FastAPI:
    _app = FastAPI()
    load_dotenv()
    init_dependencies(_app)

    return _app


app = create_app()
