from fastapi import FastAPI
from fastapi.responses import JSONResponse

from contextlib import asynccontextmanager

from kafka.kafka_consumer import statistic_consumer

import asyncio

from grpc_server.grpc_server import start_grpc


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(start_grpc())

    await statistic_consumer.create_consumer()

    asyncio.create_task(statistic_consumer.consume())
    yield
    await statistic_consumer.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def check():
    return JSONResponse(content={"message": "Ok"}, status_code=200)
