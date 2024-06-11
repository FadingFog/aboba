import asyncio
import logging
import os
from functools import partial
from typing import AsyncGenerator, Type

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, AsyncEngine

from app.main import create_app
from app.models import BaseA, BaseB, BaseC
from core.dependencies import create_session_maker, get_binds, BaseModel

pytest_plugins = ["tests.fixtures"]

load_dotenv()
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


@pytest.fixture(scope='session', autouse=True)
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def test_binds() -> dict[Type[BaseModel], AsyncEngine]:
    database_uri = os.getenv("TEST_DATABASE_URI")
    sources_mapping = {  # Map sources URI per model
        BaseA: database_uri,
        BaseB: database_uri,
        BaseC: database_uri,
    }
    return get_binds(sources_mapping)


@pytest.fixture
async def test_session_maker(test_binds) -> async_sessionmaker[AsyncSession]:
    return create_session_maker(binds=test_binds)


@pytest.fixture
async def test_session(test_session_maker) -> AsyncGenerator[AsyncSession, None]:
    async with test_session_maker() as session:
        yield session


@pytest.fixture(scope='session')
def client(test_binds) -> TestClient:
    app = create_app()
    app.dependency_overrides[AsyncSession] = partial(test_session, test_session_maker)
    app.dependency_overrides[async_sessionmaker] = partial(create_session_maker, test_binds)

    test_client = TestClient(app)
    return test_client


@pytest.fixture(scope='function', autouse=True)
async def reset_tables(test_binds):
    for model, engine in test_binds.items():
        async with engine.begin() as connection:
            await connection.run_sync(model.metadata.drop_all)
            await connection.run_sync(model.metadata.create_all)
