from typing import ClassVar

import pytest
from faker import Faker

from src.traffic_listener.crud import link_db
from src.traffic_listener.schemas import LinkCreateMany

fk = Faker()


class TestCRUDLink:
    """Класс с собранием тестов для CRUDLink.

    **Параметры**

    *length_urls* - длина списка ссылок

    *input_urls* - список с тестовыми доменами
    """

    length_urls: ClassVar[int] = 200
    input_urls: ClassVar[LinkCreateMany] = LinkCreateMany(links=[fk.url() for _ in range(length_urls)])

    @pytest.mark.asyncio()
    async def test_create_many(self) -> None:
        """Тестирование функции CRUDDomain.create_many."""
        await link_db.create_many(self.input_urls)
        result = await link_db.get_all(limit=self.length_urls)
        assert [link.unicode_string() for link in self.input_urls.links] == [link.link for link in result]

    @pytest.mark.asyncio()
    async def test_get_by_time_delta(self) -> None:
        """Тестирование функции CRUDDomain.get_by_time_delta.

        Предполагается, что все заданые в input_urls ссылки попадут в диапазон по умолчанию
        """
        result = await link_db.get_unique_domains_by_period()
        waiting_result = list({link.unicode_string() for link in self.input_urls.links})

        assert sorted(result) == waiting_result.sort()
