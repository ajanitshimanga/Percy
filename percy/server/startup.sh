#!/bin/bash

# Function to check if Docker is running
function check_docker {
  if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker and try again."
    exit 1
  fi
}

# Check if Docker is running
check_docker

# Set environment variables for PostgreSQL
export POSTGRES_USER=percy            # Change to your desired username
export POSTGRES_PASSWORD=percy-password    # Change to your desired password
export POSTGRES_DB=percy-db          # Change to your desired database name

# Start the PostgreSQL Docker container
docker run --name postgres-container -d \
  -e POSTGRES_USER=$POSTGRES_USER \
  -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
  -e POSTGRES_DB=$POSTGRES_DB \
  -p 5432:5432 \
  postgres:latest

# Wait for a few seconds to allow the database to start
sleep 3

letta server

# Wait for a few seconds to allow the database to start
sleep 3

# Provide the connection URL
echo "PostgreSQL is running."
echo "Connection URL: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}"
