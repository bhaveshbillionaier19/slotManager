# SlotSwapper Docker Setup Guide

This guide provides comprehensive instructions for setting up SlotSwapper using Docker for both development and production environments.

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Git
- 4GB+ RAM available for containers

## 🚀 Quick Start (Development)

1. **Clone and navigate to the project:**
   ```bash
   git clone <repository-url>
   cd Slotmanager
   ```

2. **Copy environment configuration:**
   ```bash
   cp .env.example .env
   ```

3. **Start development environment:**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Database: localhost:5432
   - Redis: localhost:6379

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│  (PostgreSQL)   │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │     Redis       │
                    │   (Caching)     │
                    │   Port: 6379    │
                    └─────────────────┘
```

## 🛠️ Development Setup

### Environment Configuration

Edit `.env` file with your development settings:

```env
# Database
DB_NAME=slotswapper_dev
DB_USER=dev_user
DB_PASSWORD=dev_password

# Backend
SECRET_KEY=dev-secret-key
ENVIRONMENT=development

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

### Available Commands

```bash
# Start all services
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# View logs
docker-compose logs -f [service-name]

# Stop all services
docker-compose down

# Rebuild services
docker-compose build

# Run database migrations
docker-compose exec backend alembic upgrade head

# Access database shell
docker-compose exec database psql -U dev_user -d slotswapper_dev

# Access backend shell
docker-compose exec backend bash

# Access frontend shell
docker-compose exec frontend sh
```

## 🚀 Production Deployment

### 1. Environment Setup

```bash
# Copy production environment template
cp .env.production .env

# Edit with your production values
nano .env
```

### 2. SSL Configuration

Place your SSL certificates in `nginx/ssl/`:
- `fullchain.pem` - Full certificate chain
- `privkey.pem` - Private key

### 3. Deploy with Production Profile

```bash
# Start production services
docker-compose --profile production up -d

# Or use production-specific compose file
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 📊 Service Details

### Frontend (React + Nginx)
- **Image**: Multi-stage build with Node.js and Nginx
- **Port**: 3000
- **Features**: 
  - Optimized production build
  - Gzip compression
  - Client-side routing support
  - Static asset caching

### Backend (FastAPI)
- **Image**: Python 3.11 slim
- **Port**: 8000
- **Features**:
  - Auto-reload in development
  - Health checks
  - Security optimizations
  - Non-root user

### Database (PostgreSQL)
- **Image**: PostgreSQL 15 Alpine
- **Port**: 5432
- **Features**:
  - Persistent data volumes
  - Performance optimizations
  - Automatic initialization
  - Health checks

### Redis (Caching)
- **Image**: Redis 7 Alpine
- **Port**: 6379
- **Features**:
  - Password protection
  - Persistent storage
  - Memory optimization

## 🔧 Maintenance Commands

### Database Operations

```bash
# Create database backup
docker-compose exec database pg_dump -U postgres slotswapper > backup.sql

# Restore database backup
docker-compose exec -T database psql -U postgres slotswapper < backup.sql

# Reset database
docker-compose down -v
docker-compose up -d database
```

### Log Management

```bash
# View all logs
docker-compose logs

# Follow specific service logs
docker-compose logs -f backend

# Clear logs
docker system prune -f
```

### Performance Monitoring

```bash
# Check resource usage
docker stats

# Check service health
docker-compose ps

# Inspect service configuration
docker-compose config
```

## 🔒 Security Considerations

### Production Security Checklist

- [ ] Change all default passwords
- [ ] Use strong SECRET_KEY
- [ ] Configure proper CORS origins
- [ ] Set up SSL certificates
- [ ] Enable firewall rules
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity

### Environment Variables Security

Never commit `.env` files to version control. Use:
- `.env.example` for templates
- Environment-specific files (`.env.production`, `.env.staging`)
- Secret management systems for production

## 🐛 Troubleshooting

### Common Issues

1. **Port conflicts:**
   ```bash
   # Check what's using the port
   lsof -i :3000
   
   # Change ports in .env file
   FRONTEND_PORT=3001
   ```

2. **Database connection issues:**
   ```bash
   # Check database logs
   docker-compose logs database
   
   # Verify database is ready
   docker-compose exec database pg_isready
   ```

3. **Frontend build failures:**
   ```bash
   # Clear node_modules and rebuild
   docker-compose down
   docker-compose build --no-cache frontend
   ```

4. **Permission issues:**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

### Health Check URLs

- Frontend: http://localhost:3000/health
- Backend: http://localhost:8000/health
- Database: Use `pg_isready` command

## 📈 Scaling and Performance

### Horizontal Scaling

```yaml
# Scale specific services
docker-compose up -d --scale backend=3 --scale frontend=2
```

### Resource Limits

Add to docker-compose.yml:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to production
        run: |
          docker-compose --profile production up -d --build
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [React Production Build](https://create-react-app.dev/docs/production-build/)

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review service logs
3. Create an issue in the project repository
4. Contact the development team

---

**Last Updated:** November 2024  
**Version:** 1.0.0
