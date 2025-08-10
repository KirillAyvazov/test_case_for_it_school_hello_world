import time

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.settings import settings
from src.database.model import Base
from src.project_logger.log_config import get_logger


logger = get_logger(__name__)

engine = create_async_engine(settings.DB_URI)


async_sessionmaker = sessionmaker(engine, class_=AsyncSession)
async_session = async_sessionmaker()


async def create_tables():
    for count in range(1, 4):
        time.sleep(2)
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        except Exception:
            logger.info(f"Попытка подключения к базе данных {count}")
        else:
            logger.info("Подключение к базе данных установлено")
            break
    else:
        logger.error("Не удалось подключиться к базе данных")
