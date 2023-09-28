from pydantic import BaseModel


class OkResponse(BaseModel):
    """Стандарный ответ для статуса 200."""

    status: str = "ok"
