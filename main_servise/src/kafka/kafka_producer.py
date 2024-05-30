from kafka.producer import Producer

from config.settings import settings


BOOTSTRAP_SERVER = f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}'

kafka_producer = Producer(BOOTSTRAP_SERVER)


async def get_producer():
    async with kafka_producer.producer_session() as session:
        yield session
