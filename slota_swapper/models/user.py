import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from slota_swapper.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} name={self.name}>"

    # Relationships
    events = relationship("Event", back_populates="owner", cascade="all, delete-orphan")


