from typing import Any
from collections.abc import AsyncIterator
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from sqlalchemy import Executable
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.database_config import async_session_maker


@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    """Генератор асинхронных сессий бд."""
    try:
        async_session = async_session_maker

        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()


async def async_execute(query: Executable) -> Result[Any]:
    """Курсор для ввода SQL-запросов."""
    async_session: AbstractAsyncContextManager[AsyncSession] = get_session()
    async with async_session as session:
        query_result = await session.execute(query)
        await session.commit()
    return query_result
