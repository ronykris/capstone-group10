#!/bin/bash

# Exit on error
set -e

# Get the current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${DIR}/.."

# Default values
IMAGE_NAME="food-segmentation-api"
CONTAINER_NAME="food-segmentation-dev"
PORT=8002

# Check for environment file
ENV_FILE=".env"
if [ ! -f "$ENV_FILE" ]; then
    echo "Warning: .env file not found. Creating from example..."
    cp .env.example .env
fi

# Load environment variables
set -a
source "$ENV_FILE"
set +a

# Check if container is already running
if [ "$(docker ps -q -f name=${CONTAINER_NAME})" ]; then
    echo "Stopping existing container..."
    docker stop ${CONTAINER_NAME}
fi

# Remove existing container
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    docker rm ${CONTAINER_NAME}
fi

echo "Starting development container..."

# Run the container
docker run \
    --name ${CONTAINER_NAME} \
    --env-file .env \
    -e APP_ENV=development \
    -p ${PORT}:${PORT} \
    -v "$(pwd)/app:/app/app" \
    -v "$(pwd)/config:/app/config" \
    -d \
    ${IMAGE_NAME}:latest

echo "Development container started!"
echo "API is available at http://localhost:${PORT}"
echo "Logs will be available using: docker logs -f ${CONTAINER_NAME}"
