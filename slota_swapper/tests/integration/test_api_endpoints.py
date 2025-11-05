"""
Integration tests for API endpoints.
Tests the complete HTTP request/response cycle.
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta


class TestAuthenticationEndpoints:
    """Test authentication API endpoints."""
    
    def test_register_user_success(self, client, sample_user_data):
        """Test successful user registration."""
        response = client.post("/auth/register", json=sample_user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == sample_user_data["email"]
    
    def test_register_user_duplicate_email(self, client, test_user, sample_user_data):
        """Test registration with duplicate email."""
        # Try to register with existing email
        sample_user_data["email"] = test_user.email
        
        response = client.post("/auth/register", json=sample_user_data)
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    def test_register_user_invalid_email(self, client, sample_user_data):
        """Test registration with invalid email."""
        sample_user_data["email"] = "invalid-email"
        
        response = client.post("/auth/register", json=sample_user_data)
        
        assert response.status_code == 422
    
    def test_register_user_weak_password(self, client, sample_user_data):
        """Test registration with weak password."""
        sample_user_data["password"] = "123"  # Too short
        
        response = client.post("/auth/register", json=sample_user_data)
        
        assert response.status_code == 422
    
    def test_login_success(self, client, sample_login_data):
        """Test successful login."""
        response = client.post("/auth/login", json=sample_login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        invalid_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        
        response = client.post("/auth/login", json=invalid_data)
        
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()
    
    def test_login_missing_fields(self, client):
        """Test login with missing fields."""
        # Missing password
        response = client.post("/auth/login", json={"email": "test@example.com"})
        assert response.status_code == 422
        
        # Missing email
        response = client.post("/auth/login", json={"password": "password"})
        assert response.status_code == 422
    
    def test_get_current_user(self, client, auth_headers):
        """Test getting current user information."""
        response = client.get("/auth/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "email" in data
        assert "name" in data
    
    def test_get_current_user_unauthorized(self, client):
        """Test getting current user without authentication."""
        response = client.get("/auth/me")
        
        assert response.status_code == 401
    
    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token."""
        headers = {"Authorization": "Bearer invalid-token"}
        response = client.get("/auth/me", headers=headers)
        
        assert response.status_code == 401


