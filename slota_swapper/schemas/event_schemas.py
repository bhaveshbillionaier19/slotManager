import enum
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EventStatus(str, enum.Enum):
    BUSY = "BUSY"
    SWAPPABLE = "SWAPPABLE"
    SWAP_PENDING = "SWAP_PENDING"


class EventCreate(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime


class EventUpdate(BaseModel):
    title: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[EventStatus] = None


class EventResponse(BaseModel):
    id: uuid.UUID
    title: str
    start_time: datetime
    end_time: datetime
    status: EventStatus
    owner_id: uuid.UUID

    model_config = {
        "from_attributes": True,
    }


