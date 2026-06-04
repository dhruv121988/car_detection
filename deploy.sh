#!/bin/bash
# Deployment script for Car Damage Detection App

echo "🚀 Car Damage Detection - Deployment Script"
echo "==========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create production environment
echo ""
echo "📦 Setting up production environment..."

# Check if virtual environment exists
if [ ! -d ".venv-prod" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv-prod
fi

# Activate virtual environment
source .venv-prod/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install production dependencies
echo "Installing production dependencies..."
pip install -r requirements-prod.txt

# Create necessary directories
echo ""
echo "📁 Creating necessary directories..."
mkdir -p static/uploads
mkdir -p static/results
mkdir -p logs

# Check if model exists
if [ ! -f "runs/detect/train3/weights/best.pt" ]; then
    echo ""
    echo "⚠️  Warning: Model file not found at runs/detect/train3/weights/best.pt"
    echo "Please ensure your trained model is in the correct location."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and update SECRET_KEY before running in production!"
fi

# Ask for deployment type
echo ""
echo "Choose deployment option:"
echo "1) Test run (development mode)"
echo "2) Production with Gunicorn"
echo "3) Production with Gunicorn (background)"
echo "4) Docker deployment"
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🧪 Starting in development mode..."
        python3 app.py
        ;;
    2)
        echo ""
        echo "🚀 Starting with Gunicorn (foreground)..."
        gunicorn wsgi:app --bind 0.0.0.0:5000 --workers 2 --timeout 120 --access-logfile logs/access.log --error-logfile logs/error.log
        ;;
    3)
        echo ""
        echo "🚀 Starting with Gunicorn (background)..."
        gunicorn wsgi:app --bind 0.0.0.0:5000 --workers 2 --timeout 120 --daemon --access-logfile logs/access.log --error-logfile logs/error.log --pid gunicorn.pid
        echo "✅ Application started in background. PID saved to gunicorn.pid"
        echo "📊 View logs: tail -f logs/access.log logs/error.log"
        echo "🛑 Stop server: kill \$(cat gunicorn.pid)"
        ;;
    4)
        echo ""
        echo "🐳 Building and running with Docker..."
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker is not installed. Please install Docker first."
            exit 1
        fi
        docker build -t car-damage-detection .
        docker run -d -p 5000:5000 \
            -v $(pwd)/static/uploads:/app/static/uploads \
            -v $(pwd)/static/results:/app/static/results \
            --name car-damage-app \
            car-damage-detection
        echo "✅ Docker container started!"
        echo "📊 View logs: docker logs -f car-damage-app"
        echo "🛑 Stop container: docker stop car-damage-app"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "==========================================="
echo "🎉 Deployment complete!"
echo "🌐 Access the application at: http://localhost:5000"
echo "==========================================="
