from typing import Optional

from sqlalchemy import and_
from sqlalchemy.sql.selectable import Select
from fastapi_filter.base.filter import BaseFilterModel, field_validator

from src.database.model import HeroModel


class HeroFilter(BaseFilterModel):
    name: Optional[str] = None
    intelligence: Optional[int] = None
    intelligence_gte: Optional[int] = None
    intelligence_lte: Optional[int] = None
    strength: Optional[int] = None
    strength_gte: Optional[int] = None
    strength_lte: Optional[int] = None
    speed: Optional[int] = None
    speed_gte: Optional[int] = None
    speed_lte: Optional[int] = None
    power: Optional[int] = None
    power_gte: Optional[int] = None
    power_lte: Optional[int] = None

    @field_validator("name")
    def adapted_name(cls, name: str) -> str:
        return " ".join([i_word.capitalize() if i_word[-1].islower() else i_word for i_word in name.split(" ")])

    def filter(self, query: Select) -> Select:
        conditions = []
        for i_field_name in self.__fields__:
            i_field_value = getattr(self, i_field_name)
            if i_field_value is None:
                continue

            if isinstance(i_field_value, str):
                conditions.append(getattr(HeroModel, i_field_name) == i_field_value)

            elif isinstance(i_field_value, int):
                if "gte" in i_field_name:
                    conditions.append(getattr(HeroModel, i_field_name.split("_")[0]) >= i_field_value)
                elif "lte" in i_field_name:
                    conditions.append(getattr(HeroModel, i_field_name.split("_")[0]) <= i_field_value)
                else:
                    conditions.append(getattr(HeroModel, i_field_name) == i_field_value)

        query = query.filter(and_(*conditions))

        return query
