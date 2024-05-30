from pydantic import BaseModel

class TopPostModel(BaseModel):
    post_id: str
    username: str
    count: int
