

from functools import cache

from aiokafka import AIOKafkaProducer
from fastapi import Depends
from infrastructure.kafka.sender import BaseSender, KafkaSender, get_producer
from logic.dependencies.registrator import add_factory_to_mapper


@add_factory_to_mapper(KafkaSender)
@cache
def create_sender(
    producer: AIOKafkaProducer = Depends(get_producer()),
) -> BaseSender:
    return KafkaSender(_producer=producer)
    