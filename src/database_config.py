import os

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from dotenv import load_dotenv

from src.constants import DB_NAMING_CONVENTION

load_dotenv()

db_url: str = (
    f"{os.getenv('PG_DRIVERNAME')}://"
    f"{os.getenv('PG_USER')}:{os.getenv('PG_PASS')}@"
    f"{os.getenv('PG_HOST', default='localhost')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DATABASE')}"
)
engine: AsyncEngine = create_async_engine(db_url, echo=os.getenv("F_TEST") == "true", future=True)
async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
my_metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)


class Base(AsyncAttrs, DeclarativeBase):
    """Базовый класс для всех создаваемых схем данных."""

    metadata = my_metadata

    pk: Mapped[int] = mapped_column(primary_key=True)
