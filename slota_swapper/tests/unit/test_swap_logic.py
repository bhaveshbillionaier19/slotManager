"""
Unit tests for swap request and response logic.
This is the most critical part of the application's business logic.
"""
import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from unittest.mock import Mock, patch

from models import User, Event, SwapRequest, EventStatus, SwapRequestStatus
from routers.swaps import (
    create_swap_request,
    respond_to_swap_request,
    list_incoming_requests,
    list_outgoing_requests,
    get_swappable_events
)


class TestSwapRequestCreation:
    """Test swap request creation logic."""
    
    def test_create_valid_swap_request(self, db_session, test_user, another_test_user, swappable_event, another_swappable_event):
        """Test creating a valid swap request."""
        # Create swap request
        swap_data = {
            "offered_event_id": swappable_event.id,
            "requested_event_id": another_swappable_event.id
        }
        
        result = create_swap_request(db_session, swap_data, test_user.id)
        
        assert result is not None
        assert result.requester_id == test_user.id
        assert result.offered_event_id == swappable_event.id
        assert result.requested_event_id == another_swappable_event.id
        assert result.status == SwapRequestStatus.PENDING
    
    def test_create_swap_request_with_own_event(self, db_session, test_user, swappable_event):
        """Test that user cannot request swap with their own event."""
        # Try to create swap request with own event
        swap_data = {
            "offered_event_id": swappable_event.id,
            "requested_event_id": swappable_event.id  # Same event
        }
        
        with pytest.raises(ValueError, match="Cannot swap with your own event"):
            create_swap_request(db_session, swap_data, test_user.id)
    
    def test_create_swap_request_with_non_swappable_offered_event(self, db_session, test_user, another_test_user, test_event, another_swappable_event):
        """Test creating swap request with non-swappable offered event."""
        # test_event has status BUSY, not SWAPPABLE
        swap_data = {
            "offered_event_id": test_event.id,
            "requested_event_id": another_swappable_event.id
        }
        
        with pytest.raises(ValueError, match="Offered event is not swappable"):
            create_swap_request(db_session, swap_data, test_user.id)
    
    def test_create_swap_request_with_non_swappable_requested_event(self, db_session, test_user, another_test_user, swappable_event):
        """Test creating swap request with non-swappable requested event."""
        # Create a BUSY event for another user
        busy_event = Event(
            title="Busy Meeting",
            start_time=datetime.utcnow() + timedelta(hours=1),
            end_time=datetime.utcnow() + timedelta(hours=2),
            owner_id=another_test_user.id,
            status=EventStatus.BUSY
        )
        db_session.add(busy_event)
        db_session.commit()
        
        swap_data = {
            "offered_event_id": swappable_event.id,
            "requested_event_id": busy_event.id
        }
        
        with pytest.raises(ValueError, match="Requested event is not swappable"):
            create_swap_request(db_session, swap_data, test_user.id)
    
    def test_create_duplicate_swap_request(self, db_session, test_user, test_swap_request):
        """Test creating duplicate swap request."""
        # Try to create the same swap request again
        swap_data = {
            "offered_event_id": test_swap_request.offered_event_id,
            "requested_event_id": test_swap_request.requested_event_id
        }
        
        with pytest.raises(ValueError, match="Swap request already exists"):
            create_swap_request(db_session, swap_data, test_user.id)
    
    def test_create_swap_request_with_nonexistent_event(self, db_session, test_user):
        """Test creating swap request with nonexistent events."""
        swap_data = {
            "offered_event_id": "nonexistent-id",
            "requested_event_id": "another-nonexistent-id"
        }
        
        with pytest.raises(ValueError, match="Event not found"):
            create_swap_request(db_session, swap_data, test_user.id)


