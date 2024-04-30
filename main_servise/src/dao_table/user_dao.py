from sqlalchemy import Column, Integer, String, DateTime
import datetime

from common.database_connection.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    birthday = Column(String)
    phone = Column(String)
    created_at = Column(DateTime)

    @classmethod
    def to_dao(cls, register_dto):
        return User(
            username = register_dto.username,
            password = register_dto.password,
            name = None,
            surname = None,
            email = None,
            birthday = None,
            phone = None,
            created_at = datetime.datetime.now()
        )
