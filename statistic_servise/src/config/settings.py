from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    POSTGRES_DB: str = os.environ['POSTGRES_DB']
    POSTGRES_USER: str = os.environ['POSTGRES_USER']
    POSTGRES_PASSWORD: str = os.environ['POSTGRES_PASSWORD']
    POSTGRES_HOST: str = os.environ['POSTGRES_HOST']
    KAFKA_HOST: str = os.environ['KAFKA_HOST']
    KAFKA_PORT: str = os.environ['KAFKA_PORT']
    KAFKA_TOPIC: str = os.environ['KAFKA_TOPIC']
    KAFKA_GROUP_ID: str = os.environ['KAFKA_GROUP_ID']
    GRPC_HOST: str = os.environ['GRPC_HOST']
    GRPC_PORT: str = os.environ['GRPC_PORT']
    GRPC_SERVER_PORT: str = os.environ['GRPC_SERVER_PORT']


settings = Settings()
