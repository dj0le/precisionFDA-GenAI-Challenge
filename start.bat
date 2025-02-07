@echo off
REM Kill existing processes (Windows version)
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do taskkill /f /pid %%a 2>nul
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5173" ^| find "LISTENING"') do taskkill /f /pid %%a 2>nul

REM Start the API server
echo Starting FastAPI backend...
cd api && start /B uvicorn main:app --reload

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Start the frontend
echo Starting Svelte frontend...
cd ../frontend && start /B npm run dev -- --no-clear --open

REM Keep window open
pause
