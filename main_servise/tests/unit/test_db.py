from unittest.mock import MagicMock, AsyncMock
from common.repository.generic_repository import Repository
from main_servise.src.dto_table.user_dto import UserModel
import datetime
import pytest


class TestDB:
    @pytest.mark.asyncio
    async def test_db(self):
        mock_model_object = MagicMock()
        mock_model_object.to_dao = MagicMock()

        user_repository = Repository[mock_model_object](mock_model_object)

        mock_object = MagicMock()

        mock_object.add = MagicMock()
        mock_object.flush = AsyncMock()
        mock_object.commit = AsyncMock()

        test_model = UserModel(
            username='test',
            password='test',
            name=None,
            surname=None,
            email=None,
            birthday=None,
            phone=None,
            created_at=datetime.datetime.now()
        )

        await user_repository.add(mock_object, test_model)

        mock_object.add.assert_called_once()
        mock_object.flush.assert_called_once()
        mock_object.commit.assert_called_once()
