#!/bin/bash

echo "🚀 Starting MongoDB..."

# Create directories if they don't exist
mkdir -p ~/mongodb/data ~/mongodb/logs

# Check if MongoDB is already running
if ss -tlnp | grep -q :27017; then
    echo "✅ MongoDB is already running on port 27017"
    exit 0
fi

# Start MongoDB
echo "Starting MongoDB server..."
mongod --dbpath ~/mongodb/data --logpath ~/mongodb/logs/mongod.log --port 27017 --fork

# Wait a moment and check if it started successfully
sleep 3

if ss -tlnp | grep -q :27017; then
    echo "✅ MongoDB started successfully!"
    echo "📍 MongoDB is now running on mongodb://localhost:27017"
    echo "🗄️  Data directory: ~/mongodb/data"
    echo "📝 Log file: ~/mongodb/logs/mongod.log"
else
    echo "❌ Failed to start MongoDB"
    echo "📝 Check the log file for errors: ~/mongodb/logs/mongod.log"
    exit 1
fi 