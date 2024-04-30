import json

from repository.repo import statistic_repository
from common.database_connection.base import async_session

from dto_table.dto import StatisticModel


async def get_action(msg):
    data = json.loads(msg.value.decode('utf-8'))

    action = data["action"]
    post_id = data["post_id"]

    async with async_session() as session:
        is_exist = await statistic_repository.check_if_exist_by_post_id(session, post_id)

        if not is_exist:
            new_statistic = StatisticModel(
                post_id=post_id,
                watch_count=0,
                like_count=0
            )

            await statistic_repository.add(session, new_statistic)

        await statistic_repository.update_statistic(session, post_id, action)
