@echo off
echo Starting Gmail Issue Automation Dashboard...
echo.

REM Start backend
echo [1/2] Starting backend server on port 5000...
start "Backend" cmd /k "cd backend && npm install && npm run dev"

REM Wait a moment then start frontend
timeout /t 3 /nobreak >nul

REM Start frontend
echo [2/2] Starting frontend on port 5173...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Dashboard running at: http://localhost:5173
echo Backend API at:       http://localhost:5000/api/health
echo.
pause
