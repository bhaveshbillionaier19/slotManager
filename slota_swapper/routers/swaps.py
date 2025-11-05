import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import aliased

from slota_swapper.database import get_db
from slota_swapper.auth.jwt_handler import get_current_user
from slota_swapper.models.user import User
from slota_swapper.models.event import Event, EventStatusEnum
from slota_swapper.models.swap_request import SwapRequest, SwapRequestStatusEnum
from slota_swapper.schemas.swap_schemas import (
    SwappableEventResponse,
    SwapRequestCreate,
    SwapRequestResponse,
    SwapRequestStatus,
    SwapResponseAction,
)
from slota_swapper.schemas.event_schemas import EventResponse
from slota_swapper.schemas.user_schemas import UserResponse


swaps_router = APIRouter(prefix="/swaps", tags=["Swaps"])


@swaps_router.get("/swappable-slots", response_model=List[SwappableEventResponse])
def list_swappable_slots(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = (
        select(Event, User.name)
        .join(User, Event.owner_id == User.id)
        .where(Event.status == EventStatusEnum.SWAPPABLE)
        .where(Event.owner_id != current_user.id)
        .order_by(Event.start_time.asc())
    )
    rows = db.execute(stmt).all()

    results: List[SwappableEventResponse] = []
    for event, owner_name in rows:
        # Build response combining EventResponse fields + owner_name
        results.append(
            SwappableEventResponse(
                id=event.id,
                title=event.title,
                start_time=event.start_time,
                end_time=event.end_time,
                status=event.status.value if hasattr(event.status, "value") else event.status,
                owner_id=event.owner_id,
                owner_name=owner_name,
            )
        )
    return results


@swaps_router.post("/request-swap", response_model=SwapRequestResponse, status_code=status.HTTP_201_CREATED)
def request_swap(
    payload: SwapRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    my_slot = db.query(Event).filter(Event.id == payload.my_slot_id).first()
    if my_slot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="My slot not found")

    their_slot = db.query(Event).filter(Event.id == payload.their_slot_id).first()
    if their_slot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Their slot not found")

    if my_slot.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own the offered slot")

    if their_slot.owner_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot request swap with your own slot")

    if my_slot.status != EventStatusEnum.SWAPPABLE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your slot is not swappable")

    if their_slot.status != EventStatusEnum.SWAPPABLE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Requested slot is not swappable")

    swap = SwapRequest(
        requester_id=current_user.id,
        offered_event_id=my_slot.id,
        requested_event_id=their_slot.id,
        status=SwapRequestStatusEnum.PENDING,
    )

    my_slot.status = EventStatusEnum.SWAP_PENDING
    their_slot.status = EventStatusEnum.SWAP_PENDING

    db.add(swap)
    db.add(my_slot)
    db.add(their_slot)
    db.commit()
    db.refresh(swap)

    return SwapRequestResponse(
        id=swap.id,
        requester_id=swap.requester_id,
        offered_event_id=swap.offered_event_id,
        requested_event_id=swap.requested_event_id,
        status=SwapRequestStatus(swap.status.value if hasattr(swap.status, "value") else swap.status),
        created_at=swap.created_at,
        updated_at=swap.updated_at,
        offered_event_details=EventResponse.model_validate(my_slot, from_attributes=True),
        requested_event_details=EventResponse.model_validate(their_slot, from_attributes=True),
        requester_details=UserResponse.model_validate(current_user, from_attributes=True),
    )


@swaps_router.get("/incoming-requests", response_model=List[SwapRequestResponse])
def list_incoming_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # SQLAlchemy aliasing for two joins to Event
    offered_evt = aliased(Event, name="offered_evt")
    requested_evt = aliased(Event, name="requested_evt")
    stmt = (
        select(SwapRequest, offered_evt, requested_evt, User)
        .join(offered_evt, SwapRequest.offered_event_id == offered_evt.id)
        .join(requested_evt, SwapRequest.requested_event_id == requested_evt.id)
        .join(User, SwapRequest.requester_id == User.id)
        .where(SwapRequest.status == SwapRequestStatusEnum.PENDING)
        .where(requested_evt.owner_id == current_user.id)
        .order_by(SwapRequest.created_at.desc())
    )

    rows = db.execute(stmt).all()
    responses: List[SwapRequestResponse] = []
    for swap, offered_event, requested_event, requester in rows:
        responses.append(
            SwapRequestResponse(
                id=swap.id,
                requester_id=swap.requester_id,
                offered_event_id=swap.offered_event_id,
                requested_event_id=swap.requested_event_id,
                status=SwapRequestStatus(swap.status.value if hasattr(swap.status, "value") else swap.status),
                created_at=swap.created_at,
                updated_at=swap.updated_at,
                offered_event_details=EventResponse.model_validate(offered_event, from_attributes=True),
                requested_event_details=EventResponse.model_validate(requested_event, from_attributes=True),
                requester_details=UserResponse.model_validate(requester, from_attributes=True),
            )
        )
    return responses


@swaps_router.get("/outgoing-requests", response_model=List[SwapRequestResponse])
def list_outgoing_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    offered_evt = aliased(Event, name="offered_evt")
    requested_evt = aliased(Event, name="requested_evt")
    stmt = (
        select(SwapRequest, offered_evt, requested_evt, User)
        .join(offered_evt, SwapRequest.offered_event_id == offered_evt.id)
        .join(requested_evt, SwapRequest.requested_event_id == requested_evt.id)
        .join(User, SwapRequest.requester_id == User.id)
        .where(SwapRequest.requester_id == current_user.id)
        .order_by(SwapRequest.created_at.desc())
    )
    rows = db.execute(stmt).all()
    responses: List[SwapRequestResponse] = []
    for swap, offered_event, requested_event, requester in rows:
        responses.append(
            SwapRequestResponse(
                id=swap.id,
                requester_id=swap.requester_id,
                offered_event_id=swap.offered_event_id,
                requested_event_id=swap.requested_event_id,
                status=SwapRequestStatus(swap.status.value if hasattr(swap.status, "value") else swap.status),
                created_at=swap.created_at,
                updated_at=swap.updated_at,
                offered_event_details=EventResponse.model_validate(offered_event, from_attributes=True),
                requested_event_details=EventResponse.model_validate(requested_event, from_attributes=True),
                requester_details=UserResponse.model_validate(requester, from_attributes=True),
            )
        )
    return responses


@swaps_router.post("/response-swap/{request_id}", response_model=SwapRequestResponse)
def respond_to_swap(
    request_id: uuid.UUID,
    action: SwapResponseAction,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    swap: SwapRequest | None = db.query(SwapRequest).filter(SwapRequest.id == request_id).first()
    if swap is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Swap request not found")

    offered_event: Event | None = db.query(Event).filter(Event.id == swap.offered_event_id).first()
    requested_event: Event | None = db.query(Event).filter(Event.id == swap.requested_event_id).first()
    if offered_event is None or requested_event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Related events not found")

    if requested_event.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to respond to this request")

    if swap.status != SwapRequestStatusEnum.PENDING:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Swap request already processed")

    try:
        if not action.accepted:
            swap.status = SwapRequestStatusEnum.REJECTED
            # revert statuses
            if offered_event.status == EventStatusEnum.SWAP_PENDING:
                offered_event.status = EventStatusEnum.SWAPPABLE
            if requested_event.status == EventStatusEnum.SWAP_PENDING:
                requested_event.status = EventStatusEnum.SWAPPABLE
        else:
            swap.status = SwapRequestStatusEnum.ACCEPTED
            # swap owners
            original_requested_owner = requested_event.owner_id
            requested_event.owner_id = offered_event.owner_id
            offered_event.owner_id = original_requested_owner
            # mark as busy after swap
            requested_event.status = EventStatusEnum.BUSY
            offered_event.status = EventStatusEnum.BUSY

        db.add(swap)
        db.add(offered_event)
        db.add(requested_event)
        db.commit()
        db.refresh(swap)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process swap response")

    # prepare response with details
    requester = db.query(User).filter(User.id == swap.requester_id).first()
    offered_ev = db.query(Event).filter(Event.id == swap.offered_event_id).first()
    requested_ev = db.query(Event).filter(Event.id == swap.requested_event_id).first()

    return SwapRequestResponse(
        id=swap.id,
        requester_id=swap.requester_id,
        offered_event_id=swap.offered_event_id,
        requested_event_id=swap.requested_event_id,
        status=SwapRequestStatus(swap.status.value if hasattr(swap.status, "value") else swap.status),
        created_at=swap.created_at,
        updated_at=swap.updated_at,
        offered_event_details=EventResponse.model_validate(offered_ev, from_attributes=True),
        requested_event_details=EventResponse.model_validate(requested_ev, from_attributes=True),
        requester_details=UserResponse.model_validate(requester, from_attributes=True),
    )


