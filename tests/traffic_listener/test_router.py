from typing import TYPE_CHECKING

import pytest
from fastapi import status
from async_asgi_testclient import TestClient
from faker import Faker

from src.traffic_listener.constants import ErrorMessages

if TYPE_CHECKING:
    from httpx import Response

fk = Faker()


class TestRouter:
    """Класс с собранием тестов для роутера traffic_listener."""

    @pytest.mark.asyncio()
    async def test_add_visited_links(self, client: TestClient) -> None:
        """Тестирование добавления посещенных ссылок."""
        response: Response = await client.post("/visited_links", json={"links": [fk.url() for _ in range(5)]})
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["status"] == "ok"

    @pytest.mark.asyncio()
    async def test_add_empty_list(self, client: TestClient) -> None:
        """Попытка добавления пустого списка ссылок."""
        response: Response = await client.post("/visited_links", json={"links": []})
        assert response.status_code == status.HTTP_411_LENGTH_REQUIRED
        response_data = response.json()
        assert response_data["status"] == ErrorMessages.list_is_empty

    @pytest.mark.asyncio()
    async def test_add_words(self, client: TestClient) -> None:
        """Попытка добавления списка слов вместо ссылок."""
        response: Response = await client.post("/visited_links", json={"links": [fk.name() for _ in range(5)]})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        assert response_data["status"] == ErrorMessages.list_contains_only_words

    @pytest.mark.asyncio()
    async def test_get_unique_domains_by_period(self, client: TestClient) -> None:
        """Тестирование получения уникальных доменов по заданному диапазону."""
        response: Response = await client.get("/visited_links")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "domains" in response_data

    @pytest.mark.asyncio()
    async def test_get_unique_domains_by_replace_period(self, client: TestClient) -> None:
        """Попытка получения доменов с параметрами start > end."""
        response: Response = await client.get("/visited_links?from=100&to=1")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        assert response_data["status"] == ErrorMessages.incorrect_parameters

