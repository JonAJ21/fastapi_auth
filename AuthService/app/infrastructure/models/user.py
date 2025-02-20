from datetime import UTC, datetime
from uuid import uuid4
from typing import List, Self
from passlib.hash import pbkdf2_sha256
from pydantic import EmailStr

from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    String,
)
from sqlalchemy.orm import Mapped, relationship

from infrastructure.models.social_account import SocialAccount
from infrastructure.models.user_history import UserHistory
from infrastructure.models.user_role import UserRole
from infrastructure.database.postgres import Base   
from infrastructure.models.role import Role

class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    login = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    roles: Mapped[List['Role']] = relationship(
        'Role',
        secondary=UserRole.__tablename__,
        cascade='all, delete-orphan',
        back_populates='users'
    )
    history: Mapped[List['UserHistory']] = relationship(
        'UserHistory',
        cascade='all, delete-orphan',
        back_populates='user'
    )
    social_accounts: Mapped[List['SocialAccount']] = relationship(
        'SocialAccount',
        cascade='all, delete-orphan',
        back_populates='user',
        lazy='selectin'
    )
    created = Column(
        DateTime(timezone=True), default=datetime.now(UTC)
    )
    updated = Column(
        DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )
    
    def __init__(
        self,
        login: str,
        password: str, 
        email: EmailStr | None = None
    ) -> None:
        self.login = login
        self.password_hash = pbkdf2_sha256.hash(password)
        self.email = email
        self.social_accounts = []
        
    def __repr__(self) -> str:
        return f"<User {self.login}>"
    
    def check_password(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password, self.password_hash)
    
    def change_password(self, old_password: str, new_password) -> bool:
        if not self.check_password(old_password):
            return False
        self.password_hash = pbkdf2_sha256.hash(new_password)
    
    def update_login(self, login: str) -> Self:
        self.login = login if login != "" else self.login
        return Self
    
    def update_email(self, email: EmailStr) -> Self:
        self.email = email
    
    def has_role(self, role_name: str) -> bool:
        for role in self.roles:
            if role.name == role_name:
                return True
        return False
    
    def assign_role(self, role: Role) -> None:
        if not self.has_role(role.name):
            self.roles.append(role)
        
    def remove_role(self, role: Role) -> None:
        if self.has_role(role.name):
            self.roles.remove(role)
            
    def add_user_session(self, session: UserHistory) -> None:
        self.history.append(session)
    
    def has_social_account(self, social_account: SocialAccount) -> bool:
        for account in self.social_accounts:
            if account.social_id == social_account.social_id and account.social_network == social_account.social_network:
                return True
        return False
    
    def add_social_account(self, social_account: SocialAccount) -> None:
        if not self.has_social_account(social_account):
            self.social_accounts.append(social_account)
        
    def remove_social_account(self, social_account: SocialAccount) -> None:
        if self.has_social_account(social_account):
            self.social_accounts.remove(social_account)