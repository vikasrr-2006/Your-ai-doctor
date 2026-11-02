@echo off
title Your AI Doctor - Flask Launcher
echo ========================================
echo   Your AI Doctor - Flask Application
echo ========================================
echo.

cd /d "%~dp0"
if errorlevel 1 (
    echo ERROR: Failed to navigate to project directory
    echo Current directory: %cd%
    echo Batch file location: %~dp0
    pause
    exit /b 1
)

echo Working directory: %cd%
echo.

echo Checking Python installation...
where python >nul 2>&1
if errorlevel 1 (
    echo Trying 'py' launcher...
    where py >nul 2>&1
    if errorlevel 1 (
        echo.
        echo ERROR: Python is not installed or not in PATH
        echo.
        echo Solutions:
        echo   1. Install Python from https://python.org
        echo   2. During installation, check "Add Python to PATH"
        echo   3. Or add Python manually to your system PATH
        echo.
        echo Current PATH: %PATH%
        pause
        exit /b 1
    )
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)

%PYTHON_CMD% --version
if errorlevel 1 (
    echo.
    echo ERROR: Python command failed
    echo This may be the Windows Store Python stub.
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo.
echo Checking required packages...
%PYTHON_CMD% -c "import flask; print('Flask:', flask.__version__)" 2>nul
if errorlevel 1 (
    echo Flask not found. Installing dependencies...
    pip install flask numpy scikit-learn geopy
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies
        echo Try running: pip install flask numpy scikit-learn geopy
        pause
        exit /b 1
    )
)

%PYTHON_CMD% -c "import numpy" 2>nul
if errorlevel 1 (
    echo NumPy not found. Installing...
    pip install numpy
)

%PYTHON_CMD% -c "import sklearn" 2>nul
if errorlevel 1 (
    echo scikit-learn not found. Installing...
    pip install scikit-learn
)

echo.
echo All dependencies OK.
echo.
echo ========================================
echo   Starting Flask server...
echo ========================================
echo.
echo   Access the application at:
echo     http://localhost:5000
echo.
echo   Or via XAMPP at:
echo     http://localhost/new%%20help/Your%%20AI%%20Doctor/
echo.
echo   Press Ctrl+C to stop the server
echo ========================================
echo.

%PYTHON_CMD% app.py

echo.
echo ========================================
echo   Flask server stopped
echo ========================================
pause
