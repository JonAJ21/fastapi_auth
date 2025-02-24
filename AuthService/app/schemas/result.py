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
    error_code: Error | None
    
    @staticmethod
    def success():
        return Result(is_success=True, error_code=None)
    
    @staticmethod
    def failure(error: Error):
        return Result(is_success=False, error_code=error)
    

@dataclass
class GenericResult(Result, Generic[ModelType]):
    response: ModelType | None
    is_success: bool
    error_code: Error | None
    
    @staticmethod
    def success(value: ModelType):
        return GenericResult(is_success=True, error_code=None, response=value)
    
    @staticmethod
    def failure(error: Error):
        return GenericResult(is_success=False, error_code=error, response=None)
    