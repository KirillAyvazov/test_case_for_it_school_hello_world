from typing import Optional

from pydantic import BaseModel, model_validator


class HeroSchema(BaseModel):
    id: int
    name: str
    intelligence: Optional[int] = None
    strength: Optional[int] = None
    speed: Optional[int] = None
    power: Optional[int] = None

    @model_validator(mode="before")
    def change_input_data(self):
        if isinstance(self, dict) and "powerstats" in self.keys():
            for i_field in ["intelligence", "strength", "speed", "power"]:
                if self.get("powerstats", {}).get(i_field) == "null":
                    self["powerstats"][i_field] = None

            self.update(self.pop("powerstats"))

        return self
