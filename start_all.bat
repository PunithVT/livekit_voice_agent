@echo off
REM Start all services for Voice Agent

echo =========================================
echo Starting Voice Agent Services
echo =========================================
echo.

REM Check if .env exists
if not exist "backend\.env" (
    echo ERROR: .env file not found!
    echo Please run setup_voice_agent.bat first.
    pause
    exit /b 1
)

echo Starting services in separate windows...
echo.

REM Start Django server
echo [1/3] Starting Django server...
start "Django Server" cmd /k "cd backend && python manage.py runserver"
timeout /t 3 /nobreak >nul

REM Start LiveKit agent
echo [2/3] Starting LiveKit agent...
start "LiveKit Agent" cmd /k "cd backend\voice_agent && python agent.py dev"
timeout /t 3 /nobreak >nul

REM Start frontend
echo [3/3] Starting frontend...
start "Frontend Dev Server" cmd /k "cd frontend && npm run dev"

echo.
echo =========================================
echo All services started!
echo =========================================
echo.
echo Three windows should have opened:
echo   1. Django Server (http://localhost:8000)
echo   2. LiveKit Agent
echo   3. Frontend (http://localhost:5173)
echo.
echo Open http://localhost:5173 in your browser to use the application.
echo Close this window to keep services running.
echo.
pause
