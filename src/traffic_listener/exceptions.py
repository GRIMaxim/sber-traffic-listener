from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


from .constants import ErrorMessages


class IncorrectParametersError(Exception):
    """Исключение используется в случае, если параметр *from* больше, чем *to*."""


async def incorrect_link_list_exception_handler(request: Request, # noqa: ARG001
                                                 exc: RequestValidationError) -> JSONResponse:  # noqa: ARG001
    """Обработчик для исключений, связанных с некорректным списком ссылок."""
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        content=jsonable_encoder({"status": ErrorMessages.incorrect_links}))


async def incorrect_parameters_exception_handler(request: Request, # noqa: ARG001
                                                 exc: IncorrectParametersError) -> JSONResponse:  # noqa: ARG001
    """Обработчик для исключения IncorrectParametersError."""
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content={"status": ErrorMessages.incorrect_parameters})
