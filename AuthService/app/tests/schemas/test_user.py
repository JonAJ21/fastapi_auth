import pytest
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import ValidationError

from schemas.user import (
    UserBase,
    UserDTO,
    UserCreateDTO,
    UserUpdateDTO,
    UserUpdatePasswordDTO,
    UserHistoryDTO,
    UserHistoryCreateDTO,
)
from schemas.role import RoleBase

def test_user_base():
    user_id = uuid4()
    user = UserBase(id=user_id, login="testuser", email="test@example.com")
    
    assert user.id == user_id
    assert user.login == "testuser"
    assert user.email == "test@example.com"
    
    # Проверка на необязательное поле email
    user_without_email = UserBase(id=user_id, login="testuser")
    assert user_without_email.email is None

# Тесты для UserDTO
def test_user_dto():
    user_id = uuid4()
    print(uuid4())
    role = RoleBase(id=uuid4(), name="admin")
    user = UserDTO(id=user_id, login="testuser", email="test@example.com", roles=[role])
    
    assert user.id == user_id
    assert user.login == "testuser"
    assert user.email == "test@example.com"
    assert user.roles == [role]
    
    # Проверка на необязательное поле roles
    user_without_roles = UserDTO(id=user_id, login="testuser", email="test@example.com")
    assert user_without_roles.roles is None

# Тесты для UserCreateDTO
def test_user_create_dto():
    user = UserCreateDTO(login="testuser", password="password123", email="test@example.com")
    
    assert user.login == "testuser"
    assert user.password == "password123"
    assert user.email == "test@example.com"
    
    # Проверка на необязательное поле email
    user_without_email = UserCreateDTO(login="testuser", password="password123")
    assert user_without_email.email is None

# Тесты для UserUpdateDTO
def test_user_update_dto():
    user = UserUpdateDTO(login="updateduser", email="updated@example.com")
    
    assert user.login == "updateduser"
    assert user.email == "updated@example.com"
    
    # Проверка на необязательные поля
    user_without_email = UserUpdateDTO(login="updateduser")
    assert user_without_email.email is None
    
    user_without_login = UserUpdateDTO(email="updated@example.com")
    assert user_without_login.login is None

# Тесты для UserUpdatePasswordDTO
def test_user_update_password_dto():
    user = UserUpdatePasswordDTO(old_password="oldpass", new_password="newpass")
    
    assert user.old_password == "oldpass"
    assert user.new_password == "newpass"

# Тесты для UserHistoryDTO
def test_user_history_dto():
    user_id = uuid4()
    attempted = datetime.now()
    history = UserHistoryDTO(
        id=uuid4(),
        user_id=user_id,
        attempted=attempted,
        user_agent="Mozilla/5.0",
        user_device_type="Desktop",
        success=True
    )
    
    assert isinstance(history.id, UUID)
    assert history.user_id == user_id
    assert history.attempted == attempted
    assert history.user_agent == "Mozilla/5.0"
    assert history.user_device_type == "Desktop"
    assert history.success is True

# Тесты для UserHistoryCreateDTO
def test_user_history_create_dto():
    user_id = uuid4()
    attempted = datetime.now()
    history = UserHistoryCreateDTO(
        user_id=user_id,
        attempted=attempted,
        user_agent="Mozilla/5.0",
        user_device_type="Desktop",
        success=True
    )
    
    assert history.user_id == user_id
    assert history.attempted == attempted
    assert history.user_agent == "Mozilla/5.0"
    assert history.user_device_type == "Desktop"
    assert history.success is True

# Тесты на валидацию ошибок
def test_user_base_validation_error():
    with pytest.raises(ValidationError):
        UserBase(id="invalid-uuid", login="testuser", email="test@example.com")

def test_user_create_dto_validation_error():
    with pytest.raises(ValidationError):
        UserCreateDTO(login="testuser", password="password123", email="invalid-email")

def test_user_history_create_dto_validation_error():
    with pytest.raises(ValidationError):
        UserHistoryCreateDTO(
            user_id="invalid-uuid",
            attempted="invalid-datetime",
            user_agent="Mozilla/5.0",
            user_device_type="Desktop",
            success=True
        )