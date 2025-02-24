from uuid import UUID
import pytest
from pydantic import ValidationError
from schemas.social import SocialCreateDTO, SocialNetworks, SocialUser

def test_social_networks_enum():
    # Проверка значений перечисления
    assert SocialNetworks.VK.value == 'vk'
    assert SocialNetworks.YANDEX.value == 'yandex'

# Тесты для класса SocialUser
def test_social_user_creation():
    # Проверка корректного создания объекта
    user = SocialUser(id="123", login="user_login", email="user@example.com", tg_id="123", social_name=SocialNetworks.VK)
    assert user.id == "123"
    assert user.login == "user_login"
    assert user.email == "user@example.com"
    assert user.tg_id == "123"
    assert user.social_name == SocialNetworks.VK

def test_social_user_optional_email_tg():
    # Проверка, что email, tg_idможет быть None
    user = SocialUser(id="123", login="user_login", email=None, tg_id=None, social_name=SocialNetworks.YANDEX)
    assert user.email is None
    assert user.tg_id is None

def test_social_user_invalid_email():
    # Проверка валидации email
    with pytest.raises(ValidationError):
        SocialUser(id="123", login="user_login", email="invalid-email", social_name=SocialNetworks.VK)

def test_social_user_invalid_social_name():
    # Проверка валидации social_name
    with pytest.raises(ValidationError):
        SocialUser(id="123", login="user_login", email="user@example.com", social_name="invalid_social")

# Тесты для класса SocialCreateDTO
def test_social_create_dto_creation():
    # Проверка корректного создания объекта
    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    dto = SocialCreateDTO(user_id=user_id, social_id="123", social_name=SocialNetworks.YANDEX)
    assert dto.user_id == user_id
    assert dto.social_id == "123"
    assert dto.social_name == SocialNetworks.YANDEX

def test_social_create_dto_invalid_user_id():
    # Проверка валидации user_id (должен быть UUID)
    with pytest.raises(ValidationError):
        SocialCreateDTO(user_id="invalid-uuid", social_id="123", social_name=SocialNetworks.VK)

def test_social_create_dto_invalid_social_name():
    # Проверка валидации social_name
    with pytest.raises(ValidationError):
        SocialCreateDTO(user_id=UUID("123e4567-e89b-12d3-a456-426614174000"), social_id="123", social_name="invalid_social")