@echo off
echo Starting Template Management System...
echo.

echo [1/2] Starting Backend Server (Port 8001)...
start "Backend Server" cmd /k "cd backend && call venv\Scripts\activate && python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload"

timeout /t 3 /nobreak > nul

echo [2/2] Starting Frontend Server (Port 5173)...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo ✓ All servers started!
echo.
echo Backend:  http://localhost:8001
echo Frontend: http://localhost:5173
echo.
echo Press any key to close this window...
pause > nul
