@echo off
setlocal
echo [Joy AI Setup] Initializing Local Environment...

REM 1. Set paths
set "PYTHON_DIR=C:\IT\python310"
set "PYTHON_EXE=%PYTHON_DIR%\python.exe"
set "VENV_DIR=.venv"

REM 2. Check Python exists
if not exist "%PYTHON_EXE%" (
    echo [ERROR] Python not found at %PYTHON_EXE%
    echo Please install Python 3.10 from https://www.python.org/
    pause
    exit /b 1
)

REM 3. Create venv if not exists
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo [Joy AI Setup] Creating virtual environment...
    "%PYTHON_EXE%" -m venv %VENV_DIR%
)

REM 4. Install dependencies
echo [Joy AI Setup] Installing dependencies...
%VENV_DIR%\Scripts\pip.exe install -r requirements.txt

if %errorlevel% neq 0 (
    echo [ERROR] Installation failed.
    pause
    exit /b 1
)

echo.
echo [Joy AI Setup] Launching Joy...

REM 5. Run the app using venv python
start "" "%VENV_DIR%\Scripts\pythonw.exe" main.py

REM Close the window automatically after 3 seconds
timeout /t 3 >nul
