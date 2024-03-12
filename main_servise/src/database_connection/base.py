from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_USER = os.environ['POSTGRES_USER']
DATABASE_PASSWORD = os.environ['POSTGRES_PASSWORD']
DATABASE = os.environ['POSTGRES_DB']

DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@postgresql/{DATABASE}"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = sessionmaker(bind=engine, class_=AsyncSession)

Base = declarative_base()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
