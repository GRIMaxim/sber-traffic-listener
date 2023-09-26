from sqlalchemy.orm import Mapped, mapped_column

from ..database_config import Base


class Domain(Base):

    visit_time: Mapped[int]
    domain: Mapped[str]
