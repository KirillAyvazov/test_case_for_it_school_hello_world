from datetime import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class HeroModel(Base):
    __tablename__ = 'hero'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    intelligence = Column(Integer, nullable=True)
    strength = Column(Integer, nullable=True)
    speed = Column(Integer, nullable=True)
    power = Column(Integer, nullable=True)
