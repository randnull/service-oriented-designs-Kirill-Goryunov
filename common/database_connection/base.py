from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config.settings import settings


DATABASE_USER = settings.POSTGRES_USER
DATABASE_PASSWORD = settings.POSTGRES_PASSWORD
DATABASE_NAME = settings.POSTGRES_DB
DATABASE_HOST = settings.POSTGRES_HOST

DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = sessionmaker(bind=engine, class_=AsyncSession)

Base = declarative_base()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
