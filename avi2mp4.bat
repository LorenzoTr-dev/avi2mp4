@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found. Run setup first.
    pause
    exit /b 1
)
".venv\Scripts\python" -m avi2mp4.cli --interactive
if %errorlevel% neq 0 (
    pause
)
