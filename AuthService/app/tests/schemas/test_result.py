# Пример модели для тестирования GenericResult
from pydantic import BaseModel
import pytest
from schemas.result import GenericResult, Result, Error

class ExampleModel(BaseModel):
    id: int
    name: str

# Тесты для класса Error
def test_error_creation():
    # Проверка корректного создания объекта
    error = Error(reason="Not found", error_code="404")
    assert error.reason == "Not found"
    assert error.error_code == "404"

# Тесты для класса Result
def test_result_success():
    # Проверка успешного результата
    result = Result.success()
    assert result.is_success is True
    assert result.error_code is None

def test_result_failure():
    # Проверка неудачного результата
    error = Error(reason="Not found", error_code="404")
    result = Result.failure(error)
    assert result.is_success is False
    assert result.error_code == error

# Тесты для класса GenericResult
def test_generic_result_success():
    # Проверка успешного результата с данными
    example_data = ExampleModel(id=1, name="Test")
    result = GenericResult.success(example_data)
    assert result.is_success is True
    assert result.error_code is None
    assert result.response == example_data

def test_generic_result_failure():
    # Проверка неудачного результата
    error = Error(reason="Not found", error_code="404")
    result = GenericResult.failure(error)
    assert result.is_success is False
    assert result.error_code == error
    assert result.response is None

# Дополнительные тесты для проверки типов
def test_generic_result_type_hinting():
    # Проверка, что GenericResult корректно работает с типами
    example_data = ExampleModel(id=1, name="Test")
    result = GenericResult[ExampleModel].success(example_data)
    assert isinstance(result.response, ExampleModel)
    assert result.response.id == 1
    assert result.response.name == "Test"