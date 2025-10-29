#!/bin/bash

# Voice Agent Setup Script for Autonomous Learning Platform

echo "========================================="
echo "Voice Agent Setup"
echo "========================================="
echo ""

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp backend/voice_agent/.env.example backend/.env
    echo "✅ Created .env file. Please edit it with your API keys."
    echo ""
    echo "Required API keys:"
    echo "  - LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET (from livekit.io)"
    echo "  - OPENAI_API_KEY (from platform.openai.com)"
    echo "  - DEEPGRAM_API_KEY (from deepgram.com)"
    echo ""
    read -p "Press Enter after you've updated the .env file..."
fi

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install backend dependencies"
    exit 1
fi
echo "✅ Backend dependencies installed"
echo ""

# Run migrations
echo "🔄 Running database migrations..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "❌ Failed to run migrations"
    exit 1
fi
echo "✅ Migrations completed"
echo ""

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd ../frontend
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install frontend dependencies"
    exit 1
fi
echo "✅ Frontend dependencies installed"
echo ""

echo "========================================="
echo "✅ Setup Complete!"
echo "========================================="
echo ""
echo "To start the application:"
echo ""
echo "1. Start Django server:"
echo "   cd backend && python manage.py runserver"
echo ""
echo "2. Start LiveKit agent (in a new terminal):"
echo "   cd backend/voice_agent && python agent.py dev"
echo ""
echo "3. Start frontend (in a new terminal):"
echo "   cd frontend && npm run dev"
echo ""
echo "Then open http://localhost:5173 in your browser"
echo ""
