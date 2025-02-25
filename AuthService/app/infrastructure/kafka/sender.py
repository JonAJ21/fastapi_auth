from abc import ABC, abstractmethod
from dataclasses import dataclass

from aiokafka import AIOKafkaProducer

from schemas.events import UserRegisteredEventDTO
from settings.config import settings

producer = AIOKafkaProducer(
    bootstrap_servers=settings.kafka_url,
)

def get_producer():
    return KafkaSender(producer)

@dataclass
class BaseSender(ABC):
    @abstractmethod
    async def send_on_register(self, event: UserRegisteredEventDTO) -> None:
        ...
        
        
@dataclass
class KafkaSender(BaseSender):
    _producer: AIOKafkaProducer
    async def send_on_register(self, event: UserRegisteredEventDTO) -> None:
        self._producer.send('user.registered', value=event.model_dump_json().encode('utf-8'))