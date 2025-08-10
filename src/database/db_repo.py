from typing import Optional

from sqlalchemy import select

from src.database.db_connect import async_session
from src.database.model import HeroModel
from src.schemas.filter import HeroFilter


class DataBaseRepository:
    def __init__(self):
        self._session = async_session

    async def check_hero(self, name: str) -> Optional[HeroModel]:
        """Метод проверяет существование в базе данных героя с указанным именем"""
        query = select(HeroModel).where(HeroModel.name == name)

        async with self._session as session:
            result = await session.execute(query)
            return result.scalar()

    async def save_heroes(self, list_hero_schema: list[HeroModel]) -> None:
        """Метод для сохранения списка героев в бд"""
        async with self._session as session:
            for i_hero in list_hero_schema:
                session.add(HeroModel(**i_hero.model_dump()))

            await session.commit()

    async def get_hero(self, filters: HeroFilter) -> list[HeroModel]:
        """Метод для получения героев из БД"""
        base_query = select(HeroModel)
        query = filters.filter(base_query)

        async with self._session as session:
            result = await session.execute(query)
            return result.scalars().all()


db_repo = DataBaseRepository()
