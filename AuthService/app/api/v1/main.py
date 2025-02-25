from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from redis.asyncio import Redis
from sqlalchemy import create_engine, select
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.models.role import Role
from infrastructure.models.user import User
from schemas.role import Roles
from settings.config import settings
from logic.dependencies.main import setup_dependencies
from api.v1.accounts.handlers import router as accounts_router
from api.v1.roles.handlers import router as roles_router
from api.v1.users.handlers import router as users_router
from api.v1.socials.handlers import router as socials_router
from infrastructure.database.postgres import Base, async_session

from infrastructure.database import redis

def apply_migrations():
    DATABASE_URL = str(settings.postgres_connection)
    sync_engine = create_engine(DATABASE_URL.replace("+asyncpg", ""), echo=True)
    Base.metadata.create_all(bind=sync_engine)

async def create_superuser():
    async with async_session() as session:
        try:
            user_statement = select(User).where(User.login == settings.super_admin_login)
            role_statement = select(Role).where(Role.name == Roles.SUPER_ADMIN)
            user_result = await session.execute(user_statement)
            role_result = await session.execute(role_statement)
            if user_result.scalar_one_or_none():
                return
            if role_result.scalar_one_or_none():
                return

            super_admin_role = Role(
                name=Roles.SUPER_ADMIN, description="Super Admin privilege"
            )
            super_admin_user = User(
                login=settings.super_admin_login,
                password=settings.super_admin_password,
                tg_id=settings.super_admin_tg_id,
                email=settings.super_admin_email
            )

            session.add(super_admin_role)
            session.add(super_admin_user)
            super_admin_user.assign_role(super_admin_role)
            await session.commit()
        except Exception as e:
            await session.rollback()

@asynccontextmanager
async def lifespan(_: FastAPI):
    redis.redis = Redis(
        host=settings.redis_host,
        port=6379,
        password=settings.redis_password,
        db=0
    )
    apply_migrations()
    await create_superuser()
    yield
    await redis.redis.aclose()
    
def create_app() -> FastAPI:
    app = FastAPI(
        title='AuthService',
        docs_url='/api/docs',
        description='Auth service',
        lifespan=lifespan,
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins (replace with specific domains for security)
        allow_credentials=True,
        allow_methods=["*"],  # Allows all HTTP methods
        allow_headers=["*"],  # Allows all headers
    )


    app.include_router(accounts_router, prefix='/accounts')
    app.include_router(socials_router, prefix='/socials')
    app.include_router(users_router, prefix='/users')
    app.include_router(roles_router, prefix='/roles')
    
    setup_dependencies(app)
    
    return app

