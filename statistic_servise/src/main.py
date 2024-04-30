from fastapi import FastAPI
from fastapi.responses import JSONResponse

from contextlib import asynccontextmanager

from kafka.kafka_consumer import statistic_consumer

import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    await statistic_consumer.create_consumer()

    asyncio.create_task(statistic_consumer.consume())
    yield
    await statistic_consumer.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def check():
    return JSONResponse(content={"message": "Ok"}, status_code=200)
