# SlotSwapper 🔄

A modern, full-stack web application for intelligent meeting slot swapping and scheduling management. Built with FastAPI, React, and PostgreSQL.

![SlotSwapper Banner](https://via.placeholder.com/800x200/4F46E5/FFFFFF?text=SlotSwapper+-+Smart+Meeting+Management)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Design Choices](#design-choices)
- [Quick Start](#quick-start)
- [Local Setup](#local-setup)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [Assumptions & Challenges](#assumptions--challenges)
- [Contributing](#contributing)


## 🎯 Overview

SlotSwapper is an intelligent meeting management system that allows users to create, manage, and swap meeting slots with other users. The application addresses the common problem of scheduling conflicts by enabling users to propose and negotiate meeting time exchanges.

### Key Capabilities

- **Smart Scheduling**: Create and manage meeting slots with conflict detection
- **Intelligent Swapping**: Propose meeting swaps with other users
- **Real-time Notifications**: Get notified when swap requests arrive
- **Secure Authentication**: JWT-based authentication with bcrypt password hashing
- **Responsive Design**: Modern UI that works on desktop and mobile devices
- **Performance Optimized**: Built for scalability with comprehensive testing

## ✨ Features

### Core Features
- 🔐 **User Authentication** - Secure registration and login
- 📅 **Event Management** - Create, update, and delete meeting slots
- 🔄 **Swap Requests** - Propose and respond to meeting swaps
- 🔔 **Real-time Notifications** - Live notification system with red dot indicators
- 📱 **Responsive Design** - Mobile-first, professional UI
- 🎨 **Modern Interface** - Clean, intuitive user experience

### Advanced Features
- ⚡ **Performance Monitoring** - Comprehensive testing and benchmarks
- 🐳 **Docker Support** - Full containerization for easy deployment
- 🔒 **Security First** - Input validation, SQL injection prevention, XSS protection
- 📊 **Analytics Ready** - Structured logging and monitoring hooks
- 🚀 **Production Ready** - Load balancing, SSL, and scalability features

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and Object-Relational Mapping
- **PostgreSQL** - Advanced open-source relational database
- **JWT** - JSON Web Tokens for secure authentication
- **bcrypt** - Password hashing for security
- **Pydantic** - Data validation using Python type annotations

### Frontend
- **React 18** - Modern JavaScript library for building user interfaces
- **TypeScript** - Type-safe JavaScript development
- **Vite** - Fast build tool and development server
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Production-ready motion library
- **Lucide React** - Beautiful & consistent icon library
- **Axios** - Promise-based HTTP client

### DevOps & Tools
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container Docker applications
- **Nginx** - High-performance web server and reverse proxy
- **pytest** - Comprehensive testing framework
- **GitHub Actions** - CI/CD automation

## 🎨 Design Choices

### Architecture Decisions

1. **Microservices-Ready Architecture**
   - Separated frontend and backend for independent scaling
   - RESTful API design for easy integration
   - Stateless authentication with JWT tokens

2. **Database Design**
   - Normalized schema with proper relationships
   - Enum types for status fields to ensure data integrity
   - Timestamps for audit trails and conflict resolution

3. **Security-First Approach**
   - Password hashing with bcrypt and salt
   - JWT tokens with expiration
   - Input validation at multiple layers
   - CORS configuration for cross-origin requests

4. **Performance Optimization**
   - Database indexing on frequently queried fields
   - Connection pooling for database efficiency
   - Lazy loading and pagination for large datasets
   - Caching strategies with Redis support

5. **User Experience Focus**
   - Real-time notifications without page refresh
   - Optimistic UI updates for better perceived performance
   - Mobile-first responsive design
   - Accessibility features (ARIA labels, keyboard navigation)

### Technology Rationale

- **FastAPI**: Chosen for its automatic API documentation, type safety, and high performance
- **React + TypeScript**: Provides type safety and excellent developer experience
- **Tailwind CSS**: Enables rapid UI development with consistent design
- **PostgreSQL**: Robust ACID compliance and advanced features for complex queries
- **Docker**: Ensures consistent environments across development, testing, and production

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### One-Command Setup
```bash
git clone <repository-url>
cd Slotmanager
make setup && make dev
```

Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 💻 Local Setup

### Method 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Slotmanager
   ```

2. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

3. **Start with Docker Compose**
   ```bash
   # Development environment
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
   
   # Or using Makefile
   make dev
   ```

4. **Verify Installation**
   ```bash
   # Check service health
   make health
   
   # View logs
   make logs
   ```

### Method 2: Manual Setup

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd slota_swapper
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database setup**
   ```bash
   # Install PostgreSQL and create database
   createdb slotswapper
   
   # Set environment variables
   export DATABASE_URL="postgresql://username:password@localhost/slotswapper"
   export SECRET_KEY="your-secret-key"
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the backend server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Environment configuration**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with backend URL
   echo "REACT_APP_API_URL=http://localhost:8000" > .env.local
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```

### Verification

After setup, verify the installation:

1. **Backend Health Check**
   ```bash
   curl http://localhost:8000/health
   # Should return: {"status": "healthy", "timestamp": "..."}
   ```

2. **Frontend Access**
   - Open http://localhost:3000 in your browser
   - You should see the SlotSwapper login page

3. **API Documentation**
   - Visit http://localhost:8000/docs for interactive API documentation

## 📚 API Documentation

### Base URL
- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com/api`

### Authentication
All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

### API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| **Authentication** |
| POST | `/auth/register` | Register new user | ❌ |
| POST | `/auth/login` | User login | ❌ |
| GET | `/auth/me` | Get current user info | ✅ |
| **Events** |
| GET | `/events/` | List user's events | ✅ |
| POST | `/events/` | Create new event | ✅ |
| GET | `/events/{id}` | Get specific event | ✅ |
| PUT | `/events/{id}` | Update event | ✅ |
| DELETE | `/events/{id}` | Delete event | ✅ |
| **Swap Requests** |
| POST | `/swaps/request` | Create swap request | ✅ |
| GET | `/swaps/incoming-requests` | List incoming requests | ✅ |
| GET | `/swaps/outgoing-requests` | List outgoing requests | ✅ |
| POST | `/swaps/{id}/respond` | Respond to swap request | ✅ |
| GET | `/swaps/swappable-events` | List swappable events | ✅ |
| **System** |
| GET | `/health` | Health check | ❌ |

### Request/Response Examples

#### User Registration
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": "user-uuid",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

#### Create Event
```bash
curl -X POST "http://localhost:8000/events/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Meeting",
    "description": "Weekly team sync",
    "start_time": "2024-12-01T10:00:00",
    "end_time": "2024-12-01T11:00:00"
  }'
```

#### Create Swap Request
```bash
curl -X POST "http://localhost:8000/swaps/request" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "offered_event_id": "event-uuid-1",
    "requested_event_id": "event-uuid-2"
  }'
```

#### Respond to Swap Request
```bash
curl -X POST "http://localhost:8000/swaps/{swap_id}/respond" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "response": "ACCEPTED"
  }'
```

### Postman Collection
A complete Postman collection is available at: [SlotSwapper API Collection](./docs/SlotSwapper.postman_collection.json)

### API Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests with coverage
python run_tests.py all

# Run specific test categories
python run_tests.py unit          # Unit tests only
python run_tests.py integration   # Integration tests only
python run_tests.py auth          # Authentication tests
python run_tests.py swaps         # Swap logic tests
python run_tests.py performance   # Performance tests

# Generate coverage report
python run_tests.py coverage
```

### Test Coverage

The project maintains high test coverage:
- **Overall Coverage**: 85%+
- **Critical Components**: 90%+
  - Authentication logic
  - Swap request handling
  - API endpoints
- **Performance Tests**: Load testing with 1000+ concurrent users

### Test Categories

- **Unit Tests**: Individual function testing
- **Integration Tests**: API endpoint testing
- **Performance Tests**: Load and stress testing
- **Security Tests**: Authentication and authorization

## 🐳 Docker Deployment

### Development Deployment
```bash
# Start development environment
make dev

# View logs
make logs

# Stop services
make down
```

### Production Deployment
```bash
# Setup production environment
make setup-prod

# Deploy with SSL and reverse proxy
make prod

# Monitor services
make stats
```

### Docker Services

| Service | Description | Port |
|---------|-------------|------|
| **frontend** | React application | 3000 |
| **backend** | FastAPI server | 8000 |
| **database** | PostgreSQL | 5432 |
| **redis** | Caching layer | 6379 |
| **nginx** | Reverse proxy | 80, 443 |

### Environment Variables

Key environment variables for configuration:

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/slotswapper
DB_NAME=slotswapper
DB_USER=postgres
DB_PASSWORD=secure_password

# Authentication
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend
REACT_APP_API_URL=http://localhost:8000

# Production
CORS_ORIGINS=https://yourdomain.com
ENVIRONMENT=production
```

## 🤔 Assumptions & Challenges

### Assumptions Made

1. **User Behavior**
   - Users will primarily swap meetings within the same day or week
   - Meeting durations are typically 30 minutes to 2 hours
   - Users prefer visual feedback for swap request status

2. **Business Logic**
   - Only the event owner can respond to swap requests
   - Events can only be swapped if both are marked as "SWAPPABLE"
   - Past events cannot be swapped
   - Users cannot swap with their own events

3. **Technical Assumptions**
   - Modern browsers with JavaScript enabled
   - Stable internet connection for real-time features
   - PostgreSQL for production database
   - Docker availability for deployment



### Challenges Faced & Solutions

#### 1. **Real-time Notification System**
**Challenge**: Implementing real-time notifications without WebSockets
**Solution**: 
- Implemented polling-based notification system
- Used React hooks for efficient state management
- Added visual indicators (red dots) with smooth animations

#### 2. **Complex Swap Logic**
**Challenge**: Ensuring data integrity during swap operations
**Solution**:
- Implemented comprehensive validation rules
- Added database transactions for atomic operations
- Created extensive test coverage (90%+) for swap logic

#### 3. **Authentication Security**
**Challenge**: Balancing security with user experience
**Solution**:
- JWT tokens with reasonable expiration times
- Secure password hashing with bcrypt
- Proper CORS configuration
- Input validation at multiple layers

#### 4. **Database Performance**
**Challenge**: Efficient querying with complex relationships
**Solution**:
- Proper database indexing strategy
- Optimized queries with SQLAlchemy
- Connection pooling for scalability
- Pagination for large datasets

#### 5. **Frontend State Management**
**Challenge**: Managing complex application state
**Solution**:
- React Context for authentication state
- Custom hooks for data fetching
- Optimistic UI updates for better UX
- Proper error handling and loading states

#### 6. **Cross-Origin Resource Sharing (CORS)**
**Challenge**: Frontend-backend communication in development
**Solution**:
- Proper CORS configuration in FastAPI
- Environment-specific settings
- Proxy configuration for development

#### 7. **Testing Complex Business Logic**
**Challenge**: Testing swap request workflows thoroughly
**Solution**:
- Factory pattern for test data generation
- Comprehensive unit and integration tests
- Performance testing with realistic data volumes
- Mock data for edge case testing

#### 8. **Docker Configuration**
**Challenge**: Creating efficient, secure containers
**Solution**:
- Multi-stage builds for smaller images
- Non-root users for security
- Health checks for reliability
- Environment-specific configurations

### Performance Considerations

1. **Database Optimization**
   - Indexed frequently queried columns
   - Optimized join queries for swap requests
   - Connection pooling for concurrent users

2. **Frontend Performance**
   - Code splitting for faster initial loads
   - Optimized bundle sizes with Vite
   - Efficient re-rendering with React hooks

3. **API Performance**
   - Response time targets: <500ms for most endpoints
   - Pagination for large data sets
   - Caching strategies for frequently accessed data

### Security Measures

1. **Authentication & Authorization**
   - JWT tokens with secure secret keys
   - Password hashing with bcrypt
   - Proper session management

2. **Input Validation**
   - Pydantic models for request validation
   - SQL injection prevention with SQLAlchemy
   - XSS protection with proper escaping

3. **Infrastructure Security**
   - HTTPS enforcement in production
   - Security headers (HSTS, CSP, etc.)
   - Rate limiting for API endpoints

## 🤝 Contributing

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Run tests**
   ```bash
   python run_tests.py all
   ```
5. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Code Standards

- **Backend**: Follow PEP 8 Python style guide
- **Frontend**: Use TypeScript and ESLint rules
- **Testing**: Maintain 80%+ test coverage
- **Documentation**: Update README for new features

### Commit Message Format
```
type(scope): description

Examples:
feat(auth): add password reset functionality
fix(swaps): resolve duplicate request issue
docs(api): update endpoint documentation
test(auth): add unit tests for login flow
```



---

