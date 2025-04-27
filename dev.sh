#!/bin/bash

# Check if running containers need to be stopped
if docker ps | grep -q flask-app; then
    echo "Stopping existing containers..."
    docker compose down
fi

# Start development containers
echo "Starting development environment with hot-reloading..."
echo "Your code changes will be reflected immediately!"
docker compose -f docker-compose.dev.yml up 