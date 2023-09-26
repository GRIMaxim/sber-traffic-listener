from time import time

from sqlalchemy import insert, select

from ..crud_base import CRUDBase
from ..utils import async_execute
from database import Domain
from schemas import DomainCreate, DomainUpdate, DomainCreateMany


class CRUDDomain(CRUDBase[Domain, DomainCreate, DomainUpdate]):
    async def create_many(self, data_in: DomainCreateMany) -> list[Domain]:

        data_in = [Domain(visit_time=int(time()), domain=domain) for domain in data_in]

        query = insert(self.model).values(**data_in).returning(self.model)
        result = await async_execute(query)
        created_links: list[Domain] = [link[0] for link in result.all()]

        return created_links

    async def get_by_time_delta(self, start: int, end: int) -> list[Domain]:

        query = select(self.model).where(start <= self.model.visit_time <= end)
        result = await async_execute(query)
        created_links: list[Domain] = [link[0] for link in result.all()]

        return created_links


domain_db = CRUDDomain(Domain)
