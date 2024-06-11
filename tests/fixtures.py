import pytest

from app.repositories import SomeDataRepository


@pytest.fixture
async def some_data_repo(test_session, test_session_maker) -> SomeDataRepository:
    return SomeDataRepository(test_session, test_session_maker)
