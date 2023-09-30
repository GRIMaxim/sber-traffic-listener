from typing import TYPE_CHECKING

import pytest
from fastapi import status
from httpx import AsyncClient
from faker import Faker

from src.traffic_listener.constants import ErrorMessages

if TYPE_CHECKING:
    from httpx import Response

fk = Faker()


class TestRouter:
    """Класс с собранием тестов для роутера traffic_listener."""

    @pytest.mark.asyncio()
    async def test_add_visited_links(self, client: AsyncClient) -> None:
        """Тестирование добавления посещенных ссылок."""
        response: Response = await client.post("/visited_links", json={"links": [fk.url() for _ in range(5)]})
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["status"] == "ok"

    @pytest.mark.asyncio()
    async def test_add_empty_list(self, client: AsyncClient) -> None:
        """Попытка добавления пустого списка ссылок."""
        response: Response = await client.post("/visited_links", json={"links": []})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        assert response_data["status"] == ErrorMessages.incorrect_links

    @pytest.mark.asyncio()
    async def test_add_words(self, client: AsyncClient) -> None:
        """Попытка добавления списка слов вместо ссылок."""
        response: Response = await client.post("/visited_links", json={"links": [fk.name() for _ in range(5)]})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        assert response_data["status"] == ErrorMessages.incorrect_links

    @pytest.mark.asyncio()
    async def test_get_unique_domains_by_period(self, client: AsyncClient) -> None:
        """Тестирование получения уникальных доменов по заданному диапазону."""
        response: Response = await client.get("/visited_links")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "domains" in response_data

    @pytest.mark.asyncio()
    async def test_get_unique_domains_by_replace_period(self, client: AsyncClient) -> None:
        """Попытка получения доменов с параметрами start > end."""
        response: Response = await client.get("/visited_links?from=100&to=1")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        assert response_data["status"] == ErrorMessages.incorrect_parameters

    @pytest.mark.asyncio()
    async def test_get_empty_domains(self, client: AsyncClient) -> None:
        """Полученный список доменнов оказался пустым."""
        response: Response = await client.get("/visited_links?from=1&to=2")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == ErrorMessages.empty_result

