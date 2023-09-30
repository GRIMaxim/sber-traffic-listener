from sqlalchemy.orm import Mapped

from src.database import Base


class Link(Base):
    """Схема данных для таблицы ссылок, посещенных пользователем."""

    __tablename__ = "link"

    visit_time: Mapped[int]
    link: Mapped[str]
    domain: Mapped[str]
