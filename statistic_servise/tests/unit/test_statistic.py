import pytest
from statistic_servise.src.dao_table.mock.mock_dao import Statistic
from statistic_servise.src.dto_table.dto import StatisticModel


class TestObject:
    def test_to_dto(self):
        model_dao = Statistic(
            id = 1,
            post_id = "1",
            action = "like",
            author = "name",
            username = "name2"
        )

        dto_model = StatisticModel.to_dto(model_dao)

        dto_expect_model = StatisticModel(
            post_id="1",
            action="like",
            author="name",
            username="name2"
        )

        assert dto_model == dto_expect_model

    def test_to_dao(self):
        dto_model = StatisticModel(
            post_id="1",
            action="like",
            author="name",
            username="name2"
        )

        dao_model = Statistic.to_dao(dto_model)

        dao_expect_model = Statistic(
            id=1,
            post_id="1",
            action="like",
            author="name",
            username="name2"
        )

        assert dao_model.username == dao_expect_model.username
        assert dao_model.action == dao_expect_model.action
        assert dao_model.author == dao_expect_model.author
        assert dao_model.post_id == dao_expect_model.post_id
