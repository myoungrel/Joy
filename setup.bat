@echo off
setlocal
echo [Joy AI Setup] Initializing Local Environment...

REM 1. Set paths
set "PYTHON_DIR=C:\IT\python310"
set "PYTHON_EXE=%PYTHON_DIR%\python.exe"
set "LOCAL_LIB=joy_libs"

REM 2. Always check/update dependencies
REM (Pip will skip if already satisfied, so this is safe and fast)

REM 3. Create local lib folder
if not exist "%LOCAL_LIB%" mkdir "%LOCAL_LIB%"

echo [Joy AI Setup] Installing dependencies locally to '%LOCAL_LIB%'...
echo (This avoids touching your system files)

 REM Install pip script if missing
if not exist get-pip.py (
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
)

REM Install main dependencies (removed pyautogui to fix build errors)
REM Pillow has built-in ImageGrab which works fine on Windows
"%PYTHON_EXE%" get-pip.py --target "%LOCAL_LIB%" PyQt6 requests pillow

if %errorlevel% neq 0 (
    echo [ERROR] Installation failed.
    pause
    exit /b 1
)

goto :LAUNCH

:ERROR
    echo [ERROR] Installation failed.
    pause
    exit /b 1
)

:LAUNCH
echo.
echo [Joy AI Setup] Launching Joy...

REM 4. Run the app with PYTHONPATH set to local lib
set "PYTHONPATH=%CD%\%LOCAL_LIB%"
set "PYTHONW_EXE=%PYTHON_DIR%\pythonw.exe"
if exist "%PYTHONW_EXE%" (
    start "" "%PYTHONW_EXE%" main.py
) else (
    start "" "%PYTHON_EXE%" main.py
)

REM Close the window automatically after 3 seconds
timeout /t 3 >nul
