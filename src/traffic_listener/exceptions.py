from fastapi import Request, status
from fastapi.responses import JSONResponse

from .constants import ErrorMessages


class ListIsEmptyError(Exception):
    """Исключение используется в случае, если список ссылок пуст."""


class ListIsNotContainsLinksError(Exception):
    """Исключение используется в случае, если список ссылок содержит только слова."""


class IncorrectParametersError(Exception):
    """Исключение используется в случае, если параметр *from* больше, чем *to*."""


async def empty_list_exception_handler(request: Request, exc: ListIsEmptyError) -> JSONResponse:  # noqa: ARG001
    """Обработчик для исключения ListIsEmptyError."""
    return JSONResponse(status_code=status.HTTP_411_LENGTH_REQUIRED,
                        content={"status": ErrorMessages.list_is_empty})


async def word_list_exception_handler(request: Request, # noqa: ARG001
                                      exc: ListIsNotContainsLinksError) -> JSONResponse:  # noqa: ARG001
    """Обработчик для исключения ListIsNotContainsLinksError."""
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content={"status": ErrorMessages.list_contains_only_words})


async def incorrect_parameters_exception_handler(request: Request, # noqa: ARG001
                                                 exc: ListIsNotContainsLinksError) -> JSONResponse:  # noqa: ARG001
    """Обработчик для исключения IncorrectParametersError."""
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content={"status": ErrorMessages.incorrect_parameters})
