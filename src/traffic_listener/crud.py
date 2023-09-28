from collections.abc import Sequence
from urllib.parse import urlparse
from time import time

from sqlalchemy import insert, select

from src.crud_base import CRUDBase
from src.utils import async_execute
from .database import Link
from .schemas import LinkCreate, LinkUpdate


class CRUDLink(CRUDBase[Link, LinkCreate, LinkUpdate]):
    """Расширение CRUDBase для таблицы Link."""

    async def create_many(self, data_in: Sequence[str]) -> list[str]:
        """Запись нескольких ссылок в таблицу Link."""
        values = [{"visit_time": int(time()), "link": link} for link in data_in]

        query = insert(self.model).values(values).returning(self.model.link)
        result = await async_execute(query)
        created_links: list[str] = [link[0] for link in result.all()]

        return created_links

    async def get_unique_domains_by_period(self, start: int | None = None, end: int | None = None) -> list[str]:
        """Получение списка уникальных доменов из таблицы Link по заданному диапазону.

        **Параметры**

        *start* - минимальное значение диапазона для получения доменов.
        Если start не задан, установится значение end - 10 (секунд)

        *end* - максимально значение диапазона для получения доменов.
        Если end не задан, установится значение int(time()) на момент вызова
        """
        if not end:
            end = int(time())
        if not start:
            start = end - 10

        query = select(self.model.link).where((self.model.visit_time >= start) & (self.model.visit_time <= end))
        result = await async_execute(query)
        getting_links: list[str] = [link[0] for link in result.all()]
        return list(
            {domain for link in getting_links if (domain := urlparse(link).hostname) is not None})



link_db = CRUDLink(Link)
