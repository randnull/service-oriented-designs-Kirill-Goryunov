from pydantic import BaseModel


class StatisticModel(BaseModel):
    post_id: str
    action: str
    author: str
    username: str

    @classmethod
    def to_dto(cls, statistic_dao):
        return StatisticModel(
            post_id = statistic_dao.post_id,
            action = statistic_dao.action,
            author = statistic_dao.author,
            username = statistic_dao.username
        )
