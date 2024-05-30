import json

from repository.repo import statistic_repository
from common.database_connection.base import async_session

from dto_table.dto import StatisticModel

import grpc

import posts_pb2
import posts_pb2_grpc

from config.settings import settings

grpc_host = settings.GRPC_HOST
grpc_port = settings.GRPC_PORT

grpc_channel = grpc.insecure_channel(f'{grpc_host}:{grpc_port}')
grpc_stub = posts_pb2_grpc.PostsServiceStub(grpc_channel)


async def get_action(msg):
    data = json.loads(msg.value.decode('utf-8'))

    action = data["action"]
    post_id = data["post_id"]
    username = data["username"]

    async with async_session() as session:
        response = grpc_stub.GetByIdPost(posts_pb2.GetById(id=post_id, user_id=0))

        check = await statistic_repository.check_if_like_unique(session, post_id, username, action)

        if response.status == 0 and check:
            user_id = str(response.user_id)

            new_statistic = StatisticModel(
                    post_id=post_id,
                    action=action,
                    author=user_id,
                    username=username
            )

            await statistic_repository.add(session, new_statistic)
