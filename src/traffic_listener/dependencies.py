from typing import Annotated
from collections.abc import Sequence
from urllib.parse import urlparse

from fastapi import Query

from .schemas import LinkCreateMany
from .exceptions import ListIsEmptyError, ListIsNotContainsLinksError, IncorrectParametersError


async def check_links(input_links: LinkCreateMany) -> list[str]:
    """Валидация на корректность ввода url (есть ли домен) и на пустой список."""
    links = [link for link in input_links.links if urlparse(link).hostname is not None]
    if not input_links.links:
        raise ListIsEmptyError
    if not links:
        raise ListIsNotContainsLinksError
    return links


async def check_parameters(start: Annotated[int | None, Query(alias="from")] = None,
                           end: Annotated[int | None, Query(alias="to")] = None) \
        -> Sequence[int | None]:
    """Валидация на корректность ввода параметров."""
    if start and end and start > end:
        raise IncorrectParametersError
    return start, end
