from pydantic import BaseModel

from .constants import ErrorMessages


class ListIsEmpty(BaseModel):
    """Модель ответа для ошибки ListIsEmptyError (используется только для документации)."""

    status: str = ErrorMessages.list_is_empty


class ListContainOnlyWords(BaseModel):
    """Модель ответа для ошибки ListIsNotContainsLinksError (используется только для документации)."""

    status: str = ErrorMessages.list_contains_only_words


class IncorrectParameters(BaseModel):
    """Модель ответа для ошибки IncorrectParametersError (используется только для документации)."""

    status: str = ErrorMessages.incorrect_parameters
