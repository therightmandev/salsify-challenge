#!/usr/bin/env bash

# Exit on any error
set -e

# Build the Docker image
echo "Building Docker image..."
docker build -t line_server:latest .
echo "Docker image built successfully!"
