from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseCacheService(ABC):
    @abstractmethod
    async def get(self, *args, **kwargs):
        ...

    @abstractmethod
    async def set(self, *args, **kwargs):
        ...
        
    @abstractmethod
    async def delete(self, *args, **kwargs):
        ...