from pydantic import BaseModel, ConfigDict, AnyUrl, Field
from .constants import ErrorMessages


class LinkCreate(BaseModel):
    """Модель запроса для создания записи в таблице Link."""

    link: AnyUrl


class LinkCreateMany(BaseModel):
    """Модель запроса для создания нескольких записей в таблице Link."""

    links: list[AnyUrl] = Field(
        min_length=1,
        json_schema_extra={
            "examples": [
                [
                    "http://yandex.ru/1",
                    "http://yandex.ru/2",
                    "http://yandex.ru/3",
                ],
            ],
        },
    )


class LinkRead(LinkCreate):
    """Модель ответа для записи из таблицы Link."""

    visit_time: int
    model_config = ConfigDict(from_attributes=True)


class LinkUpdate(LinkRead):
    """Модель запроса на изменение записи в таблице Link."""


class DomainReadAll(BaseModel):
    """Модель ответа при запросе доменов."""

    domains: list[str] = Field(
        json_schema_extra={
            "examples": [
                [
                    "yandex.ru",
                    "ya.ru",
                    "sber.com",
                ],
            ],
        },
    )
    status: str


class IncorrectLinks(BaseModel):
    """Модель ответа при возникновении ошибки с ссылками."""

    status: str = ErrorMessages.incorrect_links


class IncorrectParameters(BaseModel):
    """Модель ответа при возникновении ошибки."""

    status: str = ErrorMessages.incorrect_parameters
