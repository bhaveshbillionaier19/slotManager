import uuid
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from slota_swapper.database import get_db
from slota_swapper.models.event import Event, EventStatusEnum
from slota_swapper.schemas.event_schemas import EventCreate, EventUpdate, EventResponse
from slota_swapper.auth.jwt_handler import get_current_user
from slota_swapper.models.user import User


events_router = APIRouter(prefix="/events", tags=["Events"])


@events_router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    payload: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = Event(
        title=payload.title,
        start_time=payload.start_time,
        end_time=payload.end_time,
        status=EventStatusEnum.BUSY,
        owner_id=current_user.id,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@events_router.get("/", response_model=List[EventResponse])
def list_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    events = db.query(Event).where(Event.owner_id == current_user.id).order_by(Event.start_time.asc()).all()
    return events


@events_router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event


@events_router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: uuid.UUID,
    payload: EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    if payload.title is not None:
        event.title = payload.title
    if payload.start_time is not None:
        event.start_time = payload.start_time
    if payload.end_time is not None:
        event.end_time = payload.end_time
    if payload.status is not None:
        event.status = EventStatusEnum(payload.status)

    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@events_router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    db.delete(event)
    db.commit()
    return None


