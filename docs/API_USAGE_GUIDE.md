# SlotSwapper API Usage Guide

This guide provides practical examples of how to use the SlotSwapper API for common workflows.

## 🚀 Quick Start Workflow

### 1. User Registration and Authentication

```bash
# Register a new user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "name": "Alice Johnson",
    "password": "securepassword123"
  }'

# Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": "user-uuid-123",
    "email": "alice@example.com",
    "name": "Alice Johnson"
  }
}

# Save the access_token for subsequent requests
export TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### 2. Create Events

```bash
# Create a meeting event
curl -X POST "http://localhost:8000/events/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Project Planning Meeting",
    "description": "Q4 project planning session",
    "start_time": "2024-12-15T14:00:00",
    "end_time": "2024-12-15T15:30:00"
  }'

# Response:
{
  "id": "event-uuid-456",
  "title": "Project Planning Meeting",
  "description": "Q4 project planning session",
  "start_time": "2024-12-15T14:00:00",
  "end_time": "2024-12-15T15:30:00",
  "status": "BUSY",
  "owner_id": "user-uuid-123",
  "created_at": "2024-11-05T15:30:00",
  "updated_at": "2024-11-05T15:30:00"
}
```

### 3. Make Event Swappable

```bash
# Update event to be swappable
curl -X PUT "http://localhost:8000/events/event-uuid-456" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "SWAPPABLE"
  }'
```

### 4. Find Swappable Events

```bash
# Get events available for swapping
curl -X GET "http://localhost:8000/swaps/swappable-events" \
  -H "Authorization: Bearer $TOKEN"

# Response:
[
  {
    "id": "event-uuid-789",
    "title": "Team Standup",
    "start_time": "2024-12-15T09:00:00",
    "end_time": "2024-12-15T09:30:00",
    "status": "SWAPPABLE",
    "owner": {
      "id": "user-uuid-999",
      "name": "Bob Smith",
      "email": "bob@example.com"
    }
  }
]
```

### 5. Create Swap Request

```bash
# Request to swap your event with another user's event
curl -X POST "http://localhost:8000/swaps/request" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "offered_event_id": "event-uuid-456",
    "requested_event_id": "event-uuid-789"
  }'

# Response:
{
  "id": "swap-uuid-101",
  "requester_id": "user-uuid-123",
  "offered_event_id": "event-uuid-456",
  "requested_event_id": "event-uuid-789",
  "status": "PENDING",
  "created_at": "2024-11-05T15:35:00"
}
```

### 6. Check Incoming Requests (as Bob)

```bash
# Bob checks his incoming swap requests
curl -X GET "http://localhost:8000/swaps/incoming-requests" \
  -H "Authorization: Bearer $BOB_TOKEN"

# Response:
[
  {
    "id": "swap-uuid-101",
    "status": "PENDING",
    "requester": {
      "name": "Alice Johnson",
      "email": "alice@example.com"
    },
    "offered_event": {
      "title": "Project Planning Meeting",
      "start_time": "2024-12-15T14:00:00",
      "end_time": "2024-12-15T15:30:00"
    },
    "requested_event": {
      "title": "Team Standup",
      "start_time": "2024-12-15T09:00:00",
      "end_time": "2024-12-15T09:30:00"
    }
  }
]
```

### 7. Respond to Swap Request

```bash
# Bob accepts the swap request
curl -X POST "http://localhost:8000/swaps/swap-uuid-101/respond" \
  -H "Authorization: Bearer $BOB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "ACCEPTED"
  }'

# Response:
{
  "id": "swap-uuid-101",
  "status": "ACCEPTED",
  "message": "Swap completed successfully"
}
```

## 📋 Common Workflows

### Workflow 1: Daily Meeting Management

```bash
# 1. List today's events
curl -X GET "http://localhost:8000/events/" \
  -H "Authorization: Bearer $TOKEN"

# 2. Create a new meeting
curl -X POST "http://localhost:8000/events/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Client Call",
    "start_time": "2024-12-15T16:00:00",
    "end_time": "2024-12-15T17:00:00"
  }'

# 3. Make it swappable if needed
curl -X PUT "http://localhost:8000/events/{event_id}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "SWAPPABLE"}'
```

### Workflow 2: Swap Request Management

```bash
# 1. Check outgoing requests (requests you made)
curl -X GET "http://localhost:8000/swaps/outgoing-requests" \
  -H "Authorization: Bearer $TOKEN"

