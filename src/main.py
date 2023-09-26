from fastapi import FastAPI

from .traffic_listener.router import router as tl_router


def get_app() -> FastAPI:
    """Функция для инициализации и конфигурации приложения FastAPI."""
    app = FastAPI()
    app.include_router(tl_router)
    return app


main_app = get_app()
