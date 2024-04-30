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

    async def update_statistic(self, s: AsyncSession, post_id: str, action: str):
        resp = await s.execute(select(self.model).where(self.model.post_id == post_id))
        obj = resp.scalars().one_or_none()

        if action == 'like':
            resp = await s.execute(update(self.model).where(self.model.post_id == post_id).values(
                like_count=obj.like_count + 1
            ))
        else:
            resp = await s.execute(update(self.model).where(self.model.post_id == post_id).values(
                watch_count=obj.watch_count + 1
            ))
        
        await s.commit()

    async def check_if_exist_by_post_id(self, s: AsyncSession, post_id: str):
        resp = await s.execute(select(self.model).where(self.model.post_id == post_id))
        obj = resp.scalars().one_or_none()

        if obj is None:
            return False
        return True


