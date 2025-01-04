#!/bin/bash

# Exit on error
set -e

# Get the current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${DIR}/.."

# Read version from config or use latest
VERSION=${1:-latest}
IMAGE_NAME="food-segmentation-api"

echo "Building Docker image: ${IMAGE_NAME}:${VERSION}"

# Build the Docker image
docker build \
    --tag "${IMAGE_NAME}:${VERSION}" \
    --file Dockerfile \
    .

# Tag as latest if version is provided
if [ "$VERSION" != "latest" ]; then
    docker tag "${IMAGE_NAME}:${VERSION}" "${IMAGE_NAME}:latest"
fi

echo "Build completed successfully!"
