import pytest
from schemas.token import Token, TokenJTI, TokenValidaton
from pydantic import ValidationError

# Тесты для класса Token
def test_token_creation():
    # Проверка корректного создания объекта
    token = Token(access_token="access", refresh_token="refresh")
    assert token.access_token == "access"
    assert token.refresh_token == "refresh"

def test_token_optional_fields():
    # Проверка, что поля могут быть None
    token = Token(access_token=None, refresh_token=None)
    assert token.access_token is None
    assert token.refresh_token is None

def test_token_invalid_type():
    # Проверка валидации типов данных
    with pytest.raises(ValidationError):
        Token(access_token=123, refresh_token="refresh")

# Тесты для класса TokenJTI
def test_token_jti_creation():
    # Проверка корректного создания объекта
    token_jti = TokenJTI(access_token_jti="access_jti", refresh_token_jti="refresh_jti")
    assert token_jti.access_token_jti == "access_jti"
    assert token_jti.refresh_token_jti == "refresh_jti"

def test_token_jti_optional_fields():
    # Проверка, что поля могут быть None
    token_jti = TokenJTI(access_token_jti=None, refresh_token_jti=None)
    assert token_jti.access_token_jti is None
    assert token_jti.refresh_token_jti is None

def test_token_jti_invalid_type():
    # Проверка валидации типов данных
    with pytest.raises(ValidationError):
        TokenJTI(access_token_jti=123, refresh_token_jti="refresh_jti")

# Тесты для класса TokenValidaton
def test_token_validation_creation():
    # Проверка корректного создания объекта
    token_validation = TokenValidaton(access_token="access")
    assert token_validation.access_token == "access"

def test_token_validation_invalid_type():
    # Проверка валидации типов данных
    with pytest.raises(ValidationError):
        TokenValidaton(access_token=123)