"""
Test configuration and fixtures for SlotSwapper backend tests.
"""
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app, get_db
from database import Base
from models import User, Event, SwapRequest
from auth import get_password_hash, create_access_token
from datetime import datetime, timedelta


# Test database URL (SQLite in-memory for fast tests)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session) -> User:
    """Create a test user."""
    user = User(
        email="test@example.com",
        name="Test User",
        hashed_password=get_password_hash("testpassword123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def another_test_user(db_session) -> User:
    """Create another test user for multi-user tests."""
    user = User(
        email="another@example.com",
        name="Another User",
        hashed_password=get_password_hash("anotherpassword123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user) -> dict:
    """Create authentication headers for test user."""
    token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def another_auth_headers(another_test_user) -> dict:
    """Create authentication headers for another test user."""
    token = create_access_token(data={"sub": str(another_test_user.id)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_event(db_session, test_user) -> Event:
    """Create a test event."""
    event = Event(
        title="Test Meeting",
        start_time=datetime.utcnow() + timedelta(hours=1),
        end_time=datetime.utcnow() + timedelta(hours=2),
        owner_id=test_user.id,
        status="BUSY"
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)
    return event


@pytest.fixture
def swappable_event(db_session, test_user) -> Event:
    """Create a swappable test event."""
    event = Event(
        title="Swappable Meeting",
        start_time=datetime.utcnow() + timedelta(hours=3),
        end_time=datetime.utcnow() + timedelta(hours=4),
        owner_id=test_user.id,
        status="SWAPPABLE"
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)
    return event


@pytest.fixture
def another_swappable_event(db_session, another_test_user) -> Event:
    """Create a swappable event for another user."""
    event = Event(
        title="Another Swappable Meeting",
        start_time=datetime.utcnow() + timedelta(hours=5),
        end_time=datetime.utcnow() + timedelta(hours=6),
        owner_id=another_test_user.id,
        status="SWAPPABLE"
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)
    return event


@pytest.fixture
def test_swap_request(db_session, test_user, another_test_user, swappable_event, another_swappable_event) -> SwapRequest:
    """Create a test swap request."""
    swap_request = SwapRequest(
        requester_id=test_user.id,
        offered_event_id=swappable_event.id,
        requested_event_id=another_swappable_event.id,
        status="PENDING"
    )
    db_session.add(swap_request)
    db_session.commit()
    db_session.refresh(swap_request)
    return swap_request


# Sample data for testing
@pytest.fixture
def sample_user_data():
    """Sample user registration data."""
    return {
        "email": "newuser@example.com",
        "name": "New User",
        "password": "newpassword123"
    }


@pytest.fixture
def sample_event_data():
    """Sample event creation data."""
    return {
        "title": "New Test Meeting",
        "start_time": (datetime.utcnow() + timedelta(hours=24)).isoformat(),
        "end_time": (datetime.utcnow() + timedelta(hours=25)).isoformat()
    }


@pytest.fixture
def sample_login_data():
    """Sample login data."""
    return {
        "email": "test@example.com",
        "password": "testpassword123"
    }


# Mock data generators
class MockDataGenerator:
    """Generate mock data for testing."""
    
    @staticmethod
    def create_user_data(email: str = None, name: str = None) -> dict:
        """Create user data with optional overrides."""
        return {
            "email": email or "mock@example.com",
            "name": name or "Mock User",
            "password": "mockpassword123"
        }
    
    @staticmethod
    def create_event_data(title: str = None, hours_from_now: int = 1) -> dict:
        """Create event data with optional overrides."""
        start_time = datetime.utcnow() + timedelta(hours=hours_from_now)
        end_time = start_time + timedelta(hours=1)
        
        return {
            "title": title or "Mock Meeting",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        }


@pytest.fixture
def mock_data():
    """Provide mock data generator."""
    return MockDataGenerator
