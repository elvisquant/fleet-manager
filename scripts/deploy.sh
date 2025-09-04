#!/bin/bash
set -euo pipefail

cd /opt/fastapi-production

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Validate required variables
required_vars=(
    "DOCKERHUB_USERNAME"
    "DOCKERHUB_TOKEN"
    "DATABASE_PASSWORD"
    "DATABASE_NAME"
    "DATABASE_USERNAME"
    "SECRET_KEY"
    "GRAFANA_PASSWORD"
)

for var in "${required_vars[@]}"; do
    if [ -z "${!var:-}" ]; then
        echo "❌ Error: $var is not set"
        exit 1
    fi
done

# Login to Docker Hub
echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

# Pull latest image
echo "🚀 Pulling latest Docker image..."
docker pull $DOCKERHUB_USERNAME/fastapi-app:latest

# Deploy with Docker Compose
echo "🚀 Deploying application..."
docker-compose -f docker-compose.prod.yml up -d --force-recreate

# Wait for services to start
echo "⏳ Waiting for services to become healthy..."
sleep 30

# Run database migrations (if you have any)
# docker-compose -f docker-compose.prod.yml exec app alembic upgrade head

# Cleanup
echo "🧹 Cleaning up old resources..."
docker system prune -af --volumes --filter "until=24h"

# Health check
echo "🏥 Performing health check..."
./scripts/healthcheck.sh

echo "✅ Deployment completed successfully at $(date)"