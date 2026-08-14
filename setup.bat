@echo off
cd /d "%~dp0"

echo =====================================
echo PhotoMap Creator V8 Setup
echo =====================================
echo.

python --version >nul 2>&1

if errorlevel 1 (
    echo Python is not installed.
    echo.
    echo Please install Python 3.9 or later.
    echo.
    pause
    exit /b 1
)

echo Python was found.
python --version

echo.
echo Installing required libraries...
echo.

python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Setup failed.
    echo.
    pause
    exit /b 1
)

echo.
echo =====================================
echo Setup completed successfully.
echo =====================================
echo.

pause