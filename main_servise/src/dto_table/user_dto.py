from pydantic import BaseModel
import datetime
from typing import Optional

class UserModel(BaseModel):
    username: str
    password: str
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    birthday: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime.datetime

    @classmethod
    def to_dto(cls, user_dao):
        return UserModel(
            username=user_dao.username,
            password=user_dao.password,
            name=user_dao.name,
            surname=user_dao.surname,
            email=user_dao.email,
            birthday=user_dao.birthday,
            phone=user_dao.phone,
            created_at=user_dao.created_at
        )
