# Тесты для класса UserLoginDTO
from pydantic import ValidationError
import pytest
from schemas.auth import RefreshRequestDTO, UserLoginDTO


def test_user_login_dto_creation():
    # Проверка корректного создания объекта
    user_login = UserLoginDTO(login="user123", password="password123")
    assert user_login.login == "user123"
    assert user_login.password == "password123"

def test_user_login_dto_invalid_types():
    # Проверка валидации типов данных
    with pytest.raises(ValidationError):
        UserLoginDTO(login=123, password="password123")  # login должен быть строкой
    with pytest.raises(ValidationError):
        UserLoginDTO(login="user123", password=123)  # password должен быть строкой

# Тесты для класса RefreshRequestDTO
def test_refresh_request_dto_creation():
    # Проверка корректного создания объекта
    refresh_request = RefreshRequestDTO(jti="123e4567-e89b-12d3-a456-426614174000")
    assert refresh_request.jti == "123e4567-e89b-12d3-a456-426614174000"

def test_refresh_request_dto_optional_jti():
    # Проверка, что поле jti может быть None
    refresh_request = RefreshRequestDTO(jti=None)
    assert refresh_request.jti is None

def test_refresh_request_dto_invalid_jti_type():
    # Проверка валидации типа jti
    with pytest.raises(ValidationError):
        RefreshRequestDTO(jti=123)  # jti должен быть строкой