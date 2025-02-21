from dataclasses import dataclass
from typing import Any, Generic, List, Type

from fastapi.encoders import jsonable_encoder
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
    
    async def get(self, *, id: Any) -> ModelType | None:
        statement = select(self._model).where(self._model.id == id)
        return await self._session.execute(statement).scalar_one_or_none()
    
    async def insert(self, *, body: CreateSchemaType) -> ModelType:
        raw_obj = jsonable_encoder(body)
        db_obj = self._model(**raw_obj)
        self._session.add(db_obj)
        return db_obj
    
    async def delete(self, *, id: Any) -> None:
        statement = delete(self._model).where(self._model.id == id)
        await self._session.execute(statement)