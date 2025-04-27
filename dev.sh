#!/bin/bash

echo "Setting up development environment..."

# Set docker-entrypoint-dev.sh to be executable
chmod +x docker-entrypoint-dev.sh

# Check if running containers need to be stopped
if docker ps | grep -q flask-app; then
    echo "Stopping existing containers..."
    docker compose down
fi

# Clean up and recreate the postgres data directory for development
echo "Creating fresh database directory..."
rm -rf ./postgres-data-dev
mkdir -p ./postgres-data-dev
chmod 777 ./postgres-data-dev

# Start development containers
echo "Starting development environment with hot-reloading..."
echo "Your code changes will be reflected immediately!"
docker compose -f docker-compose.dev.yml up --build 