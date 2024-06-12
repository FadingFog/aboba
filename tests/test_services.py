import itertools
from unittest.mock import AsyncMock

from app.models import SomeDataA, SomeDataB, SomeDataC
from app.repositories import SomeDataRepository
from app.services import SomeDataService


async def test_get_all_data_return_sorted_list_of_data():
    mock_data = {
        SomeDataA: [
            SomeDataA(id=1, name="test"),
            SomeDataA(id=3, name="test"),
            SomeDataA(id=2, name="test"),
        ],
        SomeDataB: [
            SomeDataB(id=5, name="test"),
            SomeDataB(id=6, name="test"),
        ],
        SomeDataC: [
            SomeDataC(id=4, name="test"),
        ],
    }

    mocked_some_data_repo = AsyncMock(spec=SomeDataRepository)
    mocked_some_data_repo.get_all_by_model.side_effect = lambda x: mock_data[x]
    service = SomeDataService(mocked_some_data_repo)

    result = await service.get_all_data()

    assert len(result) == 6
    assert result == sorted(itertools.chain(*mock_data.values()), key=lambda x: x.id)


async def test_get_all_data_return_empty_list_if_no_data(
    some_data_service: SomeDataService,
):
    result = await some_data_service.get_all_data()

    assert len(result) == 0
