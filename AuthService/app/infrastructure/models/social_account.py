from uuid import uuid4

from sqlalchemy import (
    UUID,
    Column,
    ForeignKey,
    Text,
    UniqueConstraint,
    Enum
)
from sqlalchemy.orm import relationship

from schemas.social import SocialNetworks
from infrastructure.database.postgres import Base
    
class SocialAccount(Base):
    __tablename__ = "social_account"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="social_accounts", cascade="all, delete")
    social_id = Column(Text, nullable=False)
    social_name = Column(Enum(SocialNetworks))
    
    __table_args__ = (
        UniqueConstraint("social_id", "social_name", name="social_pk"),
    )
    
    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "user_id": self.user_id,
    #         "social_id": self.social_id,
    #         "social_name": self.social_name
    #     }
    
    def __init__(self, user_id: str,social_id: str, social_name: SocialNetworks) -> None:
        self.user_id = user_id
        self.social_id = social_id
        self.social_name = social_name
        
    def __repr__(self) -> str:
        return f"<SocialAccount {self.social_name}:{self.user_id}>"