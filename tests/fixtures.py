import os
from functools import partial
from typing import AsyncGenerator, Type

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, AsyncEngine

from app.main import create_app
from app.models import BaseA, BaseB, BaseC
from app.repositories import SomeDataRepository
from core.dependencies import create_session_maker, get_binds, BaseModel

load_dotenv()


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


@pytest.fixture
async def some_data_repo(test_session, test_session_maker) -> SomeDataRepository:
    return SomeDataRepository(test_session, test_session_maker)
