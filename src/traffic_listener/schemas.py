from pydantic import BaseModel
from pydantic.fields import Field


class DomainCreate(BaseModel):
    link: str = Field()


class DomainRead(DomainCreate):
    pass


class DomainUpdate(DomainCreate):
    pk: int


class DomainReadAll(BaseModel):
    domains: list[DomainRead]


class DomainCreateMany(BaseModel):
    links: list[DomainCreate]
