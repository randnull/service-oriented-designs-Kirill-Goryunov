from sqlalchemy import Column, Integer, String

from common.database_connection.base import Base


class Statistic(Base):
    __tablename__ = "statistic"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    post_id = Column(String)
    watch_count = Column(Integer)
    like_count = Column(Integer)

    @classmethod
    def to_dao(cls, statistic_dto):
        return Statistic(
            post_id = statistic_dto.post_id,
            watch_count = statistic_dto.watch_count,
            like_count = statistic_dto.like_count
        )
