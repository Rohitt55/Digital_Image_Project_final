@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Run start.bat once to set up the Python environment.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" "python_code\mobile_server.py"
pause
