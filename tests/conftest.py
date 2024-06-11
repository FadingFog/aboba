import asyncio

import pytest

pytest_plugins = ["tests.fixtures"]


@pytest.fixture(scope='session', autouse=True)
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function', autouse=True)
async def reset_tables(test_binds):
    for model, engine in test_binds.items():
        async with engine.begin() as connection:
            await connection.run_sync(model.metadata.drop_all)
            await connection.run_sync(model.metadata.create_all)
