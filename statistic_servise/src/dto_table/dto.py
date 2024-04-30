from pydantic import BaseModel


class StatisticModel(BaseModel):
    post_id: str
    watch_count: int
    like_count: int
