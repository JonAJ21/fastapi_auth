from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class BaseUnitOfWork(ABC):
    @abstractmethod
    async def commit(self):
        ...