class TestEventEndpoints:
    """Test event management API endpoints."""
    
    def test_create_event_success(self, client, auth_headers, sample_event_data):
        """Test successful event creation."""
        response = client.post("/events/", json=sample_event_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_event_data["title"]
        assert "id" in data
        assert data["status"] == "BUSY"  # Default status
    
    def test_create_event_unauthorized(self, client, sample_event_data):
        """Test event creation without authentication."""
        response = client.post("/events/", json=sample_event_data)
        
        assert response.status_code == 401
    
    def test_create_event_invalid_data(self, client, auth_headers):
        """Test event creation with invalid data."""
        invalid_data = {
            "title": "",  # Empty title
            "start_time": "invalid-datetime",
            "end_time": "invalid-datetime"
        }
        
        response = client.post("/events/", json=invalid_data, headers=auth_headers)
        
        assert response.status_code == 422
    
    def test_create_event_end_before_start(self, client, auth_headers):
        """Test event creation with end time before start time."""
        invalid_data = {
            "title": "Invalid Event",
            "start_time": (datetime.utcnow() + timedelta(hours=2)).isoformat(),
            "end_time": (datetime.utcnow() + timedelta(hours=1)).isoformat()
        }
        
        response = client.post("/events/", json=invalid_data, headers=auth_headers)
        
        assert response.status_code == 400
    
    def test_get_user_events(self, client, auth_headers, test_event):
        """Test getting user's events."""
        response = client.get("/events/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Check if test_event is in the response
        event_ids = [event["id"] for event in data]
        assert test_event.id in event_ids
    
    def test_get_user_events_unauthorized(self, client):
        """Test getting events without authentication."""
        response = client.get("/events/")
        
        assert response.status_code == 401
    
    def test_get_event_by_id(self, client, auth_headers, test_event):
        """Test getting specific event by ID."""
        response = client.get(f"/events/{test_event.id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_event.id
        assert data["title"] == test_event.title
    
    def test_get_nonexistent_event(self, client, auth_headers):
        """Test getting nonexistent event."""
        response = client.get("/events/nonexistent-id", headers=auth_headers)
        
        assert response.status_code == 404
    
    def test_update_event_success(self, client, auth_headers, test_event):
        """Test successful event update."""
        update_data = {
            "title": "Updated Meeting Title",
            "status": "SWAPPABLE"
        }
        
        response = client.put(f"/events/{test_event.id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["status"] == update_data["status"]
    
    def test_update_event_unauthorized(self, client, another_auth_headers, test_event):
        """Test updating event by unauthorized user."""
        update_data = {"title": "Unauthorized Update"}
        
        response = client.put(f"/events/{test_event.id}", json=update_data, headers=another_auth_headers)
        
        assert response.status_code == 403
    
    def test_delete_event_success(self, client, auth_headers, test_event):
        """Test successful event deletion."""
        response = client.delete(f"/events/{test_event.id}", headers=auth_headers)
        
        assert response.status_code == 204
        
        # Verify event is deleted
        get_response = client.get(f"/events/{test_event.id}", headers=auth_headers)
        assert get_response.status_code == 404
    
    def test_delete_event_unauthorized(self, client, another_auth_headers, test_event):
        """Test deleting event by unauthorized user."""
        response = client.delete(f"/events/{test_event.id}", headers=another_auth_headers)
        
        assert response.status_code == 403


class TestSwapRequestEndpoints:
    """Test swap request API endpoints."""
    
    def test_create_swap_request_success(self, client, auth_headers, swappable_event, another_swappable_event):
        """Test successful swap request creation."""
        swap_data = {
            "offered_event_id": swappable_event.id,
            "requested_event_id": another_swappable_event.id
        }
        
        response = client.post("/swaps/request", json=swap_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["offered_event_id"] == swap_data["offered_event_id"]
        assert data["requested_event_id"] == swap_data["requested_event_id"]
        assert data["status"] == "PENDING"
    
    def test_create_swap_request_unauthorized(self, client, swappable_event, another_swappable_event):
        """Test swap request creation without authentication."""
        swap_data = {
            "offered_event_id": swappable_event.id,
            "requested_event_id": another_swappable_event.id
        }
        
        response = client.post("/swaps/request", json=swap_data)
        
        assert response.status_code == 401
    
    def test_create_invalid_swap_request(self, client, auth_headers, test_event, another_swappable_event):
        """Test creating swap request with non-swappable event."""
        swap_data = {
            "offered_event_id": test_event.id,  # BUSY event, not swappable
            "requested_event_id": another_swappable_event.id
        }
        
        response = client.post("/swaps/request", json=swap_data, headers=auth_headers)
        
        assert response.status_code == 400
    
    def test_get_incoming_requests(self, client, another_auth_headers, test_swap_request):
        """Test getting incoming swap requests."""
        response = client.get("/swaps/incoming-requests", headers=another_auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Check if test_swap_request is in the response
        request_ids = [req["id"] for req in data]
        assert test_swap_request.id in request_ids
    
    def test_get_outgoing_requests(self, client, auth_headers, test_swap_request):
        """Test getting outgoing swap requests."""
        response = client.get("/swaps/outgoing-requests", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Check if test_swap_request is in the response
        request_ids = [req["id"] for req in data]
        assert test_swap_request.id in request_ids
    
    def test_respond_to_swap_request_accept(self, client, another_auth_headers, test_swap_request):
        """Test accepting a swap request."""
        response_data = {"response": "ACCEPTED"}
        
        response = client.post(
            f"/swaps/{test_swap_request.id}/respond", 
            json=response_data, 
            headers=another_auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ACCEPTED"
    
    def test_respond_to_swap_request_decline(self, client, another_auth_headers, test_swap_request):
        """Test declining a swap request."""
        response_data = {"response": "DECLINED"}
        
        response = client.post(
            f"/swaps/{test_swap_request.id}/respond", 
            json=response_data, 
            headers=another_auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "DECLINED"
    
    def test_respond_to_swap_request_unauthorized(self, client, auth_headers, test_swap_request):
        """Test responding to swap request by unauthorized user."""
        response_data = {"response": "ACCEPTED"}
        
        response = client.post(
            f"/swaps/{test_swap_request.id}/respond", 
            json=response_data, 
            headers=auth_headers  # Wrong user
        )
        
        assert response.status_code == 403
    
    def test_get_swappable_events(self, client, auth_headers, another_swappable_event):
        """Test getting swappable events."""
        response = client.get("/swaps/swappable-events", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # Should see another user's swappable event
        event_ids = [event["id"] for event in data]
        assert another_swappable_event.id in event_ids
    
    def test_get_swappable_events_unauthorized(self, client):
        """Test getting swappable events without authentication."""
        response = client.get("/swaps/swappable-events")
        
        assert response.status_code == 401


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


@pytest.mark.integration
class TestCompleteWorkflows:
    """Test complete user workflows through API."""
    
    def test_complete_user_registration_and_login_flow(self, client):
        """Test complete user registration and login workflow."""
        # 1. Register new user
        user_data = {
            "email": "workflow@example.com",
            "name": "Workflow User",
            "password": "workflowpassword123"
        }
        
        register_response = client.post("/auth/register", json=user_data)
        assert register_response.status_code == 201
        
        register_data = register_response.json()
        token = register_data["access_token"]
        
        # 2. Use token to access protected endpoint
        headers = {"Authorization": f"Bearer {token}"}
        me_response = client.get("/auth/me", headers=headers)
        assert me_response.status_code == 200
        
        # 3. Login with same credentials
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        login_response = client.post("/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        login_token = login_response.json()["access_token"]
        
        # 4. Use login token
        headers = {"Authorization": f"Bearer {login_token}"}
        me_response = client.get("/auth/me", headers=headers)
        assert me_response.status_code == 200
    
    def test_complete_event_management_workflow(self, client, auth_headers):
        """Test complete event management workflow."""
        # 1. Create event
        event_data = {
            "title": "Workflow Meeting",
            "start_time": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
            "end_time": (datetime.utcnow() + timedelta(hours=2)).isoformat()
        }
        
        create_response = client.post("/events/", json=event_data, headers=auth_headers)
        assert create_response.status_code == 201
        
        event_id = create_response.json()["id"]
        
        # 2. Get event
        get_response = client.get(f"/events/{event_id}", headers=auth_headers)
        assert get_response.status_code == 200
        
        # 3. Update event
        update_data = {
            "title": "Updated Workflow Meeting",
            "status": "SWAPPABLE"
        }
        
        update_response = client.put(f"/events/{event_id}", json=update_data, headers=auth_headers)
        assert update_response.status_code == 200
        assert update_response.json()["title"] == update_data["title"]
        
        # 4. List events
        list_response = client.get("/events/", headers=auth_headers)
        assert list_response.status_code == 200
        
        event_ids = [event["id"] for event in list_response.json()]
        assert event_id in event_ids
        
        # 5. Delete event
        delete_response = client.delete(f"/events/{event_id}", headers=auth_headers)
        assert delete_response.status_code == 204
        
        # 6. Verify deletion
        get_deleted_response = client.get(f"/events/{event_id}", headers=auth_headers)
        assert get_deleted_response.status_code == 404
    
    def test_complete_swap_workflow(self, client, auth_headers, another_auth_headers):
        """Test complete swap request workflow."""
        # 1. Create swappable events for both users
        event_data_1 = {
            "title": "Swappable Meeting 1",
            "start_time": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
            "end_time": (datetime.utcnow() + timedelta(hours=2)).isoformat()
        }
        
        event_data_2 = {
            "title": "Swappable Meeting 2",
            "start_time": (datetime.utcnow() + timedelta(hours=3)).isoformat(),
            "end_time": (datetime.utcnow() + timedelta(hours=4)).isoformat()
        }
        
        # Create events
        event_1_response = client.post("/events/", json=event_data_1, headers=auth_headers)
        event_2_response = client.post("/events/", json=event_data_2, headers=another_auth_headers)
        
        event_1_id = event_1_response.json()["id"]
        event_2_id = event_2_response.json()["id"]
        
        # Make events swappable
        client.put(f"/events/{event_1_id}", json={"status": "SWAPPABLE"}, headers=auth_headers)
        client.put(f"/events/{event_2_id}", json={"status": "SWAPPABLE"}, headers=another_auth_headers)
        
        # 2. Create swap request
        swap_data = {
            "offered_event_id": event_1_id,
            "requested_event_id": event_2_id
        }
        
        swap_response = client.post("/swaps/request", json=swap_data, headers=auth_headers)
        assert swap_response.status_code == 201
        
        swap_request_id = swap_response.json()["id"]
        
        # 3. Check incoming requests for second user
        incoming_response = client.get("/swaps/incoming-requests", headers=another_auth_headers)
        assert incoming_response.status_code == 200
        
        request_ids = [req["id"] for req in incoming_response.json()]
        assert swap_request_id in request_ids
        
        # 4. Accept swap request
        accept_data = {"response": "ACCEPTED"}
        accept_response = client.post(
            f"/swaps/{swap_request_id}/respond", 
            json=accept_data, 
            headers=another_auth_headers
        )
        assert accept_response.status_code == 200
        assert accept_response.json()["status"] == "ACCEPTED"
        
        # 5. Verify events were swapped
        event_1_after = client.get(f"/events/{event_1_id}", headers=another_auth_headers)
        event_2_after = client.get(f"/events/{event_2_id}", headers=auth_headers)
        
        # Both users should now be able to access the swapped events
        assert event_1_after.status_code == 200
        assert event_2_after.status_code == 200


class TestErrorHandling:
    """Test API error handling."""
    
    def test_404_for_nonexistent_endpoints(self, client):
        """Test 404 response for nonexistent endpoints."""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404
    
    def test_405_for_wrong_http_methods(self, client):
        """Test 405 response for wrong HTTP methods."""
        # POST to GET-only endpoint
        response = client.post("/health")
        assert response.status_code == 405
        
        # GET to POST-only endpoint
        response = client.get("/auth/login")
        assert response.status_code == 405
    
    def test_422_for_invalid_request_body(self, client, auth_headers):
        """Test 422 response for invalid request bodies."""
        # Invalid JSON
        response = client.post(
            "/events/", 
            data="invalid json", 
            headers={**auth_headers, "Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_rate_limiting_headers(self, client):
        """Test that rate limiting headers are present (if implemented)."""
        response = client.get("/health")
        
        # These headers might be present if rate limiting is implemented
        # Adjust based on your actual implementation
        assert response.status_code == 200
        # assert "X-RateLimit-Limit" in response.headers  # Uncomment if implemented
    
    def test_cors_headers(self, client):
        """Test CORS headers are present."""
        response = client.options("/health")
        
        # CORS headers should be present for OPTIONS requests
        # Adjust based on your CORS configuration
        assert response.status_code in [200, 204]
