import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from slota_swapper.database import Base


class SwapRequestStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class SwapRequest(Base):
    __tablename__ = "swap_requests"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    requester_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    offered_event_id = Column(PGUUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    requested_event_id = Column(PGUUID(as_uuid=True), ForeignKey("events.id"), nullable=False)

    status = Column(Enum(SwapRequestStatusEnum, name="swap_request_status_enum"), nullable=False, default=SwapRequestStatusEnum.PENDING)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    requester = relationship("User", foreign_keys=[requester_id])
    offered_event = relationship("Event", foreign_keys=[offered_event_id])
    requested_event = relationship("Event", foreign_keys=[requested_event_id])

    def __repr__(self) -> str:
        return f"<SwapRequest id={self.id} status={self.status}>"


