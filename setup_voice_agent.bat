@echo off
REM Voice Agent Setup Script for Autonomous Learning Platform (Windows)

echo =========================================
echo Voice Agent Setup
echo =========================================
echo.

REM Check if .env file exists
if not exist "backend\.env" (
    echo WARNING: No .env file found. Creating from template...
    copy "backend\voice_agent\.env.example" "backend\.env"
    echo Created .env file. Please edit it with your API keys.
    echo.
    echo Required API keys:
    echo   - LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET (from livekit.io^)
    echo   - OPENAI_API_KEY (from platform.openai.com^)
    echo   - DEEPGRAM_API_KEY (from deepgram.com^)
    echo.
    pause
)

REM Install backend dependencies
echo Installing backend dependencies...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install backend dependencies
    pause
    exit /b 1
)
echo Backend dependencies installed
echo.

REM Run migrations
echo Running database migrations...
python manage.py migrate
if errorlevel 1 (
    echo Failed to run migrations
    pause
    exit /b 1
)
echo Migrations completed
echo.

REM Install frontend dependencies
echo Installing frontend dependencies...
cd ..\frontend
call npm install
if errorlevel 1 (
    echo Failed to install frontend dependencies
    pause
    exit /b 1
)
echo Frontend dependencies installed
echo.

cd ..

echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo To start the application:
echo.
echo 1. Start Django server:
echo    cd backend ^&^& python manage.py runserver
echo.
echo 2. Start LiveKit agent (in a new terminal^):
echo    cd backend\voice_agent ^&^& python agent.py dev
echo.
echo 3. Start frontend (in a new terminal^):
echo    cd frontend ^&^& npm run dev
echo.
echo Then open http://localhost:5173 in your browser
echo.

pause
