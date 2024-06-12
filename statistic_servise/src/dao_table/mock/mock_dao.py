from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Statistic(Base):
    __tablename__ = "statistic"


    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    post_id = Column(String)
    action = Column(String)
    author = Column(String)
    username = Column(String)

    @classmethod
    def to_dao(cls, statistic_dto):
        return Statistic(
            post_id = statistic_dto.post_id,
            action = statistic_dto.action,
            author = statistic_dto.author,
            username = statistic_dto.username
        )
