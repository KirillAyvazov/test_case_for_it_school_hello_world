from fastapi import APIRouter, Depends, HTTPException
from fastapi_filter import FilterDepends

from src.repository.repo import get_repo, Repository
from src.schemas.hero import HeroSchema
from src.schemas.filter import HeroFilter


router = APIRouter(prefix="/hero", tags=["Hero"])


@router.post("", status_code=201)
async def get_request(
    name: str,
    repo: Repository = Depends(get_repo),
) -> None:
    """Эндпоинт для добавления нового героя по имени"""
    try:
        return await repo.add_hero(name)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("", response_model=list[HeroSchema], status_code=200)
async def get_hero(
    filters: HeroFilter = FilterDepends(HeroFilter),
    repo: Repository = Depends(get_repo),
) -> list[HeroSchema]:
    """Эндпоинт для получения данных о героях"""
    try:
        return await repo.get_hero(filters)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
