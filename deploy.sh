#!/bin/bash

# Vintage Story Log Dashboard - Deployment Script

set -e

echo "🚀 Starting Vintage Story Log Dashboard deployment..."

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p vintage-server/mods

# Build and start services
echo "🔨 Building and starting services..."
docker-compose down --remove-orphans
docker-compose build --no-cache
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 30

# Check service status
echo "🔍 Checking service status..."
docker-compose ps

# Show logs
echo "📋 Showing recent logs..."
docker-compose logs --tail=50

echo "✅ Deployment complete!"
echo ""
echo "🌐 Frontend: http://localhost"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 API Health: http://localhost:8000/health"
echo "📊 Player Logs: http://localhost:8000/players/logs"
echo ""
echo "To view logs: docker-compose logs -f [service_name]"
echo "To stop: docker-compose down"
echo "To restart: docker-compose restart [service_name]"