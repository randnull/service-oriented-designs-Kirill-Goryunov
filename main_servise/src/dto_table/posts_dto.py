from pydantic import BaseModel
import datetime
from typing import Optional


class NewPostModel(BaseModel):
    title: Optional[str]
    body: Optional[str]


class PostModel(BaseModel):
    id: Optional[str]
    user_id: Optional[int]
    title: Optional[str]
    body: Optional[str]
    created_at: datetime.datetime


class AllPosts(BaseModel):
    page_size: Optional[int]
    page_number: Optional[int]