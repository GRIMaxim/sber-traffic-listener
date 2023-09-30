from collections.abc import Sequence
from time import time

from sqlalchemy import insert, select
from pydantic import AnyUrl

from src.crud import CRUDBase
from src.utils import async_execute
from .database import Link
from .schemas import LinkCreate, LinkUpdate, LinkCreateMany


class CRUDLink(CRUDBase[Link, LinkCreate, LinkUpdate]):
    """Расширение CRUDBase для таблицы Link."""

    async def create_many(self, data_in: LinkCreateMany) -> None:
        """Запись нескольких ссылок в таблицу Link."""
        values = [{"visit_time": int(time()), "link": link.unicode_string(), "domain": link.host} for link in data_in.links]

        query = insert(self.model).values(values).returning(self.model.link)
        await async_execute(query)

    async def get_unique_domains_by_period(self, start: int | None = None, end: int | None = None) -> Sequence[str]:
        """Получение списка уникальных доменов из таблицы Link по заданному диапазону.

        **Параметры**

        *start* - минимальное значение диапазона для получения доменов.
        Если start не задан, установится значение end-10 (секунд)

        *end* - максимально значение диапазона для получения доменов.
        Если end не задан, установится значение int(time()) на момент вызова
        """
        if not end:
            end = int(time())
        if not start:
            start = end - 10

        query = (select(self.model.domain).
                 where((self.model.visit_time >= start) & (self.model.visit_time <= end)).
                 distinct())
        result = await async_execute(query)
        return result.scalars().all()


link_db = CRUDLink(Link)
