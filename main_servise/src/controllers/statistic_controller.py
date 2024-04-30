from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from common.database_connection.base import get_session

from kafka.kafka_producer import get_producer
from kafka.producer import Producer

from dto_table.user_dto import UserModel

from controllers.auth_controller import get_user

from config.settings import settings


statistic_router = APIRouter(prefix="/action", tags=["actions"])


@statistic_router.post("/view/{post_id}", tags=["actions"])
async def send_view(post_id: str, s: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_user), kafka_producer = Depends(get_producer)):
    statistic_data = {
        "action": "view",
        "post_id": post_id
    }

    await Producer.send_to_kafka(kafka_producer, statistic_data, settings.KAFKA_TOPIC)

    return JSONResponse(content={"message": "Send!"}, status_code=200)



@statistic_router.post("/like/{post_id}", tags=["actions"])
async def send_view(post_id: str, s: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_user), kafka_producer = Depends(get_producer)):
    statistic_data = {
        "action": "like",
        "post_id": post_id
    }

    await Producer.send_to_kafka(kafka_producer, statistic_data, settings.KAFKA_TOPIC)

    return JSONResponse(content={"message": "Send!"}, status_code=200)
