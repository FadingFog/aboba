import pytest

from app.models import SomeDataCommon
from app.repositories import SomeDataRepository, ModelClass
from app.services import SomeDataService


@pytest.fixture
async def some_data_repo(test_session, test_session_maker) -> SomeDataRepository:
    return SomeDataRepository(test_session, test_session_maker)


@pytest.fixture
async def some_data_service(some_data_repo) -> SomeDataService:
    return SomeDataService(some_data_repo)


@pytest.fixture
async def create_some_data(some_data_repo):
    """
    Fixture to create SomeData object in a proper database based on passed model.
     Args
      - model: should be SomeDataA | SomeDataB | SomeDataC.
      - number: (optional) number of objects to create.
      - initial_id: (optional) id of the first object to create.
     Returns
      - List of created objects.
    """
    async def _create(model: ModelClass, quantity: int = 1, initial_id: int = 1) -> list[SomeDataCommon]:
        assert initial_id > 0, "Initial id should be greater than 0."
        id_counter = initial_id

        objects = []
        for i in range(quantity):
            mock_data = {
                "id": id_counter,
                "name": f"name_{id_counter}"
            }
            obj = await some_data_repo.create(
                obj=model(**mock_data)
            )
            objects.append(obj)

            id_counter += 1

        return objects

    return _create
