from collections.abc import Mapping, Sequence
from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update

from .database import Base
from .utils import async_execute

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый класс с методами CRUD (create, read, update, delete).

    **Параметры**

    *ModelType* - схема данных SQLAlchemy

    *CreateSchemaType* - модель Pydantic для создания строки БД

    *UpdateSchemaType* - модель Pydantic для обновления строки БД
    """

    def __init__(self, model: type[ModelType]) -> None:
        self._model = model

    @property
    def model(self) -> type[ModelType]:
        """Геттер для модели SQLAlchemy."""
        return self._model

    async def create(
        self,
        data_in: CreateSchemaType | Mapping[str, Any],
    ) -> None:
        """Создание новой строки бд.

        *data_in* - модель CreateSchemaType или Mapping, с полями в соответствии с ModelType
        """
        if isinstance(data_in, BaseModel):
            data_in = data_in.model_dump()

        query = insert(self.model).values(**data_in)
        await async_execute(query)

    async def get(self, pk: int) -> ModelType | None:
        """Получение строки бд по первичному ключу."""
        query = select(self.model).where(self.model.pk == pk)
        result = await async_execute(query)

        return result.scalar_one_or_none()

    async def get_all(
        self,
        *,
        offset: int | None = 0,
        limit: int | None = 100,
    ) -> Sequence[ModelType]:
        """Получение списка строк бд в соответствии с заданными параметрами.

        *offset* - параметр OFFSET как в SQL. Игнорируется, если None

        *limit* - параметр LIMIT как в SQL. Игнорируется, если None
        """
        query = select(self.model).offset(offset).limit(limit)
        result = await async_execute(query)
        return result.scalars().all()

    async def update(
        self,
        data_update: UpdateSchemaType | dict[str, Any],
    ) -> None:
        """Обновляет поля заданной строки бд.

        *data_update* - модель UpdateSchemaType или Mapping, с полями в соответствии с ModelType
        """
        if isinstance(data_update, BaseModel):
            data_update = data_update.model_dump()
        query = (
            update(self.model)
            .where(self.model.pk == data_update["pk"])
            .values(**data_update)
        )

        await async_execute(query)

    async def delete(self, pk: int) -> None:
        """Удаление строки бд по первичному ключу."""
        query = delete(self.model).where(self.model.pk == pk).returning(self.model)
        await async_execute(query)
