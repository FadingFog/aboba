import pytest
from pydantic import TypeAdapter

from app.models import SomeDataA, SomeDataB, SomeDataC
from app.repositories import SomeDataRepository
from app.schemas import SomeData


@pytest.mark.parametrize(
    "model, initial_id",
    [
        (SomeDataA, 1),
        (SomeDataB, 4),
        (SomeDataC, 7),
    ]
)
async def test_get_all_by_model_return_objects_from_sources(
    some_data_repo: SomeDataRepository,
    create_some_data,
    model,
    initial_id,
):
    quantity = 3
    expected_data_orm = await create_some_data(
        model=model,
        quantity=quantity,
        initial_id=initial_id
    )
    expected_data = TypeAdapter(list[SomeData]).validate_python(expected_data_orm, from_attributes=True)

    result_orm = await some_data_repo.get_all_by_model(model=model)
    result = TypeAdapter(list[SomeData]).validate_python(result_orm, from_attributes=True)

    assert result == expected_data
    assert len(result) == quantity
