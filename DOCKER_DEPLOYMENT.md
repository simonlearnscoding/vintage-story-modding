# Vintage Story Log Dashboard - Docker Deployment

This document explains how to deploy the Vintage Story Log Dashboard using Docker.

## Architecture

The application consists of:
- **Frontend**: React dashboard served by Nginx
- **Backend**: FastAPI Python application
- **Database**: PostgreSQL
- **Vintage Story Mod**: C# mod that sends player events to the API

## Quick Start

1. **Clone and navigate to the project:**
   ```bash
   cd vs-modding
   ```

2. **Run the deployment script:**
   ```bash
   ./deploy.sh
   ```

3. **Access the application:**
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API Health: http://localhost:8000/health

## Manual Deployment

If you prefer to deploy manually:

1. **Build and start all services:**
   ```bash
   docker-compose down --remove-orphans
   docker-compose build --no-cache
   docker-compose up -d
   ```

2. **Check service status:**
   ```bash
   docker-compose ps
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f
   ```

## Services

### Frontend (Port 80)
- Built with React and TypeScript
- Served by Nginx
- Auto-refreshes every 30 seconds

### Backend (Port 8000)
- FastAPI Python application
- Connects to PostgreSQL
- Provides REST API for player logs

### Database
- PostgreSQL 15
- Persistent data storage
- Health checks enabled

### Vintage Story Server (Optional)
- Only starts with `--profile game-server`
- Runs on port 42420
- Includes the VSAPI mod

## Environment Variables

Create a `.env.production` file based on `.env.production.example`:

```bash
# Database
DATABASE_URL=postgresql://vsuser:vspassword@postgres:5432/vintagestory

# Backend
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here
```

## Vintage Story Mod Setup

1. **Build the mod:**
   ```bash
   cd vintage-server
   docker build -t vsapi-mod .
   ```

2. **Install mod in Vintage Story:**
   - Copy the built mod files to your Vintage Story server's `Mods` directory
   - The mod will automatically send player join/leave events to the API

## Development vs Production

### Development
```bash
docker-compose -f docker-compose.dev.yml up
```

### Production
```bash
docker-compose up
```

## Monitoring

### Health Checks
All services include health checks:
- Frontend: HTTP check on port 80
- Backend: HTTP check on `/health` endpoint
- Database: PostgreSQL connection check

### Logs
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f frontend
docker-compose logs -f backend
docker-compose logs -f postgres
```

### Scaling
```bash
# Scale backend (if needed)
docker-compose up -d --scale backend=2
```

## Troubleshooting

### Common Issues

1. **Port conflicts:**
   - Ensure ports 80, 8000, 5432 are available
   - Modify ports in `docker-compose.yml` if needed

2. **Database connection:**
   - Check PostgreSQL health: `docker-compose logs postgres`
   - Verify database credentials in environment

3. **Mod not connecting:**
   - Ensure backend is running before starting Vintage Story
   - Check network connectivity between containers

### Reset Everything
```bash
docker-compose down -v
docker system prune -f
./deploy.sh
```

## Backup and Restore

### Backup Database
```bash
docker-compose exec postgres pg_dump -U vsuser vintagestory > backup.sql
```

### Restore Database
```bash
docker-compose exec -T postgres psql -U vsuser vintagestory < backup.sql
```

## Security Considerations

- Change default passwords in production
- Use HTTPS/SSL certificates
- Restrict database access
- Monitor logs for suspicious activity
- Regular security updates

## Performance Optimization

- Enable Redis for caching (future enhancement)
- Use CDN for static assets
- Database connection pooling
- Monitor resource usage