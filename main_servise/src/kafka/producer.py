from aiokafka import AIOKafkaProducer

from contextlib import asynccontextmanager

import json


class Producer:
    def __init__(self, bootstap: str):
        self.__producer: AIOKafkaProducer = None
        self.__bootstrap = bootstap

    async def create_producer(self):
        self.__producer =  AIOKafkaProducer(bootstrap_servers=self.__bootstrap)
        await self.__producer.start()

    @asynccontextmanager
    async def producer_session(self):
        if not (self.__producer is None):
            yield self.__producer

    async def stop_producer(self):
        await self.__producer.stop()

    @staticmethod
    async def send_to_kafka(producer, msg, topic):
        await producer.send(topic, json.dumps(msg).encode('utf-8'))
