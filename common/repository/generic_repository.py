from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from typing import TypeVar, Generic

from sqlalchemy import select, and_, update, func
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

    async def get_username_by_id(self, s: AsyncSession, id: int):
        resp = await s.execute(select(self.model).where(self.model.id == id))
        obj = resp.scalars().one_or_none()
        return obj.username

    async def get_statistic(self, s: AsyncSession, post_id: str):
        resp_count_like = await s.execute(select(func.count()).where(
            self.model.post_id == post_id,
            self.model.action == "like"
            )
        )

        resp_count_view = await s.execute(select(func.count()).where(
            self.model.post_id == post_id,
            self.model.action == "view"
            )
        )

        like_count = resp_count_like.scalar()
        view_count = resp_count_view.scalar()

        return like_count, view_count

    async def get_popular_posts(self, s: AsyncSession, search_type: str):
        resp = await s.execute(
            select(self.model.post_id, self.model.author, func.count(self.model.post_id).label('count_actions'))
            .where(self.model.action == search_type)
            .group_by(self.model.post_id, self.model.author)
            .order_by(func.count(self.model.post_id).desc())
            .limit(5)
        )

        popular_posts = resp.fetchall()

        return popular_posts

    async def get_popular_users(self, s: AsyncSession):
        resp = await s.execute(
            select(self.model.author, func.count(self.model.author).label('likes'))
            .where(self.model.action == 'like')
            .group_by(self.model.author)
            .order_by(func.count(self.model.author).desc())
            .limit(3)
        )

        popular_users = resp.fetchall()

        return popular_users

    async def check_if_exist_by_post_id(self, s: AsyncSession, post_id: str):
        resp = await s.execute(select(self.model).where(self.model.post_id == post_id))
        obj = resp.scalars().one_or_none()

        if obj is None:
            return False
        return True

    async def check_if_like_unique(self, s: AsyncSession, post_id: str, username: str, action: str):
        resp = await s.execute(
            select(self.model)
            .where(
                self.model.post_id == post_id, 
                self.model.username == username,
                self.model.action == action
                ))

        obj = resp.scalars().one_or_none()

        if obj is None:
            return True
        return False
