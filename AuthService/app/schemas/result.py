from dataclasses import dataclass
from typing import Generic, TypeVar
from pydantic import BaseModel

ModelType = TypeVar('ModelType', bound=BaseModel)

@dataclass
class Error:
    reason: str
    error_code: str
    
@dataclass
class Result:
    is_success: bool
    error: Error | None
    
    @staticmethod
    def success():
        return Result(success=True, error=None)
    
    @staticmethod
    def failure(error: Error):
        return Result(success=False, error=error)
    

@dataclass
class GenericResult(Result, Generic[ModelType]):
    response: ModelType | None
    is_success: bool
    error: Error | None
    
    @staticmethod
    def success(value: ModelType):
        return GenericResult(success=True, error=None, response=value)
    
    @staticmethod
    def failure(error: Error):
        return GenericResult(success=False, error=error, response=None)
    