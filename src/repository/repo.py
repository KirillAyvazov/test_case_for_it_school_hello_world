import httpx
from fastapi import status, HTTPException

from src.settings import settings
from src.database.db_repo import db_repo
from src.schemas.hero import HeroSchema
from src.schemas.filter import HeroFilter


class Repository:
    def __init__(self):
        self._db_repo = db_repo
        self._url_external_api = settings.EXTERNAL_API

    async def add_hero(self, name: str) -> None:
        """Метод добавления нового героя"""
        name = self._adapted_name(name)

        if await self._db_repo.check_hero(name):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A hero with that name already exists")

        result = await self._get_from_external_api(name)

        if result.get("response") == "error":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        list_hero_schema = self._parse_response(result, name)
        if len(list_hero_schema) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        await self._db_repo.save_heroes(list_hero_schema)

    async def _get_from_external_api(self, name: str) -> dict:
        """Метод для обращения к стороннему API"""
        path = "".join([self._url_external_api, name])

        async with httpx.AsyncClient() as client:
            result = await client.get(path)
            return result.json()

    @staticmethod
    def _parse_response(response: dict, hero_name: str) -> list[HeroSchema]:
        """
            Метод извлекает из ответа стороннего API только тех героев, у которых имя полностью совпадает с переданным
        пользователем
        """
        filtered_result = filter(lambda hero: hero.get("name", "") == hero_name,
                                 response.get("results", []))
        return [HeroSchema(**i_hero) for i_hero in filtered_result]

    @staticmethod
    def _adapted_name(name: str) -> str:
        """Метод адаптирует введённое пользователем имя героя к нормальному виду"""
        return " ".join([i_word.capitalize() if i_word[-1].islower() else i_word for i_word in name.split(" ")])

    async def get_hero(self, filters: HeroFilter) -> list[HeroSchema]:
        """Метод получения списка героев с фильтрацией"""
        result = await self._db_repo.get_hero(filters)
        if len(result) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return [HeroSchema(**i_hero.__dict__) for i_hero in result]


repo = Repository()


def get_repo() -> Repository:
    return repo
