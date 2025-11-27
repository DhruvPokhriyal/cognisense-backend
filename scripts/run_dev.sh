#!/bin/bash
# Development startup script for CogniSense Backend

set -e

echo "🚀 Starting CogniSense Backend Development Environment"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "✓ Created .env file. Please update it with your settings."
    echo ""
fi

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed. Please install it first:"
    echo "   curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

echo "📦 Installing dependencies..."
poetry install
echo "✓ Dependencies installed"
echo ""

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "⚠️  Docker is not running. Please start Docker to run PostgreSQL."
    echo "   You can run 'docker-compose up postgres -d' manually later."
else
    echo "🐘 Starting PostgreSQL..."
    docker-compose up postgres -d
    echo "✓ PostgreSQL started"
    echo ""
    
    # Wait for PostgreSQL to be ready
    echo "⏳ Waiting for PostgreSQL to be ready..."
    sleep 3
fi

echo ""
echo "✨ Setup complete! Starting development server..."
echo ""
echo "📍 API will be available at: http://localhost:8000"
echo "📖 API Documentation at: http://localhost:8000/docs"
echo ""

# Start the development server
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
