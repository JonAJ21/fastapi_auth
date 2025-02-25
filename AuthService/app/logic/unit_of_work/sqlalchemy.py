from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from logic.unit_of_work.base import BaseUnitOfWork

@dataclass
class SqlAlchemyUnitOfWork(BaseUnitOfWork):
    _session: AsyncSession
    
    async def commit(self, *args, **kwargs) -> None:
        await self._session.commit()
        
    def __hash__(self):
        return hash((self._session))
        
    def __eq__(self, other):
        return hash(self) == hash(other)