from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from .traffic_listener.router import router as tl_router
from .traffic_listener.exceptions import (
    IncorrectParametersError,
    incorrect_parameters_exception_handler,
    incorrect_link_list_exception_handler,
)


def get_app() -> FastAPI:
    """Функция для инициализации и конфигурации приложения FastAPI."""
    app = FastAPI(title="Traffic listener")

    app.include_router(tl_router)
    app.add_exception_handler(
        RequestValidationError, incorrect_link_list_exception_handler,
    )
    app.add_exception_handler(
        IncorrectParametersError, incorrect_parameters_exception_handler,
    )

    return app


main_app = get_app()
