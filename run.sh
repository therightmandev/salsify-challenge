#!/usr/bin/env bash

# This script starts the server using the Docker image built by build.sh.
# It takes a single command-line parameter: the name of the file to serve.

# Exit on any error
set -e

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <filename>"
  exit 1
fi

FILENAME="$1"

# Remove any existing container with the same name to avoid conflicts
if [ "$(docker ps -aq -f name=line_server_container)" ]; then
    echo "Removing existing container named 'line_server_container'..."
    docker rm -f line_server_container >/dev/null 2>&1 || true
fi

echo "Running Docker container..."
docker run \
    --name line_server_container \
    -p 8000:8000 \
    -v "$(pwd)":/app \
    line_server:latest \
    python3 line_server.py "$FILENAME"

echo "Container 'line_server_container' is now running, serving '$FILENAME'."
