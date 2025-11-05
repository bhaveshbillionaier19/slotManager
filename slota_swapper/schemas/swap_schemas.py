import enum
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from slota_swapper.schemas.event_schemas import EventResponse
from slota_swapper.schemas.user_schemas import UserResponse


class SwapRequestStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class SwapRequestCreate(BaseModel):
    my_slot_id: uuid.UUID
    their_slot_id: uuid.UUID


class SwapRequestResponse(BaseModel):
    id: uuid.UUID
    requester_id: uuid.UUID
    offered_event_id: uuid.UUID
    requested_event_id: uuid.UUID
    status: SwapRequestStatus
    created_at: datetime
    updated_at: datetime
    offered_event_details: EventResponse
    requested_event_details: EventResponse
    requester_details: UserResponse

    model_config = {
        "from_attributes": True,
    }


class SwappableEventResponse(EventResponse):
    owner_name: str


class SwapResponseAction(BaseModel):
    accepted: bool

    model_config = {
        "from_attributes": True,
    }


