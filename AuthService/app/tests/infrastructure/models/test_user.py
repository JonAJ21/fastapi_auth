import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.models.user import User

@pytest.mark.asyncio
async def test_user_creation(db_session: AsyncSession):
    async with db_session as session:
        user = User(login="johndoe", password="password", email="john@example.com")
        db_session.add(user)
        query = select(User).where(User.login == "johndoe")
        user = (await session.execute(query)).scalar_one_or_none()
        assert user is not None
        assert user.login == "johndoe"