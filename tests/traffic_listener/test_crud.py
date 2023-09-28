from typing import ClassVar
from urllib.parse import urlparse

import pytest
from faker import Faker

from src.traffic_listener.crud import link_db

fk = Faker()


class TestCRUDDomain:
    """Класс с собранием тестов для CRUDDomain.

    **Параметры**

    *length_urls* - длина списка ссылок

    *input_urls* - список с тестовыми доменами
    """

    length_urls: ClassVar[int] = 200
    input_urls: ClassVar[list[str]] = [fk.url() for _ in range(length_urls)]

    @pytest.mark.asyncio()
    async def test_create_many(self) -> None:
        """Тестирование функции CRUDDomain.create_many."""
        result = await link_db.create_many(self.input_urls)
        assert result == self.input_urls

    @pytest.mark.asyncio()
    async def test_get_by_time_delta(self) -> None:
        """Тестирование функции CRUDDomain.get_by_time_delta.

        Предполагается, что все заданые в input_urls ссылки попадут в диапазон по умолчанию
        """
        result = await link_db.get_unique_domains_by_period()
        waiting_result = list({urlparse(link).hostname for link in self.input_urls})

        assert result.sort() == waiting_result.sort()
