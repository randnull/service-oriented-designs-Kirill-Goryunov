from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from common.database_connection.base import get_session

from kafka.kafka_producer import get_producer
from kafka.producer import Producer

from dto_table.user_dto import UserModel
from dto_table.top_post_dto import TopPostModel
from dto_table.top_user_dto import TopUserModel

from controllers.auth_controller import get_user

from config.settings import settings

from repository.repo import user_repository

import grpc
import statistic_pb2_grpc
import statistic_pb2


statistic_router = APIRouter(prefix="/action", tags=["actions"])

grpc_host = settings.GRPC_HOST_STATISTIC
grpc_port = settings.GRPC_PORT_STATISTIC


@statistic_router.post("/view/{post_id}", tags=["actions"])
async def send_view(post_id: str, s: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_user), kafka_producer = Depends(get_producer)):
    statistic_data = {
        "action": "view",
        "post_id": post_id,
        "username": current_user.username
    }

    await Producer.send_to_kafka(kafka_producer, statistic_data, settings.KAFKA_TOPIC)

    return JSONResponse(content={"message": "Send!"}, status_code=200)



@statistic_router.post("/like/{post_id}", tags=["actions"])
async def send_view(post_id: str, s: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_user), kafka_producer = Depends(get_producer)):
    statistic_data = {
        "action": "like",
        "post_id": post_id,
        "username": current_user.username
    }

    await Producer.send_to_kafka(kafka_producer, statistic_data, settings.KAFKA_TOPIC)

    return JSONResponse(content={"message": "Send!"}, status_code=200)


@statistic_router.get("/statistic/post/{post_id}", tags=["actions"])
async def get_statistic_by_post(post_id: str, s: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_user)):
    async with grpc.aio.insecure_channel(f'{grpc_host}:{grpc_port}') as grpc_channel:
        grpc_stub = statistic_pb2_grpc.StatisticServiceStub(grpc_channel)
    
        response = await grpc_stub.GetStatisticByPost(statistic_pb2.GetByPostRequest(id=post_id))

    return JSONResponse(content={"post_id": f"{post_id}", "likes": f"{response.likes}", "views": f"{response.views}"}, status_code=200)


@statistic_router.get("/statistic/top_posts/{top_type}", tags=["actions"])
async def get_top_posts(top_type: str, s: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_user)):
    async with grpc.aio.insecure_channel(f'{grpc_host}:{grpc_port}') as grpc_channel:
        grpc_stub = statistic_pb2_grpc.StatisticServiceStub(grpc_channel)
    
        response = await grpc_stub.GetPopularPost(statistic_pb2.GetPopularPostRequest(sort_type=top_type))

    answer_dto = list()

    for post in response.popular_posts:
        username = await user_repository.get_username_by_id(s, int(post.author))

        new_top_post = TopPostModel(
            post_id=post.post_id,
            username=username,
            count = post.count
        )

        answer_dto.append(new_top_post)

    return answer_dto


@statistic_router.get("/statistic/top_users", tags=["actions"])
async def get_top_users(s: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_user)):
    async with grpc.aio.insecure_channel(f'{grpc_host}:{grpc_port}') as grpc_channel:
        grpc_stub = statistic_pb2_grpc.StatisticServiceStub(grpc_channel)
    
        response = await grpc_stub.GetPopularUser(statistic_pb2.NoParams())

    answer_dto = list()

    for post in response.popular_users:
        username = await user_repository.get_username_by_id(s, int(post.author))

        new_top_post = TopUserModel(
            username=username,
            likes=int(post.likes)
        )

        answer_dto.append(new_top_post)

    return answer_dto
