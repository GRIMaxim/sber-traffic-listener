from pydantic import BaseModel, ConfigDict


class LinkCreate(BaseModel):
    """Модель запроса для создания записи в таблице Link."""

    link: str


class LinkCreateMany(BaseModel):
    """Модель запроса для создания нескольких записей в таблице Link."""

    links: list[str]


class LinkRead(LinkCreate):
    """Модель ответа для записи из таблицы Link."""

    visit_time: int
    model_config = ConfigDict(from_attributes=True)


class LinkUpdate(LinkRead):
    """Модель запроса на изменение записи в таблице Link."""


class DomainReadAll(BaseModel):
    """Модель ответа при запросе доменов."""

    domains: list[str]
