from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)




@dataclass
class BaseRepository(ABC):
    
    @abstractmethod
    def gets(self, *args, **kwargs):
        ...
        
    @abstractmethod
    def get(self, *args, **kwargs):
        ...
        
    @abstractmethod
    def insert(self, *args, **kwargs):
        ...
        
    @abstractmethod
    def delete(self, *args, **kwargs):
        ...