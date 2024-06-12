import pytest
from fastapi import status

from app.models import SomeDataA, SomeDataB


@pytest.mark.skip(reason="Not working because of bug in pytest-asyncio")
async def test_get_some_data_return_list_of_data(
    client, router, create_some_data,
):
    _ = await create_some_data(model=SomeDataA, quantity=2)
    _ = await create_some_data(model=SomeDataB, quantity=4)

    url = router.url_path_for("get_some_data")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 6


@pytest.mark.skip(reason="Not working because of bug in pytest-asyncio")
async def test_get_some_data_return_empty_list_if_no_data(
    client, router, create_some_data,
):
    url = router.url_path_for("get_some_data")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0
