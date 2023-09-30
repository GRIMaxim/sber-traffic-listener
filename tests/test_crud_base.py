from datetime import UTC, datetime
from typing import Any, ClassVar

import pytest
from faker import Faker
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
from src.crud import CRUDBase

fk = Faker()


class DBTestModel(Base):
    """Схема данных для тестов."""

    __tablename__ = "test_table"

    some_string: Mapped[str] = mapped_column(nullable=True)
    some_int: Mapped[int] = mapped_column(nullable=True)
    some_default_int: Mapped[int] = mapped_column(default=fk.random_int())
    some_date: Mapped[datetime] = mapped_column(nullable=True)
    some_default_date: Mapped[datetime] = mapped_column(
        __type_pos=TIMESTAMP(timezone=True), default=datetime.now(tz=UTC),
    )


class CreateTestModel(BaseModel):
    """Pydantic-модель для создания данных."""

    some_string: str | None
    some_int: int | None
    some_date: datetime | None


class UpdateTestModel(CreateTestModel):
    """Pydantic-модель для обновления данных."""

    pk: int


class CRUDTest(CRUDBase[DBTestModel, CreateTestModel, UpdateTestModel]):
    """Инициализация класса CRUD для тестовой схемы данных."""


test_db = CRUDTest(DBTestModel)


class TestCRUDBase:
    """Класс с собранием тестов, относящимся к CRUDBase.

    **Параметры**

    *items_limit* - количество создаваемых строк

    *input_data* - список из items_limit элементов, генерируемых с помощью faker
    """

    items_limit: ClassVar[int] = 100
    input_data: ClassVar[list[dict[str, Any]]] = [
        {
            "some_string": fk.name(),
            "some_int": fk.random_int(),
            "some_date": fk.date_time(),
        }
        for _ in range(items_limit)
    ]

    @pytest.mark.asyncio()
    async def test_create_get(self) -> None:
        """Тестирование функции CRUDBase.create() и get()."""
        for ind_data in range(self.items_limit):
            if ind_data % 2 != 0:
                await test_db.create(self.input_data[ind_data])
            else:
                data_in = CreateTestModel(**self.input_data[ind_data])
                await test_db.create(data_in)

        for ind_data in range(1, self.items_limit + 1):
            data_out = await test_db.get(pk=ind_data)
            assert data_out
            assert data_out.some_string == self.input_data[ind_data - 1]["some_string"]
            assert data_out.some_int == self.input_data[ind_data - 1]["some_int"]
            assert data_out.some_date == self.input_data[ind_data - 1]["some_date"]
            assert data_out.some_default_int
            assert data_out.some_default_date

        data = await test_db.get(pk=self.items_limit + 1000000)
        assert data is None

    @pytest.mark.asyncio()
    async def test_get_all(self) -> None:
        """Тестирование функции CRUDBase.get_all()."""
        data_out = await test_db.get_all(limit=self.items_limit)
        assert data_out

        for ind_data in range(self.items_limit):
            assert (
                data_out[ind_data].some_string
                == self.input_data[ind_data]["some_string"]
            )
            assert data_out[ind_data].some_int == self.input_data[ind_data]["some_int"]
            assert (
                data_out[ind_data].some_date == self.input_data[ind_data]["some_date"]
            )
            assert data_out[ind_data].some_default_int
            assert data_out[ind_data].some_default_date

        data = await test_db.get_all(
            offset=self.items_limit + 100, limit=self.items_limit + 120,
        )
        assert not data

    @pytest.mark.asyncio()
    async def test_update(self) -> None:
        """Тестирование функции CRUDBase.update()."""
        for i in range(2):
            update_data = {
                "pk": 1,
                "some_string": fk.name(),
                "some_int": fk.random_int(),
                "some_date": fk.date_time(),
            }

            await test_db.update(
                update_data if i == 0 else UpdateTestModel(**update_data),
            )

            get_updated_data = await test_db.get(pk=update_data["pk"])

            assert get_updated_data
            assert get_updated_data.some_string == update_data["some_string"]
            assert get_updated_data.some_int == update_data["some_int"]
            assert get_updated_data.some_date == update_data["some_date"]
            assert get_updated_data.some_default_int
            assert get_updated_data.some_default_date

    @pytest.mark.asyncio()
    async def test_delete(self) -> None:
        """Тестирование функции CRUDBase.delete()."""
        delete_pk = 1
        await test_db.delete(pk=delete_pk)

        deleted_data = await test_db.get(pk=delete_pk)
        assert deleted_data is None
