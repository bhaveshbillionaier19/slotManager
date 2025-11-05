"""
Test data factories using Factory Boy for generating test data.
"""
import factory
from factory.alchemy import SQLAlchemyModelFactory
from datetime import datetime, timedelta
from faker import Faker

from models import User, Event, SwapRequest, EventStatus, SwapRequestStatus
from auth import get_password_hash

fake = Faker()


class UserFactory(SQLAlchemyModelFactory):
    """Factory for creating User instances."""
    
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"
    
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker('name')
    hashed_password = factory.LazyAttribute(lambda obj: get_password_hash("testpassword123"))
    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)


class EventFactory(SQLAlchemyModelFactory):
    """Factory for creating Event instances."""
    
    class Meta:
        model = Event
        sqlalchemy_session_persistence = "commit"
    
    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('text', max_nb_chars=200)
    start_time = factory.LazyFunction(lambda: datetime.utcnow() + timedelta(hours=1))
    end_time = factory.LazyAttribute(lambda obj: obj.start_time + timedelta(hours=1))
    status = EventStatus.BUSY
    owner = factory.SubFactory(UserFactory)
    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)


class SwappableEventFactory(EventFactory):
    """Factory for creating swappable Event instances."""
    
    status = EventStatus.SWAPPABLE


class SwapRequestFactory(SQLAlchemyModelFactory):
    """Factory for creating SwapRequest instances."""
    
    class Meta:
        model = SwapRequest
        sqlalchemy_session_persistence = "commit"
    
    requester = factory.SubFactory(UserFactory)
    offered_event = factory.SubFactory(SwappableEventFactory)
    requested_event = factory.SubFactory(SwappableEventFactory)
    status = SwapRequestStatus.PENDING
    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)


# Specialized factories for different scenarios

class PastEventFactory(EventFactory):
    """Factory for creating past events."""
    
    start_time = factory.LazyFunction(lambda: datetime.utcnow() - timedelta(hours=2))
    end_time = factory.LazyAttribute(lambda obj: obj.start_time + timedelta(hours=1))


class FutureEventFactory(EventFactory):
    """Factory for creating future events."""
    
    start_time = factory.LazyFunction(lambda: datetime.utcnow() + timedelta(days=1))
    end_time = factory.LazyAttribute(lambda obj: obj.start_time + timedelta(hours=1))


class LongEventFactory(EventFactory):
    """Factory for creating long duration events."""
    
    start_time = factory.LazyFunction(lambda: datetime.utcnow() + timedelta(hours=1))
    end_time = factory.LazyAttribute(lambda obj: obj.start_time + timedelta(hours=8))


class AcceptedSwapRequestFactory(SwapRequestFactory):
    """Factory for creating accepted swap requests."""
    
    status = SwapRequestStatus.ACCEPTED


class DeclinedSwapRequestFactory(SwapRequestFactory):
    """Factory for creating declined swap requests."""
    
    status = SwapRequestStatus.DECLINED


# Batch creation helpers

class TestDataBuilder:
    """Helper class for building complex test scenarios."""
    
    def __init__(self, session):
        self.session = session
    
    def create_user_with_events(self, num_events=3, swappable_count=1):
        """Create a user with multiple events."""
        user = UserFactory(sqlalchemy_session=self.session)
        
        events = []
        for i in range(num_events):
            if i < swappable_count:
                event = SwappableEventFactory(
                    owner=user,
                    sqlalchemy_session=self.session,
                    start_time=datetime.utcnow() + timedelta(hours=i+1),
                    end_time=datetime.utcnow() + timedelta(hours=i+2)
                )
            else:
                event = EventFactory(
                    owner=user,
                    sqlalchemy_session=self.session,
                    start_time=datetime.utcnow() + timedelta(hours=i+1),
                    end_time=datetime.utcnow() + timedelta(hours=i+2)
                )
            events.append(event)
        
        return user, events
    
    def create_swap_scenario(self):
        """Create a complete swap scenario with two users and their events."""
        # Create two users with swappable events
        user1, events1 = self.create_user_with_events(num_events=2, swappable_count=1)
        user2, events2 = self.create_user_with_events(num_events=2, swappable_count=1)
        
        # Get swappable events
        swappable_event1 = next(e for e in events1 if e.status == EventStatus.SWAPPABLE)
        swappable_event2 = next(e for e in events2 if e.status == EventStatus.SWAPPABLE)
        
        # Create swap request
        swap_request = SwapRequestFactory(
            requester=user1,
            offered_event=swappable_event1,
            requested_event=swappable_event2,
            sqlalchemy_session=self.session
        )
        
        return {
            'user1': user1,
            'user2': user2,
            'events1': events1,
            'events2': events2,
            'swappable_event1': swappable_event1,
            'swappable_event2': swappable_event2,
            'swap_request': swap_request
        }
    
    def create_multiple_swap_requests(self, count=5):
        """Create multiple swap requests for testing pagination and filtering."""
        swap_requests = []
        
        for i in range(count):
            user1 = UserFactory(sqlalchemy_session=self.session)
            user2 = UserFactory(sqlalchemy_session=self.session)
            
            event1 = SwappableEventFactory(
                owner=user1,
                sqlalchemy_session=self.session,
                start_time=datetime.utcnow() + timedelta(hours=i+1)
            )
            
            event2 = SwappableEventFactory(
                owner=user2,
                sqlalchemy_session=self.session,
                start_time=datetime.utcnow() + timedelta(hours=i+10)
            )
            
            swap_request = SwapRequestFactory(
                requester=user1,
                offered_event=event1,
                requested_event=event2,
                sqlalchemy_session=self.session
            )
            
            swap_requests.append(swap_request)
        
        return swap_requests
    
    def create_time_conflict_scenario(self):
        """Create events with time conflicts for testing."""
        user = UserFactory(sqlalchemy_session=self.session)
        
        base_time = datetime.utcnow() + timedelta(hours=1)
        
        # Overlapping events
        event1 = EventFactory(
            owner=user,
            sqlalchemy_session=self.session,
            start_time=base_time,
            end_time=base_time + timedelta(hours=2)
        )
        
        event2 = EventFactory(
            owner=user,
            sqlalchemy_session=self.session,
            start_time=base_time + timedelta(hours=1),  # Overlaps with event1
            end_time=base_time + timedelta(hours=3)
        )
        
        return user, [event1, event2]


