from fastapi import APIRouter, status


router = APIRouter()


@router.post("/visited_links", status_code=status.HTTP_201_CREATED)
async def add_links():
    pass


@router.get("/visited_links", status_code=status.HTTP_200_OK)
async def get_links_by_period(start: int, end: int):
    pass
