from collections.abc import Sequence

from fastapi import APIRouter, status, Depends

from src.schemas import OkResponse
from .schemas import DomainReadAll, ListIsEmpty, ListContainOnlyWords, IncorrectParameters
from .constants import ErrorMessages
from .crud import link_db
from .dependencies import check_links, check_parameters

router = APIRouter()


@router.post(
    "/visited_links",
    status_code=status.HTTP_201_CREATED,
    response_model=OkResponse,
    tags=["Link"],
    description="Add visited links into database",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ListContainOnlyWords,
            "detail": ErrorMessages.list_contains_only_words,
        },
        status.HTTP_411_LENGTH_REQUIRED: {
            "model": ListIsEmpty,
            "detail": ErrorMessages.list_is_empty,
        },
    },
)
async def add_visited_links(links: list[str] = Depends(check_links)) -> type[OkResponse]:  # noqa: B008
    """Обработчик для добавления посещенных ссылок в бд."""
    await link_db.create_many(links)
    return OkResponse


@router.get("/visited_links",
            status_code=status.HTTP_200_OK,
            response_model=DomainReadAll,
            tags=["Link"],
            description="Get unique domains by period",
            responses={
                status.HTTP_400_BAD_REQUEST: {
                    "model": IncorrectParameters,
                    "detail": ErrorMessages.incorrect_parameters,
                },
            },
            )
async def get_unique_domains_by_period(params: Sequence[int | None] = Depends(check_parameters)) \
        -> dict[str, list[str]]:
    """Обработчик для получения доменов из бд по заданному диапазону."""
    domains = await link_db.get_unique_domains_by_period(*params)
    return {"domains": domains}
