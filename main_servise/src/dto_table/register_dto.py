from pydantic import BaseModel
import datetime

class RegisterModel(BaseModel):
    username: str
    password: str
