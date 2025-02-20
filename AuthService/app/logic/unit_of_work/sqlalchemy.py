from sqlalchemy.ext.asyncio import AsyncSession

from logic.unit_of_work.base import BaseUnitOfWork

class SqlAlchemyUnitOfWork(BaseUnitOfWork):
    _session: AsyncSession
    
    async def commit(self) -> None:
        await self._session.commit()