class TestSwapRequestResponse:
    """Test swap request response logic."""
    
    def test_accept_swap_request(self, db_session, test_swap_request, another_test_user):
        """Test accepting a swap request."""
        # Accept the swap request
        result = respond_to_swap_request(
            db_session, 
            test_swap_request.id, 
            "ACCEPTED", 
            another_test_user.id
        )
        
        assert result.status == SwapRequestStatus.ACCEPTED
        
        # Check that events were swapped
        db_session.refresh(test_swap_request)
        offered_event = db_session.query(Event).filter(Event.id == test_swap_request.offered_event_id).first()
        requested_event = db_session.query(Event).filter(Event.id == test_swap_request.requested_event_id).first()
        
        # Events should have swapped owners
        assert offered_event.owner_id == another_test_user.id
        assert requested_event.owner_id == test_swap_request.requester_id
        
        # Events should be marked as BUSY after swap
        assert offered_event.status == EventStatus.BUSY
        assert requested_event.status == EventStatus.BUSY
    
    def test_decline_swap_request(self, db_session, test_swap_request, another_test_user):
        """Test declining a swap request."""
        # Store original owners
        original_offered_owner = db_session.query(Event).filter(Event.id == test_swap_request.offered_event_id).first().owner_id
        original_requested_owner = db_session.query(Event).filter(Event.id == test_swap_request.requested_event_id).first().owner_id
        
        # Decline the swap request
        result = respond_to_swap_request(
            db_session, 
            test_swap_request.id, 
            "DECLINED", 
            another_test_user.id
        )
        
        assert result.status == SwapRequestStatus.DECLINED
        
        # Check that events were NOT swapped
        db_session.refresh(test_swap_request)
        offered_event = db_session.query(Event).filter(Event.id == test_swap_request.offered_event_id).first()
        requested_event = db_session.query(Event).filter(Event.id == test_swap_request.requested_event_id).first()
        
        # Events should keep original owners
        assert offered_event.owner_id == original_offered_owner
        assert requested_event.owner_id == original_requested_owner
        
        # Events should remain SWAPPABLE
        assert offered_event.status == EventStatus.SWAPPABLE
        assert requested_event.status == EventStatus.SWAPPABLE
    
    def test_respond_to_nonexistent_swap_request(self, db_session, another_test_user):
        """Test responding to nonexistent swap request."""
        with pytest.raises(ValueError, match="Swap request not found"):
            respond_to_swap_request(
                db_session, 
                "nonexistent-id", 
                "ACCEPTED", 
                another_test_user.id
            )
    
    def test_respond_to_swap_request_unauthorized(self, db_session, test_swap_request, test_user):
        """Test responding to swap request by unauthorized user."""
        # test_user is the requester, not the owner of requested event
        with pytest.raises(ValueError, match="Not authorized to respond to this request"):
            respond_to_swap_request(
                db_session, 
                test_swap_request.id, 
                "ACCEPTED", 
                test_user.id
            )
    
    def test_respond_to_already_responded_request(self, db_session, test_swap_request, another_test_user):
        """Test responding to already responded swap request."""
        # First response
        respond_to_swap_request(
            db_session, 
            test_swap_request.id, 
            "ACCEPTED", 
            another_test_user.id
        )
        
        # Try to respond again
        with pytest.raises(ValueError, match="Swap request has already been responded to"):
            respond_to_swap_request(
                db_session, 
                test_swap_request.id, 
                "DECLINED", 
                another_test_user.id
            )
    
    def test_invalid_response_status(self, db_session, test_swap_request, another_test_user):
        """Test responding with invalid status."""
        with pytest.raises(ValueError, match="Invalid response status"):
            respond_to_swap_request(
                db_session, 
                test_swap_request.id, 
                "INVALID_STATUS", 
                another_test_user.id
            )


class TestSwapRequestQueries:
    """Test swap request query functions."""
    
    def test_list_incoming_requests(self, db_session, test_swap_request, another_test_user):
        """Test listing incoming swap requests."""
        incoming_requests = list_incoming_requests(db_session, another_test_user.id)
        
        assert len(incoming_requests) == 1
        assert incoming_requests[0].id == test_swap_request.id
        assert incoming_requests[0].status == SwapRequestStatus.PENDING
    
    def test_list_outgoing_requests(self, db_session, test_swap_request, test_user):
        """Test listing outgoing swap requests."""
        outgoing_requests = list_outgoing_requests(db_session, test_user.id)
        
        assert len(outgoing_requests) == 1
        assert outgoing_requests[0].id == test_swap_request.id
        assert outgoing_requests[0].status == SwapRequestStatus.PENDING
    
    def test_list_incoming_requests_empty(self, db_session, test_user):
        """Test listing incoming requests when there are none."""
        incoming_requests = list_incoming_requests(db_session, test_user.id)
        assert len(incoming_requests) == 0
    
    def test_list_outgoing_requests_empty(self, db_session, another_test_user):
        """Test listing outgoing requests when there are none."""
        outgoing_requests = list_outgoing_requests(db_session, another_test_user.id)
        assert len(outgoing_requests) == 0
    
    def test_list_requests_filters_by_user(self, db_session, test_user, another_test_user):
        """Test that request lists are properly filtered by user."""
        # Create multiple users and swap requests
        third_user = User(
            email="third@example.com",
            name="Third User",
            hashed_password="hashedpassword"
        )
        db_session.add(third_user)
        db_session.commit()
        
        # Create events for third user
        third_user_event = Event(
            title="Third User Event",
            start_time=datetime.utcnow() + timedelta(hours=7),
            end_time=datetime.utcnow() + timedelta(hours=8),
            owner_id=third_user.id,
            status=EventStatus.SWAPPABLE
        )
        db_session.add(third_user_event)
        db_session.commit()
        
        # Create swap request from test_user to third_user
        swap_request_2 = SwapRequest(
            requester_id=test_user.id,
            offered_event_id=test_user.events[0].id,  # Assuming first event is swappable
            requested_event_id=third_user_event.id,
            status=SwapRequestStatus.PENDING
        )
        db_session.add(swap_request_2)
        db_session.commit()
        
        # test_user should see 2 outgoing requests
        outgoing = list_outgoing_requests(db_session, test_user.id)
        assert len(outgoing) == 2
        
        # another_test_user should see 1 incoming request
        incoming_another = list_incoming_requests(db_session, another_test_user.id)
        assert len(incoming_another) == 1
        
        # third_user should see 1 incoming request
        incoming_third = list_incoming_requests(db_session, third_user.id)
        assert len(incoming_third) == 1


