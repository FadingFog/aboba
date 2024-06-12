import pytest
from pydantic import TypeAdapter

from app.models import SomeDataA, SomeDataB, SomeDataC, BaseA
from app.repositories import SomeDataRepository
from app.schemas import SomeData


# noinspection DuplicatedCode
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
    expected_data = TypeAdapter(list[SomeData]).validate_python(expected_data_orm)

    result_orm = await some_data_repo.get_all_by_model(model=model)
    result = TypeAdapter(list[SomeData]).validate_python(result_orm)

    assert result == expected_data
    assert len(result) == quantity


# noinspection DuplicatedCode
async def test_get_all_by_model_return_objects_from_all_sources(
    some_data_repo: SomeDataRepository,
    create_some_data,
):
    quantity = 3
    initial_id = 1
    for model in [SomeDataA, SomeDataB, SomeDataC]:
        expected_data_orm = await create_some_data(
            model=model,
            quantity=quantity,
            initial_id=initial_id
        )
        initial_id += quantity
    expected_data = TypeAdapter(list[SomeData]).validate_python(expected_data_orm)

    result_orm = await some_data_repo.get_all_by_model(model=model)
    result = TypeAdapter(list[SomeData]).validate_python(result_orm)

    assert result == expected_data
    assert len(result) == quantity


async def test_get_all_by_model_return_objects_return_empty_tuple_on_exception(
    some_data_repo: SomeDataRepository,
    create_some_data,
    caplog,
):
    _ = await create_some_data(
        model=SomeDataA,
        quantity=3,
    )

    # Should raise exception in method because of abstract model BaseA
    result_orm = await some_data_repo.get_all_by_model(model=BaseA)

    assert len(result_orm) == 0
    assert "Error on getting data" in caplog.text


# noinspection DuplicatedCode
@pytest.mark.parametrize(
    "model, initial_id",
    [
        (SomeDataA, 1),
        (SomeDataB, 4),
        (SomeDataC, 7),
    ]
)
async def test_get_all_by_model_raw_return_objects_from_sources(
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
    expected_data = TypeAdapter(list[SomeData]).validate_python(expected_data_orm)

    result_orm = await some_data_repo.get_all_by_model_raw(model=model)
    result = TypeAdapter(list[SomeData]).validate_python(result_orm)

    assert result == expected_data
    assert len(result) == quantity


# noinspection DuplicatedCode
async def test_get_all_by_model_raw_return_objects_from_all_sources(
    some_data_repo: SomeDataRepository,
    create_some_data,
):
    quantity = 3
    initial_id = 1
    for model in [SomeDataA, SomeDataB, SomeDataC]:
        expected_data_orm = await create_some_data(
            model=model,
            quantity=quantity,
            initial_id=initial_id
        )
        initial_id += quantity
    expected_data = TypeAdapter(list[SomeData]).validate_python(expected_data_orm)

    result_orm = await some_data_repo.get_all_by_model_raw(model=model)
    result = TypeAdapter(list[SomeData]).validate_python(result_orm)

    assert result == expected_data
    assert len(result) == quantity


async def test_get_all_by_model_raw_return_objects_return_empty_tuple_on_exception(
    some_data_repo: SomeDataRepository,
    create_some_data,
    caplog,
):
    _ = await create_some_data(
        model=SomeDataA,
        quantity=3,
    )

    # Should raise exception in method because of abstract model BaseA
    result_orm = await some_data_repo.get_all_by_model_raw(model=BaseA)

    assert len(result_orm) == 0
    assert "Error on getting data" in caplog.text


async def test_create_creates_and_returns_obj(
    some_data_repo: SomeDataRepository,
):
    obj = SomeDataA(id=1, name="test")
    result = await some_data_repo.create(obj=obj)

    assert SomeData.model_validate(result) == SomeData.model_validate(obj)
