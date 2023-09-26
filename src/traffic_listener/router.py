from fastapi import APIRouter, status

from ..default_responses import OkResponse
from schemas import DomainCreateMany, DomainReadAll
from crud import domain_db

router = APIRouter()


@router.post(
    "/visited_links", status_code=status.HTTP_201_CREATED, response_model=OkResponse
)
async def add_links(links: DomainCreateMany):
    await domain_db.create_many(links)
    return OkResponse


@router.get("/visited_links", status_code=status.HTTP_200_OK, response_model=DomainReadAll)
async def get_links_by_period(start: int, end: int):
    await domain_db.get_by_time_delta(start, end)
    return {"message": "hello"}