class TestSwappableEventsQuery:
    """Test swappable events query logic."""
    
    def test_get_swappable_events_excludes_own_events(self, db_session, test_user, another_test_user, swappable_event, another_swappable_event):
        """Test that swappable events query excludes user's own events."""
        swappable_events = get_swappable_events(db_session, test_user.id)
        
        # Should only see another_test_user's swappable event
        event_ids = [event.id for event in swappable_events]
        assert another_swappable_event.id in event_ids
        assert swappable_event.id not in event_ids
    
    def test_get_swappable_events_only_swappable_status(self, db_session, test_user, another_test_user):
        """Test that only SWAPPABLE events are returned."""
        # Create events with different statuses
        busy_event = Event(
            title="Busy Event",
            start_time=datetime.utcnow() + timedelta(hours=1),
            end_time=datetime.utcnow() + timedelta(hours=2),
            owner_id=another_test_user.id,
            status=EventStatus.BUSY
        )
        
        pending_event = Event(
            title="Pending Event",
            start_time=datetime.utcnow() + timedelta(hours=3),
            end_time=datetime.utcnow() + timedelta(hours=4),
            owner_id=another_test_user.id,
            status=EventStatus.SWAP_PENDING
        )
        
        swappable_event = Event(
            title="Swappable Event",
            start_time=datetime.utcnow() + timedelta(hours=5),
            end_time=datetime.utcnow() + timedelta(hours=6),
            owner_id=another_test_user.id,
            status=EventStatus.SWAPPABLE
        )
        
        db_session.add_all([busy_event, pending_event, swappable_event])
        db_session.commit()
        
        swappable_events = get_swappable_events(db_session, test_user.id)
        
        # Should only see the swappable event
        event_ids = [event.id for event in swappable_events]
        assert swappable_event.id in event_ids
        assert busy_event.id not in event_ids
        assert pending_event.id not in event_ids
    
    def test_get_swappable_events_empty_result(self, db_session, test_user):
        """Test swappable events query when no swappable events exist."""
        swappable_events = get_swappable_events(db_session, test_user.id)
        assert len(swappable_events) == 0


class TestSwapLogicEdgeCases:
    """Test edge cases and error conditions in swap logic."""
    
    def test_swap_request_with_past_events(self, db_session, test_user, another_test_user):
        """Test creating swap request with past events."""
        # Create past events
        past_event_1 = Event(
            title="Past Event 1",
            start_time=datetime.utcnow() - timedelta(hours=2),
            end_time=datetime.utcnow() - timedelta(hours=1),
            owner_id=test_user.id,
            status=EventStatus.SWAPPABLE
        )
        
        past_event_2 = Event(
            title="Past Event 2",
            start_time=datetime.utcnow() - timedelta(hours=4),
            end_time=datetime.utcnow() - timedelta(hours=3),
            owner_id=another_test_user.id,
            status=EventStatus.SWAPPABLE
        )
        
        db_session.add_all([past_event_1, past_event_2])
        db_session.commit()
        
        swap_data = {
            "offered_event_id": past_event_1.id,
            "requested_event_id": past_event_2.id
        }
        
        with pytest.raises(ValueError, match="Cannot swap past events"):
            create_swap_request(db_session, swap_data, test_user.id)
    
    def test_concurrent_swap_requests(self, db_session, test_user, another_test_user, swappable_event, another_swappable_event):
        """Test handling of concurrent swap requests for the same events."""
        # This test simulates race conditions that might occur in production
        
        # Create first swap request
        swap_request_1 = SwapRequest(
            requester_id=test_user.id,
            offered_event_id=swappable_event.id,
            requested_event_id=another_swappable_event.id,
            status=SwapRequestStatus.PENDING
        )
        db_session.add(swap_request_1)
        db_session.commit()
        
        # Try to create another swap request with same events (should fail)
        with pytest.raises(ValueError, match="Swap request already exists"):
            create_swap_request(
                db_session, 
                {
                    "offered_event_id": swappable_event.id,
                    "requested_event_id": another_swappable_event.id
                }, 
                test_user.id
            )
    
    def test_swap_request_status_transitions(self, db_session, test_swap_request, another_test_user):
        """Test valid status transitions for swap requests."""
        # PENDING -> ACCEPTED
        result = respond_to_swap_request(
            db_session, 
            test_swap_request.id, 
            "ACCEPTED", 
            another_test_user.id
        )
        assert result.status == SwapRequestStatus.ACCEPTED
        
        # Create another swap request for DECLINED test
        new_swap_request = SwapRequest(
            requester_id=test_swap_request.requester_id,
            offered_event_id=test_swap_request.offered_event_id,
            requested_event_id=test_swap_request.requested_event_id,
            status=SwapRequestStatus.PENDING
        )
        db_session.add(new_swap_request)
        db_session.commit()
        
        # PENDING -> DECLINED
        result = respond_to_swap_request(
            db_session, 
            new_swap_request.id, 
            "DECLINED", 
            another_test_user.id
        )
        assert result.status == SwapRequestStatus.DECLINED


