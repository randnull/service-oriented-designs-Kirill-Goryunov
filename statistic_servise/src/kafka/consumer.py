from aiokafka import AIOKafkaConsumer


class Consumer:
    def __init__(self, topic: str, bootstrap: str, group: str, function):
        self.__kafka_consumer: AIOKafkaConsumer = None
        self.__topic = topic
        self.__bootstrap = bootstrap
        self.__function = function
        self.__group_id = group

    async def create_consumer(self):
        self.__kafka_consumer = AIOKafkaConsumer(
            self.__topic, bootstrap_servers=self.__bootstrap, 
            auto_commit_interval_ms=1000,
            auto_offset_reset="earliest",
            group_id=self.__group_id
        )
    
    async def stop(self):
        await self.__kafka_consumer.stop()

    async def consume(self):
        await self.__kafka_consumer.start()

        try:
            async for msg in self.__kafka_consumer:
                await self.__function(msg)
        finally:
            await self.stop()
