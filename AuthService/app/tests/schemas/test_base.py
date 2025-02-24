# Тесты для класса IdentifiableMixin
from uuid import UUID
from pydantic import ValidationError
import pytest
from schemas.base import IdentifiableMixin

def test_identifiable_mixin_creation():
    # Проверка корректного создания объекта
    uuid_value = "123e4567-e89b-12d3-a456-426614174000"
    identifiable = IdentifiableMixin(id=uuid_value)
    assert isinstance(identifiable.id, UUID)
    assert str(identifiable.id) == uuid_value

def test_identifiable_mixin_invalid_uuid():
    # Проверка валидации UUID (некорректный UUID)
    with pytest.raises(ValidationError):
        IdentifiableMixin(id="invalid-uuid")