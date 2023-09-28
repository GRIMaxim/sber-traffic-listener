from asyncio import AbstractEventLoop, get_event_loop_policy
from collections.abc import Iterator

import pytest
import pytest_asyncio
from async_asgi_testclient import TestClient

from src.main import main_app


@pytest.fixture(autouse=True, scope="session")
def _run_migrations() -> Iterator[None]:
    """Запуск миграций для тестовой базы данных и дальнейшее их удаление."""
    from pathlib import Path

    from alembic import command
    from alembic.config import Config

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    revision = command.revision(
        alembic_cfg, message="test_table_init", autogenerate=True,
    )
    command.upgrade(alembic_cfg, "head")

    yield

    command.downgrade(alembic_cfg, "-1")
    if revision is not None:
        if isinstance(revision, list):
            for rev in revision:
                if rev:
                    Path(rev.path).unlink()
        else:
            Path(revision.path).unlink()


@pytest.fixture(autouse=True, scope="session")
def event_loop() -> Iterator[AbstractEventLoop]:
    """Получение цикла событий."""
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def client() -> TestClient:
    """Создание клиента для тестов."""
    host, port = "127.0.0.1", "8091"
    scope = {"clien": (host, port)}
    async with TestClient(main_app, scope=scope) as client:
        yield client
