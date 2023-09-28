from pydantic import BaseModel, ConfigDict


class LinkCreate(BaseModel):
    """Модель запроса для создания записи в таблице Link."""

    link: str


class LinkCreateMany(BaseModel):
    """Модель запроса для создания нескольких записей в таблице Link."""

    links: list[str]

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "links": [
                    "http://yandex.ru/1",
                    "https://ya.ru/maps",
                    "http://sber.com/"
                ],
            },
            ],
        },
    }


class LinkRead(LinkCreate):
    """Модель ответа для записи из таблицы Link."""

    visit_time: int
    model_config = ConfigDict(from_attributes=True)


class LinkUpdate(LinkRead):
    """Модель запроса на изменение записи в таблице Link."""


class DomainReadAll(BaseModel):
    """Модель ответа при запросе доменов."""

    domains: list[str]

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "domains": [
                    "yandex.ru",
                    "ya.ru",
                    "sber.com"
                ],
            },
            ],
        },
    }
