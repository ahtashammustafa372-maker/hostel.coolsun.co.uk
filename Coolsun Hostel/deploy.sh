#!/bin/bash

# Exit on any error
set -e

echo "Starting deployment process for Coolsun Hostel ERP..."

# 1. Pull the latest changes from the main branch
echo "Pulling latest changes from GitHub..."
git pull origin main

# 2. Build the frontend
echo "Building the frontend..."
cd frontend
npm install
npm run build
cd ..

# 3. Restart the backend service
echo "Restarting the backend service..."
# Note: Adjust 'backend.service' to the actual name of your systemd service, 
# or use your preferred method like PM2, Supervisor, etc.
# sudo systemctl restart hostel_backend

echo "Deployment completed successfully!"
