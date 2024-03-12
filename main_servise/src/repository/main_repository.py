from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from typing import TypeVar, Generic

from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel


T = TypeVar('T')


class Repository(Generic[T]):
    def __init__(self, model):
        self.model = model
    
    async def get(self, s: AsyncSession, username: str) -> T:
        resp = await s.execute(select(self.model).where(self.model.username == username))
        return resp.scalars().one_or_none()

    async def add(self, s: AsyncSession, model: BaseModel):
        result_dao = self.model.to_dao(model)
        s.add(result_dao)
        await s.flush()
        await s.commit()

    async def update_info(self, s: AsyncSession, id: int, new_values):
        await s.execute(update(self.model).where(self.model.id == id).values(new_values))
        await s.commit()

    async def get_id_by_username(self, s: AsyncSession, username: str):
        resp = await s.execute(select(self.model).where(self.model.username == username))
        obj = resp.scalars().one_or_none()
        return getattr(obj, 'id')
