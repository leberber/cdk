#!/bin/bash

# Configuration variables
BACKEND_IMAGE="backend"
FRONTEND_IMAGE="frontend"
BACKEND_TAR="backend.tar.gz"
FRONTEND_TAR="frontend.tar.gz"
DOCKER_COMPOSE_FILE="docker-compose.yml"

echo "=== EC2 Deployment Script ==="

# Stop ALL running containers first
echo "Stopping all running containers..."
sudo docker stop $(sudo docker ps -q) 2>/dev/null || true

# Stop current containers if running
if [ -f $DOCKER_COMPOSE_FILE ]; then
  echo "Stopping docker-compose containers..."
  sudo docker-compose down
fi

# Remove any containers using our images
echo "Removing containers using our images..."
sudo docker rm $(sudo docker ps -aq --filter ancestor=$BACKEND_IMAGE:latest) 2>/dev/null || true
sudo docker rm $(sudo docker ps -aq --filter ancestor=$FRONTEND_IMAGE:latest) 2>/dev/null || true

# Remove old images to save space
echo "Cleaning up old images..."
sudo docker rmi $BACKEND_IMAGE:latest $FRONTEND_IMAGE:latest 2>/dev/null || true

# Load new images
echo "Loading new images..."
sudo docker load < $BACKEND_TAR
sudo docker load < $FRONTEND_TAR

# Verify images loaded
echo "Verifying images:"
sudo docker images | grep -E "($BACKEND_IMAGE|$FRONTEND_IMAGE)"

# Start containers
echo "Starting containers..."
sudo docker-compose up -d

# Show status
echo "Container status:"
sudo docker-compose ps

# Check logs if containers aren't running
if ! sudo docker-compose ps | grep -q "Up"; then
  echo "⚠️  Some containers may have issues. Checking logs:"
  sudo docker-compose logs --tail=20
fi

# Clean up tar files
rm -f $BACKEND_TAR $FRONTEND_TAR

echo "✅ EC2 deployment complete!"