# Mock data generators for API testing

class MockAPIData:
    """Generate mock data for API testing."""
    
    @staticmethod
    def user_registration_data(email=None, name=None, password=None):
        """Generate user registration data."""
        return {
            "email": email or fake.email(),
            "name": name or fake.name(),
            "password": password or "testpassword123"
        }
    
    @staticmethod
    def event_creation_data(title=None, hours_from_now=1, duration_hours=1):
        """Generate event creation data."""
        start_time = datetime.utcnow() + timedelta(hours=hours_from_now)
        end_time = start_time + timedelta(hours=duration_hours)
        
        return {
            "title": title or fake.sentence(nb_words=3),
            "description": fake.text(max_nb_chars=200),
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        }
    
    @staticmethod
    def swap_request_data(offered_event_id, requested_event_id):
        """Generate swap request data."""
        return {
            "offered_event_id": offered_event_id,
            "requested_event_id": requested_event_id
        }
    
    @staticmethod
    def login_data(email, password="testpassword123"):
        """Generate login data."""
        return {
            "email": email,
            "password": password
        }
    
    @staticmethod
    def event_update_data(title=None, status=None, description=None):
        """Generate event update data."""
        data = {}
        
        if title is not None:
            data["title"] = title
        if status is not None:
            data["status"] = status
        if description is not None:
            data["description"] = description
        
        return data


# Performance testing data generators

class PerformanceDataGenerator:
    """Generate large datasets for performance testing."""
    
    def __init__(self, session):
        self.session = session
    
    def create_large_user_base(self, count=1000):
        """Create a large number of users for performance testing."""
        users = []
        
        # Use batch creation for better performance
        for i in range(0, count, 100):  # Create in batches of 100
            batch_users = UserFactory.create_batch(
                min(100, count - i),
                sqlalchemy_session=self.session
            )
            users.extend(batch_users)
        
        return users
    
    def create_many_events(self, users, events_per_user=10):
        """Create many events for performance testing."""
        events = []
        
        for user in users:
            user_events = EventFactory.create_batch(
                events_per_user,
                owner=user,
                sqlalchemy_session=self.session
            )
            events.extend(user_events)
        
        return events
    
    def create_many_swap_requests(self, events, request_count=5000):
        """Create many swap requests for performance testing."""
        import random
        
        swap_requests = []
        swappable_events = [e for e in events if e.status == EventStatus.SWAPPABLE]
        
        if len(swappable_events) < 2:
            # Make some events swappable
            for i in range(0, min(len(events), 200), 2):
                events[i].status = EventStatus.SWAPPABLE
            swappable_events = [e for e in events if e.status == EventStatus.SWAPPABLE]
        
        for _ in range(request_count):
            # Randomly select two different events from different owners
            event1, event2 = random.sample(swappable_events, 2)
            
            if event1.owner_id != event2.owner_id:
                swap_request = SwapRequestFactory(
                    requester=event1.owner,
                    offered_event=event1,
                    requested_event=event2,
                    sqlalchemy_session=self.session
                )
                swap_requests.append(swap_request)
        
        return swap_requests


# Utility functions for test data cleanup

def cleanup_test_data(session):
    """Clean up all test data from the database."""
    # Delete in reverse order of dependencies
    session.query(SwapRequest).delete()
    session.query(Event).delete()
    session.query(User).delete()
    session.commit()


def reset_factory_sequences():
    """Reset all factory sequences to start from 1."""
    UserFactory.reset_sequence()
    EventFactory.reset_sequence()
    SwapRequestFactory.reset_sequence()
