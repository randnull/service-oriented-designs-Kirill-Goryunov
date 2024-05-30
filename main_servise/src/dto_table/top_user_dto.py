from pydantic import BaseModel

class TopUserModel(BaseModel):
    username: str
    likes: int
