from enum import Enum
from uuid import uuid4

from sqlalchemy import (
    UUID,
    Column,
    ForeignKey,
    Text,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from schemas.social import SocialNetworks
from infrastructure.database.postgres import Base
    
class SocialAccount(Base):
    __tablename__ = "social_accounts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="social_accounts", cascade="all, delete")
    social_id = Column(Text, nullable=False)
    social_network = Column(Enum(SocialNetworks))
    
    __table_args__ = (
        UniqueConstraint("social_id", "social_network", name="social_pk"),
    )
    
    def __init__(self, social_id: str, social_network: SocialNetworks) -> None:
        self.social_id = social_id
        self.social_network = social_network
        
    def __repr__(self) -> str:
        return f"<SocialAccount {self.social_network}:{self.user_id}>"