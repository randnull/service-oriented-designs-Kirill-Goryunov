from kafka.consumer import Consumer

from kafka.kafka_functions import get_action

from config.settings import settings


BOOTSTRAP_SERVER = f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}'
TOPIC = settings.KAFKA_TOPIC
GROUP_ID = settings.KAFKA_GROUP_ID


statistic_consumer = Consumer(TOPIC, BOOTSTRAP_SERVER, GROUP_ID, get_action)
