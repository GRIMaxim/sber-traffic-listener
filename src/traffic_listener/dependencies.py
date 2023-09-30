from typing import Annotated
from collections.abc import Sequence

from fastapi import Query

from .exceptions import IncorrectParametersError


async def check_parameters(start: Annotated[int | None, Query(alias="from")] = None,
                           end: Annotated[int | None, Query(alias="to")] = None) \
        -> Sequence[int | None]:
    """Валидация на корректность ввода параметров."""
    if start and end and start > end:
        raise IncorrectParametersError
    return start, end
