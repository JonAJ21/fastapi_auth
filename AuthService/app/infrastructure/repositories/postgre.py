from dataclasses import dataclass
from typing import Generic, List, Type

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.repositories.base import (
    BaseRepository,
    CreateSchemaType,
    ModelType
)

@dataclass
class PostgresRepository(BaseRepository, Generic[ModelType, CreateSchemaType]):
    _session: AsyncSession
    _model: Type[ModelType]
    
    async def gets(self, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        statement = select(self._model).order_by().offset(skip).limit(limit)
        return await self._session.execute(statement).scalars().all()
    
    async def get(self, *, id: int) -> ModelType | None:
        statement = select(self._model).where(self._model.id == id)
        return await self._session.execute(statement).scalar_one_or_none()