# 2. Check incoming requests (requests for your events)
curl -X GET "http://localhost:8000/swaps/incoming-requests" \
  -H "Authorization: Bearer $TOKEN"

# 3. Respond to a request
curl -X POST "http://localhost:8000/swaps/{swap_id}/respond" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"response": "ACCEPTED"}'  # or "DECLINED"
```

### Workflow 3: Event Lifecycle

```bash
# 1. Create event
POST /events/
{
  "title": "Weekly Review",
  "start_time": "2024-12-20T15:00:00",
  "end_time": "2024-12-20T16:00:00"
}

# 2. Update event details
PUT /events/{event_id}
{
  "description": "Added agenda items",
  "status": "SWAPPABLE"
}

# 3. Get event details
GET /events/{event_id}

# 4. Delete event (if needed)
DELETE /events/{event_id}
```

## 🔒 Authentication Examples

### Login with Existing Account

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "securepassword123"
  }'
```

### Get Current User Info

```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

## ❌ Error Handling Examples

### Invalid Authentication

```bash
# Request without token
curl -X GET "http://localhost:8000/events/"

# Response: 401 Unauthorized
{
  "detail": "Not authenticated"
}
```

### Validation Errors

```bash
# Invalid event data
curl -X POST "http://localhost:8000/events/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "",
    "start_time": "invalid-date"
  }'

# Response: 422 Validation Error
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    },
    {
      "loc": ["body", "start_time"],
      "msg": "invalid datetime format",
      "type": "value_error.datetime"
    }
  ]
}
```

### Business Logic Errors

```bash
# Try to swap with own event
curl -X POST "http://localhost:8000/swaps/request" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "offered_event_id": "event-uuid-456",
    "requested_event_id": "event-uuid-456"
  }'

# Response: 400 Bad Request
{
  "detail": "Cannot swap with your own event"
}
```

## 📊 Response Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | GET requests, successful updates |
| 201 | Created | POST requests creating new resources |
| 204 | No Content | DELETE requests |
| 400 | Bad Request | Business logic violations |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 422 | Validation Error | Invalid request data format |
| 500 | Server Error | Internal server issues |

## 🔧 Testing with Different Tools

### Using HTTPie

```bash
# Install HTTPie: pip install httpie

# Register user
http POST localhost:8000/auth/register \
  email=alice@example.com \
  name="Alice Johnson" \
  password=securepassword123

# Login and save token
http POST localhost:8000/auth/login \
  email=alice@example.com \
  password=securepassword123

# Use token for authenticated requests
http GET localhost:8000/events/ \
  Authorization:"Bearer $TOKEN"
```

### Using JavaScript/Fetch

```javascript
// Register user
const registerResponse = await fetch('http://localhost:8000/auth/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'alice@example.com',
    name: 'Alice Johnson',
    password: 'securepassword123'
  })
});

const { access_token } = await registerResponse.json();

// Create event
const eventResponse = await fetch('http://localhost:8000/events/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${access_token}`
  },
  body: JSON.stringify({
    title: 'Team Meeting',
    start_time: '2024-12-15T10:00:00',
    end_time: '2024-12-15T11:00:00'
  })
});
```

### Using Python Requests

```python
import requests

# Register user
response = requests.post('http://localhost:8000/auth/register', json={
    'email': 'alice@example.com',
    'name': 'Alice Johnson',
    'password': 'securepassword123'
})

token = response.json()['access_token']

# Create event
headers = {'Authorization': f'Bearer {token}'}
event_response = requests.post('http://localhost:8000/events/', 
    headers=headers,
    json={
        'title': 'Team Meeting',
        'start_time': '2024-12-15T10:00:00',
        'end_time': '2024-12-15T11:00:00'
    }
)
```

## 🎯 Best Practices

### 1. Token Management
- Store tokens securely (not in localStorage for production)
- Handle token expiration gracefully
- Refresh tokens before they expire

### 2. Error Handling
- Always check response status codes
- Handle network errors appropriately
- Provide user-friendly error messages

### 3. Data Validation
- Validate data on the client side before sending
- Handle validation errors from the server
- Use proper date/time formats (ISO 8601)

### 4. Performance
- Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- Implement proper caching strategies
- Paginate large result sets

### 5. Security
- Always use HTTPS in production
- Don't log sensitive information
- Validate all inputs
- Use proper CORS settings

---

For more detailed API documentation, visit: http://localhost:8000/docs
