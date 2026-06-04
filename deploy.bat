@echo off
REM Deployment script for Car Damage Detection App (Windows)

echo ========================================
echo Car Damage Detection - Deployment Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.11+
    exit /b 1
)

echo [OK] Python found
python --version

REM Create production environment
echo.
echo Setting up production environment...

REM Check if virtual environment exists
if not exist ".venv-prod" (
    echo Creating virtual environment...
    python -m venv .venv-prod
)

REM Activate virtual environment
call .venv-prod\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install production dependencies
echo Installing production dependencies...
pip install -r requirements-prod.txt

REM Create necessary directories
echo.
echo Creating necessary directories...
if not exist "static\uploads" mkdir static\uploads
if not exist "static\results" mkdir static\results
if not exist "logs" mkdir logs

REM Check if model exists
if not exist "runs\detect\train3\weights\best.pt" (
    echo.
    echo [WARNING] Model file not found at runs\detect\train3\weights\best.pt
    echo Please ensure your trained model is in the correct location.
    set /p continue="Continue anyway? (y/n): "
    if /i not "%continue%"=="y" exit /b 1
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo.
    echo Creating .env file...
    copy .env.example .env
    echo [WARNING] Please edit .env file and update SECRET_KEY before running in production!
)

REM Ask for deployment type
echo.
echo Choose deployment option:
echo 1) Test run (development mode)
echo 2) Production with Waitress
echo 3) Production with Gunicorn (requires WSL/Linux)
echo 4) Docker deployment
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Starting in development mode...
    python app.py
) else if "%choice%"=="2" (
    echo.
    echo Installing Waitress server...
    pip install waitress
    echo Starting with Waitress...
    waitress-serve --host=0.0.0.0 --port=5000 --threads=4 wsgi:app
) else if "%choice%"=="3" (
    echo.
    echo [INFO] Gunicorn is not natively supported on Windows.
    echo Please use WSL or Linux, or choose option 2 for Waitress.
    pause
    exit /b 1
) else if "%choice%"=="4" (
    echo.
    echo Building and running with Docker...
    docker --version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Docker is not installed. Please install Docker Desktop.
        exit /b 1
    )
    docker build -t car-damage-detection .
    docker run -d -p 5000:5000 -v "%cd%\static\uploads:/app/static/uploads" -v "%cd%\static\results:/app/static/results" --name car-damage-app car-damage-detection
    echo [OK] Docker container started!
    echo View logs: docker logs -f car-damage-app
    echo Stop container: docker stop car-damage-app
) else (
    echo Invalid choice. Exiting.
    exit /b 1
)

echo.
echo ========================================
echo Deployment complete!
echo Access the application at: http://localhost:5000
echo ========================================
pause
