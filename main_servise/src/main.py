from fastapi import FastAPI

from kafka.kafka_producer import kafka_producer

from contextlib import asynccontextmanager

from controllers.auth_controller import auth_router
from controllers.post_controller import posts_router
from controllers.statistic_controller import statistic_router
from controllers.user_controller import user_router


tags = [
    {
        "name": "login&register",
        "description": "Operations with registration and authentication"
    },
    {
        "name": "user",
        "description": "Operations with user profile"
    },
    {
        "name": "posts",
        "description": "Operations with posts"
    },
    {
        "name": "actions",
        "description": "Like or view"
    }
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await kafka_producer.create_producer()
    yield
    await kafka_producer.stop_producer()


app = FastAPI(lifespan=lifespan, openapi_tags=tags)

app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(statistic_router)
app.include_router(user_router)