@pytest.mark.integration
class TestSwapWorkflow:
    """Integration tests for complete swap workflows."""
    
    def test_complete_successful_swap_workflow(self, db_session, test_user, another_test_user):
        """Test complete workflow from event creation to successful swap."""
        # 1. Create swappable events
        event_1 = Event(
            title="Meeting 1",
            start_time=datetime.utcnow() + timedelta(hours=1),
            end_time=datetime.utcnow() + timedelta(hours=2),
            owner_id=test_user.id,
            status=EventStatus.SWAPPABLE
        )
        
        event_2 = Event(
            title="Meeting 2",
            start_time=datetime.utcnow() + timedelta(hours=3),
            end_time=datetime.utcnow() + timedelta(hours=4),
            owner_id=another_test_user.id,
            status=EventStatus.SWAPPABLE
        )
        
        db_session.add_all([event_1, event_2])
        db_session.commit()
        
        # 2. Create swap request
        swap_data = {
            "offered_event_id": event_1.id,
            "requested_event_id": event_2.id
        }
        swap_request = create_swap_request(db_session, swap_data, test_user.id)
        
        # 3. Verify swap request is pending
        assert swap_request.status == SwapRequestStatus.PENDING
        
        # 4. Accept swap request
        accepted_request = respond_to_swap_request(
            db_session, 
            swap_request.id, 
            "ACCEPTED", 
            another_test_user.id
        )
        
        # 5. Verify swap completed successfully
        assert accepted_request.status == SwapRequestStatus.ACCEPTED
        
        # 6. Verify events were swapped
        db_session.refresh(event_1)
        db_session.refresh(event_2)
        
        assert event_1.owner_id == another_test_user.id
        assert event_2.owner_id == test_user.id
        assert event_1.status == EventStatus.BUSY
        assert event_2.status == EventStatus.BUSY
    
    def test_complete_declined_swap_workflow(self, db_session, test_user, another_test_user):
        """Test complete workflow for declined swap."""
        # Similar setup as successful swap
        event_1 = Event(
            title="Meeting 1",
            start_time=datetime.utcnow() + timedelta(hours=1),
            end_time=datetime.utcnow() + timedelta(hours=2),
            owner_id=test_user.id,
            status=EventStatus.SWAPPABLE
        )
        
        event_2 = Event(
            title="Meeting 2",
            start_time=datetime.utcnow() + timedelta(hours=3),
            end_time=datetime.utcnow() + timedelta(hours=4),
            owner_id=another_test_user.id,
            status=EventStatus.SWAPPABLE
        )
        
        db_session.add_all([event_1, event_2])
        db_session.commit()
        
        # Store original owners
        original_owner_1 = event_1.owner_id
        original_owner_2 = event_2.owner_id
        
        # Create and decline swap request
        swap_data = {
            "offered_event_id": event_1.id,
            "requested_event_id": event_2.id
        }
        swap_request = create_swap_request(db_session, swap_data, test_user.id)
        
        declined_request = respond_to_swap_request(
            db_session, 
            swap_request.id, 
            "DECLINED", 
            another_test_user.id
        )
        
        # Verify nothing changed
        assert declined_request.status == SwapRequestStatus.DECLINED
        
        db_session.refresh(event_1)
        db_session.refresh(event_2)
        
        assert event_1.owner_id == original_owner_1
        assert event_2.owner_id == original_owner_2
        assert event_1.status == EventStatus.SWAPPABLE
        assert event_2.status == EventStatus.SWAPPABLE
